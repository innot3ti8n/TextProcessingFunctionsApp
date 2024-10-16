from dataclasses import dataclass

@dataclass
class ComponentConfig:
    handler_module_name: str
    component_names: list[str] = None

@dataclass
class Flag:
    colour: str
    characters: str

@dataclass
class ComponentData:
    name: str
    markup_id: int

@dataclass
class PromptData:
    prompt_id: int
    prompt_config: dict
    markup_id: int
    handle_comps: dict