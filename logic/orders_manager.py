# It handles all orders and uses priority queues
# TODO: the price is calculated here
import heapq
from logic.order import Order
from logic.machine import Machine
from data.products import productsAndPrices


class OrdersManager:
    def __init__(self, machines):
        self.machines = machines  # Machines list
        self.order_counter = 1  # ID for orders
        self.order_queue = []  # queue with priority (heap)

    def create_order(self, product_name, quantity):
        """
        Creates a new order, adds it to the priority queue, and returns it.
        """
        if product_name not in productsAndPrices:
            raise ValueError("El producto no existe en la lista de precios.")
        if quantity <= 0:
            raise ValueError("La cantidad debe ser mayor que 0.")

        unit_price = productsAndPrices[product_name]
        total_price = unit_price * quantity

        new_order = Order(
            id=self.order_counter,
            productName=product_name,
            quantity=quantity,
            price=total_price
        )

        self.order_counter += 1

        # Add to the priority queue, taking order.id into account to avoid errors
        heapq.heappush(self.order_queue, (new_order.priority, new_order.id, new_order))

        print(f"Orden creada (P{new_order.priority}): {new_order.productName} - ${new_order.totalPrice:,.0f}")
        return new_order

    def assign_all_orders_to_machines(self):
        """
        Asigna órdenes a máquinas según su prioridad:
        Prioridad 1 -> Máquina 1
        Prioridad 2 -> Máquina 2
        Prioridad 3 -> Máquina 3
        """
        assigned = 0
    
        while self.order_queue:
            priority, order_id, order = heapq.heappop(self.order_queue)
    
            # Determinar máquina según la prioridad (1, 2 o 3)
            index = min(priority - 1, len(self.machines) - 1)
            machine = self.machines[index]
    
            if machine.get_orders_number() < 5:
                machine.add_orders(order)
                assigned += 1
                print(f"Orden {order.id} ({order.productName}) asignada a {machine.name} (Prioridad {priority})")
            else:
                # Si la máquina está llena, intentamos otra
                alternative = None
                for m in self.machines:
                    if m.get_orders_number() < 5:
                        alternative = m
                        break
                if alternative:
                    alternative.add_orders(order)
                    assigned += 1
                    print(f"{machine.name} llena. Orden {order.id} reasignada a {alternative.name}")
                else:
                    # Si todas están llenas, reinsertar la orden y detener
                    heapq.heappush(self.order_queue, (priority, order_id, order))
                    print("Todas las máquinas están llenas. Se detuvo la asignación.")
                    break
    
        if assigned == 0:
            print("No se asignaron nuevas órdenes (cola vacía o máquinas llenas).")
    
        return assigned
    
    def update_machines_status(self):
        status = {}
        for machine in self.machines:
            orders = machine.get_orders_number()
            progress = orders / 5  # máximo 5 órdenes
            status[machine.name] = progress
        return status

    def process_next_order(self, machine_index):
        """
        Processes (removes) the next order in the specified machine.
        """
        if machine_index < 0 or machine_index >= len(self.machines):
            raise IndexError("Índice de máquina inválido.")

        machine = self.machines[machine_index]
        finished_order = machine.process_next()

        if finished_order:
            print(f"Orden procesada en {machine.name}: {finished_order.productName}")
            # Add to the history (stack)
            self.order_history.add_order(finished_order)
            return finished_order
        else:
            print(f"No hay órdenes pendientes en {machine.name}.")
            return None
