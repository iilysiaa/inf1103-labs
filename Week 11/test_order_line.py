#External code to test the OrderLine class
#An OrderLine refers to an existing Product and calculates price * quantity

from product import Supplier, ProductFactory, OrderLine


supplier = Supplier("S001", "TechWorld Distributors", "sales@techworld.com")
laptop = ProductFactory.create("physical", "2001", "MacBook Air", 4500.0, 20, supplier, weight=1.24)
game = ProductFactory.create("digital", "3001", "Minecraft", 39.9, 500, supplier, download_size=1024.5)


# Print PASS/FAIL comparing the actual subtotal with the expected one
def check_subtotal(order_line, expected):
    actual = order_line.calculate_subtotal()
    result = "PASS" if abs(actual - expected) < 0.001 else "FAIL"
    print("  " + result + " - " + order_line.product.get_name() + " x " + str(order_line.quantity)
          + " = $" + format(actual, ".2f") + " (expected $" + format(expected, ".2f") + ")")


print("OrderLine subtotals")
print("-" * 45)
laptop_line = OrderLine(laptop, 2)
game_line = OrderLine(game, 3)
check_subtotal(laptop_line, 9000.0)
check_subtotal(game_line, 119.7)
check_subtotal(OrderLine(game, 0), 0.0)
print()

print("OrderLine refers to the existing Product (not a copy)")
print("-" * 45)
print("  laptop_line.product is laptop: " + str(laptop_line.product is laptop))
