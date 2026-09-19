def get_valid_input():
    """
    Prompts the user to enter a stock quantity.
    Returns:
        int    -> a valid, non-negative quantity
        "quit" -> if the user wants to exit
        None   -> if the entry was invalid (so the caller can count it as a failure)
    """
    try:
        entry = input("Enter a stock quantity (or type 'quit' to exit): ")

        if entry.lower() == 'quit':
            return "quit"

        quantity = int(entry)

        if quantity < 0:
            print("Quantity cannot be negative. Please enter a valid number.")
            return None

        return quantity

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
    inventory = 0
    error_count = 0
    deliveries_processed = 0

    while True:
        result = get_valid_input()

        if result == "quit":
            generate_report(inventory, error_count)
            break

        elif result is None:
            error_count += 1
            continue

        else:
            tax = calculate_tax(result)
            inventory = process_delivery(inventory, result)
            deliveries_processed += 1
            print(f"Added {result} units. Tax on this delivery: {round(tax, 2)}. "
                  f"Total inventory: {inventory}")

        if inventory > 500:
            print("Warning: Inventory exceeds 500 items!")
            generate_report(inventory, error_count)
            break


if __name__ == "__main__":
    main()