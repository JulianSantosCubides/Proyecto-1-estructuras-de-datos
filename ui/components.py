import tkinter
import customtkinter
from ui.styles import CustomColors


# General label
class CustomLabel(customtkinter.CTkLabel):
    def __init__(self, master, text=""):
        super().__init__(
            master=master,
            text=text,
            text_color=CustomColors.black,
            width=120,
            height=25,
            corner_radius=8
        )


# General input
class CustomInput(customtkinter.CTkEntry):
    def __init__(self, master, placeholderText=""):
        super().__init__(
            master=master,
            width=290,
            height=25,
            corner_radius=10,
            placeholder_text=placeholderText
        )
