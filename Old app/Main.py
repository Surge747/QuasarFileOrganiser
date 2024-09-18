from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage

# Set up the base path as the directory containing your script
BASE_PATH = Path(__file__).parent
ASSETS_PATH = BASE_PATH / "assets"

def imgpath(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def load_image(filename: str) -> PhotoImage:
    """Load an image from the assets folder."""
    return PhotoImage(file=imgpath(filename))

def switch_screen(screen_name):
    """Switch the main screen content based on the sidebar button clicked."""
    canvas.delete("screen_content")
    clear_buttons()

    if screen_name == "Sort":
        layout_sort()
    elif screen_name == "Inflow":
        layout_inflow()
    elif screen_name == "Outflow":
        layout_outflow()
    elif screen_name == "Logs":
        layout_logs()
    elif screen_name == "Help":
        layout_help()
    elif screen_name == "Settings":
        layout_settings()

def clear_buttons():
    """Clear buttons from the screen."""
    for widget in window.winfo_children():
        if hasattr(widget, "_name") and widget._name == "screen_button":
            widget.destroy()

def layout_sort():
    canvas.create_text(
        681.0, 130.0, anchor="nw",
        text="Sort", fill="#FFFFFF",
        font=("Ubuntu Bold", 50 * -1),
        tags="screen_content"
    )

def layout_inflow():
    canvas.create_text(
        681.0, 130.0, anchor="nw",
        text="Inflow", fill="#FFFFFF",
        font=("Ubuntu Bold", 50 * -1),
        tags="screen_content"
    )
    canvas.create_text(
        679.0, 583.0, anchor="nw",
        text="Files to be sorted", fill="#FFFFFF",
        font=("Ubuntu Light", 32 * -1),
        tags="screen_content"
    )
    canvas.create_image(
        815.0, 396.0,
        image=blackhole,
        tags="screen_content"
    )
    create_button(
        image=button_image_1, x=217, y=69,
        width=395, height=654,
        command=lambda: print("button_1 clicked"),
        name="screen_button"
    )

def layout_outflow():
    canvas.create_text(
        679.0, 121.0, anchor="nw",
        text="Outflow", fill="#FFFFFF",
        font=("Ubuntu Bold", 50 * -1),
        tags="screen_content"
    )
    canvas.create_text(
        679.0, 583.0, anchor="nw",
        text="Where to put them", fill="#FFFFFF",
        font=("Ubuntu Light", 32 * -1),
        tags="screen_content"
    )
    canvas.create_image(
        585.0, 80.0,
        image=add_image,
        tags="screen_content"
    )
    canvas.create_image(
        819.0, 395.0,
        image=quasar,
        tags="screen_content"
    )
    create_button(
        image=button_image_1, x=217, y=130,
        width=395, height=593,
        command=lambda: print("button_1 clicked"),
        name="screen_button"
    )
    create_button(
        image=button_image_2, x=217, y=54,
        width=331, height=47,
        command=lambda: print("button_2 clicked"),
        name="screen_button"
    )
    create_button(
        image=button_image_3, x=557, y=54,
        width=55, height=47,
        command=lambda: print("button_3 clicked"),
        name="screen_button"
    )

def layout_logs():
    canvas.create_text(
        681.0, 130.0, anchor="nw",
        text="Logs", fill="#FFFFFF",
        font=("Ubuntu Bold", 50 * -1),
        tags="screen_content"
    )

def layout_help():
    canvas.create_text(
        681.0, 130.0, anchor="nw",
        text="Help", fill="#FFFFFF",
        font=("Ubuntu Bold", 50 * -1),
        tags="screen_content"
    )

def layout_settings():
    canvas.create_text(
        681.0, 130.0, anchor="nw",
        text="Settings", fill="#FFFFFF",
        font=("Ubuntu Bold", 50 * -1),
        tags="screen_content"
    )

def create_button(image: PhotoImage, x: int, y: int, width: int, height: int, command, name: str) -> Button:
    button = Button(
        window,
        image=image,
        borderwidth=0,
        highlightthickness=0,
        command=command,
        relief="flat",
        bg="#2B2B2B",  # Ensure background matches the sidebar
        activebackground="#2B2B2B"
    )
    button.place(x=x, y=y, width=width, height=height)
    button._name = name
    return button

def create_sidebar_buttons(screens):
    y_positions = {
        "Sort": 60, "Inflow": 107, "Outflow": 154,
        "Logs": 600, "Help": 647, "Settings": 697
    }
    for screen_name, image in screens.items():
        create_button(
            image=image, x=0, y=y_positions[screen_name],
            width=195, height=50,
            command=lambda name=screen_name: switch_screen(name),
            name=f"{screen_name.lower()}_button"
        )

window = Tk()
window.geometry("1000x750")
window.configure(bg="#212528")

canvas = Canvas(
    window,
    bg="#212528",
    height=750,
    width=1000,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(
    0.0, 36.0, 195.0, 751.0,
    fill="#2B2B2B", outline=""
)
canvas.create_rectangle(
    0.0, 0.0, 1000.0, 35.0,
    fill="#65407B", outline=""
)

# Preload images
blackhole = load_image("blackhole.png")
quasar = load_image("quasar.png")
button_image_1 = load_image("inflowdirectory.png")
button_image_2 = load_image("outflowdropdownmenu.png")
button_image_3 = load_image("outflowadd.png")
add_image = load_image("add.png")

# Sidebar button images
sidebar_images = {
    "Sort": load_image("sort.png"),
    "Inflow": load_image("inflow.png"),
    "Outflow": load_image("outflow.png"),
    "Logs": load_image("logs.png"),
    "Help": load_image("help.png"),
    "Settings": load_image("settings.png")
}

# Create sidebar buttons
create_sidebar_buttons(sidebar_images)

# Top bar text
canvas.create_text(
    315.0, 3.0, anchor="nw",
    text="Quasar - File Organizer",
    fill="#FFFFFF",
    font=("Ubuntu Light", 24 * -1)
)

# Main content (initially showing Sort)
canvas.create_rectangle(
    192.0, 36.0, 1000.0, 750.0,
    fill="#212528", outline=""
)

# Load the default screen (Sort)
switch_screen("Sort")

window.resizable(False, False)
window.mainloop()
