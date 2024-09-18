# file_ops.py (Updated)
import os
import shutil
import threading
import time
import difflib
import subprocess
from settings import save_settings
from constants import FILE_TYPES
import PyPDF2
import pytesseract
from PIL import Image
import winreg
import json

# Initialize Tesseract path if necessary
# Replace the path below with your Tesseract-OCR installation path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Global variables to manage logs and undo stack
log_entries = []
undo_stack = []

def add_log(entry):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_entry = {
        'timestamp': timestamp,
        'message': entry,
        'action': None  # To store move actions for undo
    }
    log_entries.append(log_entry)

def get_logs():
    return log_entries

def clear_logs():
    log_entries.clear()

def check_if_installed(exe_name):
    """
    Check if an application corresponding to the exe_name is installed.
    This function searches the Windows Registry for installed applications.
    """
    try:
        # Registry paths for installed applications
        registry_paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        for reg_path in registry_paths:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
            for i in range(0, winreg.QueryInfoKey(key)[0]):
                sub_key_name = winreg.EnumKey(key, i)
                sub_key = winreg.OpenKey(key, sub_key_name)
                try:
                    display_name = winreg.QueryValueEx(sub_key, "DisplayName")[0]
                    uninstall_string = winreg.QueryValueEx(sub_key, "UninstallString")[0]
                    if exe_name.lower() in display_name.lower():
                        return True
                except FileNotFoundError:
                    continue
    except Exception as e:
        add_log(f"Error checking installation for {exe_name}: {str(e)}")
    return False

def sort_files(inflow_dirs, outflow_dirs):
    processed_files = set()
    for inflow in inflow_dirs:
        for root, _, files in os.walk(inflow):
            for filename in files:
                file_path = os.path.join(root, filename)
                if file_path in processed_files:
                    continue
                processed_files.add(file_path)
                if os.path.isfile(file_path):
                    ext = filename.split('.')[-1].lower()
                    dest_dir = outflow_dirs.get(ext, None)
                    if ext == 'exe':
                        app_name = os.path.splitext(filename)[0]
                        if check_if_installed(app_name):
                            try:
                                os.remove(file_path)
                                add_log(f"Deleted installer {filename} as {app_name} is already installed.")
                                continue
                            except Exception as e:
                                add_log(f"Error deleting {filename}: {str(e)}")
                    if dest_dir:
                        dest_path = os.path.join(dest_dir, filename)
                        try:
                            shutil.move(file_path, dest_path)
                            add_log(f"Moved {filename} to {dest_dir}")
                            # Record action for undo
                            undo_stack.append({
                                'src': dest_path,
                                'dest': file_path
                            })
                        except Exception as e:
                            add_log(f"Error moving {filename}: {str(e)}")
                    else:
                        # Try intelligent sorting
                        suggested_dir, detail = intelligent_sort(file_path, outflow_dirs)
                        if suggested_dir:
                            dest_path = os.path.join(suggested_dir, filename)
                            try:
                                shutil.move(file_path, dest_path)
                                add_log(f"Intelligently moved {filename} to {suggested_dir} ({detail})")
                                # Record action for undo
                                undo_stack.append({
                                    'src': dest_path,
                                    'dest': file_path
                                })
                            except Exception as e:
                                add_log(f"Error moving {filename}: {str(e)}")
                        else:
                            add_log(f"No outflow directory for .{ext} files")

def start_sorting_thread(inflow_dirs, outflow_dirs):
    threading.Thread(target=sort_files, args=(inflow_dirs, outflow_dirs), daemon=True).start()

def intelligent_sort(file_path, outflow_dirs):
    filename = os.path.basename(file_path)
    ext = filename.split('.')[-1].lower()
    detail = ""
    # Analyze filename
    for key, dir_path in outflow_dirs.items():
        if key in filename.lower():
            detail = f"matched extension '{key}' in filename"
            return dir_path, detail

    # Analyze file content for PDFs and images
    text_content = ''
    if ext == 'pdf':
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text_content += page.extract_text() or ''
        except:
            pass
    elif ext in FILE_TYPES['images']:
        try:
            text_content = pytesseract.image_to_string(Image.open(file_path))
        except:
            pass

    # Search for keywords in content
    for key in outflow_dirs.keys():
        if key.lower() in text_content.lower():
            detail = f"found '{key}' in file content"
            return outflow_dirs[key], detail

    # Find similar filenames in outflow directories
    for dir_path in set(outflow_dirs.values()):
        try:
            existing_files = os.listdir(dir_path)
            matches = difflib.get_close_matches(filename, existing_files)
            if matches:
                detail = f"similar filename found in '{dir_path}'"
                return dir_path, detail
        except:
            continue

    return None, detail

def undo_move(action):
    src = action['src']
    dest = action['dest']
    if os.path.exists(src):
        try:
            shutil.move(src, dest)
            add_log(f"Undo: Moved {os.path.basename(src)} back to {dest}")
            # Remove the action from undo stack
            undo_stack.remove(action)
        except Exception as e:
            add_log(f"Error undoing move for {os.path.basename(src)}: {str(e)}")
    else:
        add_log(f"Undo failed: Source file {src} does not exist.")

def undo_all_moves():
    # Create a copy of the stack to iterate over
    for action in undo_stack.copy():
        undo_move(action)
