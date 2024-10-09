from spacy.language import Language

from . import keep_lowest_comp_index, get_nlp, get_results

# Custom component for detecting proper nouns and ensuring they are capitalized
@Language.component("detect_proper_nouns")
def detect_proper_nouns(doc):
    results = get_results(doc)
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG', 'GPE']:
            # Check if the proper noun is capitalized
            is_capitalized = ent.text.istitle()
            results.append({
                "comp_index": 1,  # Index for proper nouns
                "start": ent.start_char,
                "end": ent.end_char,
                "flag": 10 if is_capitalized else 11  # Flag 10 if capitalized, 11 if not
            })
    return doc

# Custom component for detecting key events and ensuring they are capitalized
@Language.component("detect_key_events")
def detect_key_events(doc):
    results = get_results(doc)
    for ent in doc.ents:
        if ent.label_ in ['EVENT']:
            # Check if the key event is capitalized
            is_capitalized = ent.text.istitle()
            results.append({
                "comp_index": 2,  # Index for key events
                "start": ent.start_char,
                "end": ent.end_char,
                "flag": 10 if is_capitalized else 11  # Flag 10 if capitalized, 11 if not
            })
    return doc

# Custom component for detecting possessive apostrophes
@Language.component("detect_possessive_apostrophes")
def detect_possessive_apostrophes(doc):
    results = get_results(doc)
    for token in doc:
        if token.dep_ == 'poss' and "’s" in token.head.text:
            results.append({
                "comp_index": 3,
                "start": token.head.idx,
                "end": token.head.idx + len(token.head.text),
                "flag": 10 if token.head.text.endswith("’s") or token.head.text.endswith("s’") else 11
            })

    return doc

# Custom component for detecting sentence boundary punctuation
@Language.component("detect_sentence_boundary_punctuation")
def detect_sentence_boundary_punctuation(doc):
    results = get_results(doc)
    for sent in doc.sents:
        # Check if the last character is a quotation mark
        if sent.text[-1] == '”':
            # Check the character before the quotation mark
            if sent.text[-2] in '.!?':
                flag = 10  # Correct usage
                punctuation_start = sent.end_char - 2
                punctuation_end = sent.end_char - 1
            else:
                flag = 11  # Incorrect usage
                punctuation_start = sent.end_char - 1
                punctuation_end = sent.end_char
        else:
            # Check the last character directly
            if sent.text[-1] in '.!?':
                flag = 10  # Correct usage
                punctuation_start = sent.end_char - 1
                punctuation_end = sent.end_char
            else:
                flag = 11  # Incorrect usage
                punctuation_start = sent.end_char - 1
                punctuation_end = sent.end_char

        results.append({
            "comp_index": 4,
            "start": punctuation_start,
            "end": punctuation_end,
            "flag": flag
        })
    
    return doc

# Custom component for detecting commas in lists (improved)
@Language.component("detect_commas_in_lists")
def detect_commas_in_lists(doc):
    results = get_results(doc)
    for token in doc:
        # Detect items in a list using conjunctions (e.g., apples, oranges, and bananas)
        if token.dep_ == 'cc' and token.text.lower() in ['and', 'or']:
            # Check if the previous item in the list has a comma
            if token.i > 1 and token.nbor(-2).text == ',':
                flag = 10  # Correct usage
            else:
                flag = 11  # Incorrect usage
            
            results.append({
                "comp_index": 5,
                "start": token.nbor(-2).idx if token.i > 1 else token.idx,  # Highlight the previous item and its comma
                "end": token.nbor(-2).idx + len(token.nbor(-2).text) if token.i > 1 else token.idx + len(token.text),
                "flag": flag
            })
    return doc

# Custom component for detecting commas in dates
@Language.component("detect_commas_in_dates")
def detect_commas_in_dates(doc):
    results = get_results(doc)
    for ent in doc.ents:
        if ent.label_ == 'DATE':
        # Check for commas in the date entity
            if ',' in ent.text:
                flag = 10  # Correct usage
                # Find the position of the comma
                comma_index = ent.text.index(',')
                start = ent.start_char + comma_index
                end = start + 1
            else:
                flag = 11  # Incorrect usage
                # If no comma, highlight the end of the entity
                start = ent.end_char - 1
                end = ent.end_char

            results.append({
                "comp_index": 6,
                "start": start,
                "end": end,
                "flag": flag
            })
    return doc

# Custom component for detecting commas for pauses (improved)
@Language.component("detect_commas_for_pauses")
def detect_commas_for_pauses(doc):
    results = get_results(doc)
    for token in doc:
        # Check for introductory clauses or adverbial clauses (advcl) that require a comma
        if token.dep_ == 'advcl' and token.head.pos_ == 'VERB':
            # Ensure a comma is present after the clause
            if token.i < len(doc) - 1 and token.nbor(1).text == ',':
                flag = 10  # Correct usage
                start = token.nbor(1).idx
                end = start + 1
            else:
                flag = 11  # Incorrect usage
                start = token.idx
                end = token.idx + len(token.text)

            results.append({
                "comp_index": 7,
                "start": start,
                "end": end,
                "flag": flag
            })
    return doc

