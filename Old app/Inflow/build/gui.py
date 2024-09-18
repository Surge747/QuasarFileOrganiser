from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"/Old app/Inflow\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def switch_screen(screen_name):
    """Switch the main screen content based on the sidebar button clicked."""
    # Clear the main content area
    canvas.delete("screen_content")

    if screen_name == "Inflow":
        # Restore the Inflow layout
        canvas.create_text(
            681.0,
            130.0,
            anchor="nw",
            text="Inflow",
            fill="#FFFFFF",
            font=("Ubuntu Bold", 50 * -1),
            tags="screen_content"  # Tag for easy deletion later
        )
        canvas.create_text(
            679.0,
            583.0,
            anchor="nw",
            text="Files to be sorted",
            fill="#FFFFFF",
            font=("Ubuntu Light", 32 * -1),
            tags="screen_content"
        )
        canvas.create_image(
            815.0,
            396.0,
            image=image_image_5,
            tags="screen_content"
        )

        # Add the button only for the Inflow screen
        button_1 = Button(
            window,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=217.0,
            y=69.0,
            width=395.0,
            height=654.0
        )
        button_1.lift()  # Ensure the button is above other widgets
        # Add a tag to the button for easy management
        button_1._name = "inflow_button"
    else:
        # Remove the inflow button if it exists
        for widget in window.winfo_children():
            if hasattr(widget, "_name") and widget._name == "inflow_button":
                widget.destroy()

    if screen_name == "Outflow":
        canvas.create_text(
            681.0,
            130.0,
            anchor="nw",
            text="Outflow",
            fill="#FFFFFF",
            font=("Ubuntu Bold", 50 * -1),
            tags="screen_content"
        )

    elif screen_name == "Settings":
        canvas.create_text(
            681.0,
            130.0,
            anchor="nw",
            text="Settings",
            fill="#FFFFFF",
            font=("Ubuntu Bold", 50 * -1),
            tags="screen_content"
        )

    elif screen_name == "Help":
        canvas.create_text(
            681.0,
            130.0,
            anchor="nw",
            text="Help",
            fill="#FFFFFF",
            font=("Ubuntu Bold", 50 * -1),
            tags="screen_content"
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
    0.0,
    36.0,
    195.0,
    751.0,
    fill="#2B2B2B",
    outline=""
)

canvas.create_rectangle(
    0.0,
    0.0,
    1000.0,
    35.0,
    fill="#65407B",
    outline=""
)

# Convert sidebar text and images to buttons with screen switching functionality

# Inflow Button (with icon representing Inflow, e.g., download arrow)
button_inflow_image = PhotoImage(file=relative_to_assets("image_4.png"))
button_inflow = Button(
    window,
    image=button_inflow_image,
    text="Inflow",
    compound="left",
    font=("Ubuntu Bold", 24 * -1),
    fg="#FFFFFF",
    bg="#2B2B2B",
    bd=0,
    command=lambda: switch_screen("Inflow")
)
button_inflow.place(x=0, y=57, width=195, height=50)

# Outflow Button (with icon representing Outflow, e.g., upload arrow)
button_outflow_image = PhotoImage(file=relative_to_assets("image_3.png"))
button_outflow = Button(
    window,
    image=button_outflow_image,
    text="Outflow",
    compound="left",
    font=("Ubuntu Bold", 24 * -1),
    fg="#FFFFFF",
    bg="#2B2B2B",
    bd=0,
    command=lambda: switch_screen("Outflow")
)
button_outflow.place(x=0, y=107, width=195, height=50)

# Help Button (with icon representing Help, e.g., question mark)
button_help_image = PhotoImage(file=relative_to_assets("image_2.png"))
button_help = Button(
    window,
    image=button_help_image,
    text="Help",
    compound="left",
    font=("Ubuntu Bold", 24 * -1),
    fg="#FFFFFF",
    bg="#2B2B2B",
    bd=0,
    command=lambda: switch_screen("Help")
)
button_help.place(x=0, y=643, width=195, height=50)

# Settings Button (with icon representing Settings, e.g., gear icon)
button_settings_image = PhotoImage(file=relative_to_assets("image_1.png"))
button_settings = Button(
    window,
    image=button_settings_image,
    text="Settings",
    compound="left",
    font=("Ubuntu Bold", 24 * -1),
    fg="#FFFFFF",
    bg="#2B2B2B",
    bd=0,
    command=lambda: switch_screen("Settings")
)
button_settings.place(x=0, y=694, width=195, height=50)

# Top bar text
canvas.create_text(
    315.0,
    3.0,
    anchor="nw",
    text="Quasar - File Organizer",
    fill="#FFFFFF",
    font=("Ubuntu Light", 24 * -1)
)

# Main content (initially showing Inflow)
canvas.create_rectangle(
    192.0,
    36.0,
    1000.0,
    750.0,
    fill="#212528",
    outline=""
)

# Inflow screen background image (e.g., visual related to file inflow)
image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))

# Add Directory button for the Inflow screen
button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))

# Load the default screen (Inflow)
switch_screen("Inflow")

window.resizable(False, False)
window.mainloop()
