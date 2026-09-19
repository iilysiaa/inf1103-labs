def get_valid_input():
    """
    Prompts the user for a stock quantity.
    Returns:
        int   -> a valid, non-negative quantity
        "quit" -> if the user wants to exit
        None  -> if the entry was invalid (lets the caller count it as a failure)
    """
    entry = input("Enter a stock quantity (or type 'quit' to exit): ")
 
    if entry.lower() == "quit":
        return "quit"
 
    try:
        quantity = int(entry)
    except ValueError:
        print("Please enter a valid whole number.")
        return None
 
    if quantity < 0:
        print("Quantity cannot be negative. Please enter a valid number.")
        return None
 
    return quantity
 
 
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
    failed_attempts = 0
    deliveries_processed = 0
    total_tax_collected = 0
 
    while True:
        result = get_valid_input()
 
        if result == "quit":
            generate_report(inventory, failed_attempts)
            print("Total Tax Collected:", round(total_tax_collected, 2))
            print("Deliveries Processed (count):", deliveries_processed)
            break
 
        elif result is None:
            failed_attempts += 1
            continue
 
        else:
            inventory = process_delivery(inventory, result)
            tax = calculate_tax(result)
            total_tax_collected += tax
            deliveries_processed += 1
            print(f"Added {result} units. Tax on this delivery: {round(tax, 2)}. "
                  f"Running inventory total: {inventory}")
 
 
if __name__ == "__main__":
    main()