# constants.py
import os

# User's home directory
USER_HOME = os.path.expanduser('~')

# Default Windows folders
DEFAULT_OUTFLOW_DIRS = {
    'images': os.path.join(USER_HOME, 'Pictures'),
    'documents': os.path.join(USER_HOME, 'Documents'),
    'music': os.path.join(USER_HOME, 'Music')
}

# File extensions mapping
FILE_TYPES = {
    'images': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'],
    'documents': ['pdf', 'doc', 'docx', 'txt', 'xls', 'xlsx', 'ppt', 'pptx'],
    'music': ['mp3', 'wav', 'aac', 'flac', 'ogg'],
    'executables': ['exe']
}
