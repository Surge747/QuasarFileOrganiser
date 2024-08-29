import tkinter as tk
from tkinter import filedialog
import os
from pathlib import Path

# Initialize the main window
app = tk.Tk()
app.title("Quasar - File Organizer")
app.geometry("800x600")
app.configure(bg='#191970')  # Midnight blue background

# Define colors and styles
faded_text_color = "#778899"  # Light Slate Gray for faded text
bright_text_color = "#ffffff"  # White for brightened text
canvas_bg_color = "#1c1c3d"  # Slightly lighter midnight color
font_style = ("Helvetica", 14, "bold")

# Function to select a directory and add it to the corresponding list
def select_directory(side):
    directory = filedialog.askdirectory()
    if directory:
        directory_name = os.path.basename(directory)
        if side == 'inflow':
            inflow_listbox.insert(tk.END, directory_name)
        elif side == 'outflow_folders':
            outflow_folders_listbox.insert(tk.END, directory_name)
        elif side == 'outflow_music':
            outflow_music_listbox.insert(tk.END, directory_name)
        elif side == 'outflow_images':
            outflow_images_listbox.insert(tk.END, directory_name)

# Function to start the file organization process
def start_sorting():
    print("Sorting the files and folders...")

# Inflow Title and Listbox
inflow_title = tk.Label(app, text="Inflow", font=font_style, bg='#191970', fg=bright_text_color)
inflow_title.grid(row=0, column=0, padx=20, pady=10, sticky='n')

inflow_listbox = tk.Listbox(app, font=font_style, bg=canvas_bg_color, fg=bright_text_color, bd=0, highlightthickness=0)
inflow_listbox.grid(row=1, column=0, padx=20, pady=10, sticky='nsew')

# Outflow Title and Sections
outflow_title = tk.Label(app, text="Outflow", font=font_style, bg='#191970', fg=bright_text_color)
outflow_title.grid(row=0, column=1, padx=20, pady=10, sticky='n')

# Folders Section
outflow_folders_title = tk.Label(app, text="Folders", font=font_style, bg='#191970', fg=bright_text_color)
outflow_folders_title.grid(row=1, column=1, padx=20, pady=5, sticky='n')

outflow_folders_listbox = tk.Listbox(app, font=font_style, bg=canvas_bg_color, fg=bright_text_color, bd=0, highlightthickness=0)
outflow_folders_listbox.grid(row=2, column=1, padx=20, pady=5, sticky='nsew')

# Music Section
outflow_music_title = tk.Label(app, text="Music", font=font_style, bg='#191970', fg=bright_text_color)
outflow_music_title.grid(row=3, column=1, padx=20, pady=5, sticky='n')

outflow_music_listbox = tk.Listbox(app, font=font_style, bg=canvas_bg_color, fg=bright_text_color, bd=0, highlightthickness=0)
outflow_music_listbox.grid(row=4, column=1, padx=20, pady=5, sticky='nsew')

# Default Windows Music Folder
default_music_folder = str(Path.home() / "Music")
outflow_music_listbox.insert(tk.END, os.path.basename(default_music_folder))

# Images Section
outflow_images_title = tk.Label(app, text="Images", font=font_style, bg='#191970', fg=bright_text_color)
outflow_images_title.grid(row=5, column=1, padx=20, pady=5, sticky='n')

outflow_images_listbox = tk.Listbox(app, font=font_style, bg=canvas_bg_color, fg=bright_text_color, bd=0, highlightthickness=0)
outflow_images_listbox.grid(row=6, column=1, padx=20, pady=5, sticky='nsew')

# Default Windows Images Folder
default_images_folder = str(Path.home() / "Pictures")
outflow_images_listbox.insert(tk.END, os.path.basename(default_images_folder))

# Sort Button
sort_button = tk.Button(app, text="Sort", font=font_style, command=start_sorting, bd=0, bg='#2980b9', fg=bright_text_color)
sort_button.grid(row=7, column=0, columnspan=2, pady=20)

# Configure the grid to be responsive
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)
app.grid_rowconfigure(3, weight=1)
app.grid_rowconfigure(4, weight=1)
app.grid_rowconfigure(5, weight=1)
app.grid_rowconfigure(6, weight=1)

# Run the application
app.mainloop()
