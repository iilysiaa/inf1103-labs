#External code to test that saving and loading keeps each product's type and extra attributes
#It saves to a separate test file so the real inventory.json is not changed

import json
import os

import product
from product import Inventory, PhysicalProduct, DigitalProduct, save_inventory, load_inventory

TEST_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_inventory.json")
#Point the save/load functions at the test file instead of inventory.json
product.INVENTORY_FILE = TEST_FILE


# Print PASS/FAIL for one check and return whether it passed
def check(description, passed):
    if passed:
        print("  PASS - " + description)
    else:
        print("  FAIL - " + description)
    return passed


#---------- 1. Build an inventory with both product types and save it ----------
inventory = Inventory()
inventory.add_product(PhysicalProduct("P100", "Office Chair", 350.0, 12, 8.5))
inventory.add_product(DigitalProduct("D200", "Photo Editor", 59.9, 500, 850.0))

print("Saving inventory with one physical and one digital product...")
save_inventory(inventory)

print()
print("Saved JSON:")
with open(TEST_FILE, "r") as file:
    saved = json.load(file)
print(json.dumps(saved, indent=4))

results = []
print()
print("Checking the saved file:")
results.append(check("physical product saved with type \"physical\"", saved[0]["type"] == "physical"))
results.append(check("physical product saved with its weight", saved[0]["weight"] == 8.5))
results.append(check("digital product saved with type \"digital\"", saved[1]["type"] == "digital"))
results.append(check("digital product saved with its download size", saved[1]["download_size"] == 850.0))

#---------- 2. "Restart" by loading into a brand new Inventory ----------
print()
print("Restarting: loading the file into a new Inventory...")
del inventory
loaded = load_inventory()

chair = loaded.search_product("P100")
editor = loaded.search_product("D200")

print()
print("Checking the restored physical product:")
results.append(check("restored as a PhysicalProduct", isinstance(chair, PhysicalProduct)))
results.append(check("common information restored", chair.get_name() == "Office Chair" and chair.get_price() == 350.0 and chair.get_stock() == 12))
results.append(check("weight restored", chair.get_weight() == 8.5))
results.append(check("shipping cost still works", round(chair.calculate_shipping_cost(), 2) == 26.25))

print()
print("Checking the restored digital product:")
results.append(check("restored as a DigitalProduct", isinstance(editor, DigitalProduct)))
results.append(check("common information restored", editor.get_name() == "Photo Editor" and editor.get_price() == 59.9 and editor.get_stock() == 500))
results.append(check("download size restored", editor.get_download_size() == 850.0))

print()
print("Restored inventory:")
loaded.display_all()

#Clean up the test file
os.remove(TEST_FILE)

print()
if all(results):
    print("All checks passed.")
else:
    print("Some checks failed.")
