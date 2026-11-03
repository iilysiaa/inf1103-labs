#External code to test get_fulfilment_info() on PhysicalProduct and DigitalProduct

from product import Product, PhysicalProduct, DigitalProduct

laptop = PhysicalProduct("2001", "MacBook Air", 4500.0, 20, 1.24)
game = DigitalProduct("3001", "Minecraft", 39.9, 500, 1024.5)

#Polymorphism: the same method call gives a different message depending on the product type
for product in [laptop, game]:
    print(product.get_name() + ": " + product.get_fulfilment_info())

print()
#Check each message describes the right kind of delivery
if "physical shipping" in laptop.get_fulfilment_info():
    print("PASS - PhysicalProduct requires physical shipping")
else:
    print("FAIL - PhysicalProduct message is wrong")

if "delivered digitally" in game.get_fulfilment_info():
    print("PASS - DigitalProduct is delivered digitally")
else:
    print("FAIL - DigitalProduct message is wrong")

#Product is abstract, so creating one directly should fail
try:
    Product("1001", "Iphone 17", 2100.0, 150)
    print("FAIL - Product could be created directly")
except TypeError:
    print("PASS - Product cannot be created directly (it is abstract)")
