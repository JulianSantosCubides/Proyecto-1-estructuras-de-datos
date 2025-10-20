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


# General button
class CustomButton(customtkinter.CTkButton):
    def __init__(self, master, text="", function=None):
        super().__init__(
            master=master,
            text=text,
            command=function,
            width=120,
            height=32,
            border_width=0,
            corner_radius=8
        )


# General progress bar
class CustomProgressBar(customtkinter.CTkProgressBar):
    def __init__(self, master):
        super().__init__(
            master=master,
            width=160,
            height=20,
            border_width=2
        )


# General frame (for machines representation)
class customFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master=master,
            width=100,
            height=100,
            corner_radius=10
        )
