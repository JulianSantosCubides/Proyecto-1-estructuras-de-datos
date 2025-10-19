# Import custom tkinter for  user interface
import tkinter
import customtkinter

# Import components
from ui.components import CustomLabel, CustomInput  # Classes for general texts, inputs, buttons and frames

# Import styles
from ui.styles import CustomColors

# Colors
black = '#000000'

root_tk = tkinter.Tk()  # The window
root_tk.geometry("800x480")  # Size
root_tk.title("CustomTkinter Test")  # Window title


# Functions
def button_event():
    print("button pressed")
    text = firstEntry.get()
    print('texto: ', text)


# Introduction text
introductionText = 'Bienvenido. Este es un programa para gestionar las ordenes de producción para productos metálicos.'

# Main label
introductionLabel = CustomLabel(root_tk, introductionText)
introductionLabel.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

# TODO: validate if the priority should be given or calculated based on price or quantity or product type or anything
# Inputs
firstEntry = CustomInput(root_tk, "Ingresa la cantidad del producto requerido")
firstEntry.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

# Buttons
button = customtkinter.CTkButton(master=root_tk,
                                 text="Crear orden de pedido",
                                 command=button_event,
                                 width=120,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8)
button.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

# Progress bar
progressbar = customtkinter.CTkProgressBar(master=root_tk,
                                           width=160,
                                           height=20,
                                           border_width=2)
progressbar.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

progressbarValue = 0.7  #  Set this value for progress bar. It can be time, and it can be applied to progress work in machines and be updating each minute or something like that.
progressbar.set(progressbarValue)

#  frame: it can be used to visually represent the machines
frame = customtkinter.CTkFrame(master=root_tk,
                               width=100,
                               height=100,
                               corner_radius=10)
frame.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

# run UI
root_tk.mainloop()
