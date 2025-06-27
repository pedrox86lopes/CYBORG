

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from datetime import datetime

from database import get_monthly_expenses, get_all_expenses, search_expenses

console = Console()

def display_splash():
    """Displays the ASCII art splash screen."""
    splash_text = Text("""
    ██████╗ ██╗   ██╗██████╗  ██████╗ ██████╗  ██████╗
    ██╔════╝ ██║   ██║██╔══██╗██╔═══██╗██╔══██╗██╔════╝
    ██║      ██║   ██║██████╔╝██║   ██║██████╔╝██║  ███╗
    ██║      ██║   ██║██╔══██╗██║   ██║██╔══██╗██║   ██║
    ╚██████╗ ╚██████╔╝██████╔╝╚██████╔╝██║  ██║╚██████╔╝
     ╚═════╝  ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝
    Cybernetic Yield & Budgetary Oversight Record Gadget
    """, style="bold cyan")
    console.print(Panel(splash_text, border_style="green"))

def display_monthly_report():
    """Displays a formatted table of the current month's expenses."""
    now = datetime.now()
    expenses = get_monthly_expenses(now.month, now.year)

    if not expenses:
        console.print(Text("\n>> No transactions recorded for this fiscal period.", style="yellow"))
        return

    table = Table(title=f"Fiscal Report: {now.strftime('%B %Y')}", style="cyan")
    table.add_column("ID", style="dim cyan")
    table.add_column("Date", style="magenta")
    table.add_column("Description", style="white")
    table.add_column("Category", style="yellow")
    table.add_column("Amount", justify="right", style="green")

    category_totals = {}
    total_spend = 0

    for expense in expenses:
        table.add_row(
            str(expense['id']),
            datetime.strptime(expense['timestamp'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'),
            expense['description'],
            expense['category'],
            f"€{expense['amount']:.2f}"
        )
        category_totals[expense['category']] = category_totals.get(expense['category'], 0) + expense['amount']
        total_spend += expense['amount']

    console.print(table)

    # Display category summaries
    summary_table = Table(title="Category Summary", style="cyan", show_header=True, header_style="bold cyan")
    summary_table.add_column("Category", style="yellow")
    summary_table.add_column("Total Spent", justify="right", style="green")
    for category, total in sorted(category_totals.items()):
        summary_table.add_row(category, f"€{total:.2f}")

    console.print(summary_table)
    console.print(Panel(Text(f"Total Monthly Expenditure: €{total_spend:.2f}", justify="right"), style="bold red"))

def display_all_expenses():
    """Displays a formatted table of all expenses."""
    expenses = get_all_expenses()
    if not expenses:
        console.print(Text("\n>> No transactions in the databanks.", style="yellow"))
        return

    table = Table(title="Complete Transaction History", style="cyan")
    table.add_column("ID", style="dim cyan")
    table.add_column("Date", style="magenta")
    table.add_column("Description", style="white")
    table.add_column("Category", style="yellow")
    table.add_column("Amount", justify="right", style="green")

    for expense in expenses:
        table.add_row(
            str(expense['id']),
            datetime.strptime(expense['timestamp'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'),
            expense['description'],
            expense['category'],
            f"€{expense['amount']:.2f}"
        )

    console.print(table)

def display_search_results(keyword):
    """Displays a formatted table of search results."""
    expenses = search_expenses(keyword)
    if not expenses:
        console.print(Text(f"\n>> No transactions found matching '{keyword}'.", style="yellow"))
        return

    table = Table(title=f"Search Results for '{keyword}'")
    table.add_column("ID", style="dim cyan")
    table.add_column("Date", style="magenta")
    table.add_column("Description", style="white")
    table.add_column("Category", style="yellow")
    table.add_column("Amount", justify="right", style="green")

    for expense in expenses:
        table.add_row(
            str(expense['id']),
            datetime.strptime(expense['timestamp'], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d'),
            expense['description'],
            expense['category'],
            f"€{expense['amount']:.2f}"
        )

    console.print(table)

