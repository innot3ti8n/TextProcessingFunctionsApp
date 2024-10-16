from spacy.language import Language
from textprocessor.utils import get_results
from .constants import punct

# Custom component for detecting proper nouns and ensuring they are capitalized
@Language.component(punct.CAP_PROP_NOUN)
def detect_proper_nouns(doc):
    results = get_results(doc)
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG', 'GPE']:
            # Check if the proper noun is capitalized
            is_capitalized = ent.text.istitle()
            results.append({
                "comp_id": 1,  # Component ID for proper nouns
                "start": ent.start_char,
                "end": ent.end_char,
                "flag": 10 if is_capitalized else 11  # Flag 10 if capitalized, 11 if not
            })
    return doc

# Custom component for detecting key events and ensuring they are capitalized
@Language.component(punct.CAP_KEY_EVT)
def detect_key_events(doc):
    results = get_results(doc)
    for ent in doc.ents:
        if ent.label_ in ['EVENT']:
            # Check if the key event is capitalized
            is_capitalized = ent.text.istitle()
            results.append({
                "comp_id": 2,  # Component ID for key events
                "start": ent.start_char,
                "end": ent.end_char,
                "flag": 10 if is_capitalized else 11  # Flag 10 if capitalized, 11 if not
            })
    return doc

# Custom component for detecting possessive apostrophes
@Language.component(punct.POSS_APOS)
def detect_possessive_apostrophes(doc):
    results = get_results(doc)
    for token in doc:
        if token.dep_ == 'poss' and "’s" in token.head.text:
            results.append({
                "comp_id": 3,
                "start": token.head.idx,
                "end": token.head.idx + len(token.head.text),
                "flag": 10 if token.head.text.endswith("’s") or token.head.text.endswith("s’") else 11
            })

    return doc

# Custom component for detecting sentence boundary punctuation
@Language.component(punct.SENT_BOUND_PUNCT)
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
            "comp_id": 4,
            "start": punctuation_start,
            "end": punctuation_end,
            "flag": flag
        })
    
    return doc

@Language.component(punct.COMMAS)
def detect_commas(doc):
    results = get_results(doc)
    assigned_comma_indices = set()
    
    # Iterate over all tokens in the doc
    for token in doc:
        if token.text == ',' and token.idx not in assigned_comma_indices:
            # Initialize the comma_info with start and end positions of the comma
            comma_info = {"comp_id": None, "start": token.idx, "end": token.idx + 1}
            potential_flags = []

            # Check if the comma is part of a list
            if token.i < len(doc) - 1:
                next_token = token.nbor(1)
                prev_token = token.nbor(-1)

                # Detect list commas by looking at noun and conjunction relationships
                if (
                    prev_token.dep_ in ['conj', 'npadvmod', 'dobj', 'pobj', 'nsubj', 'appos']
                    or next_token.dep_ in ['conj', 'npadvmod', 'dobj', 'pobj', 'nsubj', 'appos']
                    or next_token.pos_ == 'CCONJ'  # Check for "and", "or", etc.
                ):
                    potential_flags.append({"comp_id": 5, "flag": 10})  # Comma in a list

            # Check if the comma is part of a date
            for ent in doc.ents:
                if ent.label_ == 'DATE' and token.idx in range(ent.start_char, ent.end_char):
                    potential_flags.append({"comp_id": 6, "flag": 10})  # Comma in a date

            # Check if the comma is for a pause
            if token.i > 0 and token.nbor(-1).dep_ == 'advcl':
                potential_flags.append({"comp_id": 7, "flag": 10})  # Comma for pause

            # Check if the comma precedes a quote
            if token.i < len(doc) - 1 and token.nbor(1).text in ['"', "'"]:
                potential_flags.append({"comp_id": 8, "flag": 10})  # Comma before quote

            # Store the potential flags in the comma info
            comma_info["potential_flags"] = potential_flags
            results.append(comma_info)
            assigned_comma_indices.add(token.idx)

        # Detect commas separating clauses in the same first pass
        if token.dep_ in ['advcl', 'relcl']:  # Detect adverbial and relative clauses
            comma_found = False
            for child in token.children:
                if child.text == ',' and child.idx not in assigned_comma_indices:
                    comma_found = True
                    # Store potential flags for commas separating clauses
                    results.append({
                        "comp_id": None,  # Will be assigned in the second pass
                        "start": child.idx,  # Start Component ID of the comma
                        "end": child.idx + 1,  # End Component ID is one character after the comma
                        "potential_flags": [{"comp_id": 10, "flag": 10}]  # Clause-separating comma
                    })
                    assigned_comma_indices.add(child.idx)  # Mark this comma as assigned

            # If no comma is found but the clause should be separated, flag it as missing
            if not comma_found:
                results.append({
                    "comp_id": 10,  # Assign comp_id as 10 directly for missing clause commas
                    "start": token.idx,  # Start Component ID of the token where comma should be
                    "end": token.idx + len(token.text),  # End Component ID of the token
                    "potential_flags": [{"comp_id": 10, "flag": 11}]  # Missing comma for clause separation
                })

    for comma_info in results:
        potential_flags = comma_info.pop("potential_flags", [])
        if potential_flags:
            # Prioritize or select the final type (for now just take the first valid match)
            best_flag = potential_flags[0]
            comma_info["comp_id"] = best_flag["comp_id"]
            comma_info["flag"] = best_flag["flag"]
        else:
            # If no valid flags found, keep the comp_id from the original (e.g., clause-related)
            if comma_info["comp_id"] is None:
                comma_info["comp_id"] = 10  # Ensure clause-related issues get the correct comp_id
            comma_info["flag"] = 11  # Incorrect usage
    return doc

