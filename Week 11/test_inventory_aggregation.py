#External code to test the aggregation between Inventory and Product
#The Inventory groups Product objects, but the products are created outside it and can exist without it

from product import Supplier, ProductFactory, Product, Inventory


supplier = Supplier("S001", "TechWorld Distributors", "sales@techworld.com")

# 1. Create the products independently of any Inventory
laptop = ProductFactory.create("physical", "2001", "MacBook Air", 4500.0, 20, supplier, weight=1.24)
game = ProductFactory.create("digital", "3001", "Minecraft", 39.9, 500, supplier, download_size=1024.5)

# 2. Add both kinds of Product to the same Inventory (list[Product] accepts either)
inventory = Inventory()
inventory.add_product(laptop)
inventory.add_product(game)
inventory.display_all_products()
print()

print("Collection check")
print("-" * 45)
print("Number of products in inventory: " + str(len(inventory.products)))
for product in inventory.products:
    print(product.get_name() + " is a " + type(product).__name__ + " and a Product: " + str(isinstance(product, Product)))
print("Inventory stores the same laptop object (not a copy): " + str(inventory.products[0] is laptop))
print()

# 3. Delete the Inventory - the products still exist on their own
del inventory
print("After 'del inventory'")
print("-" * 45)
laptop.display_information()
print()
game.display_information()
