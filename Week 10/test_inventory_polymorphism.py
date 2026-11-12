#External code to test polymorphism through the Inventory's Product collection
#PhysicalProduct and DigitalProduct objects are stored in the SAME Inventory, and ONE loop calls
#display_information() and get_fulfilment_info() on each one - no separate loops, no isinstance().
#Each object runs its own specialised implementation.

import io
from contextlib import redirect_stdout

from product import Supplier, Product, PhysicalProduct, DigitalProduct, Inventory


# Run display_information() and return what it printed, so the output can be checked
def capture_display(product: Product) -> str:
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        product.display_information()
    return buffer.getvalue()


# Print PASS/FAIL for a True/False check
def check(description: str, condition: bool) -> bool:
    print("  " + ("PASS" if condition else "FAIL") + " - " + description)
    return condition


supplier = Supplier("S001", "TechWorld Distributors", "sales@techworld.com")

inventory = Inventory()
inventory.add_product(PhysicalProduct("2001", "MacBook Air", 4500.0, 20, supplier, 1.24))
inventory.add_product(DigitalProduct("3001", "Minecraft", 39.9, 500, supplier, 1024.5))
inventory.add_product(PhysicalProduct("2002", "Wireless Mouse", 59.0, 75, supplier, 0.1))
inventory.add_product(DigitalProduct("3002", "Python Crash Course", 29.5, 100, supplier, 12.0))

# What each product's OWN implementation should produce, looked up by product ID
#(the test decides what is correct - the loop below never decides which method to call)
EXPECTED = {
    "2001": {"display": "Weight: 1.24 kg", "fulfilment": "This product requires physical shipping (1.24 kg)."},
    "3001": {"display": "Download Size: 1024.50 MB", "fulfilment": "This product is delivered digitally as a download (1024.50 MB)."},
    "2002": {"display": "Weight: 0.10 kg", "fulfilment": "This product requires physical shipping (0.10 kg)."},
    "3002": {"display": "Download Size: 12.00 MB", "fulfilment": "This product is delivered digitally as a download (12.00 MB)."},
}

all_passed = True
# ONE loop over the Product collection - the same two calls for every object
for product in inventory.products:
    display_output = capture_display(product)
    fulfilment = product.get_fulfilment_info()
    expected = EXPECTED[product.get_product_id()]

    print(product.get_name())
    print("-" * 45)
    print(display_output + fulfilment)
    print()
    #Common part printed by Product's display_information() (via super())
    all_passed &= check("shows the common Product information",
                        "ID: " + product.get_product_id() in display_output and "Supplier: TechWorld Distributors" in display_output)
    #Specialised part printed by the subclass's own display_information()
    all_passed &= check("display_information() shows \"" + expected["display"] + "\"", expected["display"] in display_output)
    #Specialised get_fulfilment_info() from the subclass
    all_passed &= check("get_fulfilment_info() is correct", fulfilment == expected["fulfilment"])
    #Make sure it did not ALSO run the other subclass's behaviour
    wrong_detail = "Download Size" if "Weight" in expected["display"] else "Weight"
    all_passed &= check("does not show \"" + wrong_detail + "\"", wrong_detail not in display_output)
    print()

print("=" * 45)
print("ALL TESTS PASSED" if all_passed else "SOME TESTS FAILED")
