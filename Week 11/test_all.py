#Final checklist test for Week 10 - one section per requirement, PASS/FAIL for each check
#Run from the Week 10 folder:  python test_all.py

from __future__ import annotations

import ast
import html
import io
import os
import re
from contextlib import redirect_stdout

from product import (Supplier, ProductFactory, Product, PhysicalProduct,
                     DigitalProduct, Inventory, OrderLine, Order)

HERE = os.path.dirname(os.path.abspath(__file__))
results: list[bool] = []


def check(description: str, condition: bool) -> None:
    results.append(bool(condition))
    print("  " + ("PASS" if condition else "FAIL") + " - " + description)


def section(title: str) -> None:
    print()
    print(title)
    print("-" * 60)


def capture(function) -> str:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        function()
    return buffer.getvalue()


def make_supplier() -> Supplier:
    return Supplier("S001", "TechWorld Distributors", "sales@techworld.com")


# ---------------------------------------------------------------------------
section("1. Supplier and Product: association, both exist independently")
supplier = make_supplier()
check("Supplier can be created with no Product", isinstance(supplier, Supplier))
laptop = ProductFactory.create("physical", "2001", "MacBook Air", 4500.0, 20, supplier, weight=1.24)
game = ProductFactory.create("digital", "3001", "Minecraft", 39.9, 500, supplier, download_size=1024.5)
check("Product and Supplier are different objects", laptop is not supplier)
check("one Supplier can supply many Products", laptop.supplier is game.supplier)
kept = laptop.supplier
del supplier
check("Products still reach the Supplier after 'del supplier'", laptop.supplier.get_name() == "TechWorld Distributors")
del laptop
check("Supplier still exists after a Product is deleted", game.supplier is kept)

# ---------------------------------------------------------------------------
section("2. Product stores a reference to its Supplier (not a copy, name or ID)")
supplier = make_supplier()
laptop = ProductFactory.create("physical", "2001", "MacBook Air", 4500.0, 20, supplier, weight=1.24)
check("product.supplier is the same Supplier object", laptop.supplier is supplier)
check("product.supplier is a Supplier, not a str", isinstance(laptop.supplier, Supplier))
output = capture(laptop.display_supplier_information)
check("Product can display its supplier's details", "sales@techworld.com" in output)

# ---------------------------------------------------------------------------
section("3. Inventory aggregates Product objects")
game = ProductFactory.create("digital", "3001", "Minecraft", 39.9, 500, supplier, download_size=1024.5)
inventory = Inventory()
check("add_product returns True", inventory.add_product(laptop) is True)
inventory.add_product(game)
check("Inventory stores the original object, not a copy", inventory.products[0] is laptop)
check("duplicate ID is rejected", inventory.add_product(laptop) is False)
check("find_product returns the Product", inventory.find_product("3001") is game)
check("find_product returns None when not found", inventory.find_product("9999") is None)
del inventory
check("Products still work after the Inventory is deleted", laptop.get_name() == "MacBook Air")

# ---------------------------------------------------------------------------
section("4. Products move between Inventories without being destroyed")
inventory_a, inventory_b = Inventory(), Inventory()
inventory_a.add_product(laptop)
check("remove_product returns True", inventory_a.remove_product("2001") is True)
check("Inventory A no longer has it", inventory_a.find_product("2001") is None)
check("Product still usable after removal", laptop.update_stock(15) is True and laptop.get_stock() == 15)
inventory_b.add_product(laptop)
check("same object now in Inventory B", inventory_b.find_product("2001") is laptop)
inventory_b.remove_product("2001")
check("emptying an Inventory does not destroy the Product", len(inventory_b.products) == 0 and laptop.get_stock() == 15)
check("removing a missing ID returns False", inventory_b.remove_product("9999") is False)

# ---------------------------------------------------------------------------
section("5. Order creates and manages its own OrderLines")
order = Order("ORD001")
check("new Order has no lines", order.order_lines == [])
order.add_order_line(laptop, 2)
order.add_order_line(game, 3)
check("add_order_line(product, quantity) created 2 lines", len(order.order_lines) == 2)
check("the lines are OrderLine objects made by the Order", all(type(line) is OrderLine for line in order.order_lines))
other_order = Order("ORD002")
other_order.add_order_line(laptop, 5)
check("same Product in two Orders -> two different OrderLines",
      order.order_lines[0] is not other_order.order_lines[0])
check("remove_order_line removes through the Order", order.remove_order_line("3001") is True and len(order.order_lines) == 1)
check("removing a missing line returns False", order.remove_order_line("9999") is False)
order.add_order_line(game, 3)

