import itertools
from textprocessor.utils import parse_llm_markup, markup_text

def preprocess_result(data):
    data_list = list(itertools.chain.from_iterable(data))
    data = {}
    for d in data_list:
        data.update(d)

    return data

def process_llm_annotated(data, text):
    if "llm_annotated" not in data: 
        return data
    
    llm_annotated = data['llm_annotated']
    data['llm_annotated'] = list(itertools.chain.from_iterable([parse_llm_markup(text, markup) for markup in llm_annotated]))

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

    if "llm_notes" not in data:
        pass
    else:
        notes = data.pop('llm_notes', None)
        data['notes'] = '\n\n'.join(notes)

    return data

def remove_overlaps(data):
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
            # If there's an overlap, keep the one with the lower comp_id
            if result[-1]['comp_id'] > item['comp_id']:
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


        
    

