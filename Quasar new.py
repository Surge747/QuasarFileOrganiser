import os
import shutil
import threading
import time
import json
import difflib
from pathlib import Path
import PySimpleGUI as sg
import PyPDF2
import pytesseract
from PIL import Image
import subprocess

# ------------------- Constants ------------------- #

# User's home directory
USER_HOME = os.path.expanduser('~')

# Default Windows folders
DEFAULT_OUTFLOW_DIRS = {
    'images': os.path.join(USER_HOME, 'Pictures'),
    'documents': os.path.join(USER_HOME, 'Documents'),
    'music': os.path.join(USER_HOME, 'Music'),
    'executables': os.path.join(USER_HOME, 'Applications')  # Custom folder for executables
}

# File extensions mapping
FILE_TYPES = {
    'images': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'],
    'documents': ['pdf', 'doc', 'docx', 'txt', 'xls', 'xlsx', 'ppt', 'pptx'],
    'music': ['mp3', 'wav', 'aac', 'flac', 'ogg'],
    'executables': ['exe']
}

# Any extension folder
ANY_EXTENSION = 'all_other'

# Settings file
SETTINGS_FILE = 'settings.json'

# Max depth for subfolders in intelligent sorting
MAX_SUBFOLDER_DEPTH = 4

# Path to Tesseract OCR executable (update if necessary)
# Example for Windows:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# ------------------- Settings Management ------------------- #

def save_settings(inflow_dirs, outflow_dirs, any_ext_dir):
    settings = {
        'inflow_dirs': inflow_dirs,
        'outflow_dirs': outflow_dirs,
        'any_extension_dir': any_ext_dir
    }
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            settings = json.load(f)
            inflow_dirs = settings.get('inflow_dirs', [])
            outflow_dirs = settings.get('outflow_dirs', {})
            any_ext_dir = settings.get('any_extension_dir', '')
    else:
        # Initialize with default outflow directories
        inflow_dirs = []
        outflow_dirs = {}
        any_ext_dir = ''

        # Map extensions to default directories
        for category, exts in FILE_TYPES.items():
            if category == 'executables':
                continue  # Handle executables separately
            dir_path = DEFAULT_OUTFLOW_DIRS.get(category, '')
            if os.path.exists(dir_path):
                for ext in exts:
                    outflow_dirs[ext] = dir_path

        # Handle 'any extension' directory
        any_ext_dir = DEFAULT_OUTFLOW_DIRS.get('executables', '')

    return inflow_dirs, outflow_dirs, any_ext_dir

# ------------------- Logging and Undo Management ------------------- #

log_entries = []
move_history = []  # List of tuples (source, destination)

def add_log(entry):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"{timestamp} - {entry}"
    log_entries.append(log_entry)

def get_logs():
    return log_entries

def add_move_history(source, destination):
    move_history.append((source, destination))

# ------------------- File Operations ------------------- #

def is_exe_installed(exe_name):
    """
    Check if an executable is installed by searching in Program Files directories.
    """
    program_files = [os.environ.get('ProgramFiles', ''), os.environ.get('ProgramFiles(x86)', '')]
    for pf in program_files:
        if not pf:
            continue
        for root, dirs, files in os.walk(pf):
            if exe_name.lower() in [f.lower() for f in files]:
                return True
            # Limit search depth
            if root[len(pf):].count(os.sep) >= 4:
                continue
    return False

