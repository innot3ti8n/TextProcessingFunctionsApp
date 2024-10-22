import re
from textprocessor.data_models import Flag

def markup_text(text, text_elements, metadata):

    # Sort entities by start position in descending order to
    # avoid shifting start and end position when marking up text
    text_elements = sorted(text_elements, key=lambda x: x['start'], reverse=True)
    components = metadata['components']
    flags = metadata['flags']
    
    component_ids = list(components.keys())
    component_data = list(components.values())

    # Insert <mark> and </mark> tags
    for element in text_elements:
        comp_index = component_ids.index(element['comp_id'])

        has_flag = element['flag'] != None

        name = component_data[comp_index].name

        # Define tag attributes
        attributes = {}
        attributes.setdefault("data", f"{element['comp_id']},{element['flag'] or '*'}")
        attributes.setdefault("class", "highlight" + (" flag" if has_flag else ""))
        attributes.setdefault("data-component-name", name)
        attributes.setdefault("style", [])
        attributes['style'].append(f"--component-background: var(--c{comp_index + 1}-background)")

        if (has_flag):
            flag: Flag = flags[element['flag']]
            colour = flag.colour
            characters = flag.characters

            attributes.setdefault("data-subcomponent-text", characters or '\u2003')
            attributes['style'].append(f"--subcomponent-background: {colour}")

        attributes = dict(sorted(attributes.items()))

        # Markup text by constructing text contains <mark> html elements with attributes
        text = text[:element['start']] + f"""<mark {' '.join([f'{attr_name}="{attr_value if attr_name != "style" else "; ".join(attr_value)}"' for attr_name, attr_value in attributes.items()])}>""" + text[element['start']:element['end']] + '</mark>' + text[element['end']:]

    return text


def parse_llm_markup(text, llm_markup):
    marks = []
    current_pos = 0

    # Regex to find all <mark>...</mark> patterns
    for match in re.finditer(r'(<mark[^>]*>)(.*?)(</mark>)', llm_markup):
        marked_text = match.group(2)     # Extract the text inside the <mark> tags

        data = re.search(r'<mark data="([^"]*)">', match.group(1))

        if data:
            component_id, flag_id = data.group(1).split(',')

            flag_id = None if flag_id.strip() == '*' else int(flag_id)

            # Search for the marked text in the plain text, starting from the last found position
            start = text.find(marked_text, current_pos)
            
            # If found, calculate the end position
            if start != -1:
                end = start + len(marked_text)
                marks.append({
                    "comp_id": (int(component_id)),
                    "start": start,
                    "end": end,
                    "flag": flag_id
                })

                # Update the current position to continue searching after this point
                current_pos = end

    return marks