# Custom component for detecting quotes for dialogue
@Language.component(punct.QUOTES_DLG)
def detect_quotes_for_dialogue(doc):
    results = get_results(doc)
    quote_open = False
    for token in doc:
        if token.text in ['"', "'"]:
            quote_open = not quote_open
        if quote_open:
            # Inside dialogue, checking for quotes
            results.append({
                "comp_id": 9,  # Component ID for quotes for dialogue
                "start": token.idx,
                "end": token.idx + len(token.text),
                "flag": 10 if quote_open else 11
            })
    return doc

# Custom component for detecting subordinating clauses
@Language.component(punct.SUB_CLAUSE)
def detect_subordinating_clauses(doc):
    results = get_results(doc)
    for token in doc:
        if token.dep_ == 'mark' and token.head.dep_ == 'advcl':
            results.append({
                "comp_id": 11,  # Component ID for subordinating clauses
                "start": token.idx,
                "end": token.idx + len(token.text),
                "flag": None
            })
    return doc

# Custom component for detecting complex dialogue
@Language.component(punct.COMP_DLG)
def detect_complex_dialogue(doc):
    results = get_results(doc)
    dialogue = False
    for token in doc:
        if token.text in ['"', "'"]:
            dialogue = not dialogue
        if dialogue and token.pos_ in ['VERB', 'PRON']:
            results.append({
                "comp_id": 12,  # Component ID for complex dialogue
                "start": token.idx,
                "end": token.idx + len(token.text),
                "flag": None
            })
    return doc

# Custom component for detecting simple punctuation (basic sentence end)
@Language.component(punct.SIMPLE_PUNCT)
def detect_simple_punctuation(doc):
    results = get_results(doc)
    for sent in doc.sents:
        if sent[-1].text not in '.!?':
            results.append({
                "comp_id": 13,  # Component ID for simple punctuation
                "start": sent.end_char - 1,
                "end": sent.end_char,
                "flag": 11  # Flag 11 if simple punctuation is missing
            })
        else:
            results.append({
                "comp_id": 13,
                "start": sent.end_char - 1,
                "end": sent.end_char,
                "flag": 10  # Flag 10 if simple punctuation is correct
            })
    return doc

# Custom component for detecting complex punctuation (handling colons, semicolons, etc.)
@Language.component(punct.COMP_PUNCT)
def detect_complex_punctuation(doc):
    results = get_results(doc)
    for token in doc:
        if token.text in [':', ';', '--']:
            results.append({
                "comp_id": 14,  # Component ID for complex punctuation
                "start": token.idx,
                "end": token.idx + len(token.text),
                "flag": 10  # Flag 10 for correct complex punctuation usage
            })
    return doc


# # Function to process text and return the results
# def process_text(text, component_names=None):
#     if not component_names:
#         component_names=get_constants(punct)

#     # Process text
#     nlp = get_nlp(component_names)
#     doc = nlp(text)

#     # Access the results
#     results = get_results(doc)

#     return results   