def intelligent_sort(file_path, outflow_dirs, any_ext_dir):
    """
    Intelligent sorting based on filename and content.
    Returns the destination directory and reason for sorting.
    """
    filename = os.path.basename(file_path)
    name, ext = os.path.splitext(filename)
    ext = ext[1:].lower()

    # Analyze filename for keywords
    for keyword, dir_path in outflow_dirs.items():
        if keyword.lower() in filename.lower():
            reason = f'Keyword "{keyword}" found in filename'
            return dir_path, reason

    # Analyze file content for PDFs and images
    text_content = ''
    if ext == 'pdf':
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text_content += page.extract_text() or ''
        except Exception as e:
            add_log(f"Error reading PDF content from {filename}: {str(e)}")
    elif ext in FILE_TYPES['images']:
        try:
            text_content = pytesseract.image_to_string(Image.open(file_path))
        except Exception as e:
            add_log(f"Error performing OCR on {filename}: {str(e)}")

    # Search for keywords in content
    for keyword, dir_path in outflow_dirs.items():
        if keyword.lower() in text_content.lower():
            reason = f'Keyword "{keyword}" found in file content'
            return dir_path, reason

    # Similarity matching with existing files in outflow directories
    for dir_path in set(outflow_dirs.values()):
        try:
            existing_files = os.listdir(dir_path)
            matches = difflib.get_close_matches(name, [os.path.splitext(f)[0] for f in existing_files], n=1, cutoff=0.8)
            if matches:
                reason = f'Filename similar to existing file "{matches[0]}" in {dir_path}'
                return dir_path, reason
        except Exception as e:
            add_log(f"Error accessing directory {dir_path} for similarity matching: {str(e)}")
            continue

    # Any extension directory
    if any_ext_dir and os.path.exists(any_ext_dir):
        reason = 'No specific criteria met; moved to "Any Extension" directory'
        return any_ext_dir, reason

    return None, None

def get_subfolders(dir_path, current_depth=1, max_depth=4):
    """
    Recursively get subfolders up to a specified depth.
    """
    subfolders = []
    if current_depth > max_depth:
        return subfolders
    try:
        for entry in os.scandir(dir_path):
            if entry.is_dir():
                subfolders.append(entry.path)
                subfolders.extend(get_subfolders(entry.path, current_depth + 1, max_depth))
    except Exception as e:
        add_log(f"Error accessing subfolders in {dir_path}: {str(e)}")
    return subfolders

def sort_files(inflow_dirs, outflow_dirs, any_ext_dir):
    """
    Sort files from inflow directories to outflow directories based on extension and intelligent criteria.
    """
    processed_files = set()
    for inflow in inflow_dirs:
        if not os.path.exists(inflow):
            add_log(f"Inflow directory does not exist: {inflow}")
            continue
        for root, dirs, files in os.walk(inflow):
            # Skip subdirectories in inflow
            if root != inflow:
                continue
            for filename in files:
                file_path = os.path.join(root, filename)
                if file_path in processed_files:
                    continue
                processed_files.add(file_path)

                if not os.path.isfile(file_path):
                    continue

                name, ext = os.path.splitext(filename)
                ext = ext[1:].lower()

                # Handle executables separately
                if ext == 'exe':
                    exe_name = filename
                    if is_exe_installed(exe_name):
                        try:
                            os.remove(file_path)
                            add_log(f"Deleted setup executable {filename} as it is already installed.")
                        except Exception as e:
                            add_log(f"Error deleting {filename}: {str(e)}")
                        continue

                # Extension-based sorting
                dest_dir = outflow_dirs.get(ext, None)
                if dest_dir and os.path.exists(dest_dir):
                    try:
                        dest_path = os.path.join(dest_dir, filename)
                        shutil.move(file_path, dest_path)
                        add_log(f"Moved {filename} to {dest_dir} based on extension .{ext}")
                        add_move_history(file_path, dest_path)
                    except Exception as e:
                        add_log(f"Error moving {filename} to {dest_dir}: {str(e)}")
                else:
                    # Intelligent sorting
                    intelligent_dest, reason = intelligent_sort(file_path, outflow_dirs, any_ext_dir)
                    if intelligent_dest and os.path.exists(intelligent_dest):
                        try:
                            dest_path = os.path.join(intelligent_dest, filename)
                            shutil.move(file_path, dest_path)
                            add_log(f"Intelligently moved {filename} to {intelligent_dest} because {reason}.")
                            add_move_history(file_path, dest_path)
                        except Exception as e:
                            add_log(f"Error intelligently moving {filename} to {intelligent_dest}: {str(e)}")
                    else:
                        add_log(f"No outflow directory for .{ext} files and intelligent sorting did not find a destination.")

def start_sorting_thread(inflow_dirs, outflow_dirs, any_ext_dir):
    threading.Thread(target=sort_files, args=(inflow_dirs, outflow_dirs, any_ext_dir), daemon=True).start()

