from collections import namedtuple

Flag = namedtuple('Flag', ['colour', 'characters'])
ComponentData = namedtuple('ComponentData', ['name', 'markup_id'])
PromptData = namedtuple('PromptData', ['prompt_id', 'prompt_config', 'markup_id', 'handle_comps'])