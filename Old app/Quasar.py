import os
import shutil
import threading
import time
import PySimpleGUI as sg
from pathlib import Path

# Global variables
inflow_dirs = []
outflow_dirs = {}
log_entries = []

# Function to save settings
def save_settings():
    settings = {'inflow_dirs': inflow_dirs, 'outflow_dirs': outflow_dirs}
    with open('../settings.ini', 'w') as f:
        f.write(str(settings))

# Function to load settings
def load_settings():
    global inflow_dirs, outflow_dirs
    if os.path.exists('../settings.ini'):
        with open('../settings.ini', 'r') as f:
            settings = eval(f.read())
            inflow_dirs = settings.get('inflow_dirs', [])
            outflow_dirs = settings.get('outflow_dirs', {})

# Function to log actions
def add_log(entry):
    log_entries.append(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {entry}")

# Function to sort files
def sort_files():
    for inflow in inflow_dirs:
        for filename in os.listdir(inflow):
            file_path = os.path.join(inflow, filename)
            if os.path.isfile(file_path):
                ext = filename.split('.')[-1].lower()
                dest_dir = outflow_dirs.get(ext, None)
                if dest_dir:
                    dest_path = os.path.join(dest_dir, filename)
                    shutil.move(file_path, dest_path)
                    add_log(f"Moved {filename} to {dest_dir}")
                else:
                    add_log(f"No outflow directory for .{ext} files")

# Function to start sorting in a separate thread
def start_sorting_thread():
    threading.Thread(target=sort_files, daemon=True).start()

# GUI Layouts
def create_main_window():
    menu_def = [['File', ['Exit']], ['Help', ['About']]]

    # Define the layouts for different tabs
    sort_layout = [
        [sg.Text('Click "Start Sorting" to sort files.')],
        [sg.Button('Start Sorting', key='-START_SORTING-')]
    ]

    inflow_layout = [
        [sg.Text('Inflow Directories:')],
        [sg.Listbox(values=inflow_dirs, size=(50, 10), key='-INFLOW_LIST-')],
        [sg.Button('Add Inflow Directory', key='-ADD_INFLOW-'), sg.Button('Remove Selected', key='-REMOVE_INFLOW-')]
    ]

    outflow_layout = [
        [sg.Text('Outflow Directories (by file extension):')],
        [sg.Table(values=[[k, v] for k, v in outflow_dirs.items()],
                  headings=['Extension', 'Directory'],
                  key='-OUTFLOW_TABLE-', auto_size_columns=True)],
        [sg.Button('Add Outflow Directory', key='-ADD_OUTFLOW-'), sg.Button('Remove Selected', key='-REMOVE_OUTFLOW-')]
    ]

    logs_layout = [
        [sg.Text('Log Entries:')],
        [sg.Multiline('\n'.join(log_entries), size=(80, 20), key='-LOGS-')]
    ]

    help_layout = [
        [sg.Text('Quasar - File Organizer')],
        [sg.Text('Version 1.0')],
        [sg.Text('Developed by Madhav Krishnan')]
    ]

    settings_layout = [
        [sg.Text('Settings will be here')],
        [sg.Button('Save Settings', key='-SAVE_SETTINGS-')]
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

    return sg.Window('Quasar - File Organizer', layout, finalize=True)

def main():
    load_settings()
    window = create_main_window()

    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == '-ADD_INFLOW-':
            folder = sg.popup_get_folder('Select Inflow Directory')
            if folder:
                inflow_dirs.append(folder)
                window['-INFLOW_LIST-'].update(values=inflow_dirs)
        elif event == '-REMOVE_INFLOW-':
            selected = values['-INFLOW_LIST-']
            if selected:
                inflow_dirs.remove(selected[0])
                window['-INFLOW_LIST-'].update(values=inflow_dirs)
        elif event == '-ADD_OUTFLOW-':
            ext = sg.popup_get_text('Enter File Extension (e.g., txt)')
            folder = sg.popup_get_folder('Select Outflow Directory')
            if ext and folder:
                outflow_dirs[ext.lower()] = folder
                window['-OUTFLOW_TABLE-'].update(values=[[k, v] for k, v in outflow_dirs.items()])
        elif event == '-REMOVE_OUTFLOW-':
            selected = values['-OUTFLOW_TABLE-']
            if selected:
                ext = selected[0][0]
                del outflow_dirs[ext]
                window['-OUTFLOW_TABLE-'].update(values=[[k, v] for k, v in outflow_dirs.items()])
        elif event == '-START_SORTING-':
            start_sorting_thread()
        elif event == '-SAVE_SETTINGS-':
            save_settings()
            sg.popup('Settings saved successfully!')
        elif event == 'About':
            sg.popup('Quasar - File Organizer\nVersion 1.0\nDeveloped by Madhav Krishnan')

        # Update logs
        window['-LOGS-'].update('\n'.join(log_entries))

    window.close()
    save_settings()

if __name__ == '__main__':
    main()
