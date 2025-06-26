

import argparse
from datetime import datetime

from database import initialize_database, add_expense
from cli import display_splash, display_monthly_report, display_all_expenses

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
    elif args.command == "report":
        display_monthly_report()
    elif args.command == "list":
        display_all_expenses()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

