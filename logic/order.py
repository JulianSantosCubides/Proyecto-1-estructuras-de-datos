## It uses a stack

class Order:
    #  TODO: set the order id as an incrementer value from order-1, to order-n
    #  TODO: the priority is calculated based on the price, and the price is calculated based on the quantity.
    #  TODO: create a dictionary with product prices and set a product selector to avoid enter any text. Add too an number input to set the quantity
    def __init__(self, id, productName, quantity, price): #  TODO: the price is calculated before and received as parameter
        self.productName = productName
        self.quantity = quantity
        self.price = price  # TODO: the price should be calculated when the order is created
        self.priority = calculate_priority(self.price)
        self.status = "pendiente"


#  As the queue handle the priority from highest to lowest.
#  So The priority is handled from 1 (highest priority) to 3 (lowest priority)
def calculate_priority(price):
    if price >= 3000000:
        return 1
    elif price >= 1500000 and price < 3000000:
        return 2
    elif price < 1500000:
        return 3
