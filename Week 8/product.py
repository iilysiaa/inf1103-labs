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

    def update_stock(self, quantity):
        if quantity < 0:
            print("Stock cannot be negative.")
            return
        self.__stock = quantity

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    # Convert the product back to a dictionary so it can be saved as JSON
    def to_dict(self):
        return {"id": self.__product_id, "name": self.__name, "price": self.__price, "stock": self.__stock}

# ==================== Inventory Class ====================

class Inventory:
    def __init__(self):
        self.__products = []

    # Returns True if added, False if a product with the same ID already exists
    def add_product(self, product):
        if self.search_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    # Find a Product by its ID (not case-sensitive), or None if not found
    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id().upper() == product_id.upper():
                return product
        return None