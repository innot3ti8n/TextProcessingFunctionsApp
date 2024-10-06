import spacy
from spacy.tokens import Doc

def keep_lowest_comp_index(output):
    n = len(output)
    to_remove = set()  # Set to keep track of components to remove

    for i in range(n):
        for j in range(i + 1, n):
            # Get ranges
            start_i, end_i = output[i]['start'], output[i]['end']
            start_j, end_j = output[j]['start'], output[j]['end']

            # Check for overlap
            if start_i <= end_j and start_j <= end_i:
                # Identify the component with the lower comp_index
                if output[i]['comp_index'] < output[j]['comp_index']:
                    to_remove.add(j)  # Mark the component j for removal
                else:
                    to_remove.add(i)  # Mark the component i for removal

    # Create a new list without the components to remove
    non_overlapping_components = [comp for index, comp in enumerate(output) if index not in to_remove]

    return non_overlapping_components

def get_nlp(component_names):
    # Register custom attributes
    Doc.set_extension("result", default=[])
    
    # Load spaCy model
    nlp = spacy.load("en_core_web_sm")

    # Add all components to the pipeline for detection only
    for component_name in component_names:
        nlp.add_pipe(component_name, last=True)
    
    return nlp