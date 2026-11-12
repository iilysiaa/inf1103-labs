#External code to test the discount strategies (Strategy pattern)

from product import DiscountStrategy, NoDiscount, PercentageDiscount, BulkDiscount


# Print PASS/FAIL for a True/False check
def check(description: str, condition: bool) -> None:
    print("  " + ("PASS" if condition else "FAIL") + " - " + description)


# Compare money values without floating point rounding problems
def same(a: float, b: float) -> bool:
    return abs(a - b) < 0.001


# 1. Each strategy on its own
print("1. Strategies on their own")
print("-" * 45)
check("NoDiscount: 100 -> 100", same(NoDiscount().apply(100.0), 100.0))
check("PercentageDiscount(10): 100 -> 90", same(PercentageDiscount(10).apply(100.0), 90.0))
check("PercentageDiscount(0): 100 -> 100", same(PercentageDiscount(0).apply(100.0), 100.0))
check("PercentageDiscount(100): 100 -> 0", same(PercentageDiscount(100).apply(100.0), 0.0))
check("BulkDiscount(200, 20): 250 -> 230", same(BulkDiscount(200, 20).apply(250.0), 230.0))
check("BulkDiscount(200, 20): exactly 200 -> 180", same(BulkDiscount(200, 20).apply(200.0), 180.0))
check("BulkDiscount(200, 20): 199.99 -> unchanged", same(BulkDiscount(200, 20).apply(199.99), 199.99))
check("BulkDiscount(10, 50): 20 -> 0, never negative", same(BulkDiscount(10, 50).apply(20.0), 0.0))
for strategy in (NoDiscount(), PercentageDiscount(10), BulkDiscount(200, 20)):
    check(type(strategy).__name__ + " is a DiscountStrategy", isinstance(strategy, DiscountStrategy))
print()

# 2. Invalid values are rejected when the strategy is created
print("2. Invalid strategy values")
print("-" * 45)
for description, make in [("PercentageDiscount(-5)", lambda: PercentageDiscount(-5)),
                          ("PercentageDiscount(150)", lambda: PercentageDiscount(150)),
                          ("BulkDiscount(200, -20)", lambda: BulkDiscount(200, -20))]:
    try:
        make()
        check(description + " raises ValueError", False)
    except ValueError:
        check(description + " raises ValueError", True)
try:
    DiscountStrategy()
    check("DiscountStrategy itself cannot be created (abstract)", False)
except TypeError:
    check("DiscountStrategy itself cannot be created (abstract)", True)
print()
