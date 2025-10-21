# It handles all orders and uses priority queues
# TODO: the price is calculated here
import heapq
from logic.order import Order
from logic.machine import Machine
from data.products import productsAndPrices


class OrdersManager:
    def __init__(self, machines):
        self.machines = machines  # Lista de objetos Machine
        self.order_counter = 1  # ID autoincremental para órdenes (lo sigues usando si quieres)
        self.order_queue = []  # Cola con prioridad (heap)

    def create_order(self, product_name, quantity):
        """
        Crea una nueva orden, la añade a la cola con prioridad y la retorna.
        """
        if product_name not in productsAndPrices:
            raise ValueError("El producto no existe en la lista de precios.")
        if quantity <= 0:
            raise ValueError("La cantidad debe ser mayor que 0.")

        unit_price = productsAndPrices[product_name]
        total_price = unit_price * quantity

        # Crear la orden (la clase Order asigna su propio id usando Order.nextId)
        new_order = Order(
            id=self.order_counter,
            productName=product_name,
            quantity=quantity,
            price=total_price
        )

        # Si prefieres mantener self.order_counter separado, incrementarlo:
        self.order_counter += 1

        # Agregar a la cola con prioridad. Desempate por order.id para evitar TypeError
        heapq.heappush(self.order_queue, (new_order.priority, new_order.id, new_order))

        print(f"🟢 Orden creada (P{new_order.priority}): {new_order.productName} - ${new_order.totalPrice:,.0f}")
        return new_order

    def assign_all_orders_to_machines(self):
        """
        Asigna órdenes de la cola a las máquinas disponibles respetando prioridad (1 > 2 > 3).
        Intenta asignar tantas órdenes como sea posible hasta llenar las máquinas.
        """
        assigned = 0
        while self.order_queue:
            # Extraer la siguiente orden por prioridad (y desempate por id)
            priority, order_id, order = heapq.heappop(self.order_queue)

            assigned_successfully = False
            for machine in self.machines:
                if machine.get_orders_number() < 5:
                    machine.add_orders(order)
                    assigned_successfully = True
                    assigned += 1
                    print(f"⚙️ Orden {order.id} ({order.productName}) asignada a {machine.name} (P{priority})")
                    break

            if not assigned_successfully:
                # Si no hay espacio en las máquinas, reinsertamos la orden y salimos.
                heapq.heappush(self.order_queue, (priority, order_id, order))
                print("❌ No hay más espacio en máquinas; se detuvo la asignación.")
                break

        if assigned == 0:
            print("⚠️ No se asignaron nuevas órdenes (cola vacía o máquinas llenas).")
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
        Procesa (remueve) la siguiente orden en la máquina indicada.
        """
        if machine_index < 0 or machine_index >= len(self.machines):
            raise IndexError("Índice de máquina inválido.")

        machine = self.machines[machine_index]
        finished_order = machine.process_next()

        if finished_order:
            print(f"Orden procesada en {machine.name}: {finished_order.productName}")
            # manager asume tener order_history asignado externamente (como lo haces en main_window)
            self.order_history.add_order(finished_order)
            return finished_order
        else:
            print(f"No hay órdenes pendientes en {machine.name}.")
            return None