#External code to test polymorphism
#show_product_details() accepts ANY Product and only uses behaviour every Product supports,
#so it works for PhysicalProduct and DigitalProduct without being changed

from product import Supplier, Product, PhysicalProduct, DigitalProduct, Inventory


# Accepts any Product - it does not check which subclass it was given
def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


# Print PASS/FAIL for a True/False check
def check(description: str, condition: bool) -> None:
    print("  " + ("PASS" if condition else "FAIL") + " - " + description)


supplier = Supplier("S001", "TechWorld Distributors", "sales@techworld.com")
laptop = PhysicalProduct("2001", "MacBook Air", 4500.0, 20, supplier, 1.24)
game = DigitalProduct("3001", "Minecraft", 39.9, 500, supplier, 1024.5)

# 1. The same function works for both product types
print("1. show_product_details() with a PhysicalProduct")
print("-" * 45)
show_product_details(laptop)
print()
print("2. show_product_details() with a DigitalProduct")
print("-" * 45)
show_product_details(game)
print()

# 2. Both product types can be added to an Inventory and used by its normal operations
inventory = Inventory()
print("3. Inventory operations with both product types")
print("-" * 45)
check("add_product(laptop) returns True", inventory.add_product(laptop) is True)
check("add_product(game) returns True", inventory.add_product(game) is True)
check("adding a duplicate ID returns False", inventory.add_product(laptop) is False)
check("inventory holds 2 products", len(inventory.products) == 2)
check("find_product('2001') returns the laptop", inventory.find_product("2001") is laptop)
check("find_product('3001') returns the game", inventory.find_product("3001") is game)
check("find_product('9999') returns None", inventory.find_product("9999") is None)

# Products found through the Inventory can be passed straight to the same function
print()
print("  Every product in the inventory through show_product_details():")
for product in inventory.products:
    show_product_details(product)
print()

# to_list() asks each product for its own dictionary, so each keeps its own extra field
data = inventory.to_list()
check("to_list() includes the laptop's weight", data[0]["weight"] == 1.24)
check("to_list() includes the game's download_size", data[1]["download_size"] == 1024.5)

check("remove_product('2001') returns True", inventory.remove_product("2001") is True)
check("remove_product('3001') returns True", inventory.remove_product("3001") is True)
check("inventory is now empty", len(inventory.products) == 0)
print()
inventory.display_all_products()
