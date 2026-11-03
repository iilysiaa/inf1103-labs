#External code to test PhysicalProduct and DigitalProduct together
#Each product is displayed, then its output is checked for:
#  - the common information printed by the parent class (Product)
#  - the extra information printed by the child class

import io
from contextlib import redirect_stdout

from product import PhysicalProduct, DigitalProduct


# Run display_information() and return what it printed, so the output can be checked
def capture_display(product):
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        product.display_information()
    return buffer.getvalue()


# Print PASS/FAIL for each piece of text that should appear in the output
def check_output(output, expected_parts):
    all_passed = True
    for part in expected_parts:
        if part in output:
            print("  PASS - found \"" + part + "\"")
        else:
            print("  FAIL - missing \"" + part + "\"")
            all_passed = False
    return all_passed


laptop = PhysicalProduct("2001", "MacBook Air", 4500.0, 20, 1.24)
game = DigitalProduct("3001", "Minecraft", 39.9, 500, 1024.5)

print("Physical Product")
print("-" * 45)
output = capture_display(laptop)
print(output, end="")
print("-" * 45)
print("Common information (from Product):")
physical_common = check_output(output, ["ID: 2001", "Name: MacBook Air", "Price: $4500.00", "Stock: 20"])
print("Physical information (from PhysicalProduct):")
physical_extra = check_output(output, ["Weight: 1.24 kg"])

print()
print("Digital Product")
print("-" * 45)
output = capture_display(game)
print(output, end="")
print("-" * 45)
print("Common information (from Product):")
digital_common = check_output(output, ["ID: 3001", "Name: Minecraft", "Price: $39.90", "Stock: 500"])
print("Digital information (from DigitalProduct):")
digital_extra = check_output(output, ["Download Size: 1024.50 MB"])

print()
if physical_common and physical_extra and digital_common and digital_extra:
    print("All checks passed.")
else:
    print("Some checks failed.")
