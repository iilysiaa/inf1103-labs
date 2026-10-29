#INF1103 Lab 6 - Inventory Management System refactored using OOP
#Product   -> represents and manages ONE product
#Inventory -> manages a collection of Product objects

import json
import os

#inventory.json is kept in the same folder as this script, so it is found no matter which folder the program is run from
INVENTORY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory.json")


# ==================== Product Class ====================
class Product:
    def __init__(self, product_id, name, price, stock):
        #Private attributes (name mangling) - outside code should use the methods below
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # Getters so other code can read the values without changing them directly
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    # The Product controls how its stock is changed
    # Returns True if updated, False if the quantity is invalid
    def update_stock(self, quantity):
        if isinstance(quantity, int) and quantity >= 0:
            self.__stock = quantity
            return True
        return False

    def display_information(self):
        print("ID: " + self.__product_id + " | Name: " + self.__name + " | Price: $" + format(self.__price, ".2f") + " | Stock: " + str(self.__stock))

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

    def display_all(self):
        print("Current Inventory")
        print("-" * 45)
        if len(self.__products) == 0:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()
        print("-" * 45)

    # Returns the products as a list of dictionaries (used when saving to JSON)
    def to_list(self):
        result = []
        for product in self.__products:
            result.append(product.to_dict())
        return result


# ==================== File Handling ====================
# Load inventory.json into an Inventory object, or start with an empty Inventory
def load_inventory():
    inventory = Inventory()
    if not os.path.exists(INVENTORY_FILE):
        print("inventory.json not found.")
        print("Starting with an empty inventory.")
        return inventory

    print("inventory.json found.")
    try:
        with open(INVENTORY_FILE, "r") as file:
            items = json.load(file)
        #Turn each dictionary from the file into a Product object
        for item in items:
            inventory.add_product(Product(item["id"], item["name"], item["price"], item["stock"]))
        print("Inventory loaded successfully.")
    except (json.JSONDecodeError, KeyError, TypeError):
        #File exists but does not contain valid inventory data
        print("inventory.json is invalid. Starting with an empty inventory.")
        inventory = Inventory()
    return inventory


# Save the Inventory to inventory.json
# Returns True if saved, False if the file could not be written
def save_inventory(inventory):
    try:
        with open(INVENTORY_FILE, "w") as file:
            json.dump(inventory.to_list(), file, indent=4)
        return True
    except OSError:
        print("Error! Could not save inventory to inventory.json.")
        return False


# ==================== Main Program (menu + user input) ====================
# Helper: keep asking until the user enters a price that is a number and not negative
def get_valid_price(prompt):
    while True:
        try:
            price = float(input(prompt))
            if price >= 0:
                return price
        except ValueError:
            pass
        print("Invalid price! Please enter a positive number.")


# Helper: keep asking until the user enters a whole number that is not negative
#isdigit() rejects text and negative numbers as "-" is not a digit
def get_valid_stock(prompt):
    while True:
        stock = input(prompt)
        if stock.isdigit():
            return int(stock)
        print("Invalid quantity! We only accept positive whole numbers.")


def add_product_menu(inventory):
    print("Add New Product")
    product_id = input("Product ID: ").strip().upper()
    if product_id == "":
        print("Product ID cannot be empty.")
        return
    if inventory.search_product(product_id) is not None:
        print("Product ID " + product_id + " already exists.")
        return

    name = input("Product Name: ").strip()
    if name == "":
        print("Product name cannot be empty.")
        return

    price = get_valid_price("Price: ")
    stock = get_valid_stock("Stock Quantity: ")

    product = Product(product_id, name, price, stock)
    inventory.add_product(product)
    print()
    print("Product added successfully!")


def update_stock_menu(inventory):
    print("Update Stock")
    product_id = input("Enter Product ID: ").strip()
    print()
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return

    print("Product Found:")
    print("Name: " + product.get_name())
    print("Current Stock: " + str(product.get_stock()))
    print()
    new_stock = get_valid_stock("New Stock Quantity: ")
    product.update_stock(new_stock)
    print()
    print("Stock updated successfully!")


def search_product_menu(inventory):
    print("Search Product")
    product_id = input("Enter Product ID: ").strip()
    print()
    product = inventory.search_product(product_id)
    if product is None:
        print("Product not found.")
        return

    print("Product Found")
    print("-" * 45)
    print("ID: " + product.get_product_id())
    print("Name: " + product.get_name())
    print("Price: $" + format(product.get_price(), ".2f"))
    print("Stock: " + str(product.get_stock()))
    print("-" * 45)


def display_menu():
    print()
    print("----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print()
    inventory = load_inventory()

    while True:
        display_menu()
        print()
        option = input("Enter option: ").strip()
        print()

        if option == "1":
            inventory.display_all()
        elif option == "2":
            add_product_menu(inventory)
        elif option == "3":
            update_stock_menu(inventory)
        elif option == "4":
            search_product_menu(inventory)
        elif option == "5":
            print("Saving inventory...")
            if save_inventory(inventory):
                print("Inventory saved successfully to inventory.json.")
        elif option == "6":
            #Save automatically before exiting so no changes are lost
            print("Saving inventory before exit...")
            if save_inventory(inventory):
                print("Inventory saved successfully.")
            print()
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option! Please choose from the menu.")


if __name__ == "__main__":
    main()