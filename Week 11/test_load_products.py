#External code to test load_products() (try / except / else / finally)
#Each test writes its own temporary CSV file, so products.csv is never changed

import io
import os
import tempfile
from contextlib import redirect_stdout

from product import Supplier, Inventory, PhysicalProduct, DigitalProduct, load_products

HEADER = "product_type,product_id,name,price,stock_quantity,weight,download_size\n"
supplier = Supplier("S001", "TechWorld Distributors", "sales@techworld.com")


# Print PASS/FAIL for a True/False check
def check(description: str, condition: bool) -> None:
    print("  " + ("PASS" if condition else "FAIL") + " - " + description)


# Write the CSV text to a temporary file, load it into a new Inventory, and return (inventory, printed lines)
def load_from_text(csv_text: str) -> tuple:
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as temp:
        temp.write(csv_text)
        path = temp.name
    try:
        return load_from_path(path)
    finally:
        os.remove(path)


def load_from_path(path: str) -> tuple:
    inventory = Inventory()
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        load_products(path, inventory, supplier)
    return inventory, buffer.getvalue().splitlines()


# 1. File does not exist -> message, no crash, finally still runs
print("1. File does not exist")
print("-" * 45)
inventory, lines = load_from_path("no_such_file.csv")
check("prints 'Products file not found: no_such_file.csv'", lines[0] == "Products file not found: no_such_file.csv")
check("finally prints 'Load attempt finished.'", lines[-1] == "Load attempt finished.")
check("no products-loaded line (the else block did not run)", not any("products loaded" in l for l in lines))
check("inventory is still empty", len(inventory.products) == 0)
print()

# 2. All rows valid
print("2. All rows valid")
print("-" * 45)
inventory, lines = load_from_text(HEADER
                                  + "physical,2001,MacBook Air,4500.00,20,1.24,\n"
                                  + "digital,3001,Minecraft,39.90,500,,1024.5\n")
check("prints '2 products loaded.' then 'Load attempt finished.'",
      lines == ["2 products loaded.", "Load attempt finished."])
laptop, game = inventory.find_product("2001"), inventory.find_product("3001")
check("physical row -> PhysicalProduct with weight 1.24", type(laptop) is PhysicalProduct and laptop.get_weight() == 1.24)
check("digital row -> DigitalProduct with download size 1024.5",
      type(game) is DigitalProduct and game.get_download_size() == 1024.5)
check("values converted: price is a float, stock is an int", laptop.get_price() == 4500.0 and laptop.get_stock() == 20)
check("every product gets the supplier passed in", laptop.supplier is supplier and game.supplier is supplier)
print()

# 3. Invalid rows are reported and skipped; loading carries on
print("3. Invalid rows are skipped, the rest still load")
print("-" * 45)
inventory, lines = load_from_text(HEADER
                                  + "physical,2001,MacBook Air,4500.00,20,1.24,\n"   # row 2  valid
                                  + "ebook,4001,Old Manual,15.00,10,,2.0\n"          # row 3  unknown type
                                  + "physical,2002,Keyboard,abc,10,0.8,\n"           # row 4  price not a number
                                  + "physical,2003,Monitor,-5,10,3.0,\n"             # row 5  price <= 0
                                  + "digital,3002,Antivirus,49.00,-1,,300\n"         # row 6  negative stock
                                  + "digital,3003,Game,20.00,ten,,500\n"             # row 7  stock not a number
                                  + "physical,2004,Desk,150.00,5,heavy,\n"           # row 8  weight not a number
                                  + "digital,3004,Too Short,10.00\n"                 # row 9  too few columns
                                  + "physical,2001,Duplicate ID,99.00,1,1.0,\n"      # row 10 duplicate ID
                                  + "\n"                                             # row 11 blank line, ignored
                                  + "digital,3001,Minecraft,39.90,500,,1024.5\n")    # row 12 valid
for line in lines:
    print("    output: " + line)
skipped = [l for l in lines if l.startswith("Row ")]
check("8 bad rows reported (rows 3-10)", len(skipped) == 8)
check("rows are numbered as in the file (row 3 is the unknown type)", skipped[0] == "Row 3 skipped: Unknown product type: ebook")
check("price 'abc' reported", any(l.startswith("Row 4 skipped") and "abc" in l for l in skipped))
check("price -5 reported with the Product's validation message", "Row 5 skipped: Price must be greater than zero." in skipped)
check("negative stock reported", "Row 6 skipped: Stock quantity cannot be negative." in skipped)
check("weight that is not a number reported", any(l.startswith("Row 8 skipped") and "heavy" in l for l in skipped))
check("too few columns reported", "Row 9 skipped: expected 5 to 7 columns, got 4" in skipped)
check("duplicate ID reported", "Row 10 skipped: product ID 2001 already exists." in skipped)
check("the valid row AFTER the bad rows still loaded", inventory.find_product("3001") is not None)
check("prints '2 products loaded.'", "2 products loaded." in lines)
check("'Load attempt finished.' is the last line", lines[-1] == "Load attempt finished.")
print()

# 4. Only the 5 required columns -> weight / download size default to 0.0
print("4. Rows with only the 5 required columns")
print("-" * 45)
inventory, lines = load_from_text("product_type,product_id,name,price,stock_quantity\n"
                                  + "physical,P001,Desk Lamp,25.00,10\n"
                                  + "digital,D001,Photo Editor,49.90,100\n"
                                  + "physical,P009,Too Many,10.00,1,1.0,2.0,extra\n")
check("2 products loaded", "2 products loaded." in lines)
check("physical with no weight column -> weight 0.0", inventory.find_product("P001").get_weight() == 0.0)
check("digital with no download_size column -> 0.0", inventory.find_product("D001").get_download_size() == 0.0)
check("a row with 8 columns is skipped", "Row 4 skipped: expected 5 to 7 columns, got 8" in lines)
print()

# 5. Header only -> nothing to load
print("5. File with only a header row")
print("-" * 45)
inventory, lines = load_from_text(HEADER)
check("prints '0 products loaded.' then 'Load attempt finished.'",
      lines == ["0 products loaded.", "Load attempt finished."])
print()

# 6. The products.csv in this folder (5 columns: no weight / download size)
print("6. products.csv")
print("-" * 45)
inventory, lines = load_from_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "products.csv"))
for line in lines:
    print("    output: " + line)
check("3 products loaded: P001, D001, P003",
      "3 products loaded." in lines and [p.get_product_id() for p in inventory.products] == ["P001", "D001", "P003"])
check("'service' row skipped", "Row 4 skipped: Unknown product type: service" in lines)
check("price 'abc' row skipped", any(l.startswith("Row 5 skipped") and "abc" in l for l in lines))
check("'Load attempt finished.' is the last line", lines[-1] == "Load attempt finished.")
