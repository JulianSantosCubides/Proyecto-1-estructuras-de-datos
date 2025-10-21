# It handles all orders and uses priority queues
# TODO: the price is calculated here

# It handles all orders and uses priority queues
from logic.order import Order
from logic.machine import Machine
from data.products import productsAndPrices


class OrdersManager:
    def __init__(self, machines):
        self.machines = machines  # Lista de objetos Machine
        self.order_counter = 1  # ID autoincremental para órdenes

    def create_order(self, product_name, quantity):
        """
        Crea una nueva orden y la retorna.
        Calcula el precio multiplicando la cantidad por el valor unitario.
        """
        if product_name not in productsAndPrices:
            raise ValueError("El producto no existe en la lista de precios.")
        if quantity <= 0:
            raise ValueError("La cantidad debe ser mayor que 0.")

        # Calcular precio total
        unit_price = productsAndPrices[product_name]
        totalPrice = unit_price * quantity

        # Crear la orden
        new_order = Order(
            id=self.order_counter,
            productName=product_name,
            quantity=quantity,
            price=totalPrice
        )

        # Incrementar contador para la siguiente orden
        self.order_counter += 1
        return new_order

    def assign_order_to_machine(self, order):
        """
        Busca una máquina con espacio (< 5 órdenes) y le asigna la orden.
        Si todas las máquinas están llenas, retorna False.
        """
        for machine in self.machines:
            if machine.get_orders_number() < 5:
                machine.add_orders(order)
                return True
        print("Error: No hay máquinas disponibles (todas tiene 5 órdenes).")
        return False

    def update_machines_status(self):
        """
        Retorna un diccionario con el estado actual de las máquinas,
        para actualizar las progress bars.
        """
        status = {}
        for machine in self.machines:
            orders = machine.get_orders_number()
            progress = orders / 5  # máximo 5 órdenes
            status[machine.name] = progress
        return status

    def process_next_order(self, machine_index):
        """
        Procesa (remueve) la siguiente orden en la máquina indicada.
        """
        if machine_index < 0 or machine_index >= len(self.machines):
            raise IndexError("Índice de máquina inválido.")

        machine = self.machines[machine_index]
        finished_order = machine.process_next()

        if finished_order:
            print(f"Orden procesada en {machine.name}: {finished_order.productName}")
            self.order_history.add_order(finished_order)
            return finished_order  # TODO: validate if it's necessary to remove this order
        else:
            print(f"No hay órdenes pendientes en {machine.name}.")
            return None


