#External code to test composition between Order and OrderLine
#The Order creates and manages its own OrderLines; the Products are only referred to
#
#PREDICTION (write this BEFORE running):
#  If I add the same Product to two different Orders, how many OrderLine objects
#  and how many Product objects will exist?
#  My prediction: ... OrderLine objects, ... Product objects
#
#RESULT (after running): ...
#  Did it match? If not, why: ...
#
#WHY an OrderLine should not be managed independently or moved to another Order: ...

from product import Supplier, ProductFactory, Order


# Print PASS/FAIL for a True/False check
def check(description, condition):
    print("  " + ("PASS" if condition else "FAIL") + " - " + description)


supplier = Supplier("S001", "TechWorld Distributors", "sales@techworld.com")
laptop = ProductFactory.create("physical", "2001", "MacBook Air", 4500.0, 20, supplier, weight=1.24)
game = ProductFactory.create("digital", "3001", "Minecraft", 39.9, 500, supplier, download_size=1024.5)
ebook = ProductFactory.create("digital", "3002", "Python Crash Course", 29.5, 100, supplier, download_size=12.0)

# 1. Create an Order and add products with add_order_line() - the Order creates the OrderLines
order_1 = Order("ORD001")
order_1.add_order_line(laptop, 1)
order_1.add_order_line(game, 2)
order_1.add_order_line(ebook, 3)

# 2. Display each order line and the total
print("1. First order")
order_1.display_order()
print()

# 3. Add the SAME laptop to a different Order - Order 2 creates its own OrderLine
order_2 = Order("ORD002")
order_2.add_order_line(laptop, 5)
print("2. Second order with the same laptop")
order_2.display_order()
print()

line_in_order_1 = order_1.order_lines[0]
line_in_order_2 = order_2.order_lines[0]
print("3. Comparing objects")
print("-" * 45)
print("  OrderLine in ORD001 id: " + str(id(line_in_order_1)) + " | quantity " + str(line_in_order_1.quantity))
print("  OrderLine in ORD002 id: " + str(id(line_in_order_2)) + " | quantity " + str(line_in_order_2.quantity))
print("  Product in ORD001 line id: " + str(id(line_in_order_1.product)))
print("  Product in ORD002 line id: " + str(id(line_in_order_2.product)))
check("the two OrderLines are DIFFERENT objects", line_in_order_1 is not line_in_order_2)
check("both OrderLines refer to the SAME Product object", line_in_order_1.product is line_in_order_2.product)
check("that Product is the original laptop", line_in_order_1.product is laptop)
print()

# 4. Remove an order line through the Order's own method
removed = order_1.remove_order_line("2001")
print("4. Removed the laptop line from ORD001")
order_1.display_order()
check("remove_order_line('2001') returned True", removed)
check("ORD002 still has its own laptop line", order_2.order_lines[0].product is laptop)
check("removing a line that is not there returns False", order_1.remove_order_line("9999") is False)
print()

# 5. Remove the whole Order from the scenario - its OrderLines go with it, the Products remain
del order_2
print("5. After 'del order_2'")
print("-" * 45)
print("  The laptop still exists:")
laptop.display_information()
