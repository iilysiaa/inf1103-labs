from __future__ import annotations

import json
import os
from abc import ABC, abstractmethod
from typing import Any

class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email

    def get_supplier_id(self) -> str:
        return self.__supplier_id

    def get_name(self) -> str:
        return self.__name

    def get_contact_email(self) -> str:
        return self.__contact_email

    def display_information(self) -> None:
        print("Supplier ID: " + self.__supplier_id + " | Name: " + self.__name + " | Email: " + self.__contact_email)

    def to_dict(self) -> dict[str, str]:
        return {"supplier_id": self.__supplier_id, "name": self.__name, "contact_email": self.__contact_email}

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> Supplier:
        return cls(data["supplier_id"], data["name"], data["contact_email"])


# ==================== Product Class ====================
#Product is an abstract base class (ABC) - it cannot be created directly, only through its subclasses
#Association: each Product HAS-A Supplier. The Supplier is created on its own and passed in,
#so the Product only stores a reference to it (it does not create or own the Supplier)
class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, supplier: Supplier) -> None:
        #Private attributes (name mangling) - outside code should use the methods below
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock_quantity
        #Type hint shows this attribute refers to a Supplier object (not just a name or ID)
        self.supplier: Supplier = supplier

    # Getters so other code can read the values without changing them directly
    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    # The Product controls how its stock is changed
    # Returns True if updated, False if the quantity is invalid
    def update_stock(self, quantity: int) -> bool:
        if isinstance(quantity, int) and quantity >= 0:
            self.__stock = quantity
            return True
        return False

    def display_information(self) -> None:
        print("ID: " + self.__product_id + " | Name: " + self.__name + " | Price: $" + format(self.__price, ".2f") + " | Stock: " + str(self.__stock))
        print("Supplier: " + self.supplier.get_name())

    # Access the supplier's information through the stored reference
    def display_supplier_information(self) -> None:
        self.supplier.display_information()

    # Convert the product back to a dictionary so it can be saved as JSON
    # dict[str, Any]: the keys are always str, but the values have different types per key
    # (str for "id", float for "price", int for "stock", a dict for "supplier"), which is what JSON data looks like
    def to_dict(self) -> dict[str, Any]:
        return {"id": self.__product_id, "name": self.__name, "price": self.__price,
                "stock": self.__stock, "supplier": self.supplier.to_dict()}

    # Abstract method - no implementation here, every subclass must provide its own
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass


# ==================== CanBeShipped Interface ====================
#An interface (abstract base class) for anything that can be shipped - not only products
class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass


# ==================== PhysicalProduct Class (inherits from Product, implements CanBeShipped) ====================
class PhysicalProduct(Product, CanBeShipped):
    PRODUCT_TYPE: str = "physical"
    #Shipping rule: a flat base fee plus a charge for every kilogram
    BASE_SHIPPING_FEE: float = 5.00
    SHIPPING_FEE_PER_KG: float = 2.50

    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, supplier: Supplier, weight: float) -> None:
        #Pass the common attributes (including the Supplier) up to the Product constructor
        super().__init__(product_id, name, price, stock_quantity, supplier)
        #Extra attribute only a physical product has: weight in kilograms
        self.__weight: float = weight

    def get_weight(self) -> float:
        return self.__weight

    def display_information(self) -> None:
        super().display_information()
        print("Weight: " + format(self.__weight, ".2f") + " kg")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping (" + format(self.__weight, ".2f") + " kg)."

    def calculate_shipping_cost(self) -> float:
        return self.BASE_SHIPPING_FEE + self.SHIPPING_FEE_PER_KG * self.__weight

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["weight"] = self.__weight
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PhysicalProduct:
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   Supplier.from_dict(data["supplier"]), data["weight"])


# ==================== DigitalProduct Class (inherits from Product) ====================
class DigitalProduct(Product):
    PRODUCT_TYPE: str = "digital"

    def __init__(self, product_id: str, name: str, price: float,
                 stock_quantity: int, supplier: Supplier, download_size: float) -> None:
        #Pass the common attributes (including the Supplier) up to the Product constructor
        super().__init__(product_id, name, price, stock_quantity, supplier)
        #Extra attribute only a digital product has: download size in megabytes
        self.__download_size: float = download_size

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print("Download Size: " + format(self.__download_size, ".2f") + " MB")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally as a download (" + format(self.__download_size, ".2f") + " MB)."

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["download_size"] = self.__download_size
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DigitalProduct:
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   Supplier.from_dict(data["supplier"]), data["download_size"])


