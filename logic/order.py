## It uses a stack

class Order:
    nextId = 1  # static counter
    def __init__(self, id, productName, quantity, price):
        self.id = Order.nextId
        Order.nextId +=1  # Increment the counter for the next order
        self.productName = productName
        self.quantity = quantity
        self.price = price
        self.priority = calculate_priority(self.price)
        self.status = "pendiente"
        self.totalPrice = price


#  As the queue handle the priority from highest to lowest.
#  So The priority is handled from 1 (highest priority) to 3 (lowest priority)
def calculate_priority(price):
    if price >= 3000000:
        return 1
    elif price >= 1500000:
        return 2
    else:
        return 3
