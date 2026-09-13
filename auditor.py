inventory = 0
error_count = 0

while True:
    try:
        item = input("Enter an inventory item (or type 'quit' to exit): ")
        if item.lower() == 'quit':
            print("Total Units in Inventory:", inventory, "Number of Failed/Rejected Entries:", error_count)
        quantity = int(input(f"Enter the quantity of {item}: "))
        if quantity < 0:
            print("Quantity cannot be negative. Please enter a valid number.")
            error_count += 1
            continue
        inventory += quantity
        print(f"Added {quantity} {item}(s). Total inventory: {inventory}")
    except ValueError:
        print("Please enter a valid number for quantity.")
        error_count += 1

    if inventory > 500:
        print("Warning: Inventory exceeds 500 items!")
        print("Total Units in Inventory:", inventory, "\tNumber of Failed/Rejected Entries:", error_count)
        break

    else:
        continue