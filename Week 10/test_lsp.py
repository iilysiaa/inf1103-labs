from product import Supplier, Product, PhysicalProduct, DigitalProduct, Inventory


# Print PASS/FAIL for a True/False check
def check(description: str, condition: bool) -> None:
    print("  " + ("PASS" if condition else "FAIL") + " - " + description)


# Code written ONLY against Product - it relies on the update_stock() expectation above
def check_update_stock_contract(product: Product) -> None:
    start = product.get_stock()
    check("valid 15 returns True", product.update_stock(15) is True)
    check("stock is now 15", product.get_stock() == 15)
    check("valid 0 returns True", product.update_stock(0) is True)
    check("stock is now 0", product.get_stock() == 0)
    product.update_stock(start)
    check("invalid -5 returns False", product.update_stock(-5) is False)
    check("invalid 2.5 returns False", product.update_stock(2.5) is False)
    check("invalid 'ten' returns False", product.update_stock("ten") is False)
    check("stock unchanged after invalid inputs", product.get_stock() == start)


supplier = Supplier("S001", "TechWorld Distributors", "sales@techworld.com")
laptop = PhysicalProduct("2001", "MacBook Air", 4500.0, 20, supplier, 1.24)
game = DigitalProduct("3001", "Minecraft", 39.9, 500, supplier, 1024.5)

# 1. Both subclasses keep the update_stock() expectation set by Product
print("1. PhysicalProduct keeps the update_stock() expectation")
print("-" * 45)
check_update_stock_contract(laptop)
print()
print("2. DigitalProduct keeps the update_stock() expectation")
print("-" * 45)
check_update_stock_contract(game)
print()


# 2. The teammate's proposed DigitalProduct
class TeammateDigitalProduct(DigitalProduct):
    def update_stock(self, quantity: int) -> None:
        raise NotImplementedError("Digital products have no stock")


ebook = TeammateDigitalProduct("3002", "Python Crash Course", 29.5, 100, supplier, 12.0)
inventory = Inventory()
inventory.add_product(laptop)
inventory.add_product(ebook)

# Code that uses the Inventory and only knows about Product - e.g. "restock everything to 50"
print("3. Restocking every product in the Inventory to 50 (teammate's version)")
print("-" * 45)
for product in inventory.products:
    try:
        result = product.update_stock(50)
        print("  " + product.get_name() + ": update_stock(50) returned " + str(result))
    except NotImplementedError as error:
        print("  " + product.get_name() + ": CRASHED with NotImplementedError - " + str(error))
print()
check("teammate's version accepts the valid input 50 like Product does",
      ebook.get_stock() == 50)
