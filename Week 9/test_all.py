#Full test of the Week 9 Inventory Management System
#Each section matches one requirement from the lab sheet
#Saving/loading uses a separate test file so the real inventory.json is not changed

import io
import json
import os
from contextlib import redirect_stdout

import product
from product import Product, CanBeShipped, PhysicalProduct, DigitalProduct, Inventory, save_inventory, load_inventory

TEST_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_inventory.json")
product.INVENTORY_FILE = TEST_FILE

results = []


# Print PASS/FAIL for one check and remember the result
def check(description, passed):
    if passed:
        print("  PASS - " + description)
    else:
        print("  FAIL - " + description)
    results.append(passed)


# Run a function and return everything it printed, so the output can be checked
def capture(function):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        function()
    return buffer.getvalue()


def section(title):
    print()
    print(title)
    print("-" * 60)


laptop = PhysicalProduct("P100", "MacBook Air", 4500.0, 20, 1.24)
game = DigitalProduct("D200", "Minecraft", 39.9, 500, 1024.5)

#---------- 1. Physical products store and display their weights ----------
section("1. Physical products store and display their weights")
output = capture(laptop.display_information)
print(output, end="")
check("weight is stored", laptop.get_weight() == 1.24)
check("display shows the common information from Product", "ID: P100 | Name: MacBook Air | Price: $4500.00 | Stock: 20" in output)
check("display shows the weight", "Weight: 1.24 kg" in output)

#---------- 2. Digital products store and display their download sizes ----------
section("2. Digital products store and display their download sizes")
output = capture(game.display_information)
print(output, end="")
check("download size is stored", game.get_download_size() == 1024.5)
check("display shows the common information from Product", "ID: D200 | Name: Minecraft | Price: $39.90 | Stock: 500" in output)
check("display shows the download size", "Download Size: 1024.50 MB" in output)

#---------- 3. Both subclasses implement get_fulfilment_info() ----------
section("3. Both subclasses implement get_fulfilment_info()")
print("  " + laptop.get_fulfilment_info())
print("  " + game.get_fulfilment_info())
check("PhysicalProduct defines its own get_fulfilment_info()", "get_fulfilment_info" in PhysicalProduct.__dict__)
check("DigitalProduct defines its own get_fulfilment_info()", "get_fulfilment_info" in DigitalProduct.__dict__)
check("physical message mentions shipping", "physical shipping" in laptop.get_fulfilment_info())
check("digital message mentions digital delivery", "delivered digitally" in game.get_fulfilment_info())

#---------- 4. The abstract Product class cannot be instantiated directly ----------
section("4. The abstract Product class cannot be instantiated directly")
try:
    Product("X1", "Generic", 1.0, 1)
    check("Product() raises TypeError", False)
except TypeError as error:
    print("  " + str(error))
    check("Product() raises TypeError", True)

#---------- 5. Physical products can calculate shipping costs ----------
section("5. Physical products can calculate shipping costs ($5.00 + $2.50 per kg)")
for weight, expected in [(0.0, 5.00), (1.24, 8.10), (6.5, 21.25), (30.0, 80.00)]:
    item = PhysicalProduct("S1", "Box", 10.0, 1, weight)
    cost = item.calculate_shipping_cost()
    check(format(weight, ".2f") + " kg costs $" + format(expected, ".2f") + " (got $" + format(cost, ".2f") + ")", round(cost, 2) == expected)
check("PhysicalProduct implements CanBeShipped", isinstance(laptop, CanBeShipped))


# A physical product that forgets calculate_shipping_cost() should not be allowed
class BrokenPhysicalProduct(Product, CanBeShipped):
    def get_fulfilment_info(self):
        return "Shipped"

try:
    BrokenPhysicalProduct("B1", "Broken", 1.0, 1)
    check("a CanBeShipped class without calculate_shipping_cost() is rejected", False)
except TypeError:
    check("a CanBeShipped class without calculate_shipping_cost() is rejected", True)

#---------- 6. Digital products are not required to implement shipping behaviour ----------
section("6. Digital products are not required to implement shipping behaviour")
check("DigitalProduct can be created without calculate_shipping_cost()", isinstance(game, DigitalProduct))
check("DigitalProduct does not implement CanBeShipped", not isinstance(game, CanBeShipped))
check("DigitalProduct has no calculate_shipping_cost()", not hasattr(game, "calculate_shipping_cost"))

#---------- 7. Inventory operations continue to work ----------
section("7. Inventory operations continue to work")
inventory = Inventory()
check("add a physical product", inventory.add_product(laptop))
check("add a digital product", inventory.add_product(game))
check("duplicate product ID is rejected", not inventory.add_product(DigitalProduct("p100", "Copy", 1.0, 1, 1.0)))
check("search finds a product (not case-sensitive)", inventory.search_product("p100") is laptop)
check("search returns None for a missing ID", inventory.search_product("Z999") is None)
check("update stock with a valid quantity", game.update_stock(450) and inventory.search_product("D200").get_stock() == 450)
check("update stock rejects a negative quantity", not game.update_stock(-5) and game.get_stock() == 450)
output = capture(inventory.display_all)
print(output, end="")
check("display all shows both products and their extra details", "MacBook Air" in output and "Weight: 1.24 kg" in output and "Minecraft" in output and "Download Size: 1024.50 MB" in output)
check("to_list returns one dictionary per product", len(inventory.to_list()) == 2)
output = capture(Inventory().display_all)
check("display all handles an empty inventory", "No products in inventory." in output)

#---------- 8. JSON saving and loading preserve the correct product types ----------
section("8. JSON saving and loading preserve the correct product types")
capture(lambda: save_inventory(inventory))
with open(TEST_FILE, "r") as file:
    saved = json.load(file)
print(json.dumps(saved, indent=4))
check("physical product saved with type and weight", saved[0]["type"] == "physical" and saved[0]["weight"] == 1.24)
check("digital product saved with type and download size", saved[1]["type"] == "digital" and saved[1]["download_size"] == 1024.5)

#"Restart" by loading the file into a brand new Inventory
loaded = None
def do_load():
    global loaded
    loaded = load_inventory()
capture(do_load)
chair = loaded.search_product("P100")
editor = loaded.search_product("D200")
check("physical product restored as PhysicalProduct", isinstance(chair, PhysicalProduct))
check("physical product restored with all its values", chair.to_dict() == laptop.to_dict())
check("digital product restored as DigitalProduct", isinstance(editor, DigitalProduct))
check("digital product restored with all its values (including updated stock)", editor.to_dict() == game.to_dict())
check("restored physical product can still calculate shipping", round(chair.calculate_shipping_cost(), 2) == 8.10)

#A file with an unknown type should be reported as invalid, not crash the program
with open(TEST_FILE, "w") as file:
    json.dump([{"type": "subscription", "id": "S1", "name": "Plan", "price": 9.9, "stock": 1}], file)
output = capture(do_load)
check("unknown product type is reported as invalid data", "invalid" in output and loaded.to_list() == [])

os.remove(TEST_FILE)

print()
print("=" * 60)
print(str(results.count(True)) + " / " + str(len(results)) + " checks passed.")
if all(results):
    print("All checks passed.")
else:
    print("Some checks failed.")
