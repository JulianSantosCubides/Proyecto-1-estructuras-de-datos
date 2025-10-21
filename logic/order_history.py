# TODO: the idea is to use stacks of some way

# It uses a stack (LIFO) to store finished orders

class OrderHistory:
    def __init__(self):
        # Representamos la pila con una lista de Python
        self.history = []

    def add_order(self, order):
        """
        Agrega una orden completada al historial.
        """
        self.history.append(order)
        print(f"🟩 Orden agregada al historial: {order.productName} (ID: {order.id})")

    def get_last_order(self):
        """
        Retorna la última orden completada sin eliminarla.
        Si la pila está vacía, retorna None.
        """
        if not self.history:
            print("⚠️ No hay órdenes en el historial.")
            return None
        return self.history[-1]

    def remove_last_order(self):
        """
        Elimina y retorna la última orden completada (LIFO).
        """
        if not self.history:
            print("⚠️ No hay órdenes para eliminar del historial.")
            return None
        order = self.history.pop()
        print(f"🟥 Orden eliminada del historial: {order.productName} (ID: {order.id})")
        return order

    def get_all_history(self):
        """
        Retorna una lista con todas las órdenes completadas.
        La primera en la lista es la más antigua.
        """
        return list(self.history)

    def get_all_orders(self):
        """
        Retorna las órdenes completadas como una lista de diccionarios
        para que puedan mostrarse fácilmente en la interfaz.
        """
        return [
            {
                "id": order.id,
                "producto": order.productName,
                "cantidad": order.quantity,
                "precio_total": order.totalPrice
            }
            for order in self.history
        ]
