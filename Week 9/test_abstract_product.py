#External code to observe what happens when the abstract Product class is created directly

from product import Product, PhysicalProduct

print("Attempting to create a Product object directly...")
try:
    product = Product("1001", "Iphone 17", 2100.0, 150)
    product.display_information()
except TypeError as error:
    #Product still has an unimplemented abstract method, so Python refuses to create it
    print("TypeError: " + str(error))

print()
#A child class that implements get_fulfilment_info() can be created,
#and it can still use the regular (already implemented) methods from Product
print("Creating a PhysicalProduct object instead...")
laptop = PhysicalProduct("2001", "MacBook Air", 4500.0, 20, 1.24)
laptop.update_stock(25)                   # regular method inherited from Product
print("Name: " + laptop.get_name())       # regular method inherited from Product
print("Stock: " + str(laptop.get_stock()))
print(laptop.get_fulfilment_info())       # abstract method completed by PhysicalProduct
