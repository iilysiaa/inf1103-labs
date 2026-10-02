import os

INVENTORY_FILE = "inventory.txt"


def load_inventory(filename=INVENTORY_FILE):
    """
    Reads previously saved inventory from the file.
    Each line is stored as: item,quantity
    Returns a dictionary {item: quantity}.
    If the file does not exist (or can't be read), returns an empty inventory.
    """
    inventory = {}

    if not os.path.exists(filename):
        print("No saved inventory found. Starting with an empty inventory.")
        return inventory

    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                try:
                    item, quantity = line.rsplit(",", 1)
                    inventory[item] = inventory.get(item, 0) + int(quantity)
                except ValueError:
                    print(f"Skipping invalid line in inventory file: {line}")
    except OSError:
        print("Could not read the inventory file. Starting with an empty inventory.")
        return {}

    return inventory


def save_inventory(inventory, filename=INVENTORY_FILE):
    """Writes the inventory dictionary to the file, one 'item,quantity' per line."""
    try:
        with open(filename, "w") as file:
            for item, quantity in inventory.items():
                file.write(f"{item},{quantity}\n")
    except OSError:
        print("Warning: could not save inventory to file.")


def display_inventory(inventory):
    """Prints every item in the inventory, one 'item, quantity' per line."""
    print("Current Inventory:\n")
    if not inventory:
        print("(no items yet)")
    for item, quantity in inventory.items():
        print(f"{item}, {quantity}")
    print(f"\nTotal Inventory: {sum(inventory.values())}\n")


def get_valid_input():
    """
    Prompts the user for an item name and a stock quantity.
    Returns:
        (item, quantity) -> a valid item name and non-negative quantity
        "quit"           -> if the user wants to exit
        None             -> if the quantity entered was invalid (so the caller can count it as a failure)
    """
    try:
        item = input("Enter an inventory item (or type 'quit' to exit): ")
    except EOFError:
        print("\nNo input available (run with docker run -it). Exiting.")
        return "quit"

    if item.lower() == 'quit':
        return "quit"

    try:
        quantity = int(input(f"Enter the quantity of {item}: "))

        if quantity < 0:
            print("Quantity cannot be negative. Please enter a valid number.")
            return None

        return item, quantity

    except ValueError:
        print("Please enter a valid number for quantity.")
        return None
    except EOFError:
        return "quit"


def process_delivery(current_total, new_value):
    """Adds a new delivery to the running total and returns the new total."""
    return current_total + new_value


def calculate_tax(amount):
    """Returns 10% tax on a single delivery amount."""
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    """Prints the final summary report."""
    print("\n--- Final Audit Report ---")
    print("Total Deliveries Processed (units):", total_units)
    print("Number of Failed/Rejected Entries:", failed_attempts)


def show_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def exit_program(products, transactions):
    print("Saving inventory before exit...")
    if save_inventory(products, transactions):
        print("Inventory saved successfully.")
    print("Thank you for using Inventory Management System.")
    print("Program terminated.")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    products, transactions = load_inventory()

    while True:
        show_menu()
        option = read_input("Enter option: ")

        if option is None or option == "6":
            exit_program(products, transactions)
            break
        elif option == "1":
            display_all(products)
        elif option == "2":
            add_product(products, transactions)
        elif option == "3":
            update_stock(products, transactions)
        elif option == "4":
            search_product(products)
        elif option == "5":
            print("Saving inventory...")
            if save_inventory(products, transactions):
                print(f"Inventory saved successfully to {os.path.basename(INVENTORY_FILE)}.")
        else:
            print("Invalid option. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
