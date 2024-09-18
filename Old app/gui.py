from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage

# Set up the base path as the directory containing your script
BASE_PATH = Path(__file__).parent

# Define the assets path relative to the base path
ASSETS_PATH = BASE_PATH / "assets"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()

window.geometry("1000x750")
window.configure(bg = "#212528")


canvas = Canvas(
    window,
    bg = "#212528",
    height = 750,
    width = 1000,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    36.0,
    195.0,
    751.0,
    fill="#2B2B2B",
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    1000.0,
    35.0,
    fill="#65407B",
    outline="")

canvas.create_text(
    68.0,
    697.0,
    anchor="nw",
    text="Settings",
    fill="#FFFFFF",
    font=("Ubuntu Bold", 24 * -1)
)

image_image_1 = PhotoImage(
    file=relative_to_assets("settings.png"))
image_1 = canvas.create_image(
    38.0,
    708.0,
    image=image_image_1
)

canvas.create_text(
    68.0,
    647.0,
    anchor="nw",
    text="Help",
    fill="#FFFFFF",
    font=("Ubuntu Bold", 24 * -1)
)

canvas.create_text(
    68.0,
    600.0,
    anchor="nw",
    text="Logs",
    fill="#FFFFFF",
    font=("Ubuntu Bold", 24 * -1)
)

image_image_2 = PhotoImage(
    file=relative_to_assets("help.png"))
image_2 = canvas.create_image(
    36.0,
    661.0,
    image=image_image_2
)

canvas.create_text(
    68.0,
    154.0,
    anchor="nw",
    text="Outflow",
    fill="#FFFFFF",
    font=("Ubuntu Bold", 24 * -1)
)

image_image_3 = PhotoImage(
    file=relative_to_assets("outflow.png"))
image_3 = canvas.create_image(
    40.0,
    167.0,
    image=image_image_3
)

canvas.create_text(
    68.0,
    107.0,
    anchor="nw",
    text="Inflow",
    fill="#FFFFFF",
    font=("Ubuntu Bold", 24 * -1)
)

canvas.create_text(
    68.0,
    60.0,
    anchor="nw",
    text="Sort",
    fill="#FFFFFF",
    font=("Ubuntu Bold", 24 * -1)
)

image_image_4 = PhotoImage(
    file=relative_to_assets("inflow.png"))
image_4 = canvas.create_image(
    36.0,
    120.0,
    image=image_image_4
)

canvas.create_text(
    315.0,
    3.0,
    anchor="nw",
    text="Quasar - File Organizer",
    fill="#FFFFFF",
    font=("Ubuntu Light", 24 * -1)
)

canvas.create_rectangle(
    192.0,
    36.0,
    1000.0,
    750.0,
    fill="#212528",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("outflowdirectory.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=217.0,
    y=130.0,
    width=395.0,
    height=593.0
)

button_image_2 = PhotoImage(
    file=relative_to_assets("outflowdropdownmenu.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=217.0,
    y=54.0,
    width=331.0,
    height=47.0
)

button_image_3 = PhotoImage(
    file=relative_to_assets("outflowadd.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 clicked"),
    relief="flat"
)
button_3.place(
    x=557.0,
    y=54.0,
    width=55.0,
    height=47.0
)

canvas.create_text(
    679.0,
    121.0,
    anchor="nw",
    text="Outflow",
    fill="#FFFFFF",
    font=("Ubuntu Bold", 50 * -1)
)

canvas.create_text(
    679.0,
    583.0,
    anchor="nw",
    text="Where to put them",
    fill="#FFFFFF",
    font=("Ubuntu Light", 32 * -1)
)

image_image_5 = PhotoImage(
    file=relative_to_assets("add.png"))
image_5 = canvas.create_image(
    585.0,
    80.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("quasar.png"))
image_6 = canvas.create_image(
    819.0,
    395.0,
    image=image_image_6
)

image_image_7 = PhotoImage(
    file=relative_to_assets("sort.png"))
image_7 = canvas.create_image(
    38.0,
    77.0,
    image=image_image_7
)

image_image_8 = PhotoImage(
    file=relative_to_assets("logs.png"))
image_8 = canvas.create_image(
    36.0,
    613.0,
    image=image_image_8
)
window.resizable(False, False)
window.mainloop()