def undo_move(source, destination):
    """
    Move file back from destination to source.
    """
    if os.path.exists(destination):
        try:
            shutil.move(destination, source)
            add_log(f"Undo: Moved {os.path.basename(destination)} back to {source}")
            return True
        except Exception as e:
            add_log(f"Error undoing move for {destination}: {str(e)}")
    else:
        add_log(f"Cannot undo move: Destination file does not exist: {destination}")
    return False

def undo_all_moves():
    """
    Undo all file moves in reverse order.
    """
    while move_history:
        source, destination = move_history.pop()
        undo_move(source, destination)

# ------------------- GUI Layout ------------------- #

def create_main_window(inflow_dirs, outflow_dirs, any_ext_dir):
    sg.theme('LightBlue')

    menu_def = [['File', ['Exit']], ['Help', ['About']]]

    # Define the layouts for different tabs
    sort_layout = [
        [sg.Text('Click "Start Sorting" to sort files.')],
        [sg.Button('Start Sorting', key='-START_SORTING-', size=(15, 1))]
    ]

    inflow_layout = [
        [sg.Text('Inflow Directories:')],
        [sg.Listbox(values=inflow_dirs, size=(60, 10), key='-INFLOW_LIST-', select_mode=sg.SELECT_MODE_SINGLE)],
        [sg.Button('Add Inflow Directory', key='-ADD_INFLOW-', size=(20, 1)),
         sg.Button('Remove Selected', key='-REMOVE_INFLOW-', size=(20, 1))]
    ]

    # Prepare outflow data with subfolders up to 4 levels deep
    outflow_data = []
    for ext, dir_path in outflow_dirs.items():
        outflow_data.append([ext, dir_path])
        subfolders = get_subfolders(dir_path, current_depth=1, max_depth=MAX_SUBFOLDER_DEPTH)
        for sub in subfolders:
            outflow_data.append([f"{ext} (sub)", sub])

    outflow_layout = [
        [sg.Text('Outflow Directories (by file extension):')],
        [sg.Table(values=outflow_data,
                  headings=['Extension', 'Directory'],
                  key='-OUTFLOW_TABLE-',
                  auto_size_columns=False,
                  col_widths=[15, 60],
                  display_row_numbers=True,
                  num_rows=10,
                  enable_events=True,
                  select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
        [sg.Button('Add Outflow Directory', key='-ADD_OUTFLOW-', size=(20, 1)),
         sg.Button('Remove Selected', key='-REMOVE_OUTFLOW-', size=(20, 1))]
    ]

    logs_layout = [
        [sg.Text('Log Entries:')],
        [sg.Listbox(values=get_logs(), size=(80, 20), key='-LOG_LIST-', select_mode=sg.SELECT_MODE_SINGLE)],
        [sg.Button('Undo Selected', key='-UNDO_SELECTED-', size=(15, 1)),
         sg.Button('Undo All', key='-UNDO_ALL-', size=(15, 1))]
    ]

    help_layout = [
        [sg.Text('Quasar - File Organizer', font=('Any', 16))],
        [sg.Text('Version 1.1')],
        [sg.Text('Developed by Madhav Krishnan')],
        [sg.Text('This application helps you organize your files by automatically moving them from inflow directories to outflow directories based on file types or intelligent sorting criteria.')]
    ]

    settings_layout = [
        [sg.Text('Any Extension Directory:')],
        [sg.InputText(any_ext_dir, key='-ANY_EXT_DIR-', size=(50,1)),
         sg.FolderBrowse('Browse', key='-BROWSE_ANY_EXT_DIR-')],
        [sg.Button('Save Settings', key='-SAVE_SETTINGS-', size=(15, 1))]
    ]

    layout = [
        [sg.Menu(menu_def)],
        [sg.TabGroup([
            [sg.Tab('Sort', sort_layout),
             sg.Tab('Inflow', inflow_layout),
             sg.Tab('Outflow', outflow_layout),
             sg.Tab('Logs', logs_layout),
             sg.Tab('Help', help_layout),
             sg.Tab('Settings', settings_layout)]
        ])]
    ]

    return sg.Window('Quasar - File Organizer', layout, finalize=True, size=(800, 600))

# ------------------- Main Function ------------------- #

def main():
    inflow_dirs, outflow_dirs, any_ext_dir = load_settings()
    window = create_main_window(inflow_dirs, outflow_dirs, any_ext_dir)

    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == '-ADD_INFLOW-':
            folder = sg.popup_get_folder('Select Inflow Directory')
            if folder and folder not in inflow_dirs:
                inflow_dirs.append(folder)
                window['-INFLOW_LIST-'].update(values=inflow_dirs)
                add_log(f"Added inflow directory: {folder}")
        elif event == '-REMOVE_INFLOW-':
            selected = values['-INFLOW_LIST-']
            if selected:
                inflow_dirs.remove(selected[0])
                window['-INFLOW_LIST-'].update(values=inflow_dirs)
                add_log(f"Removed inflow directory: {selected[0]}")
        elif event == '-ADD_OUTFLOW-':
            ext = sg.popup_get_text('Enter File Extension (e.g., txt)').lower()
            if not ext:
                sg.popup('File extension cannot be empty.')
                continue
            folder = sg.popup_get_folder('Select Outflow Directory')
            if folder and ext:
                outflow_dirs[ext] = folder
                add_log(f"Added outflow directory for .{ext} files: {folder}")
                # Update the outflow table
                outflow_data = []
                for ex, dir_path in outflow_dirs.items():
                    outflow_data.append([ex, dir_path])
                    subfolders = get_subfolders(dir_path, current_depth=1, max_depth=MAX_SUBFOLDER_DEPTH)
                    for sub in subfolders:
                        outflow_data.append([f"{ex} (sub)", sub])
                window['-OUTFLOW_TABLE-'].update(values=outflow_data)
        elif event == '-REMOVE_OUTFLOW-':
            selected = values['-OUTFLOW_TABLE-']
            if selected:
                ext = selected[0][0]
                dir_path = selected[0][1]
                if ext.endswith('(sub)'):
                    sg.popup('Cannot remove subfolder entries directly.')
                else:
                    del outflow_dirs[ext]
                    add_log(f"Removed outflow directory for .{ext} files: {dir_path}")
                    # Update the outflow table
                    outflow_data = []
                    for ex, dir_path in outflow_dirs.items():
                        outflow_data.append([ex, dir_path])
                        subfolders = get_subfolders(dir_path, current_depth=1, max_depth=MAX_SUBFOLDER_DEPTH)
                        for sub in subfolders:
                            outflow_data.append([f"{ex} (sub)", sub])
                    window['-OUTFLOW_TABLE-'].update(values=outflow_data)
        elif event == '-START_SORTING-':
            start_sorting_thread(inflow_dirs, outflow_dirs, any_ext_dir)
            add_log("Started sorting process.")
        elif event == '-SAVE_SETTINGS-':
            any_ext_dir_input = values['-ANY_EXT_DIR-']
            any_ext_dir = any_ext_dir_input
            save_settings(inflow_dirs, outflow_dirs, any_ext_dir)
            add_log("Settings saved successfully.")
            sg.popup('Settings saved successfully!')
        elif event == 'About':
            sg.popup('Quasar - File Organizer\nVersion 1.1\nDeveloped by Madhav Krishnan')
        elif event == '-UNDO_SELECTED-':
            selected_log = values['-LOG_LIST-']
            if selected_log:
                # Extract source and destination from log
                log_entry = selected_log[0]
                # Example log: "2023-10-10 10:10:10 - Moved file.txt to C:\Documents"
                try:
                    parts = log_entry.split(' - ')[1].split(' to ')
                    filename = parts[0].replace('Moved ', '').replace('Intelligently moved ', '').replace('deleted setup executable ', '')
                    dest_dir = parts[1].strip('.')
                    # Find the destination path
                    for move in move_history:
                        src, dest = move
                        if os.path.basename(dest) == filename:
                            undo_move(src, dest)
                            move_history.remove(move)
                            add_log(f"Undid move of {filename} back to {src}")
                            break
                    window['-LOG_LIST-'].update(values=get_logs())
                except Exception as e:
                    add_log(f"Error undoing selected move: {str(e)}")
        elif event == '-UNDO_ALL-':
            undo_all_moves()
            add_log("Undid all moves.")
            window['-LOG_LIST-'].update(values=get_logs())

        # Update logs in the GUI
        window['-LOG_LIST-'].update(values=get_logs())

    window.close()
    save_settings(inflow_dirs, outflow_dirs, any_ext_dir)

if __name__ == '__main__':
    main()
