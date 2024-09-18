# settings.py
import os
import json
from constants import DEFAULT_OUTFLOW_DIRS, FILE_TYPES

SETTINGS_FILE = 'settings.json'

def save_settings(inflow_dirs, outflow_dirs):
    settings = {
        'inflow_dirs': inflow_dirs,
        'outflow_dirs': outflow_dirs
    }
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
            inflow_dirs = settings.get('inflow_dirs', [])
            outflow_dirs = settings.get('outflow_dirs', {})
    else:
        # Initialize with default outflow directories
        inflow_dirs = []
        outflow_dirs = {}

        # Map extensions to default directories
        for category, exts in FILE_TYPES.items():
            if category == 'executables':
                continue  # We'll handle executables separately
            dir_path = DEFAULT_OUTFLOW_DIRS.get(category, '')
            if os.path.exists(dir_path):
                for ext in exts:
                    outflow_dirs[ext] = dir_path

    return inflow_dirs, outflow_dirs
