# It handles all orders and uses priority queues
# TODO: the price is calculated here

# It handles all orders and uses priority queues
from queue import PriorityQueue, Queue
from order import Order, calculate_priority
from machine import Machine
from order_history import OrderHistory

class OrdersManager:
    _order_id_counter = 0
    _machine_id_counter = 0

    def __init__(self, history_manager=None):
        # Queues by priority
        self.pending_orders_priority_1 = PriorityQueue()
        self.pending_orders_priority_2 = PriorityQueue()
        self.pending_orders_priority_3 = PriorityQueue()
        # General tracking
        self.in_process_orders = {}
        self.available_machines = []
        self.all_machines = {}
        self.history_manager = history_manager if history_manager else OrderHistory()

    # --- ORDERS ---

    def create_order(self, product_name, quantity, price):
        # Creates and adds a new order
        OrdersManager._order_id_counter += 1
        order_id = f"order-{OrdersManager._order_id_counter}"
        new_order = Order(order_id, product_name, quantity, price)
        self._add_order_to_priority_queue(new_order)
        print(f"Order '{new_order.id}' created with priority {new_order.priority} and status '{new_order.status}'.")
        return new_order

    def _add_order_to_priority_queue(self, order):
        # Adds an order to its corresponding priority queue
        if order.priority == 1:
            self.pending_orders_priority_1.put((order.price * -1, order))
        elif order.priority == 2:
            self.pending_orders_priority_2.put((order.price * -1, order))
        elif order.priority == 3:
            self.pending_orders_priority_3.put((order.price * -1, order))
        else:
            print(f"Warning: Unknown priority for order {order.id}.")

    def get_next_pending_order(self):
        # Gets the next pending order from the queues
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
        # Returns the total number of pending orders
        return self.pending_orders_priority_1.qsize() + \
               self.pending_orders_priority_2.qsize() + \
               self.pending_orders_priority_3.qsize()

    def update_order_status(self, order_id, new_status):
        # Updates the status of an active order
        if order_id in self.in_process_orders:
            self.in_process_orders[order_id].status = new_status
            print(f"Order '{order_id}' status updated to '{new_status}'.")
            return True
        print(f"Error: Order '{order_id}' not found in process list.")
        return False

    def mark_order_as_completed(self, order_id):
        # Marks an order as completed and moves it to history
        if order_id in self.in_process_orders:
            order = self.in_process_orders.pop(order_id)
            order.status = "completed"
            self.history_manager.add_to_history(order)
            print(f"Order '{order_id}' marked as completed.")
            return True
        print(f"Error: Cannot mark '{order_id}', not found in process list.")
        return False

    # --- MACHINES ---

    def register_machine(self, name):
        # Registers a new machine
        OrdersManager._machine_id_counter += 1
        machine_id = f"machine-{OrdersManager._machine_id_counter}"
        new_machine = Machine(machine_id, name)
        self.all_machines[machine_id] = new_machine
        self.available_machines.append(new_machine)
        print(f"Machine '{name}' ({machine_id}) registered.")
        return new_machine

    def get_available_machines(self):
        # Returns all available machines
        return self.available_machines

    def set_machine_unavailable(self, machine):
        # Marks a machine as busy/unavailable
        if machine in self.available_machines:
            self.available_machines.remove(machine)
            print(f"Machine '{machine.name}' ({machine.id}) set as unavailable.")
            return True
        print(f"Warning: '{machine.name}' was already unavailable.")
        return False

    def set_machine_available(self, machine):
        # Marks a machine as available/free
        if machine not in self.available_machines and machine in self.all_machines.values():
            self.available_machines.append(machine)
            print(f"Machine '{machine.name}' ({machine.id}) set as available.")
            return True
        print(f"Warning: '{machine.name}' was already available or not registered.")
        return False

    # --- ORDER ASSIGNMENT ---

    def assign_orders_to_machines(self):
        # Assigns pending orders to available machines
        assigned_count = 0
        while self.available_machines and self.get_pending_orders_count() > 0:
            order_to_assign = self.get_next_pending_order()
            if order_to_assign:
                if self.available_machines:
                    machine = self.available_machines.pop(0)
                    machine.add_orders(order_to_assign)
                    order_to_assign.status = "in process"
                    self.in_process_orders[order_to_assign.id] = order_to_assign
                    self.set_machine_unavailable(machine)
                    print(f"Order '{order_to_assign.id}' assigned to '{machine.name}'.")
                    assigned_count += 1
                else:
                    self._add_order_to_priority_queue(order_to_assign)
                    print("No machines available, order reinserted.")
                    break
            else:
                print("No pending orders left.")
                break
        if assigned_count == 0:
            print("No new orders were assigned.")
        return assigned_count

    def process_machine_completion(self, machine_id):
        # Processes the completion of a machine’s current order
        machine = self.all_machines.get(machine_id)
        if not machine:
            print(f"Error: Machine '{machine_id}' not found.")
            return None
        completed_order = machine.process_next()
        if completed_order:
            self.mark_order_as_completed(completed_order.id)
            self.set_machine_available(machine)
            return completed_order
        else:
            print(f"Machine '{machine.name}' had no orders to process.")
            self.set_machine_available(machine)
            return None

    # --- MONITORING ---

    def get_system_status(self):
        # Returns a summary of the current system state
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
        # Prints the current system status
        status = self.get_system_status()
        print("\n--- System Status ---")
        print(f"Pending Orders: {status['pending_orders']['total']}")
        print(f"  - P1: {status['pending_orders']['priority_1']}")
        print(f"  - P2: {status['pending_orders']['priority_2']}")
        print(f"  - P3: {status['pending_orders']['priority_3']}")
        print(f"In Process: {status['in_process_orders']}")
        print(f"Available Machines: {status['available_machines']}")
        print(f"Total Machines: {status['total_machines']}")
        print(f"History: {status['history_count']}")
        print("----------------------")
        if status['in_process_orders'] > 0:
            print("Orders in process:")
            for order_id, order in self.in_process_orders.items():
                print(f"  - {order_id} ({order.productName}), Qty: {order.quantity}, Price: ${order.price}, P: {order.priority}")
        if status['available_machines'] < status['total_machines']:
            print("Busy machines:")
            occupied_machines = [m for m in self.all_machines.values() if m not in self.available_machines]
            for machine in occupied_machines:
                print(f"  - {machine.name} ({machine.id}) with {machine.get_orders_number()} orders.")
