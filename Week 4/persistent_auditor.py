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

    print(f"Loaded {len(inventory)} item(s) from {filename}.")
    return inventory


def save_inventory(inventory, filename=INVENTORY_FILE):
    """Writes the inventory dictionary to the file, one 'item,quantity' per line."""
    try:
        with open(filename, "w") as file:
            for item, quantity in inventory.items():
                file.write(f"{item},{quantity}\n")
    except OSError:
        print("Warning: could not save inventory to file.")


def get_valid_input():
    """
    Prompts the user for an item name and a stock quantity.
    Returns:
        (item, quantity) -> a valid item name and non-negative quantity
        "quit"           -> if the user wants to exit
        None             -> if the quantity entered was invalid (so the caller can count it as a failure)
    """
    item = input("Enter an inventory item (or type 'quit' to exit): ")

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


def main():
    items = load_inventory()              # previously saved stock, per item
    inventory = sum(items.values())       # running total starts from saved stock
    error_count = 0
    deliveries_processed = 0

    print(f"Current total inventory: {inventory}")

    while True:
        result = get_valid_input()

        if result == "quit":
            save_inventory(items)
            generate_report(inventory, error_count)
            break

        elif result is None:
            error_count += 1
            continue

        else:
            item, quantity = result
            tax = calculate_tax(quantity)
            inventory = process_delivery(inventory, quantity)
            items[item] = process_delivery(items.get(item, 0), quantity)
            deliveries_processed += 1
            save_inventory(items)         # save after every delivery so nothing is lost
            print(f"Added {quantity} {item}(s). Tax on this delivery: {round(tax, 2)}. "
                  f"Total inventory: {inventory}")

        if inventory > 500:
            print("Warning: Inventory exceeds 500 items!")
            generate_report(inventory, error_count)
            break


if __name__ == "__main__":
    main()