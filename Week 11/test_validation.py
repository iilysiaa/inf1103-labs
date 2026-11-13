#External code to test validation
#Each class checks its own rules and raises ValueError with a clear message:
#  Product   -> price must be greater than zero, stock quantity cannot be negative
#  OrderLine -> quantity must be greater than zero

from product import Supplier, Product, ProductFactory, PhysicalProduct, DigitalProduct, OrderLine, Order


# Print PASS/FAIL for a True/False check
def check(description: str, condition: bool) -> None:
    print("  " + ("PASS" if condition else "FAIL") + " - " + description)


# Run make() and check it raises ValueError with the expected message
def check_rejected(description: str, make, expected_message: str) -> None:
    try:
        make()
        check(description + " is rejected", False)
    except ValueError as error:
        check(description + " is rejected: \"" + str(error) + "\"", str(error) == expected_message)


supplier = Supplier("S001", "TechWorld Distributors", "sales@techworld.com")
PRICE_MESSAGE = "Price must be greater than zero."
STOCK_MESSAGE = "Stock quantity cannot be negative."
QUANTITY_MESSAGE = "Quantity must be greater than zero."

# 1. Product price
print("1. Product price must be greater than zero")
print("-" * 45)
check_rejected("price 0 (physical)", lambda: PhysicalProduct("2001", "Laptop", 0, 5, supplier, 1.0), PRICE_MESSAGE)
check_rejected("price -10 (digital)", lambda: DigitalProduct("3001", "Game", -10, 5, supplier, 100.0), PRICE_MESSAGE)
check_rejected("price 0 through the factory",
               lambda: ProductFactory.create("digital", "3001", "Game", 0, 5, supplier, download_size=100.0), PRICE_MESSAGE)
check("price 0.01 is accepted", PhysicalProduct("2001", "Pen", 0.01, 5, supplier, 0.01).get_price() == 0.01)
print()

# 2. Product stock quantity
print("2. Product stock quantity cannot be negative")
print("-" * 45)
check_rejected("stock -1 (physical)", lambda: PhysicalProduct("2001", "Laptop", 100.0, -1, supplier, 1.0), STOCK_MESSAGE)
check_rejected("stock -5 (digital)", lambda: DigitalProduct("3001", "Game", 20.0, -5, supplier, 100.0), STOCK_MESSAGE)
check("stock 0 is accepted (out of stock is allowed)",
      DigitalProduct("3001", "Game", 20.0, 0, supplier, 100.0).get_stock() == 0)
#update_stock() already protects the same rule after creation: it returns False and leaves the stock unchanged
product = PhysicalProduct("2001", "Laptop", 100.0, 10, supplier, 1.0)
check("update_stock(-3) returns False and stock stays 10", product.update_stock(-3) is False and product.get_stock() == 10)
print()

# 3. OrderLine quantity
print("3. OrderLine quantity must be greater than zero")
print("-" * 45)
check_rejected("OrderLine quantity 0", lambda: OrderLine(product, 0), QUANTITY_MESSAGE)
check_rejected("OrderLine quantity -2", lambda: OrderLine(product, -2), QUANTITY_MESSAGE)
#Order creates its OrderLines, so the OrderLine's own check also protects Order - Order has no check of its own
order = Order("ORD001")
check_rejected("Order.add_order_line(product, 0)", lambda: order.add_order_line(product, 0), QUANTITY_MESSAGE)
check("the rejected line was not added to the order", len(order.order_lines) == 0)
order.add_order_line(product, 1)
check("quantity 1 is accepted", len(order.order_lines) == 1 and order.calculate_total() == 100.0)
print()

# 4. The check lives in the class that owns the rule
print("4. Each rule is checked in the class that owns it")
print("-" * 45)
import inspect
product_source = inspect.getsource(Product.__init__)
check("Product.__init__ checks the price", PRICE_MESSAGE in product_source)
check("Product.__init__ checks the stock", STOCK_MESSAGE in product_source)
check("OrderLine.__init__ checks the quantity", QUANTITY_MESSAGE in inspect.getsource(OrderLine.__init__))
check("Order does not repeat the quantity check", QUANTITY_MESSAGE not in inspect.getsource(Order))
