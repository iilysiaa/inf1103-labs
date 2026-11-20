#Week 11 checklist test - one section per requirement, PASS/FAIL for each check
#Run from the Week 11 folder:  python test_week11.py

from __future__ import annotations

import ast
import builtins
import glob
import inspect
import io
import os
import tempfile
from contextlib import redirect_stdout

from product import (Supplier, Product, PhysicalProduct, DigitalProduct, ProductFactory, Inventory,
                     OrderLine, Order, DiscountStrategy, NoDiscount, PercentageDiscount, BulkDiscount,
                     StudentDiscount, get_positive_float, load_products)

HERE = os.path.dirname(os.path.abspath(__file__))
results: list[bool] = []


def check(description: str, condition: bool) -> None:
    results.append(bool(condition))
    print("  " + ("PASS" if condition else "FAIL") + " - " + description)


def section(title: str) -> None:
    print()
    print(title)
    print("-" * 60)


def same(a: float, b: float) -> bool:
    return abs(a - b) < 0.001


def capture(function) -> str:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        function()
    return buffer.getvalue()


# Returns the error message if make() raises ValueError, otherwise None
def value_error_message(make) -> str | None:
    try:
        make()
    except ValueError as error:
        return str(error)
    return None


def parse(path: str) -> ast.Module:
    with open(path, encoding="utf-8") as file:
        return ast.parse(file.read())


PRODUCT_TREE = parse(os.path.join(HERE, "product.py"))
ORDER_NODE = [n for n in PRODUCT_TREE.body if isinstance(n, ast.ClassDef) and n.name == "Order"][0]
supplier = Supplier("S001", "TechWorld Distributors", "sales@techworld.com")
lamp = ProductFactory.create("physical", "P001", "Desk Lamp", 25.0, 10, supplier, weight=1.5)
editor = ProductFactory.create("digital", "D001", "Photo Editor", 49.9, 100, supplier, download_size=850.0)


def make_order(discount: DiscountStrategy | None = None) -> Order:
    order = Order("ORD001") if discount is None else Order("ORD001", discount)
    order.add_order_line(lamp, 4)       # 100.00
    order.add_order_line(editor, 2)     #  99.80  -> 199.80
    return order


# ---------------------------------------------------------------------------
section("1. Order calculates totals through a DiscountStrategy, with no discount if/elif")
check("default strategy is NoDiscount -> 199.80", isinstance(make_order().discount, NoDiscount)
      and same(make_order().calculate_total(), 199.80))
check("PercentageDiscount(10) -> 179.82", same(make_order(PercentageDiscount(10)).calculate_total(), 179.82))
check("BulkDiscount(150, 20) -> 179.80", same(make_order(BulkDiscount(150, 20)).calculate_total(), 179.80))
check("BulkDiscount(200, 20) below threshold -> 199.80", same(make_order(BulkDiscount(200, 20)).calculate_total(), 199.80))
check("calculate_total() calls self.discount.apply(...)", "self.discount.apply(" in inspect.getsource(Order.calculate_total))
strategy_names = {"PercentageDiscount", "BulkDiscount", "StudentDiscount"}
order_names = {n.id for n in ast.walk(ORDER_NODE) if isinstance(n, ast.Name)}
check("Order never names a specific discount (Percentage/Bulk/Student)", not (strategy_names & order_names))
check("Order never uses isinstance() or type()", not ({"isinstance", "type"} & order_names))
total_method = [n for n in ORDER_NODE.body if isinstance(n, ast.FunctionDef) and n.name == "calculate_total"][0]
check("calculate_total() contains no if/elif", not any(isinstance(n, (ast.If, ast.IfExp)) for n in ast.walk(total_method)))

# ---------------------------------------------------------------------------
section("2. A new discount strategy can be added without changing Order")


class FlatDiscount(DiscountStrategy):          # brand-new strategy defined only in this test
    def apply(self, total: float) -> float:
        return max(total - 15.0, 0.0)


