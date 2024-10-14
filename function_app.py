import logging
import azure.functions as func
import mysql.connector
import os
import re
import json

from textprocessor.process_manager import ProcessManager, Process
from textprocessor.data_models import Flag, ComponentData, PromptData

from textprocessor.processing_pipeline import ProcessingPipeline
from textprocessor.task_runners import ConcurrentTaskRunner
from textprocessor.handlers.llm import openai_gpt
from textprocessor.handlers.nlp import punctuation
from textprocessor.utils import merge_markups, update_dictionary

dbConfig = {
    'host': os.getenv('AZURE_DB_HOST'),
    'database': os.getenv('AZURE_DB_NAME'),
    'user': os.getenv('AZURE_DB_USER'),
    'password': os.getenv('AZURE_DB_PASSWORD'),
    'ssl_ca': './DigiCertGlobalRootCA.pem',
    'ssl_disabled': False
}

app = func.FunctionApp()

# Create connection object
def connect_to_db():
    return mysql.connector.connect(**dbConfig)

# Generate error response
def error_response(error, user_message=None, status_code=400):
    logging.error(f"{type(error).__name__}: {str(error)}")

    return func.HttpResponse(json.dumps({
        'error': "Request Error" if status_code == 400 else "Internal Server Error",
        'message': user_message
    }), mimetype="application/json", status_code=status_code)


@app.function_name(name="AnnotateText")
@app.route("annotate", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def annotate(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Received a request for skill processing with both NLP and LLM.')

    try:
        req_body = req.get_json()
    except ValueError as err:
        return error_response(err, "Invalid JSON received.")

# Check for required keys
    required_keys = ['skill_id', 'text']
    missing_keys = [key for key in required_keys if key not in req_body]
    
    if missing_keys:
        error_message = f"Missing required information: {', '.join(missing_keys)}"
        return error_response(ValueError(error_message), error_message)

    # Get selected skill and text from frontend
    skill_id = req_body.get('skill_id')
    text = req_body.get('text')
    conn = None
    annotations = dict()
    components_list = dict()

    try:
        conn = connect_to_db()
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

        pm = ProcessManager(
                Process(skill_id=1, skill_processor=punctuation),
                Process(2, openai_gpt), 
                Process(3, openai_gpt),
                Process(4, openai_gpt),
                Process(5, openai_gpt)
            ).createContext(skill_id, text)

        runner = ConcurrentTaskRunner()
        r_markups = []
        r_notes = []

        pp = ProcessingPipeline(pm)

        for processor in pm.processors:

            processed_with_llm = processed_with_nlp = False

            # If processing with llm
            if pm.processor_type(processor) == 'llm':
                processed_with_llm = True

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
                runner.add_task(pp.process_with_llm, processor, prompts_data, metadata)

            # If processing with nlp
            if pm.processor_type(processor) == 'nlp':
                processed_with_nlp = True

                runner.add_task(pp.process_with_nlp, processor, metadata)
            
            nlp_annotated = llm_annotated = llm_notes = ""

            r_result = runner.run_all()

            if r_result:
                if processed_with_nlp and not processed_with_llm:
                    nlp_annotated  = r_result[0]

                elif not processed_with_nlp and processed_with_llm:
                    llm_result = r_result[0]
                    if 'llm_annotated' in llm_result: llm_annotated = llm_result['llm_annotated']
                    if 'llm_notes' in llm_result: llm_notes = llm_result['llm_notes']

                elif processed_with_nlp and processed_with_llm:
                    nlp_annotated, llm_result = r_result
                    if 'llm_annotated' in llm_result: llm_annotated = llm_result['llm_annotated']
                    if 'llm_notes' in llm_result: llm_notes = llm_result['llm_notes']

                if nlp_annotated: r_markups.append(nlp_annotated)
                if llm_annotated: r_markups.append(llm_annotated)
                if llm_notes: r_notes.append(llm_notes)

        if r_markups: 
            annotations = update_dictionary(annotations, 'highlighted_text', merge_markups(text, r_markups)) 
        
        if r_notes:
            annotations = update_dictionary(annotations, 'notes', "\n\n".join(r_notes))
        
        if 'highlighted_text' in annotations:
            present_component_names = set(re.findall(r'data-component-name="([^"]+)"', annotations['highlighted_text']))

            components_list = update_dictionary(components_list, 'present', [component for component in all_components if component['name'] in present_component_names and component['markup_id'] == 1])
            components_list = update_dictionary(components_list, 'missing', [component for component in all_components if component['name'] not in present_component_names and component['markup_id'] == 1])

    except mysql.connector.Error as err:
        return error_response(err, "There was an issue connecting to the database", status_code=500)

    except Exception as err:
        return error_response(err, "An unexpected issue occurred. Please try again later.", status_code=500)

    finally:
        if conn:
            conn.close()

    result = dict()
    result = update_dictionary(result, 'annotations', annotations) 
    result = update_dictionary(result, 'components_list', components_list) 

    return func.HttpResponse(
            json.dumps(result, ensure_ascii=False), mimetype="application/json", status_code=200
        )
