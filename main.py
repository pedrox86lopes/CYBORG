

import argparse
from datetime import datetime

from database import initialize_database, add_expense, delete_expense, update_expense
from cli import display_splash, display_monthly_report, display_all_expenses, display_search_results

def main():
    """Main function to run the C.Y.B.O.R.G. Expense Tracker."""
    display_splash()

    parser = argparse.ArgumentParser(
        description="C.Y.B.O.R.G. - Cybernetic Yield & Budgetary Oversight Record Gadget"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init command
    parser_init = subparsers.add_parser("init", help="Initialize the expense database.")

    # Add command
    parser_add = subparsers.add_parser("add", help="Add a new expense.")
    parser_add.add_argument("amount", type=float, help="The amount of the expense.")
    parser_add.add_argument("description", type=str, help="A brief description of the expense.")
    parser_add.add_argument("-c", "--category", type=str, default="Uncategorized", help="The category of the expense.")

    # Delete command
    parser_delete = subparsers.add_parser("delete", help="Delete an expense by its ID.")
    parser_delete.add_argument("id", type=int, help="The ID of the expense to delete.")

    # Update command
    parser_update = subparsers.add_parser("update", help="Update an existing expense.")
    parser_update.add_argument("id", type=int, help="The ID of the expense to update.")
    parser_update.add_argument("-a", "--amount", type=float, help="The new amount of the expense.")
    parser_update.add_argument("-d", "--description", type=str, help="The new description of the expense.")
    parser_update.add_argument("-c", "--category", type=str, help="The new category of the expense.")

    # Search command
    parser_search = subparsers.add_parser("search", help="Search for expenses by keyword.")
    parser_search.add_argument("keyword", type=str, help="The keyword to search for in the description.")

    # Report command
    parser_report = subparsers.add_parser("report", help="Display a report of the current month's expenses.")

    # List command
    parser_list = subparsers.add_parser("list", help="List all expenses ever recorded.")

    args = parser.parse_args()

    if args.command == "init":
        initialize_database()
    elif args.command == "add":
        add_expense(args.amount, args.description, args.category)
        print(f"\n>> Logged: €{args.amount:.2f} for '{args.description}'")
        display_monthly_report()
    elif args.command == "delete":
        delete_expense(args.id)
        print(f"\n>> Deleted expense with ID: {args.id}")
        display_all_expenses()
    elif args.command == "update":
        update_expense(args.id, args.amount, args.description, args.category)
        print(f"\n>> Updated expense with ID: {args.id}")
        display_all_expenses()
    elif args.command == "search":
        display_search_results(args.keyword)
    elif args.command == "report":
        display_monthly_report()
    elif args.command == "list":
        display_all_expenses()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