# ---------------------------------------------------------------------------
section("6. OrderLine refers to a Product but does not own it")
line = order.order_lines[0]
check("OrderLine.product is the original Product", line.product is laptop)
check("both Orders refer to the SAME Product", other_order.order_lines[0].product is laptop)
del other_order
check("Product survives its Order being deleted", laptop.get_name() == "MacBook Air")
check("Product can be in an Inventory and an Order at once",
      inventory_a.add_product(laptop) and order.order_lines[0].product is inventory_a.find_product("2001"))

# ---------------------------------------------------------------------------
section("7. Order calculates its total using its OrderLines")
check("OrderLine subtotal = price x quantity (4500 x 2)", line.calculate_subtotal() == 9000.0)
check("total = sum of line subtotals", order.calculate_total() == sum(l.calculate_subtotal() for l in order.order_lines))
check("total is $9119.70", abs(order.calculate_total() - 9119.70) < 0.001)
check("empty Order total is 0.0", Order("ORD003").calculate_total() == 0.0)

# ---------------------------------------------------------------------------
section("8. Type hints on attributes, parameters and return values")
#Reads product.py itself and checks every function/method and every self.attribute assignment
with open(os.path.join(HERE, "product.py"), encoding="utf-8") as file:
    tree = ast.parse(file.read())

missing: list[str] = []
methods: dict[str, list[ast.FunctionDef]] = {}       # class -> methods
for class_node in [n for n in tree.body if isinstance(n, ast.ClassDef)]:
    methods[class_node.name] = []
    for item in class_node.body:
        if isinstance(item, ast.FunctionDef):
            methods[class_node.name].append(item)
            where = class_node.name + "." + item.name
            for arg in item.args.args:
                if arg.arg not in ("self", "cls") and arg.annotation is None:
                    missing.append(where + " parameter '" + arg.arg + "'")
            if item.returns is None:
                missing.append(where + " return type")
            #Attributes are declared in __init__, so that is where they need a type hint
            #(later re-assignments such as self.__stock = quantity reuse the declared type)
            for node in (ast.walk(item) if item.name == "__init__" else []):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == "self":
                            missing.append(where + " attribute 'self." + target.attr + "' (no type hint)")
for problem in missing:
    print("    missing: " + problem)
check("every parameter, return value and self.attribute has a type hint", len(missing) == 0)

# ---------------------------------------------------------------------------
section("9. UML diagram types match the Python implementation")
#Python annotation -> the language-independent type name used in the diagram
def to_uml(annotation: str) -> str:
    annotation = annotation.strip().strip("'\"")
    if annotation.endswith("| None"):
        return to_uml(annotation[:-len("| None")]) + " [0..1]"
    if annotation.startswith("list["):
        return to_uml(annotation[5:-1]) + " [0..*]"
    if annotation.startswith("dict"):
        return "Dictionary"
    return {"str": "String", "int": "Integer", "float": "Real", "bool": "Boolean", "None": "void"}.get(annotation, annotation)

#Python 3.7 has no ast.unparse, so read annotation text straight from the source lines
source_lines = open(os.path.join(HERE, "product.py"), encoding="utf-8").read().splitlines()
def annotation_text(node) -> str:
    if hasattr(ast, "unparse"):
        return ast.unparse(node)
    line = source_lines[node.lineno - 1]
    return line[node.col_offset:node.end_col_offset] if hasattr(node, "end_col_offset") else _slice_annotation(node)

def _slice_annotation(node) -> str:
    #Fallback for 3.7: take text from the annotation's start up to the next ',' ')' ':' or '=' at depth 0
    line = source_lines[node.lineno - 1][node.col_offset:]
    depth, out = 0, ""
    for ch in line:
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        elif depth == 0 and ch in ",)=:":
            break
        out += ch
    return out.strip()

with open(os.path.join(HERE, "class_diagram.svg"), encoding="utf-8") as file:
    svg_text = " ".join(html.unescape(t) for t in re.findall(r">([^<]*)</text>", file.read()))
svg_text = re.sub(r"\s+", " ", svg_text)

not_in_diagram: list[str] = []
for class_name, class_methods in methods.items():
    expected_parts: list[str] = []
    for method in class_methods:
        params = ", ".join(a.arg + ": " + to_uml(annotation_text(a.annotation))
                           for a in method.args.args if a.arg not in ("self", "cls"))
        if method.name == "__init__":
            expected_parts.append("«create» " + class_name + "(" + params + ")")
        else:
            expected_parts.append(method.name + "(" + params + "): " + to_uml(annotation_text(method.returns)))
        for node in ast.walk(method):
            if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Attribute) and method.name == "__init__":
                name = node.target.attr.lstrip("_")
                visibility = "-" if node.target.attr.startswith("__") else "+"
                expected_parts.append(visibility + " " + name + ": " + to_uml(annotation_text(node.annotation)))
    for item in [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == class_name][0].body:
        if isinstance(item, ast.AnnAssign):
            expected_parts.append(item.target.id + ": " + to_uml(annotation_text(item.annotation)))
    for part in expected_parts:
        if part not in svg_text:
            not_in_diagram.append(class_name + ": " + part)
