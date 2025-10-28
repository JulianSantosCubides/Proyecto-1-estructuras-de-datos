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
        Assigns orders to machines based on order priority.
        - Priority 1 -> Machines 1,2,3
        - Priority 2 -> Machines 4,5
        - Priority 3 -> Machine 6
        Within each priority group, assign the order to the machine with the fewest pending orders.
        If all machines in the group are full, try any machine with available capacity.
        If all machines are full, reinsert the order and stop assigning.
        """
        assigned = 0

        # Helper to determine a machine's configured priority.
        # First try an explicit attribute 'priority' (if user modified Machine),
        # otherwise fallback to a mapping by machine id (1-3 -> p1, 4-5 -> p2, 6 -> p3).
        def machine_priority(m):
            # if machine has attribute 'priority' and it's 1/2/3, use it
            p = getattr(m, "priority", None)
            if isinstance(p, int) and p in (1, 2, 3):
                return p
            # fallback mapping by id (safe default)
            if hasattr(m, "id"):
                if 1 <= m.id <= 3:
                    return 1
                elif 4 <= m.id <= 5:
                    return 2
                else:
                    return 3
            # final fallback
            return 1

        # Build groups once per call
        priority_groups = {
            1: [m for m in self.machines if machine_priority(m) == 1],
            2: [m for m in self.machines if machine_priority(m) == 2],
            3: [m for m in self.machines if machine_priority(m) == 3],
        }

        while self.order_queue:
            priority, order_id, order = heapq.heappop(self.order_queue)

            # Get machines for this priority
            group = priority_groups.get(priority, [])
            if not group:
                print(f"No machines configured for priority {priority}.")
                # try fallback: any machine at all
                group = list(self.machines)

            # Filter machines in group that have capacity (<5)
            available_in_group = [m for m in group if m.get_orders_number() < 5]

            chosen_machine = None

            if available_in_group:
                # pick machine with the fewest orders; tie-breaker by machine.id to keep deterministic behavior
                chosen_machine = min(available_in_group, key=lambda m: (m.get_orders_number(), getattr(m, "id", 0)))
            else:
                # group full: try any machine in entire factory with free capacity
                any_available = [m for m in self.machines if m.get_orders_number() < 5]
                if any_available:
                    chosen_machine = min(any_available, key=lambda m: (m.get_orders_number(), getattr(m, "id", 0)))
                    print(f"All machines for priority {priority} are full. Reassigning order to {chosen_machine.name}.")
                else:
                    # all machines full -> reinsert and stop
                    heapq.heappush(self.order_queue, (priority, order_id, order))
                    print("All machines are full. Stopping assignment.")
                    break

            # Assign the order
            chosen_machine.add_orders(order)
            assigned += 1
            print(f"Order {order.id} ({order.productName}) assigned to {chosen_machine.name} (Priority {priority})")

        if assigned == 0:
            print("No new orders were assigned (empty queue or all machines full).")

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
