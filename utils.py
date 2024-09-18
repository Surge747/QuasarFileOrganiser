# utils.py
import os
import subprocess

def is_application_installed(exe_name):
    """
    Check if an application corresponding to the given exe_name is installed.
    This function searches common installation directories for the exe.

    Parameters:
        exe_name (str): The name of the executable file (e.g., 'setup.exe').

    Returns:
        bool: True if the application is installed, False otherwise.
    """
    # Common installation directories
    program_files = os.environ.get('ProgramFiles', r"C:\Program Files")
    program_files_x86 = os.environ.get('ProgramFiles(x86)', r"C:\Program Files (x86)")
    install_dirs = [program_files, program_files_x86]

    for install_dir in install_dirs:
        for root, dirs, files in os.walk(install_dir):
            if exe_name.lower() in (f.lower() for f in files):
                return True
    return False
