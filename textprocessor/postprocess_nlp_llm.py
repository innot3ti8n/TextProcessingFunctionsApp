import itertools
from textprocessor.utils import parse_llm_markup, markup_text

def preprocess_result(data):
    data_list = list(itertools.chain.from_iterable(data))
    data = {}
    for d in data_list:
        data.update(d)

    return data

def process_llm_response(data, text):
    if "llm_annotated" not in data: 
        return data
    
    llm_annotated = data['llm_annotated']
    data['llm_annotated'] = list(itertools.chain.from_iterable([parse_llm_markup(text, markup) for markup in llm_annotated]))

    if "llm_notes" not in data:
        return data
    
    llm_notes = data['llm_notes']
    data['llm_notes'] = '\n\n'.join(llm_notes)

    return data

def make_nlp_notes(data, text, metadata):
    if "nlp_notes" not in data:
        return data
    
    nlp_notes = data['nlp_notes']
    raw_notes = {}

    for note in nlp_notes:
        if note['comp_id'] not in raw_notes:
            raw_notes[note['comp_id']] = []
        
        raw_notes[note['comp_id']].append(note)

    processed_notes = []

    for comp_id, note in raw_notes.items():
        processed_notes.append(f"{metadata['components'][comp_id].name}:\n\n{markup_text(text, note, metadata)}")

    data['nlp_notes'] = '\n\n'.join(processed_notes)

    return data
    

def combine_llm_nlp(data):
    if "llm_annotated" not in data and "nlp_annotated" not in data:
        pass
    elif "llm_annotated" not in data or "nlp_annotated" not in data:
        annotated = data.pop('llm_annotated', None) or data.pop('nlp_annotated', None)
        data['annotated'] = annotated
    else:
        del data['nlp_annotated']
        del data['llm_annotated']

        data['annotated'] = data['nlp_annotated'] + data['llm_annotated']

    if "llm_notes" not in data and "nlp_notes" not in data:
        pass
    elif "llm_notes" not in data or "nlp_notes" not in data:
        notes = data.pop('llm_notes', None) or data.pop('nlp_notes', None)
        data['notes'] = notes
    else:
        del data['llm_notes']
        del data['nlp_notes']

        data['notes'] = data['llm_notes'] + data['nlp_notes']

    return data

def remove_low_order_overlaps(data, order):
    if not order:
        return data
    if "annotated" not in data:
        return data

    annotated = data['annotated']

    # Sort the array first by start char index, then by end char index, then by comp_id
    arr = sorted(annotated, key=lambda x: (x['start'], x['end'], x['comp_id']))
    
    # Initialize data list
    result = []
    
    # Traverse the sorted array and remove overlaps
    for item in arr:
        # If result is empty or there's no overlap, add the item
        if not result or result[-1]['end'] <= item['start']:
            result.append(item)
        else:
            # If there's an overlap, keep the one with the higher order
            if order[result[-1]['comp_id']] < order[item['comp_id']]:
                result[-1] = item

    data['annotated'] = result 
    return data

def markup_annotated(data, text, metadata):
    if "annotated" not in data:
        data['annotated'] = None
    else:
        annotated = data['annotated']
        data['annotated'] = markup_text(text, annotated, metadata)

    return data


        
    

