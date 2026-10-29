class Product:
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = float(price)
        self.__stock = int(stock)

    def get_product_id(self): return self.__product_id
    def get_name(self):       return self.__name
    def get_price(self):      return self.__price
    def get_stock(self):      return self.__stock
