#External code to show why Inventory.products is list[Product] (the base class)
#rather than list[PhysicalProduct] or list[DigitalProduct]
#A NEW kind of Product is defined here, and the Inventory and Order accept it without being changed

from product import Supplier, Product, PhysicalProduct, DigitalProduct, Inventory, Order


# A new Product subclass that did not exist when Inventory and Order were written
class GiftCard(Product):
    def get_fulfilment_info(self) -> str:
        return "This gift card is sent by email."


# Print PASS/FAIL for a True/False check
def check(description, condition):
    print("  " + ("PASS" if condition else "FAIL") + " - " + description)


supplier = Supplier("S001", "TechWorld Distributors", "sales@techworld.com")
laptop = PhysicalProduct("2001", "MacBook Air", 4500.0, 20, supplier, 1.24)
game = DigitalProduct("3001", "Minecraft", 39.9, 500, supplier, 1024.5)
gift_card = GiftCard("4001", "Store Gift Card", 50.0, 1000, supplier)

# One Inventory holds all three kinds of Product
inventory = Inventory()
inventory.add_product(laptop)
inventory.add_product(game)
inventory.add_product(gift_card)
inventory.display_all_products()

print("Checks")
print("-" * 45)
check("Inventory holds 3 products", len(inventory.products) == 3)
check("find_product works for the new GiftCard", inventory.find_product("4001") is gift_card)
for product in inventory.products:
    check(type(product).__name__ + " is a Product", isinstance(product, Product))

# An Order also accepts the new subclass
order = Order("ORD001")
order.add_order_line(gift_card, 2)
order.add_order_line(game, 1)
check("Order total with a GiftCard is $139.90", abs(order.calculate_total() - 139.90) < 0.001)
print()
order.display_order()
