# This is a programa to management production orders to manufacture...

# Import custom tkinter for  user interface
import tkinter
import customtkinter

# Define colors
black = '#000000'

root_tk = tkinter.Tk()  # create the window
root_tk.geometry("400x240") # Assign size
root_tk.title("CustomTkinter Test") # Set title

def button_event():
    print("button pressed")
    text = entry.get()
    print('texto: ', text)

# Main label
label = customtkinter.CTkLabel(master=root_tk,
                               text="Text introduction",
                               text_color=black,
                               width=120,
                               height=25,
                               corner_radius=8)
label.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

# Inputs
entry = customtkinter.CTkEntry(master=root_tk,
                               width=120,
                               height=25,
                               corner_radius=10)
entry.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)



#Buttons
button = customtkinter.CTkButton(master=root_tk,
                                 text="Crear orden de pedido",
                                 command=button_event,
                                 width=120,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8)
button.place(relx=0.5, rely=0.65, anchor=tkinter.CENTER)




root_tk.mainloop()