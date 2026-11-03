#External code to test calculate_shipping_cost() on physical products of different weights
#Shipping rule: $5.00 base fee + $2.50 per kg

from product import CanBeShipped, PhysicalProduct, DigitalProduct

#Each test: (product, expected shipping cost)
tests = [
    (PhysicalProduct("2001", "USB Cable", 15.0, 200, 0.0), 5.00),
    (PhysicalProduct("2002", "Phone Case", 25.0, 300, 0.2), 5.50),
    (PhysicalProduct("2003", "MacBook Air", 4500.0, 20, 1.24), 8.10),
    (PhysicalProduct("2004", "Monitor", 900.0, 15, 6.5), 21.25),
    (PhysicalProduct("2005", "Desk", 650.0, 5, 30.0), 80.00),
]

print("Shipping Cost Tests")
print("-" * 55)
for product, expected in tests:
    cost = product.calculate_shipping_cost()
    #round() avoids tiny floating point differences when comparing money values
    if round(cost, 2) == expected:
        result = "PASS"
    else:
        result = "FAIL (expected $" + format(expected, ".2f") + ")"
    print(result + " - " + product.get_name() + " (" + format(product.get_weight(), ".2f") + " kg): $" + format(cost, ".2f"))

print()
print("Interface Checks")
print("-" * 55)
laptop = tests[2][0]
game = DigitalProduct("3001", "Minecraft", 39.9, 500, 1024.5)

if isinstance(laptop, CanBeShipped):
    print("PASS - PhysicalProduct implements CanBeShipped")
else:
    print("FAIL - PhysicalProduct does not implement CanBeShipped")

if not isinstance(game, CanBeShipped):
    print("PASS - DigitalProduct does not implement CanBeShipped")
else:
    print("FAIL - DigitalProduct should not implement CanBeShipped")

if not hasattr(game, "calculate_shipping_cost"):
    print("PASS - DigitalProduct has no calculate_shipping_cost()")
else:
    print("FAIL - DigitalProduct should not have calculate_shipping_cost()")
