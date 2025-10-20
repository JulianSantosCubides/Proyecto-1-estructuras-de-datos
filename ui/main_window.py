# Import custom tkinter for  user interface
import tkinter
import customtkinter

# Import components
from ui.components import CustomLabel, CustomInput, CustomProgressBar, CustomButton, customFrame  # Classes for general texts, inputs, progressBar, buttons and frames

# Import styles
from ui.styles import CustomColors

def run_program():
    root_tk = tkinter.Tk()  # The window
    root_tk.geometry("800x480")  # Size
    root_tk.title("Sistema de gestión de producción")  # Window title


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
    createOrderButton = CustomButton(root_tk, "Crear orden de pedido", button_event)
    createOrderButton.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

    # Progress bar
    progressbar = CustomProgressBar(root_tk)
    progressbar.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

    progressbarValue = 0.7  #  Set this value for progress bar. It can be time, and it can be applied to progress work in machines and be updating each minute or something like that.
    progressbar.set(progressbarValue)

    #  frame: it can be used to visually represent the machines (3 machines)
    firstMachineFrame = customFrame(root_tk)
    firstMachineFrame.place(relx=0.3, rely=0.75, anchor=tkinter.CENTER)

    #  frame for second machine
    secondMachineFrame = customFrame(root_tk)
    secondMachineFrame.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)

    #  frame for third machine
    thirdMachineFrame = customFrame(root_tk)
    thirdMachineFrame.place(relx=0.7, rely=0.75, anchor=tkinter.CENTER)

    # run UI
    root_tk.mainloop()