## Andres changes
'''from queue import PriorityQueue, Queue
from order import Order, calculate_priority
from machine import Machine
from order_history import OrderHistory

class OrdersManager:
    _order_id_counter = 0
    _machine_id_counter = 0

    def __init__(self, history_manager=None):
        # Colas por prioridad
        self.pending_orders_priority_1 = PriorityQueue()
        self.pending_orders_priority_2 = PriorityQueue()
        self.pending_orders_priority_3 = PriorityQueue()
        # Seguimiento general
        self.in_process_orders = {}
        self.available_machines = []
        self.all_machines = {}
        self.history_manager = history_manager if history_manager else OrderHistory()

    # --- ÓRDENES ---

    def create_order(self, product_name, quantity, price):
        # Crea y agrega una nueva orden
        OrdersManager._order_id_counter += 1
        order_id = f"order-{OrdersManager._order_id_counter}"
        new_order = Order(order_id, product_name, quantity, price)
        self._add_order_to_priority_queue(new_order)
        print(f"Orden '{new_order.id}' creada con prioridad {new_order.priority} y estado '{new_order.status}'.")
        return new_order

    def _add_order_to_priority_queue(self, order):
        # Añade la orden a su cola según prioridad
        if order.priority == 1:
            self.pending_orders_priority_1.put((order.price * -1, order))
        elif order.priority == 2:
            self.pending_orders_priority_2.put((order.price * -1, order))
        elif order.priority == 3:
            self.pending_orders_priority_3.put((order.price * -1, order))
        else:
            print(f"Advertencia: Prioridad desconocida para la orden {order.id}.")

    def get_next_pending_order(self):
        # Obtiene la siguiente orden pendiente
        if not self.pending_orders_priority_1.empty():
            _, order = self.pending_orders_priority_1.get()
            return order
        elif not self.pending_orders_priority_2.empty():
            _, order = self.pending_orders_priority_2.get()
            return order
        elif not self.pending_orders_priority_3.empty():
            _, order = self.pending_orders_priority_3.get()
            return order
        return None

    def get_pending_orders_count(self):
        # Total de órdenes pendientes
        return self.pending_orders_priority_1.qsize() + \
               self.pending_orders_priority_2.qsize() + \
               self.pending_orders_priority_3.qsize()

    def update_order_status(self, order_id, new_status):
        # Actualiza el estado de una orden activa
        if order_id in self.in_process_orders:
            self.in_process_orders[order_id].status = new_status
            print(f"Estado de la orden '{order_id}' actualizado a '{new_status}'.")
            return True
        print(f"Error: Orden '{order_id}' no encontrada en proceso.")
        return False

    def mark_order_as_completed(self, order_id):
        # Marca la orden como terminada y la pasa al historial
        if order_id in self.in_process_orders:
            order = self.in_process_orders.pop(order_id)
            order.status = "terminada"
            self.history_manager.add_to_history(order)
            print(f"Orden '{order_id}' marcada como completada.")
            return True
        print(f"Error: No se puede marcar '{order_id}', no está en proceso.")
        return False

    # --- MÁQUINAS ---

    def register_machine(self, name):
        # Registra una nueva máquina
        OrdersManager._machine_id_counter += 1
        machine_id = f"machine-{OrdersManager._machine_id_counter}"
        new_machine = Machine(machine_id, name)
        self.all_machines[machine_id] = new_machine
        self.available_machines.append(new_machine)
        print(f"Máquina '{name}' ({machine_id}) registrada.")
        return new_machine

    def get_available_machines(self):
        # Devuelve máquinas disponibles
        return self.available_machines

    def set_machine_unavailable(self, machine):
        # Marca una máquina como ocupada
        if machine in self.available_machines:
            self.available_machines.remove(machine)
            print(f"Máquina '{machine.name}' ({machine.id}) no disponible.")
            return True
        print(f"Advertencia: '{machine.name}' ya no estaba disponible.")
        return False

    def set_machine_available(self, machine):
        # Marca una máquina como libre
        if machine not in self.available_machines and machine in self.all_machines.values():
            self.available_machines.append(machine)
            print(f"Máquina '{machine.name}' ({machine.id}) disponible.")
            return True
        print(f"Advertencia: '{machine.name}' ya estaba disponible o no registrada.")
        return False

    # --- ASIGNACIÓN DE ÓRDENES ---

    def assign_orders_to_machines(self):
        # Asigna órdenes pendientes a máquinas libres
        assigned_count = 0
        while self.available_machines and self.get_pending_orders_count() > 0:
            order_to_assign = self.get_next_pending_order()
            if order_to_assign:
                if self.available_machines:
                    machine = self.available_machines.pop(0)
                    machine.add_orders(order_to_assign)
                    order_to_assign.status = "en proceso"
                    self.in_process_orders[order_to_assign.id] = order_to_assign
                    self.set_machine_unavailable(machine)
                    print(f"Orden '{order_to_assign.id}' asignada a '{machine.name}'.")
                    assigned_count += 1
                else:
                    self._add_order_to_priority_queue(order_to_assign)
                    print("No hay máquinas disponibles, orden reinsertada.")
                    break
            else:
                print("No hay órdenes pendientes.")
                break
        if assigned_count == 0:
            print("No se asignaron nuevas órdenes.")
        return assigned_count

    def process_machine_completion(self, machine_id):
        # Procesa la finalización de una orden
        machine = self.all_machines.get(machine_id)
        if not machine:
            print(f"Error: Máquina '{machine_id}' no encontrada.")
            return None
        completed_order = machine.process_next()
        if completed_order:
            self.mark_order_as_completed(completed_order.id)
            self.set_machine_available(machine)
            return completed_order
        else:
            print(f"Máquina '{machine.name}' no tenía órdenes.")
            self.set_machine_available(machine)
            return None

    # --- MONITOREO ---

    def get_system_status(self):
        # Retorna resumen del sistema
        return {
            "pending_orders": {
                "total": self.get_pending_orders_count(),
                "priority_1": self.pending_orders_priority_1.qsize(),
                "priority_2": self.pending_orders_priority_2.qsize(),
                "priority_3": self.pending_orders_priority_3.qsize(),
            },
            "in_process_orders": len(self.in_process_orders),
            "available_machines": len(self.available_machines),
            "total_machines": len(self.all_machines),
            "history_count": self.history_manager.get_history_count()
        }

    def display_system_status(self):
        # Muestra el estado actual
        status = self.get_system_status()
        print("\n--- Estado del Sistema ---")
        print(f"Órdenes Pendientes: {status['pending_orders']['total']}")
        print(f"  - P1: {status['pending_orders']['priority_1']}")
        print(f"  - P2: {status['pending_orders']['priority_2']}")
        print(f"  - P3: {status['pending_orders']['priority_3']}")
        print(f"En Proceso: {status['in_process_orders']}")
        print(f"Máquinas Libres: {status['available_machines']}")
        print(f"Máquinas Totales: {status['total_machines']}")
        print(f"Historial: {status['history_count']}")
        print("--------------------------")
        if status['in_process_orders'] > 0:
            print("Órdenes en proceso:")
            for order_id, order in self.in_process_orders.items():
                print(f"  - {order_id} ({order.productName}), Cant: {order.quantity}, Precio: ${order.price}, P: {order.priority}")
        if status['available_machines'] < status['total_machines']:
            print("Máquinas ocupadas:")
            occupied_machines = [m for m in self.all_machines.values() if m not in self.available_machines]
            for machine in occupied_machines:
                print(f"  - {machine.name} ({machine.id}) con {machine.get_orders_number()} órdenes.")
                '''

