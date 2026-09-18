inventory = 0
error_count = 0
deliveries_processed = 0


def get_valid_input():
    while True:
        try:
            quantity = input("Enter the stock quantity (or type 'quit' to exit): ")

            if quantity.lower() == "quit":
                return "quit"

            quantity = int(quantity)

            if quantity < 0:
                print("Quantity cannot be negative.")
                return None

            return quantity

        except ValueError:
            print("Please enter a valid number.")
            return None


def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total


def calculate_tax(amount):
    tax = amount * 0.10
    return tax


def generate_report(total_units, failed_attempts):
    print("Total Units in Inventory:", total_units)
    print("Total Deliveries Processed:", deliveries_processed)
    print("Number of Failed/Rejected Entries:", failed_attempts)


while True:
    quantity = get_valid_input()

    if quantity == "quit":
        generate_report(inventory, error_count)
        break

    if quantity is None:
        error_count += 1
        continue

    inventory = process_delivery(inventory, quantity)

    tax = calculate_tax(quantity)

    deliveries_processed += 1

    print(f"Added {quantity} units.")
    print(f"Tax for this delivery: ${tax:.2f}")
    print(f"Total inventory: {inventory}")

    if inventory > 500:
        print("Warning: Inventory exceeds 500 items!")
        generate_report(inventory, error_count)
        break