# gui.py
import PySimpleGUI as sg
from settings import load_settings, save_settings
from file_ops import start_sorting_thread, get_logs, add_log, undo_move, undo_all_moves,log_entries,undo_stack
from constants import FILE_TYPES,DEFAULT_OUTFLOW_DIRS
import os

def create_main_window(inflow_dirs, outflow_dirs):
    sg.theme('DarkBlue3')  # You can choose a different theme

    menu_def = [['File', ['Exit']], ['Help', ['About']]]

    # Define the layouts for different tabs
    sort_layout = [
        [sg.Text('Click "Start Sorting" to sort files.')],
        [sg.Button('Start Sorting', key='-START_SORTING-', size=(15, 1))]
    ]

    inflow_layout = [
        [sg.Text('Inflow Directories:')],
        [sg.Listbox(values=inflow_dirs, size=(50, 10), key='-INFLOW_LIST-', enable_events=True)],
        [sg.Button('Add Inflow Directory', key='-ADD_INFLOW-'), sg.Button('Remove Selected', key='-REMOVE_INFLOW-')]
    ]

    outflow_data = [[k, v] for k, v in outflow_dirs.items()]
    outflow_layout = [
        [sg.Text('Outflow Directories (by file extension):')],
        [sg.Table(values=outflow_data, headings=['Extension', 'Directory'], key='-OUTFLOW_TABLE-', auto_size_columns=True, num_rows=10, enable_events=True)],
        [sg.Button('Add Outflow Directory', key='-ADD_OUTFLOW-'), sg.Button('Remove Selected', key='-REMOVE_OUTFLOW-')]
    ]

    logs_layout = [
        [sg.Text('Log Entries:')],
        [sg.Table(values=[], headings=['Timestamp', 'Message'], key='-LOG_TABLE-', auto_size_columns=True, display_row_numbers=True, num_rows=20, enable_events=True, select_mode=sg.TABLE_SELECT_MODE_BROWSE)],
        [sg.Button('Undo Selected', key='-UNDO_SELECTED-', size=(15, 1)), sg.Button('Undo All', key='-UNDO_ALL-', size=(15,1))]
    ]

    help_layout = [
        [sg.Text('Quasar - File Organizer')],
        [sg.Text('Version 1.1')],
        [sg.Text('Developed by Madhav Krishnan')]
    ]

    settings_layout = [
        [sg.Text('Settings will be here')],
        [sg.Button('Save Settings', key='-SAVE_SETTINGS-', size=(15,1))]
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

def update_log_table(window, logs):
    table_data = [[log['timestamp'], log['message']] for log in logs]
    window['-LOG_TABLE-'].update(values=table_data)

def main():
    inflow_dirs, outflow_dirs = load_settings()
    window = create_main_window(inflow_dirs, outflow_dirs)

    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == '-ADD_INFLOW-':
            folder = sg.popup_get_folder('Select Inflow Directory')
            if folder:
                if folder not in inflow_dirs:
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
                ext = ext.lower()
                outflow_dirs[ext] = folder
                window['-OUTFLOW_TABLE-'].update(values=[[k, v] for k, v in outflow_dirs.items()])
        elif event == '-REMOVE_OUTFLOW-':
            selected = values['-OUTFLOW_TABLE-']
            if selected:
                ext = selected[0][0]
                del outflow_dirs[ext]
                window['-OUTFLOW_TABLE-'].update(values=[[k, v] for k, v in outflow_dirs.items()])
        elif event == '-START_SORTING-':
            if not inflow_dirs:
                sg.popup('Please add at least one inflow directory.', title='Error')
                continue
            if not outflow_dirs:
                sg.popup('Please add at least one outflow directory.', title='Error')
                continue
            start_sorting_thread(inflow_dirs, outflow_dirs)
            add_log("Started sorting process.")
        elif event == '-SAVE_SETTINGS-':
            save_settings(inflow_dirs, outflow_dirs)
            sg.popup('Settings saved successfully!', title='Success')
        elif event == 'About':
            sg.popup('Quasar - File Organizer\nVersion 1.1\nDeveloped by Madhav Krishnan', title='About')

        # Update logs in the Logs tab
        update_log_table(window, get_logs())

        # Handle Undo Actions
        if event == '-UNDO_SELECTED-':
            selected_indices = values['-LOG_TABLE-']
            if selected_indices:
                selected_index = selected_indices[0]
                if selected_index < len(log_entries):
                    action = log_entries[selected_index]
                    if 'Moved' in action['message'] or 'Intelligently moved' in action['message']:
                        # Extract file paths from the log message
                        try:
                            parts = action['message'].split(' moved ')
                            filename = parts[0].split('Moved ')[1] if 'Moved' in parts[0] else parts[0].split('Intelligently moved ')[1]
                            dest_dir = parts[1].split(' (')[0] if 'Intelligently moved' in action['message'] else parts[1]
                            src = os.path.join(dest_dir, filename)
                            dest = next((act['dest'] for act in undo_stack if os.path.basename(act['src']) == filename), None)
                            if dest and os.path.exists(src):
                                undo_move({'src': src, 'dest': dest})
                        except Exception as e:
                            add_log(f"Error parsing log for undo: {str(e)}")
            else:
                sg.popup('Please select a log entry to undo.', title='Info')
        elif event == '-UNDO_ALL-':
            undo_all_moves()

    window.close()
    save_settings(inflow_dirs, outflow_dirs)

if __name__ == '__main__':
    main()