# Custom component for detecting commas in quotes (improved with boundary checks)
@Language.component("detect_commas_in_quotes")
def detect_commas_in_quotes(doc):
    results = get_results(doc)
    quote_open = False
    for token in doc:
        if token.text in ['"', "'"]:
            quote_open = not quote_open
        if not quote_open:
            # Ensure token index is greater than 0 before accessing previous token
            if token.i > 0 and token.nbor(-1).text == ',':
                flag = 10  # Correct usage
            else:
                flag = 11  # Incorrect usage
            
            results.append({
                "comp_index": 8,
                "start": token.nbor(-1).idx if token.i > 0 else token.idx,
                "end": token.nbor(-1).idx + len(token.nbor(-1).text) if token.i > 0 else token.idx + len(token.text),
                "flag": flag
            })
    return doc

# Custom component for detecting quotes for dialogue
@Language.component("detect_quotes_for_dialogue")
def detect_quotes_for_dialogue(doc):
    results = get_results(doc)
    quote_open = False
    for token in doc:
        if token.text in ['"', "'"]:
            quote_open = not quote_open
        if quote_open:
            # Inside dialogue, checking for quotes
            results.append({
                "comp_index": 9,  # Index for quotes for dialogue
                "start": token.idx,
                "end": token.idx + len(token.text),
                "flag": 10 if quote_open else 11
            })
    return doc

# Custom component for detecting commas separating clauses
@Language.component("detect_commas_separating_clauses")
def detect_commas_separating_clauses(doc):
    results = get_results(doc)
    for token in doc:
        if token.dep_ in ['advcl', 'relcl']:
            comma_found = False
            for child in token.children:
                if child.text == ',':
                    comma_found = True
                    results.append({
                        "comp_index": 10,  # Index for commas separating clauses
                        "start": child.idx,
                        "end": child.idx + len(child.text),
                        "flag": 10
                    })
            if not comma_found:
                results.append({
                    "comp_index": 10,
                    "start": token.idx,
                    "end": token.idx + len(token.text),
                    "flag": 11  # Flag 11 if comma is missing
                })
    return doc

# Custom component for detecting subordinating clauses
@Language.component("detect_subordinating_clauses")
def detect_subordinating_clauses(doc):
    results = get_results(doc)
    for token in doc:
        if token.dep_ == 'mark' and token.head.dep_ == 'advcl':
            results.append({
                "comp_index": 11,  # Index for subordinating clauses
                "start": token.idx,
                "end": token.idx + len(token.text),
                "flag": None
            })
    return doc

# Custom component for detecting complex dialogue
@Language.component("detect_complex_dialogue")
def detect_complex_dialogue(doc):
    results = get_results(doc)
    dialogue = False
    for token in doc:
        if token.text in ['"', "'"]:
            dialogue = not dialogue
        if dialogue and token.pos_ in ['VERB', 'PRON']:
            results.append({
                "comp_index": 12,  # Index for complex dialogue
                "start": token.idx,
                "end": token.idx + len(token.text),
                "flag": None
            })
    return doc

# Custom component for detecting simple punctuation (basic sentence end)
@Language.component("detect_simple_punctuation")
def detect_simple_punctuation(doc):
    results = get_results(doc)
    for sent in doc.sents:
        if sent[-1].text not in '.!?':
            results.append({
                "comp_index": 13,  # Index for simple punctuation
                "start": sent.end_char - 1,
                "end": sent.end_char,
                "flag": 11  # Flag 11 if simple punctuation is missing
            })
        else:
            results.append({
                "comp_index": 13,
                "start": sent.end_char - 1,
                "end": sent.end_char,
                "flag": 10  # Flag 10 if simple punctuation is correct
            })
    return doc

# Custom component for detecting complex punctuation (handling colons, semicolons, etc.)
@Language.component("detect_complex_punctuation")
def detect_complex_punctuation(doc):
    results = get_results(doc)
    for token in doc:
        if token.text in [':', ';', '--']:
            results.append({
                "comp_index": 14,  # Index for complex punctuation
                "start": token.idx,
                "end": token.idx + len(token.text),
                "flag": 10  # Flag 10 for correct complex punctuation usage
            })
    return doc


# Components list to add to pipeline
component_names = [
    "detect_proper_nouns",
    "detect_key_events",
    "detect_possessive_apostrophes",
    "detect_sentence_boundary_punctuation",
    "detect_commas_in_lists",   
    "detect_commas_in_dates",
    "detect_commas_for_pauses",
    "detect_commas_in_quotes",
    
    "detect_quotes_for_dialogue",
    "detect_commas_separating_clauses",
    "detect_subordinating_clauses",
    "detect_complex_dialogue",
    "detect_simple_punctuation",
    "detect_complex_punctuation"
]

# Function to process text and return the results
def process_text(text):

    # Process text
    nlp = get_nlp(component_names)
    doc = nlp(text)

    # Access the results
    results = get_results(doc)

    return keep_lowest_comp_index(results)   

