"""
Aptura Tech Solution
Batch 3 Internship - Week 2
Task 1: CLI Expense Tracker

A simple command-line expense management application.
"""

import json
from pathlib import Path
from datetime import datetime


DATA_FILE = Path("expenses.json")

CATEGORIES = [
    "Food",
    "Transport",
    "Education",
    "Shopping",
    "Bills",
    "Health",
    "Entertainment",
    "Other"
]



# DATA HANDLING


def load_expenses():
    """Load expenses from the JSON file."""

    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            print("Warning: Expense file contains invalid data.")
            return []

        return data

    except json.JSONDecodeError:
        print("Warning: Expense file is corrupted.")
        return []

    except OSError as error:
        print(f"Unable to read expense file: {error}")
        return []


def save_expenses(expenses):
    """Save expenses to JSON."""

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(expenses, file, indent=4)

        return True

    except OSError as error:
        print(f"Unable to save expenses: {error}")
        return False



# INPUT VALIDATION


def get_amount():
    """Ask the user for a valid positive amount."""

    while True:

        try:
            amount = float(input("Amount: ").strip())

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            return round(amount, 2)

        except ValueError:
            print("Please enter a valid number.")


def get_date():
    """Get a valid expense date."""

    while True:

        date_text = input(
            "Date (YYYY-MM-DD) [Press Enter for today]: "
        ).strip()

        if not date_text:
            return datetime.now().strftime("%Y-%m-%d")

        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return date_text

        except ValueError:
            print("Invalid date. Example: 2026-09-01")


def choose_category():
    """Display categories and return selected category."""

    print("\nCategories:")

    for index, category in enumerate(CATEGORIES, start=1):
        print(f"{index}. {category}")

    while True:

        choice = input("Choose category: ").strip()

        if choice.isdigit():

            number = int(choice)

            if 1 <= number <= len(CATEGORIES):
                return CATEGORIES[number - 1]

        print("Please select a valid category number.")



# EXPENSE OPERATIONS


def add_expense(expenses):
    """Add a new expense."""

    print("\n" + "-" * 45)
    print("ADD NEW EXPENSE")
    print("-" * 45)

    title = input("Expense description: ").strip()

    if not title:
        print("Description cannot be empty.")
        return

    amount = get_amount()
    category = choose_category()
    date = get_date()

    expense = {
        "id": len(expenses) + 1,
        "description": title,
        "amount": amount,
        "category": category,
        "date": date
    }

    expenses.append(expense)

    if save_expenses(expenses):
        print("\n✓ Expense added successfully.")


def list_expenses(expenses):
    """Display all expenses."""

    print("\n" + "=" * 80)
    print("EXPENSE HISTORY")
    print("=" * 80)

    if not expenses:
        print("No expenses found.")
        return

    print(
        f"{'ID':<5}"
        f"{'Date':<14}"
        f"{'Description':<25}"
        f"{'Category':<18}"
        f"{'Amount':>10}"
    )

    print("-" * 80)

    for expense in expenses:

        print(
            f"{expense['id']:<5}"
            f"{expense['date']:<14}"
            f"{expense['description'][:23]:<25}"
            f"{expense['category']:<18}"
            f"Rs. {expense['amount']:>7.2f}"
        )

    print("-" * 80)

    total = sum(expense["amount"] for expense in expenses)

    print(f"{'Total':>62} Rs. {total:>7.2f}")


def search_expenses(expenses):
    """Search expenses by description."""

    print("\n" + "-" * 45)
    print("SEARCH EXPENSES")
    print("-" * 45)

    keyword = input(
        "Enter description keyword: "
    ).strip().lower()

    if not keyword:
        print("Search keyword cannot be empty.")
        return

    results = [
        expense
        for expense in expenses
        if keyword in expense["description"].lower()
    ]

    if results:
        list_expenses(results)

    else:
        print("No matching expenses found.")


def filter_by_category(expenses):
    """Filter expenses by category."""

    print("\n" + "-" * 45)
    print("CATEGORY FILTER")
    print("-" * 45)

    category = choose_category()

    results = [
        expense
        for expense in expenses
        if expense["category"] == category
    ]

    print(f"\nExpenses in category: {category}")

    if results:
        list_expenses(results)

    else:
        print("No expenses found in this category.")


def monthly_total(expenses):
    """Calculate total expenses for a selected month."""

    print("\n" + "-" * 45)
    print("MONTHLY EXPENSE TOTAL")
    print("-" * 45)

    month = input(
        "Enter month (YYYY-MM): "
    ).strip()

    try:
        datetime.strptime(month, "%Y-%m")

    except ValueError:
        print("Invalid format. Example: 2026-09")
        return

    monthly_expenses = [
        expense
        for expense in expenses
        if expense["date"].startswith(month)
    ]

    total = sum(
        expense["amount"]
        for expense in monthly_expenses
    )

    print(f"\nMonth: {month}")
    print(f"Number of expenses: {len(monthly_expenses)}")
    print(f"Monthly total: Rs. {total:.2f}")


def category_summary(expenses):
    """Show spending grouped by category."""

    print("\n" + "=" * 50)
    print("CATEGORY SUMMARY")
    print("=" * 50)

    if not expenses:
        print("No expenses available.")
        return

    totals = {}

    for expense in expenses:

        category = expense["category"]

        totals[category] = (
            totals.get(category, 0)
            + expense["amount"]
        )

    for category, amount in sorted(
        totals.items(),
        key=lambda item: item[1],
        reverse=True
    ):

        print(f"{category:<20} Rs. {amount:>10.2f}")



# MENU


def show_menu():
    """Display the main menu."""

    print("\n")
    print("=" * 55)
    print("             CLI EXPENSE TRACKER")
    print("=" * 55)

    print("1. Add Expense")
    print("2. List Expenses")
    print("3. Search Expenses")
    print("4. Filter by Category")
    print("5. Monthly Total")
    print("6. Category Summary")
    print("0. Exit")

    print("-" * 55)


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    expenses = load_expenses()

    while True:

        show_menu()

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            list_expenses(expenses)

        elif choice == "3":
            search_expenses(expenses)

        elif choice == "4":
            filter_by_category(expenses)

        elif choice == "5":
            monthly_total(expenses)

        elif choice == "6":
            category_summary(expenses)

        elif choice == "0":

            print("\nThank you for using CLI Expense Tracker!")
            print("Your expenses have been saved.")
            break

        else:
            print("\nInvalid option. Please try again.")


if __name__ == "__main__":
    main()