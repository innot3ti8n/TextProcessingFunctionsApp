# import helper
from textprocessor_tests.test_utils.helpers import filterListBy

# import conftest helpers

# Result args: 
    #   <comp_index>: Int, 
    #   <start>: Int, 
    #   <end>: Int, 
    #   <flag>: Int | None
from textprocessor_tests.test_utils.helpers import Result

# import module that contains function to be tested
import textprocessor.handlers.nlp.punctuation as punct

# Test cases
def test_detect_proper_nouns(test, detect_with_nlp):
    test(
        punct.detect_proper_nouns
    ).given(
        { 'text': "One sunny moring my mum and I were cleaning out the shed, then my mum got a call from work and needed to go, she said to me “can you please stay and clean the shed?” “yes mum” I said “do you want a friend to come over?” she said “ok I’ll go call Hannah to see if she can come over” So my mum left and hannah came over, we were cleaning until hannah said “What’s in this little red box?” I said “Open it and find out.”" }
    ).expects(
        Result(1, 0, 10, 11),  # Person: "john" is not capitalised
        Result(1, 14, 20, 10), # Organisation: "Google" is capitalised
        Result(1, 24, 32, 10), # Place: "New York" is capitalised
    ).using(
        detect_with_nlp
    )
    

def test_detect_key_events(test, detect_with_nlp):
    test(
        punct.detect_key_events
    ).given(
        { 'text': "The World Cup will be held next year." }
    ).expects(
        Result(2, 0, 13, 10)  # Key event: "The World Cup" is correctly capitalized
    ).using(
        detect_with_nlp
    )

def test_detect_possessive_apostrophes(test, detect_with_nlp):
    test(
        punct.detect_possessive_apostrophes
    ).given(
        { 'text': "John’s book is on the table." }
    ).expects(
        Result(3, 4, 6, 10)  # "’s" in John’s is correctly marked as possessive
    ).using(
        detect_with_nlp
    )

def test_detect_sentence_boundary_punctuation(test, detect_with_nlp):
    test(
        punct.detect_sentence_boundary_punctuation
    ).given(
        { 'text': "Hello world." }
    ).expects(
        Result(4, 11, 12, 10)  # Correct usage of sentence boundary
    ).using(
        detect_with_nlp
    )

def test_detect_commas_in_lists(test, detect_with_nlp):
    test(
        punct.detect_commas
    ).given(
        { 'text': "I like apples, oranges and bananas." }
    ).expects(
        Result(5, 13, 14, 10)  # Correct usage of comma in a list
    ).using(
        detect_with_nlp,
        filterListBy,
        lambda x: x['comp_id'] == 5
    )

def test_detect_commas_in_dates(test, detect_with_nlp):
    test(
        punct.detect_commas
    ).given(
        { 'text': "July was born on July 4 2000." }
    ).expects(
        None  # Missing comma in date
    ).using(
        detect_with_nlp,
        filterListBy,
        lambda x: x['comp_id'] == 6
    )

def test_detect_commas_for_pauses(test, detect_with_nlp):
    test(
        punct.detect_commas
    ).given(
        { 'text': "After dinner we went for a walk." }
    ).expects(
        None  # Missing comma after "dinner"
    ).using(
        detect_with_nlp,
        filterListBy,
        lambda x: x['comp_id'] == 7
    )

def test_detect_commas_in_quotes(test, detect_with_nlp):
    test(
        punct.detect_commas
    ).given(
        { 'text': '"Hello," he said.' }
    ).expects(
        Result(8, 6, 7, 10)  # Correct usage of comma inside quotes
    ).using(
        detect_with_nlp,
        filterListBy,
        lambda x: x['comp_id'] == 8
    )

def test_detect_quotes_for_dialogue(test, detect_with_nlp):
    test(
        punct.detect_quotes_for_dialogue
    ).given(
        { 'text': '"What are you doing?" she asked.' }
    ).expects(
        Result(9, 0, 1, 10),   # Correct usage of opening quote
        Result(9, 20, 21, 10)  # Correct usage of closing quote
    ).using(
        detect_with_nlp
    )

def test_detect_commas_separating_clauses(test, detect_with_nlp):
    test(
        punct.detect_commas
    ).given(
        { 'text': "After finishing his work, John decided to take a stroll in the park." }
    ).expects(
        Result(10, 24, 25, 10)  # Correct usage of comma separating clauses
    ).using(
        detect_with_nlp
    )


#  Detect the relevant clause not punctuation
def test_detect_subordinating_clauses(test, detect_with_nlp):
    test(
        punct.detect_subordinating_clauses
    ).given(
        { 'text': "Although it was raining, we went outside." }
    ).expects(
        Result(11, 0, 23, None)  # Existence of subordinating clause
    ).using(
        detect_with_nlp
    )

#  Detect the dialogue clause not punctuation
def test_detect_complex_dialogue(test, detect_with_nlp):
    test(
        punct.detect_complex_dialogue
    ).given(
        { 'text': '"I don\'t know," she said, "maybe we should go."' }
    ).expects(
        Result(12, 0, 48, None)  # Existence of complex dialogue
    ).using(
        detect_with_nlp
    )

def test_detect_simple_punctuation(test, detect_with_nlp):
    test(
        punct.detect_simple_punctuation
    ).given(
        { 'text': "This is a test" }
    ).expects(
        Result(13, 13, 14, 11)  # Missing simple punctuation
    ).using(
        detect_with_nlp
    )

def test_detect_complex_punctuation(test, detect_with_nlp):
    test(
        punct.detect_complex_punctuation
    ).given(
        { 'text': "Here are two options: go outside, or stay inside." }
    ).expects(
        Result(14, 20, 21, 10)  # Correct usage of complex punctuation (colon)
    ).using(
        detect_with_nlp
    )
