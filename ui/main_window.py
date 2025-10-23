import tkinter
import customtkinter

# Import components
from ui.components import CustomLabel, CustomMachineLabel, CustomInput, CustomProgressBar, CustomButton, customFrame, CustomSelector

# Import products
from data.products import productsAndPrices

# Import styles
from ui.styles import CustomColors

# Import logic
import heapq  # to handle queue with priority
from logic.machine import Machine
from logic.orders_manager import OrdersManager
from logic.order_history import OrderHistory


def run_program():
    root_tk = tkinter.Tk()
    root_tk.geometry("750x800")
    root_tk.title("Sistema de gestión de producción")

    # --- CREAR LÓGICA PRINCIPAL ---
    machines = [
        Machine(1, "Máquina 1"),
        Machine(2, "Máquina 2"),
        Machine(3, "Máquina 3"),
        Machine(4, "Máquina 4"),
        Machine(5, "Máquina 5"),
        Machine(6, "Máquina 6"),
    ]

    order_queue = []  # queue with priority
    order_history = OrderHistory()
    manager = OrdersManager(machines)
    manager.order_history = order_history

    # --- FUNCIONES ---
    def product_selected(selected_product):
        try:
            product = selected_product
            quantity = int(firstEntry.get()) if firstEntry.get() else 0
            totalPriceice = productsAndPrices[product] * quantity
            print(f"Producto: {product}, Cantidad: {quantity}, Precio total: ${totalPriceice:,.0f}")
        except ValueError:
            print("⚠️ Ingresa una cantidad válida para seleccionar un producto.")

    def create_order():
        try:
            product_name = productSelector.get()
            quantity = int(firstEntry.get())

            order = manager.create_order(product_name, quantity)
            print(f"Orden creada: {product_name}, cantidad {quantity}")
        except ValueError as e:
            print(f"⚠️ Error: {e}")

    def update_progress_bars():
        status = manager.update_machines_status()
        firstMachineProgressbar.set(status["Máquina 1"])
        secondMachineProgressbar.set(status["Máquina 2"])
        thirdMachineProgressbar.set(status["Máquina 3"])
        fourthMachineProgressbar.set(status["Máquina 4"])
        fifthMachineProgressbar.set(status["Máquina 5"])
        sixthMachineProgressbar.set(status["Máquina 6"])

    def process_order(machine_index):
        finished_order = manager.process_next_order(machine_index)
        if finished_order:
            update_progress_bars()
            print(f"Orden completada: {finished_order}")
        else:
            print("⚠️ No hay órdenes pendientes en esta máquina.")

    def show_order_history():
        """Muestra una ventana con las órdenes completadas (historial tipo pila)."""
        history_window = customtkinter.CTkToplevel(root_tk)
        history_window.title("Historial de órdenes completadas")
        history_window.geometry("400x350")

        title_label = CustomLabel(history_window, "Historial de órdenes completadas")
        title_label.pack(pady=15)

        history_textbox = customtkinter.CTkTextbox(
            history_window,
            width=350,
            height=220,
            fg_color=CustomColors.darkGray,
            text_color="white",
            corner_radius=8
        )
        history_textbox.pack(pady=10)

        completed_orders = order_history.get_all_orders()
        if not completed_orders:
            history_textbox.insert("0.0", "No hay órdenes completadas todavía.")
        else:
            for i, order in enumerate(reversed(completed_orders), start=1):
                order_text = (
                    f"{i}. {order['producto']} - Cantidad: {order['cantidad']} - "
                    f"Precio total: ${order['precio_total']:,}\n"
                )
                history_textbox.insert("end", order_text)

        history_textbox.configure(state="disabled")
        CustomButton(history_window, "Cerrar", history_window.destroy).pack(pady=10)

    # --- UI PRINCIPAL ---
    introductionText = 'Bienvenido. Este es un programa para gestionar las órdenes de producción de una manufacturera de productos metálicos.'
    introductionLabel = CustomLabel(root_tk, introductionText)
    introductionLabel.place(relx=0.5, rely=0.08, anchor=tkinter.CENTER)

    # Product selector
    productNames = list(productsAndPrices.keys())
    selectorLabel = CustomLabel(root_tk, "Ingresa la cantidad y selecciona el producto de la orden:")
    selectorLabel.place(relx=0.5, rely=0.16, anchor=tkinter.CENTER)

    selected_product = tkinter.StringVar(value=productNames[0])
    productSelector = CustomSelector(root_tk, productNames, productNames[0], product_selected)
    productSelector.place(relx=0.5, rely=0.31, anchor=tkinter.CENTER)

    # Quantity input
    firstEntry = CustomInput(root_tk, "Cantidad del producto requerido")
    firstEntry.place(relx=0.5, rely=0.23, anchor=tkinter.CENTER)

    # Create order buttons
    CustomButton(root_tk, "Crear orden", create_order).place(relx=0.35, rely=0.41, anchor=tkinter.CENTER)
    CustomButton(root_tk, "Asignar órdenes a maquinaria",
                 lambda: (manager.assign_all_orders_to_machines(), update_progress_bars())).place(relx=0.6, rely=0.41, anchor=tkinter.CENTER)

    # --- MÁQUINAS FILA SUPERIOR ---
    # Máquina 1
    firstMachineFrame = customFrame(root_tk)
    firstMachineFrame.place(relx=0.25, rely=0.50, anchor=tkinter.CENTER)
    firstMachineFrameName = CustomMachineLabel(root_tk, "Máquina 1")
    firstMachineFrameName.place(relx=0.25, rely=0.50, anchor="center")
    firstMachineProgressbar = CustomProgressBar(root_tk)
    firstMachineProgressbar.place(relx=0.25, rely=0.57, anchor=tkinter.CENTER)
    CustomButton(root_tk, "Procesar orden", lambda: process_order(0)).place(relx=0.25, rely=0.63, anchor=tkinter.CENTER)

    # Máquina 2
    secondMachineFrame = customFrame(root_tk)
    secondMachineFrame.place(relx=0.5, rely=0.50, anchor=tkinter.CENTER)
    secondMachineFrameName = CustomMachineLabel(root_tk, "Máquina 2")
    secondMachineFrameName.place(relx=0.5, rely=0.50, anchor="center")
    secondMachineProgressbar = CustomProgressBar(root_tk)
    secondMachineProgressbar.place(relx=0.5, rely=0.57, anchor=tkinter.CENTER)
    CustomButton(root_tk, "Procesar orden", lambda: process_order(1)).place(relx=0.5, rely=0.63, anchor=tkinter.CENTER)

    # Máquina 3
    thirdMachineFrame = customFrame(root_tk)
    thirdMachineFrame.place(relx=0.75, rely=0.50, anchor=tkinter.CENTER)
    thirdMachineFrameName = CustomMachineLabel(root_tk, "Máquina 3")
    thirdMachineFrameName.place(relx=0.75, rely=0.50, anchor="center")
    thirdMachineProgressbar = CustomProgressBar(root_tk)
    thirdMachineProgressbar.place(relx=0.75, rely=0.57, anchor=tkinter.CENTER)
    CustomButton(root_tk, "Procesar orden", lambda: process_order(2)).place(relx=0.75, rely=0.63, anchor=tkinter.CENTER)

    # --- MÁQUINAS FILA INFERIOR ---
    # Máquina 4
    fourthMachineFrame = customFrame(root_tk)
    fourthMachineFrame.place(relx=0.25, rely=0.75, anchor=tkinter.CENTER)
    fourthMachineFrameName = CustomMachineLabel(root_tk, "Máquina 4")
    fourthMachineFrameName.place(relx=0.25, rely=0.75, anchor="center")
    fourthMachineProgressbar = CustomProgressBar(root_tk)
    fourthMachineProgressbar.place(relx=0.25, rely=0.80, anchor=tkinter.CENTER)
    CustomButton(root_tk, "Procesar orden", lambda: process_order(3)).place(relx=0.25, rely=0.86, anchor=tkinter.CENTER)

    # Máquina 5
    fifthMachineFrame = customFrame(root_tk)
    fifthMachineFrame.place(relx=0.5, rely=0.75, anchor=tkinter.CENTER)
    fifthMachineFrameName = CustomMachineLabel(root_tk, "Máquina 5")
    fifthMachineFrameName.place(relx=0.5, rely=0.75, anchor="center")
    fifthMachineProgressbar = CustomProgressBar(root_tk)
    fifthMachineProgressbar.place(relx=0.5, rely=0.80, anchor=tkinter.CENTER)
    CustomButton(root_tk, "Procesar orden", lambda: process_order(4)).place(relx=0.5, rely=0.86, anchor=tkinter.CENTER)

    # Máquina 6
    sixthMachineFrame = customFrame(root_tk)
    sixthMachineFrame.place(relx=0.75, rely=0.75, anchor=tkinter.CENTER)
    sixthMachineFrameName = CustomMachineLabel(root_tk, "Máquina 6")
    sixthMachineFrameName.place(relx=0.75, rely=0.75, anchor="center")
    sixthMachineProgressbar = CustomProgressBar(root_tk)
    sixthMachineProgressbar.place(relx=0.75, rely=0.80, anchor=tkinter.CENTER)
    CustomButton(root_tk, "Procesar orden", lambda: process_order(5)).place(relx=0.75, rely=0.86, anchor=tkinter.CENTER)

    # --- BOTÓN DE HISTORIAL ---
    CustomButton(root_tk, "Ver historial de órdenes completadas", show_order_history).place(relx=0.83, rely=0.05, anchor=tkinter.CENTER)

    update_progress_bars()
    root_tk.mainloop()
