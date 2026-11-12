#External code to test the Inventory operations (add_product, remove_product, find_product)
#and show aggregation: removing a Product from an Inventory does not destroy the Product
#
#PREDICTION (write this BEFORE running - before step 3):
#  Will the Product still work after it is removed from Inventory A? Why?
#  My prediction: ...
#
#RESULT (after running): ...
#  Did it match? If not, why: ...

from product import Supplier, PhysicalProduct, DigitalProduct, Inventory


supplier = Supplier("S001", "TechWorld Distributors", "sales@techworld.com")

# 1. Create a Product BEFORE any Inventory exists
laptop = PhysicalProduct("2001", "MacBook Air", 4500.0, 20, supplier, 1.24)
print("1. Product created before any Inventory")
print("-" * 45)
laptop.display_information()
print()

# 2. Add the Product to Inventory A
inventory_a = Inventory()
inventory_a.add_product(laptop)
print("2. Added to Inventory A")
print("-" * 45)
print("find_product('2001') in A returns the same object: " + str(inventory_a.find_product("2001") is laptop))
print()

# 3. Remove it from Inventory A and confirm the Product object can still be used
removed = inventory_a.remove_product("2001")
print("3. Removed from Inventory A")
print("-" * 45)
print("remove_product('2001') returned: " + str(removed))
print("find_product('2001') in A now returns: " + str(inventory_a.find_product("2001")))
print("Product still works:")
laptop.display_information()
laptop.update_stock(15)
print("Stock updated through the Product itself: " + str(laptop.get_stock()))
print()

# 4. Add the same Product object to Inventory B
inventory_b = Inventory()
inventory_b.add_product(laptop)
print("4. Same Product added to Inventory B")
print("-" * 45)
print("Inventory B holds the same object (not a copy): " + str(inventory_b.find_product("2001") is laptop))
print("Stock change from step 3 is visible through B: " + str(inventory_b.find_product("2001").get_stock()))
print()

# 5. Empty an inventory - the products are not destroyed
game = DigitalProduct("3001", "Minecraft", 39.9, 500, supplier, 1024.5)
inventory_b.add_product(game)
inventory_b.remove_product("2001")
inventory_b.remove_product("3001")
print("5. Inventory B emptied")
print("-" * 45)
inventory_b.display_all_products()
print("Both products still exist and work:")
laptop.display_information()
game.display_information()
print()

# Edge case: removing or finding a product that is not in the inventory
print("Edge cases")
print("-" * 45)
print("remove_product('9999') returned: " + str(inventory_b.remove_product("9999")))
print("find_product('9999') returned: " + str(inventory_b.find_product("9999")))
