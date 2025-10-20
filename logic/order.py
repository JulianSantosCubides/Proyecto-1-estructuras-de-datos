## It uses a stack


class Order:
    #  TODO: set the order id as an incrementer value from order-1, to order-n
    #  TODO: the priority is calculated based on the price, and the price is calculated based on the quantity.
    #  TODO: create a dictionary with product prices and set a product selector to avoid enter any text. Add too an number input to set the quantity
    def __init__(self, id, productName, quantity): #  TODO: the price is calculated
        self.productName = productName
        self.quantity = quantity
        # self.price = productsDictionary[productName] # TODO: uses the dictionary here and to display in main_screen
