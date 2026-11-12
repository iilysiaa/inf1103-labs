import json
import os
from abc import ABC, abstractmethod

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

    def to_dict(self) -> dict:
        return {"supplier_id": self.__supplier_id, "name": self.__name, "contact_email": self.__contact_email}

    @classmethod
    def from_dict(cls, data: dict) -> "Supplier":
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
    def to_dict(self) -> dict:
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
    PRODUCT_TYPE = "physical"
    #Shipping rule: a flat base fee plus a charge for every kilogram
    BASE_SHIPPING_FEE = 5.00
    SHIPPING_FEE_PER_KG = 2.50

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

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["weight"] = self.__weight
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "PhysicalProduct":
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   Supplier.from_dict(data["supplier"]), data["weight"])


# ==================== DigitalProduct Class (inherits from Product) ====================
class DigitalProduct(Product):
    PRODUCT_TYPE = "digital"

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

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["type"] = self.PRODUCT_TYPE
        data["download_size"] = self.__download_size
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "DigitalProduct":
        return cls(data["id"], data["name"], data["price"], data["stock"],
                   Supplier.from_dict(data["supplier"]), data["download_size"])