for problem in not_in_diagram:
    print("    not in diagram: " + problem)
total_members = sum(len(m) for m in methods.values())
check("every method, constructor and attribute type in product.py appears in class_diagram.svg ("
      + str(total_members) + " methods checked, plus their attributes)", len(not_in_diagram) == 0)
for relationship in ["manages", "contains", "refers to", "supplied by", "inherits from", "implements"]:
    check("diagram shows the '" + relationship + "' relationship", relationship in svg_text)

# ---------------------------------------------------------------------------
section("10. Inventory works with both subclasses through the Product abstraction")
inventory = Inventory()
mouse = ProductFactory.create("physical", "2002", "Wireless Mouse", 59.0, 75, supplier, weight=0.1)
ebook = ProductFactory.create("digital", "3002", "Python Crash Course", 29.5, 100, supplier, download_size=12.0)
for product in (mouse, ebook):
    inventory.add_product(product)
check("one collection holds both product types", {type(p) for p in inventory.products} == {PhysicalProduct, DigitalProduct})
output = capture(inventory.display_all_products)
check("display_all_products shows both", "Wireless Mouse" in output and "Python Crash Course" in output)
data = inventory.to_list()
check("to_list keeps each subclass's own fields", data[0]["weight"] == 0.1 and data[1]["download_size"] == 12.0)
inventory_source = [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Inventory"][0]
inventory_calls = {n.func.id for n in ast.walk(inventory_source) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
inventory_names = {n.id for n in ast.walk(inventory_source) if isinstance(n, ast.Name)}
check("Inventory code never uses isinstance()/type()", not ({"isinstance", "type"} & inventory_calls))
check("Inventory code never names PhysicalProduct or DigitalProduct",
      not ({"PhysicalProduct", "DigitalProduct"} & inventory_names))

# ---------------------------------------------------------------------------
section("11. Both subclasses preserve Product's expected behaviour (LSP)")
for product in (ProductFactory.create("physical", "2003", "Keyboard", 99.0, 10, supplier, weight=0.8),
                ProductFactory.create("digital", "3003", "Antivirus", 49.0, 10, supplier, download_size=300.0)):
    name = type(product).__name__
    check(name + ": update_stock(7) -> True and stock is 7", product.update_stock(7) is True and product.get_stock() == 7)
    check(name + ": update_stock(0) -> True", product.update_stock(0) is True)
    check(name + ": invalid -1 / 2.5 / 'x' -> False, stock unchanged",
          product.update_stock(-1) is False and product.update_stock(2.5) is False
          and product.update_stock("x") is False and product.get_stock() == 0)
    check(name + ": get_fulfilment_info() returns a non-empty str",
          isinstance(product.get_fulfilment_info(), str) and product.get_fulfilment_info() != "")
    returned: list = []
    printed = capture(lambda: returned.append(product.display_information()))
    check(name + ": display_information() prints and returns None", printed != "" and returned == [None])
    check(name + ": get_price() returns a float", isinstance(product.get_price(), float))
try:
    Product("X", "X", 1.0, 1, supplier)
    check("Product itself cannot be created (abstract)", False)
except TypeError:
    check("Product itself cannot be created (abstract)", True)

# ---------------------------------------------------------------------------
section("12. Polymorphic calls through Product references run the subclass version")
expected = {
    "2002": ("Weight: 0.10 kg", "This product requires physical shipping (0.10 kg)."),
    "3002": ("Download Size: 12.00 MB", "This product is delivered digitally as a download (12.00 MB)."),
}
for product in inventory.products:          # one loop, no isinstance()
    detail, fulfilment = expected[product.get_product_id()]
    check(product.get_name() + ": display_information() shows '" + detail + "'", detail in capture(product.display_information))
    check(product.get_name() + ": get_fulfilment_info() is the subclass version", product.get_fulfilment_info() == fulfilment)

# ---------------------------------------------------------------------------
print()
print("=" * 60)
print(str(results.count(True)) + "/" + str(len(results)) + " checks passed")
print("ALL TESTS PASSED" if all(results) else "SOME TESTS FAILED")
