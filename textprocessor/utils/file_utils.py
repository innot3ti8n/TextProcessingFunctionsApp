import json
import os

def get_file_path(base_dir, file_name):
    return os.path.join(base_dir, file_name)

def get_dir(*toDir):
    return os.path.join(os.path.dirname(__file__), '..', *toDir)

def get_constants(constants_module):
    return [getattr(constants_module, attr) for attr in dir(constants_module)]