# ==================== Inventory Class ====================
#Aggregation: an Inventory groups Product objects, but the products are created outside
#and can exist on their own - removing them from (or deleting) the Inventory does not destroy them
class Inventory:
    def __init__(self) -> None:
        #Typed with the base class Product, not PhysicalProduct or DigitalProduct:
        #the Inventory only uses what every Product has (ID, display_information, to_dict...),
        #so it can hold any kind of Product - including new subclasses added later - without being changed
        self.products: list[Product] = []

    # Add an existing Product object (the Inventory only stores a reference to it)
    # Returns True if added, False if a product with the same ID already exists
    # (returns bool rather than None so the caller can tell whether the add worked)
    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.products.append(product)
        return True

    # Remove the matching Product reference from the collection - the Product object itself is not destroyed
    # Returns True if removed, False if no product has that ID
    def remove_product(self, product_id: str) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        self.products.remove(product)
        return True

    # Find a Product by its ID (not case-sensitive), or None if not found
    def find_product(self, product_id: str) -> Product | None:
        for product in self.products:
            if product.get_product_id().upper() == product_id.upper():
                return product
        return None

    def display_all_products(self) -> None:
        print("Current Inventory")
        print("-" * 45)
        if len(self.products) == 0:
            print("No products in inventory.")
        #Polymorphism: the Inventory does not check whether a product is Physical or Digital -
        #it asks each Product to display itself, and the object runs its own display_information()
        for product in self.products:
            product.display_information()
            print("-" * 45)

    # Returns the products as a list of dictionaries (used when saving to JSON)
    def to_list(self) -> list[dict[str, Any]]:
        result: list[dict[str, Any]] = []
        for product in self.products:
            result.append(product.to_dict())
        return result


# ==================== OrderLine Class ====================
#One line of an order: a reference to a Product and how many of it were requested
#The OrderLine does not create or own the Product, it only refers to an existing one
class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        self.product: Product = product
        self.quantity: int = quantity

    # Price is a private attribute of Product, so it is read through get_price()
    def calculate_subtotal(self) -> float:
        return self.product.get_price() * self.quantity


# ==================== Discount Strategies (Strategy pattern) ====================
#Each discount rule is its own class with the same apply() method,
#so a new discount (e.g. a student discount) is added as a NEW class
class DiscountStrategy(ABC):
    # Takes the order total and returns the discounted total
    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    # Returns the total unchanged
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    # e.g. PercentageDiscount(10) takes 10% off
    def __init__(self, percentage: float) -> None:
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage: float = percentage

    def get_percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
    # e.g. BulkDiscount(200, 20) takes 20 off any total of 200 or more
    def __init__(self, threshold: float, amount: float) -> None:
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and amount cannot be negative.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    def get_threshold(self) -> float:
        return self.__threshold

    def get_amount(self) -> float:
        return self.__amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            #Never return a negative total, even if the amount is larger than the total
            return max(total - self.__amount, 0.0)
        return total


# ==================== Order Class ====================
#Composition: an Order creates and owns its OrderLine objects - they are made inside the Order
#and only exist as part of it. The Products they refer to are NOT owned by the Order
#(they exist independently and may also be in an Inventory)
class Order:
    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    # Takes a Product and quantity, and creates the OrderLine internally
    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    # Removes the OrderLine for the given product ID - the OrderLine is discarded with it,
    # but the Product it referred to is not affected
    # Returns True if removed, False if the order has no line for that product
    def remove_order_line(self, product_id: str) -> bool:
        order_line: OrderLine
        for order_line in self.order_lines:
            if order_line.product.get_product_id().upper() == product_id.upper():
                self.order_lines.remove(order_line)
                return True
        return False

    # Asks each OrderLine for its own subtotal and adds them up
    def calculate_total(self) -> float:
        total: float = 0.0
        for order_line in self.order_lines:
            total += order_line.calculate_subtotal()
        return total

    def display_order(self) -> None:
        print("Order " + self.order_id)
        print("-" * 45)
        if len(self.order_lines) == 0:
            print("No order lines.")
        for order_line in self.order_lines:
            print(order_line.product.get_name() + " | $" + format(order_line.product.get_price(), ".2f")
                  + " x " + str(order_line.quantity) + " = $" + format(order_line.calculate_subtotal(), ".2f"))
        print("Total: $" + format(self.calculate_total(), ".2f"))
