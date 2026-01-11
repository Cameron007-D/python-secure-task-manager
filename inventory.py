"""
inventory.py

Inventory management system using OOP for shoes.
Includes class definition and full menu-driven functionality for managing stock.

Author: [Your Name]
Date: [Submission Date]
"""

import os

# File path handling to ensure portability
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INVENTORY_FILE = os.path.join(BASE_DIR, "inventory.txt")


#================ Shoe Class ================#
class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = float(cost)
        self.quantity = int(quantity)

    def get_cost(self):
        """Returns the cost of the shoe."""
        return self.cost

    def get_quantity(self):
        """Returns the quantity of the shoe."""
        return self.quantity

    def __str__(self):
        """Returns a string representation of a shoe object."""
        return (f"Product: {self.product}\n"
                f"Code: {self.code}\n"
                f"Country: {self.country}\n"
                f"Cost: R{self.cost:.2f}\n"
                f"Quantity: {self.quantity}\n")


#============= Shoe List ============#
shoe_list = []


#================ Functions ================#
def read_shoes_data():
    """Read shoes data from inventory.txt and create Shoe objects."""
    try:
        with open(INVENTORY_FILE, "r") as file:
            next(file)  # Skip header
            for line in file:
                if line.strip() == "":
                    continue
                country, code, product, cost, quantity = line.strip().split(",")
                shoe = Shoe(country, code, product, cost, quantity)
                shoe_list.append(shoe)
    except FileNotFoundError:
        print("Error: inventory.txt file not found.")
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")


def capture_shoes():
    """Allow user to capture and add a new shoe."""
    try:
        country = input("Enter country: ")
        code = input("Enter code: ")
        product = input("Enter product name: ")
        cost = float(input("Enter cost: "))
        quantity = int(input("Enter quantity: "))
    except ValueError:
        print("Error: Cost and quantity must be numbers.")
        return

    new_shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(new_shoe)

    try:
        with open(INVENTORY_FILE, "a") as file:
            file.write(f"\n{country},{code},{product},{cost},{quantity}")
        print("Shoe added successfully.")
    except IOError:
        print("Error: Could not write to file.")


def view_all():
    """Display all shoes in the inventory."""
    if not shoe_list:
        print("No shoe data available.")
        return
    print("\n=== All Shoes in Inventory ===")
    for shoe in shoe_list:
        print(shoe)


def re_stock():
    """Find the shoe with the lowest quantity and update only its line in the file."""
    if not shoe_list:
        print("No shoes to restock.")
        return

    lowest_shoe = min(shoe_list, key=lambda x: x.quantity)
    print("Lowest stock item:\n", lowest_shoe)

    try:
        amount = int(input("Enter quantity to add for restocking: "))
        lowest_shoe.quantity += amount

        # Read file lines
        with open(INVENTORY_FILE, "r") as file:
            lines = file.readlines()

        # Update the specific line (line number matches shoe_list index + 1 due to header)
        for i, shoe in enumerate(shoe_list):
            if shoe == lowest_shoe:
                line_index = i + 1
                break

        updated_line = f"{lowest_shoe.country},{lowest_shoe.code},{lowest_shoe.product},{lowest_shoe.cost},{lowest_shoe.quantity}\n"
        lines[line_index] = updated_line

        with open(INVENTORY_FILE, "w") as file:
            file.writelines(lines)

        print("Inventory updated successfully.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    except FileNotFoundError:
        print("Could not find inventory file.")
    except Exception as e:
        print(f"Unexpected error: {e}")


def search_shoe():
    """Search for a shoe by its code and print the details."""
    code = input("Enter shoe code to search: ").strip().upper()
    for shoe in shoe_list:
        if shoe.code.upper() == code:
            print("Shoe found:\n", shoe)
            return
    print("No shoe found with that code.")


def value_per_item():
    """Calculate and print total value of each shoe."""
    print("\n=== Value Per Shoe ===")
    for shoe in shoe_list:
        total_value = shoe.get_cost() * shoe.get_quantity()
        print(f"{shoe.product} ({shoe.code}) - R{total_value:.2f}")


def highest_qty():
    """Find and display the shoe with the highest quantity."""
    if not shoe_list:
        print("Inventory is empty.")
        return
    max_shoe = max(shoe_list, key=lambda x: x.quantity)
    print(f"The product with the highest quantity is '{max_shoe.product}' (FOR SALE!)")
    print(max_shoe)


#==================== Menu ====================#
read_shoes_data()

while True:
    print("\n===== Shoe Inventory Menu =====")
    print("1 - View all shoes")
    print("2 - Add a new shoe")
    print("3 - Restock lowest quantity shoe")
    print("4 - Search for a shoe by code")
    print("5 - Calculate value per item")
    print("6 - Display item with highest quantity (for sale)")
    print("7 - Exit")

    choice = input("Enter your choice (1-7): ")

    if choice == "1":
        view_all()
    elif choice == "2":
        capture_shoes()
    elif choice == "3":
        re_stock()
    elif choice == "4":
        search_shoe()
    elif choice == "5":
        value_per_item()
    elif choice == "6":
        highest_qty()
    elif choice == "7":
        print("Exiting program. Goodbye!")
        break
    else:
        print("Invalid option. Please choose between 1 and 7.")
