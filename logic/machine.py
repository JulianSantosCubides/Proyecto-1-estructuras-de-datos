#  It uses queue for machines work list

# Import queue library
from queue import Queue

class Machine:
    #TODO: set the machine id as an incrementer value from machine-1, to machine-n
    def __init__(self, id, name):  # It's possible to add another attributes, like  capacity or velocity
        self.id = id
        self.name = name
        self.queue = Queue() # queue to handle work orders
        self.currentOrder = None

    # Function to add orders to the machine
    def add_orders(self, order):
        self.queue.put(order)


    # Function to get the work list
    def get_orders_number(self): # G
        return self.queue.qsize()

    # Function to process the next order
    def process_next(self):  # It gets and remove the finished order and continues to the following
        if (self.queue.empty()):
            return None
        else:
            return self.queue.get() #  The order time is handled by the manager class, not for this function
