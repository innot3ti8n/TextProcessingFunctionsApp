# import required modules
import pytest
import mysql.connector
import os
import logging
import pprint
from dataclasses import asdict

from textprocessor.data_models import ComponentData, PromptData, Flag
from .helpers import Result

class TestCase:
    def __init__(self, func):
        self.test_func = func
    
    def given(self, context):
        self.context = context
        return self
    
    def expects(self, *expected_result):
        self.expected_result = list(expected_result)
        return self
    
    def using(self, testcase_factory_fixture, transformer=None, *transformerArgs):
        testcase_factory_fixture(self, transformer, *transformerArgs)

        
@pytest.fixture
def test():
    def _test(test_func):
        return TestCase(test_func)
    return _test


@pytest.fixture
def detect_with_nlp(create_doc, verify_detection):
    def _detect_with_nlp(text, detect_func, *args):
        doc = create_doc(text)
        doc = detect_func(doc)
        
        verify_detection(doc, *args)
    return _detect_with_nlp



@pytest.fixture(scope="module")
def conn():

    dbConfig = {
        'host': os.getenv('AZURE_DB_HOST'),
        'database': os.getenv('AZURE_DB_NAME'),
        'user': os.getenv('AZURE_DB_USER'),
        'password': os.getenv('AZURE_DB_PASSWORD'),
        'ssl_ca': './DigiCertGlobalRootCA.pem',
        'ssl_disabled': False
    }

    connection = None
    try:
        connection = mysql.connector.connect(**dbConfig)
        yield connection
    except mysql.connector.Error as err:
        logging.error(f"Error connecting to database: {err}")
        pytest.fail("Database connection failed.")
    finally:
        if connection:
            connection.close()

@pytest.fixture
def get_skill_data(conn):
    def _get_skill_data(skill_id):
        cursor = conn.cursor(dictionary=True)
        
        # Get the list of all text components for the skill from the database
        query = "SELECT text_component_id, skill_id, name, example, markup_id FROM text_component WHERE skill_id = %s"
        cursor.execute(query, (skill_id,))
        all_components = cursor.fetchall()

        # Dictionary of text component id and name
        components = {component['text_component_id']: ComponentData(component['name'], component['markup_id']) for component in all_components}

        # Get the list of flags of text component
        query = "SELECT flag_id, colour, characters FROM flag"
        cursor.execute(query)
        all_flags = cursor.fetchall()

        # Dictionary of flag id, colour, and characters
        flags = {flag['flag_id']: Flag(flag['colour'], flag['characters']) for flag in all_flags}
        
        metadata = {'components': components, 'flags': flags}

        # get the prompt for current skill id
        query = "SELECT p.prompt_id, p.prompt, p.markup_id, pc.text_component_id, pc.order FROM prompt AS p LEFT JOIN prompt_comp AS pc ON p.prompt_id = pc.prompt_id WHERE p.skill_id = %s"
        cursor.execute(query, (skill_id,))
        prompts = cursor.fetchall()


        # Initialize a dictionary to hold the structured data
        prompts_dict = {}

        # Process the fetched data
        for row in prompts:
            prompt_id, prompt_config, markup_id, text_component_id, order = row.values()
            if prompt_id not in prompts_dict:
                prompts_dict[prompt_id] = {
                    'prompt_config': prompt_config,
                    'markup_id': markup_id,
                    'handle_comps': {}
                }
            prompts_dict[prompt_id]['handle_comps'][text_component_id] = order

        # Convert the dictionary to a list of named tuples
        prompts_data = [
            PromptData(prompt_id, data['prompt_config'], data['markup_id'], data['handle_comps']) for prompt_id, data in prompts_dict.items()
        ]
        
        metadata['prompts_data'] = prompts_data

        return metadata
    return _get_skill_data

def fancy_print(text, text_color_code=37, bg_color_code=None):
    # ANSI escape codes for text and background colors
    # 30-37: Text colors (black, red, green, yellow, blue, magenta, cyan, white)
    # 40-47: Background colors (black, red, green, yellow, blue, magenta, cyan, white)

    bg_color_code = "" if not bg_color_code else f";{bg_color_code}"

    # Construct the ANSI escape code
    ansi_code = f"\n\033[1m\033[{text_color_code}{bg_color_code}m[ {text} ]\033[0m\n"
    
    # Print the colored text
    print(ansi_code)

@pytest.fixture
def verify_result():
    def _verify_result(context, expect, get, transformer, *transformerArgs):
        
        if all(isinstance(item, Result) for item in expect):
            expect = [asdict(item) for item in expect]

        if transformer:
            get = transformer(get, *transformerArgs)

        if expect == [None]:
            expect = None

        if not isinstance(get, list):
            expect = expect[0]

        if expect != get:
            fancy_print("GIVEN", 34)
            pprint.pprint(context)
            fancy_print("EXPECT", 32)
            pprint.pprint(expect, sort_dicts=False)
            fancy_print("GET", 31)
            pprint.pprint(get, sort_dicts=False)
            print()
        assert expect == get
    return _verify_result