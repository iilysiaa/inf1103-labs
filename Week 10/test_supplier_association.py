#External code to test the association between Product and Supplier
#
#PREDICTION (write this BEFORE running):
#  If I run "del supplier" after creating the products, can each Product still display its supplier information?
#  My prediction: ...
#
#RESULT (after running): ...
#  Did it match? If not, why: ...

from product import Supplier, PhysicalProduct, DigitalProduct


# 1. Create a Supplier object on its own
supplier = Supplier("S001", "TechWorld Distributors", "sales@techworld.com")

# 2. Create a PhysicalProduct and a DigitalProduct, passing in that same Supplier object
laptop = PhysicalProduct("2001", "MacBook Air", 4500.0, 20, supplier, 1.24)
game = DigitalProduct("3001", "Minecraft", 39.9, 500, supplier, 1024.5)

# 3. Display the supplier information through each Product
print("Supplier information through each Product")
print("-" * 45)
print(laptop.get_name() + ":")
laptop.display_supplier_information()
print(game.get_name() + ":")
game.display_supplier_information()
print()

# 4. Confirm the Supplier and Products are separate objects
print("Separate objects check")
print("-" * 45)
print("Supplier object id: " + str(id(supplier)))
print("Laptop object id:   " + str(id(laptop)))
print("Game object id:     " + str(id(game)))
print("Laptop is a different object from the Supplier: " + str(laptop is not supplier))
print("Both products refer to the SAME Supplier object: " + str(laptop.supplier is supplier and game.supplier is supplier))
print()

# 5. Delete the supplier variable - does each Product still have its supplier?
del supplier
print("After 'del supplier'")
print("-" * 45)
laptop.display_information()
laptop.display_supplier_information()
print()
game.display_information()
game.display_supplier_information()
print()

# 6. The Supplier can also outlive a Product: delete the laptop, the Supplier is still there
kept_supplier = game.supplier
del laptop
print("After 'del laptop'")
print("-" * 45)
print("Supplier still exists:")
kept_supplier.display_information()
