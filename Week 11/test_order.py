#External code to test the Order class
#Composition: the Order creates and owns its OrderLines
#The Products are only referred to - they exist independently and can also be in an Inventory

from product import Supplier, ProductFactory, Inventory, OrderLine, Order


supplier = Supplier("S001", "TechWorld Distributors", "sales@techworld.com")
laptop = ProductFactory.create("physical", "2001", "MacBook Air", 4500.0, 20, supplier, weight=1.24)
game = ProductFactory.create("digital", "3001", "Minecraft", 39.9, 500, supplier, download_size=1024.5)

# The same Products are also in an Inventory
inventory = Inventory()
inventory.add_product(laptop)
inventory.add_product(game)


# Print PASS/FAIL for a True/False check
def check(description, condition):
    print("  " + ("PASS" if condition else "FAIL") + " - " + description)


# 1. An empty order has a total of 0
order = Order("ORD001")
print("1. Empty order")
print("-" * 45)
check("total of an empty order is $0.00", order.calculate_total() == 0.0)
print()

# 2. Add lines by passing a Product and a quantity - the Order creates the OrderLines itself
order.add_order_line(laptop, 2)
order.add_order_line(game, 3)
print("2. Order " + order.order_id + " after adding 2 lines")
print("-" * 45)
for line in order.order_lines:
    print("  " + line.product.get_name() + " x " + str(line.quantity) + " = $" + format(line.calculate_subtotal(), ".2f"))
print("  Total: $" + format(order.calculate_total(), ".2f"))
check("order has 2 order lines", len(order.order_lines) == 2)
check("every order line is an OrderLine created by the Order", all(isinstance(line, OrderLine) for line in order.order_lines))
check("total is $9119.70 (9000.00 + 119.70)", abs(order.calculate_total() - 9119.70) < 0.001)
print()

# 3. The OrderLine refers to the Product but does not own it
print("3. Order lines refer to the existing Products")
print("-" * 45)
check("first line's product is the same laptop object", order.order_lines[0].product is laptop)
check("the same laptop is also in the Inventory", inventory.find_product("2001") is laptop)
print()

# 4. Delete the Order - its OrderLines go with it, but the Products still exist
del order
print("4. After 'del order'")
print("-" * 45)
check("laptop still in the Inventory", inventory.find_product("2001") is laptop)
check("game still in the Inventory", inventory.find_product("3001") is game)
laptop.display_information()
