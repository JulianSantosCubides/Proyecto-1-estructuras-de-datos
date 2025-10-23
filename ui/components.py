import tkinter
import customtkinter
from ui.styles import CustomColors


'''NOTE: the 'master' attribute in the following classes indicate which is the parent
screen where the component should be displayed'''
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

# Custom label for machine names
class CustomMachineLabel(customtkinter.CTkLabel):
    def __init__(self, master, text=""):
        super().__init__(
            master=master,
            text=text,
            text_color=CustomColors.white,
            width=60,
            height=25,
            corner_radius=0,
            fg_color=CustomColors.black  # Make black the background
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
            command=function,  # Function to run when an option is selected
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
            width=120,
            height=20,
            border_width=2
        )


# General frame (for machines representation)
class customFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(
            master=master,
            width=100,
            height=50,
            corner_radius=10
        )


# General selector (for products list)
class CustomSelector(customtkinter.CTkOptionMenu):
    def __init__(self, master, values, default_product=None, function=None):
        super().__init__(
            master=master,
            values=values,  # products list
            width=290,
            height=30,
            corner_radius=8,
            command=function  # Function to run when an option is selected
        )
