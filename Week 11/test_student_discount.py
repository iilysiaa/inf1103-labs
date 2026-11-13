#External code to test the new StudentDiscount strategy
#Open/Closed Principle: StudentDiscount is a NEW class - Order was not changed to support it

from product import Supplier, ProductFactory, Order, DiscountStrategy, StudentDiscount


# Print PASS/FAIL for a True/False check
def check(description: str, condition: bool) -> None:
    print("  " + ("PASS" if condition else "FAIL") + " - " + description)


# Compare money values without floating point rounding problems
def same(a: float, b: float) -> bool:
    return abs(a - b) < 0.001


# 1. The strategy on its own
print("1. StudentDiscount on its own")
print("-" * 45)
check("StudentDiscount is a DiscountStrategy", isinstance(StudentDiscount(), DiscountStrategy))
check("100 -> 95 (5% off)", same(StudentDiscount().apply(100.0), 95.0))
check("0 -> 0", same(StudentDiscount().apply(0.0), 0.0))
print()

# 2. The existing Order uses it without any change
supplier = Supplier("S001", "TechWorld Distributors", "sales@techworld.com")
mouse = ProductFactory.create("physical", "2002", "Wireless Mouse", 59.0, 75, supplier, weight=0.1)
game = ProductFactory.create("digital", "3001", "Minecraft", 39.9, 500, supplier, download_size=1024.5)

print("2. Order created with StudentDiscount()")
print("-" * 45)
order = Order("ORD001", StudentDiscount())
order.add_order_line(mouse, 3)      # 177.00
order.add_order_line(game, 1)       #  39.90  -> 216.90
order.display_order()
check("total is 216.90 - 5% = 206.055", same(order.calculate_total(), 206.055))
print()

print("3. set_discount(StudentDiscount()) on an existing order")
print("-" * 45)
other = Order("ORD002")
other.add_order_line(game, 2)       # 79.80
check("before: 79.80 with no discount", same(other.calculate_total(), 79.80))
other.set_discount(StudentDiscount())
check("after: 79.80 - 5% = 75.81", same(other.calculate_total(), 75.81))
