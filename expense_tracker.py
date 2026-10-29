import sys
import os
import json
from datetime import datetime
import argparse
import calendar

EXPENSES_FILE = "expenses.json"

def load_expense():
    if not os.path.exists(EXPENSES_FILE):
        return []

    with open(EXPENSES_FILE, 'r', encoding= "utf-8") as f:
        return json.load(f)

def save_expense(expenses):

    with open(EXPENSES_FILE,"w", encoding="utf-8") as f:
        json.dump(expenses,f,indent=4)

def add_expense(amount, description):

    expenses = load_expense()
    if expenses:
        ids = []
        for expense in expenses:
            ids.append(expense["id"])
        biggest_id = max(ids)
        new_id = biggest_id + 1
    else:
        new_id = 1

    now = datetime.now().date().isoformat()

    new_expense = {
        "id": new_id,
        "description": description,
        "amount": amount,
        "date" : now,
    }

    expenses.append(new_expense)
    save_expense(expenses)
    print(f"Expense added successfully (ID: {new_id}) ")



def list_expenses():

    expenses = load_expense()

    if expenses:
        print(f"{'ID':<4}{'Date':<12}{'Description':<15}{'Amount'}")
        for expense in expenses:
            print(f"{expense['id']:<4}{expense['date']:<12}{expense['description']:<15}${expense['amount']:.2f}")
    else:
        print(f"No expenses found.")


def summary_list(month=None):
    expenses = load_expense()
    current_year = datetime.now().year
    total = 0

    for expense in expenses:
        parts = expense["date"].split("-")
        expense_year = int(parts[0])
        expense_month = int(parts[1])

        if month is None:
            total += expense["amount"]
        elif expense_year == current_year and expense_month == month:
            total += expense["amount"]

    if month is None:
        print(f"Total expenses: ${total:.2f}")
    else:
        print(f"Total expenses for {calendar.month_name[month]}: ${total:.2f}")


def main():
   
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description", required=True)
    add_parser.add_argument("--amount", type=float, required=True)

    list_parser = subparsers.add_parser("list")

    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--month",type=int ,choices=range(1, 13))

    args = parser.parse_args()
    if args.command == "add":
        if args.amount <= 0:
           print("Error: amount must be greater than 0")
        else:
            add_expense(args.amount, args.description)

    elif args.command == "list":
        list_expenses()

    elif args.command == "summary":
        summary_list(args.month)

    else:
        parser.print_help()

    


if __name__ == "__main__":
    main()