check("FlatDiscount (defined only in this test) works: 199.80 -> 184.80",
      same(make_order(FlatDiscount()).calculate_total(), 184.80))
check("StudentDiscount (added after Order) works: 199.80 - 5% = 189.81",
      same(make_order(StudentDiscount()).calculate_total(), 189.81))
check("Order's code does not mention StudentDiscount or FlatDiscount",
      not ({"StudentDiscount", "FlatDiscount"} & order_names))

# ---------------------------------------------------------------------------
section("3. The strategy on an existing order can be changed with set_discount()")
order = make_order()
original_lines = list(order.order_lines)
for strategy, expected in [(PercentageDiscount(50), 99.90), (StudentDiscount(), 189.81),
                           (BulkDiscount(100, 99.80), 100.0), (NoDiscount(), 199.80)]:
    order.set_discount(strategy)
    check("set_discount(" + type(strategy).__name__ + ") -> " + format(expected, ".2f"),
          order.discount is strategy and same(order.calculate_total(), expected))
check("changing the strategy did not change the order lines", order.order_lines == original_lines)

# ---------------------------------------------------------------------------
section("4. Products are created through ProductFactory rather than directly")
check("'physical' -> PhysicalProduct", type(lamp) is PhysicalProduct)
check("'digital' -> DigitalProduct", type(editor) is DigitalProduct)
#Scan product.py and every test file for PhysicalProduct(...) / DigitalProduct(...) calls outside the factory
direct_calls: list[str] = []
for path in [os.path.join(HERE, "product.py")] + sorted(glob.glob(os.path.join(HERE, "test_*.py"))):
    tree = parse(path)
    allowed: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == "ProductFactory":
            allowed |= {id(n) for n in ast.walk(node)}
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id in ("PhysicalProduct", "DigitalProduct") and id(node) not in allowed):
            direct_calls.append(os.path.basename(path) + " line " + str(node.lineno))
for call in direct_calls:
    print("    direct creation: " + call)
check("no PhysicalProduct(...) / DigitalProduct(...) calls outside ProductFactory", len(direct_calls) == 0)
check("load_products() creates products with ProductFactory.create",
      "ProductFactory.create(" in inspect.getsource(load_products))

# ---------------------------------------------------------------------------
section("5. An unknown product type raises a ValueError with a clear message")
message = value_error_message(lambda: ProductFactory.create("service", "S001", "Installation", 30.0, 5, supplier))
check("'service' -> ValueError \"" + str(message) + "\"", message == "Unknown product type: service")
check("'' -> ValueError naming the empty type",
      value_error_message(lambda: ProductFactory.create("", "X", "X", 1.0, 1, supplier)) == "Unknown product type: ")

# ---------------------------------------------------------------------------
section("6. Invalid prices, stock quantities and order quantities are rejected")
for description, make, expected in [
        ("price 0", lambda: ProductFactory.create("physical", "X", "X", 0, 1, supplier, weight=1.0), "Price must be greater than zero."),
        ("price -5", lambda: ProductFactory.create("digital", "X", "X", -5, 1, supplier, download_size=1.0), "Price must be greater than zero."),
        ("stock -1", lambda: ProductFactory.create("physical", "X", "X", 1.0, -1, supplier, weight=1.0), "Stock quantity cannot be negative."),
        ("order quantity 0", lambda: OrderLine(lamp, 0), "Quantity must be greater than zero."),
        ("order quantity -3 via add_order_line", lambda: Order("X").add_order_line(lamp, -3), "Quantity must be greater than zero.")]:
    check(description + " -> \"" + expected + "\"", value_error_message(make) == expected)
check("valid boundary values accepted: price 0.01, stock 0, quantity 1",
      ProductFactory.create("physical", "X", "X", 0.01, 0, supplier, weight=1.0).get_stock() == 0
      and OrderLine(lamp, 1).calculate_subtotal() == 25.0)

