def get_constants(constants_module):
    return [getattr(constants_module, attr) for attr in dir(constants_module) if not attr.startswith("__") and not callable(getattr(constants_module, attr))]