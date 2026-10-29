import sys
import os
import json
from datetime import datetime
import argparse

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


def main():
   
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description", required=True)
    add_parser.add_argument("--amount", type=float, required=True)

    list_parser = subparsers.add_parser("list")



    args = parser.parse_args()
    if args.command == "add":
        if args.amount <= 0:
           print("Error: amount must be greater than 0")
        else:
            add_expense(args.amount, args.description)

    elif args.command == "list":
        list_expenses()

    else:
        parser.print_help()

    


if __name__ == "__main__":
    main()