# ---------------------------------------------------------------------------
section("7. Invalid user input is handled without crashing, and the user is asked again")
typed = ["abc", "", "-5", "0", "nan", "12.50"]
prompts: list[str] = []
real_input = builtins.input
builtins.input = lambda prompt: (prompts.append(prompt), typed[len(prompts) - 1])[1]
try:
    output = io.StringIO()
    with redirect_stdout(output):
        value = get_positive_float("Price: ")
finally:
    builtins.input = real_input
check("bad answers 'abc', '', '-5', '0', 'nan' did not crash; 12.50 returned", value == 12.5)
check("the user was asked again after each bad answer (6 prompts)", len(prompts) == 6)
check("a message was shown for each of the 5 bad answers", len(output.getvalue().splitlines()) == 5)

# ---------------------------------------------------------------------------
section("8. A missing products file is handled gracefully")
inventory = Inventory()
lines = capture(lambda: load_products("does_not_exist.csv", inventory, supplier)).splitlines()
check("no crash; prints 'Products file not found: does_not_exist.csv'", lines[0] == "Products file not found: does_not_exist.csv")
check("finally still prints 'Load attempt finished.'", lines == ["Products file not found: does_not_exist.csv", "Load attempt finished."])
check("inventory left empty", inventory.products == [])

# ---------------------------------------------------------------------------
section("9. Bad rows are reported and skipped, and valid rows still load (products.csv)")
inventory = Inventory()
lines = capture(lambda: load_products(os.path.join(HERE, "products.csv"), inventory, supplier)).splitlines()
for line in lines:
    print("    output: " + line)
check("'service' row reported", "Row 4 skipped: Unknown product type: service" in lines)
check("price 'abc' row reported", any(l.startswith("Row 5 skipped") and "abc" in l for l in lines))
check("valid rows loaded: P001, D001 and P003 (after the bad rows)",
      [p.get_product_id() for p in inventory.products] == ["P001", "D001", "P003"])
check("prints '3 products loaded.' then 'Load attempt finished.'", lines[-2:] == ["3 products loaded.", "Load attempt finished."])
with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as temp:
    temp.write("product_type,product_id,name,price,stock_quantity\n"
               "physical,P010,Lamp,-1,1\nphysical,P011,Chair,10,-2\ndigital,D010,App,9.99,1\n")
try:
    inventory = Inventory()
    lines = capture(lambda: load_products(temp.name, inventory, supplier)).splitlines()
finally:
    os.remove(temp.name)
check("rows breaking Product validation are also reported and skipped",
      "Row 2 skipped: Price must be greater than zero." in lines and "Row 3 skipped: Stock quantity cannot be negative." in lines
      and [p.get_product_id() for p in inventory.products] == ["D010"])

# ---------------------------------------------------------------------------
section("10. Each except catches a specific exception")
handlers: list[tuple[int, str]] = []
for node in ast.walk(PRODUCT_TREE):
    if isinstance(node, ast.ExceptHandler):
        name = node.type.id if isinstance(node.type, ast.Name) else ("(none)" if node.type is None else "(other)")
        handlers.append((node.lineno, name))
for line_number, name in sorted(handlers):
    print("    product.py line " + str(line_number) + ": except " + name)
check("product.py has except clauses to check", len(handlers) > 0)
check("no bare 'except:'", all(name != "(none)" for _, name in handlers))
check("no broad 'except Exception' / 'except BaseException'",
      all(name not in ("Exception", "BaseException") for _, name in handlers))
check("only ValueError and FileNotFoundError are caught",
      {name for _, name in handlers} <= {"ValueError", "FileNotFoundError"})

# ---------------------------------------------------------------------------
print()
print("=" * 60)
print(str(results.count(True)) + "/" + str(len(results)) + " checks passed")
print("ALL TESTS PASSED" if all(results) else "SOME TESTS FAILED")
