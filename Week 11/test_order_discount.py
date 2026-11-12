#External code to test how Order uses a DiscountStrategy (Strategy pattern)
#Order is GIVEN a strategy and calls apply() on it - it does not decide the discount itself

from product import (Supplier, PhysicalProduct, DigitalProduct, Order,
                     NoDiscount, PercentageDiscount, BulkDiscount)


# Print PASS/FAIL for a True/False check
def check(description: str, condition: bool) -> None:
    print("  " + ("PASS" if condition else "FAIL") + " - " + description)


# Compare money values without floating point rounding problems
def same(a: float, b: float) -> bool:
    return abs(a - b) < 0.001


supplier = Supplier("S001", "TechWorld Distributors", "sales@techworld.com")
mouse = PhysicalProduct("2002", "Wireless Mouse", 59.0, 75, supplier, 0.1)
game = DigitalProduct("3001", "Minecraft", 39.9, 500, supplier, 1024.5)

# 1. No strategy given -> NoDiscount
print("1. Order with no discount given")
print("-" * 45)
order = Order("ORD001")
order.add_order_line(mouse, 3)      # 177.00
order.add_order_line(game, 1)       #  39.90  -> line subtotals add up to 216.90
check("default strategy is NoDiscount", isinstance(order.discount, NoDiscount))
check("total is the full 216.90", same(order.calculate_total(), 216.90))
check("each Order gets its own NoDiscount object", Order("A").discount is not Order("B").discount)
print()

# 2. Strategy given when the Order is created
print("2. Order created with PercentageDiscount(10)")
print("-" * 45)
order_10 = Order("ORD002", PercentageDiscount(10))
order_10.add_order_line(mouse, 3)
order_10.add_order_line(game, 1)
order_10.display_order()
check("total is 216.90 - 10% = 195.21", same(order_10.calculate_total(), 195.21))
print()

# 3. set_discount() changes the strategy on the same Order
print("3. set_discount() on the same order")
print("-" * 45)
order.set_discount(BulkDiscount(200, 20))
check("BulkDiscount(200, 20): 216.90 -> 196.90", same(order.calculate_total(), 196.90))
order.set_discount(PercentageDiscount(25))
check("PercentageDiscount(25): 216.90 -> 162.675", same(order.calculate_total(), 162.675))
order.set_discount(NoDiscount())
check("back to NoDiscount: 216.90", same(order.calculate_total(), 216.90))
order.remove_order_line("2002")
order.set_discount(BulkDiscount(200, 20))
check("below the bulk threshold after removing a line: 39.90 unchanged", same(order.calculate_total(), 39.90))
check("empty order with a discount totals 0.0", same(Order("ORD003", PercentageDiscount(10)).calculate_total(), 0.0))
