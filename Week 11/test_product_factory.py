#External code to test ProductFactory (Factory pattern)
#The factory decides which Product subclass to create from a product type string

from product import Supplier, Product, PhysicalProduct, DigitalProduct, ProductFactory


# Print PASS/FAIL for a True/False check
def check(description: str, condition: bool) -> None:
    print("  " + ("PASS" if condition else "FAIL") + " - " + description)


supplier = Supplier("S001", "TechWorld Distributors", "sales@techworld.com")

# 1. "physical" creates a PhysicalProduct with all its values
print("1. ProductFactory.create(\"physical\", ...)")
print("-" * 45)
laptop = ProductFactory.create("physical", "2001", "MacBook Air", 4500.0, 20, supplier, weight=1.24)
check("returns a PhysicalProduct", type(laptop) is PhysicalProduct)
check("it is a Product", isinstance(laptop, Product))
check("values are set (ID, name, price, stock)",
      (laptop.get_product_id(), laptop.get_name(), laptop.get_price(), laptop.get_stock()) == ("2001", "MacBook Air", 4500.0, 20))
check("weight is 1.24", laptop.get_weight() == 1.24)
check("supplier is the same Supplier object", laptop.supplier is supplier)
print()

# 2. "digital" creates a DigitalProduct with all its values
print("2. ProductFactory.create(\"digital\", ...)")
print("-" * 45)
game = ProductFactory.create("digital", "3001", "Minecraft", 39.9, 500, supplier, download_size=1024.5)
check("returns a DigitalProduct", type(game) is DigitalProduct)
check("it is a Product", isinstance(game, Product))
check("download size is 1024.5", game.get_download_size() == 1024.5)
check("each call creates a new object",
      ProductFactory.create("digital", "3001", "Minecraft", 39.9, 500, supplier, download_size=1024.5) is not game)
print()

# 3. Invalid requests raise ValueError
print("3. Invalid requests")
print("-" * 45)
for description, product_type, extra in [
        ("unknown type 'ebook'", "ebook", {}),
        ("type is case-sensitive: 'Physical'", "Physical", {"weight": 1.0}),
        ("physical with no weight", "physical", {}),
        ("digital with no download size", "digital", {}),
        ("physical given only a download size", "physical", {"download_size": 5.0})]:
    try:
        ProductFactory.create(product_type, "X", "X", 1.0, 1, supplier, **extra)
        check(description + " raises ValueError", False)
    except ValueError as error:
        check(description + " raises ValueError (" + str(error) + ")", True)
