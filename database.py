
import sqlite3
import os
from datetime import datetime

DB_FILE = "expenses.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """Initializes the database and creates the expenses table if it doesn't exist."""
    if os.path.exists(DB_FILE):
        print("Database already initialized.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        description TEXT NOT NULL,
        category TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()
    print("C.Y.B.O.R.G. database initialized successfully.")

def add_expense(amount, description, category):
    """Adds a new expense to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (amount, description, category) VALUES (?, ?, ?)",
        (amount, description, category)
    )
    conn.commit()
    conn.close()

def delete_expense(expense_id):
    """Deletes an expense from the database by its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

def update_expense(expense_id, amount=None, description=None, category=None):
    """Updates an expense in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    fields_to_update = []
    params = []

    if amount is not None:
        fields_to_update.append("amount = ?")
        params.append(amount)
    if description is not None:
        fields_to_update.append("description = ?")
        params.append(description)
    if category is not None:
        fields_to_update.append("category = ?")
        params.append(category)

    if not fields_to_update:
        print("No fields to update.")
        return

    params.append(expense_id)
    query = f"UPDATE expenses SET {', '.join(fields_to_update)} WHERE id = ?"

    cursor.execute(query, tuple(params))
    conn.commit()
    conn.close()

def search_expenses(keyword):
    """Searches for expenses by keyword in the description."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, amount, description, category, timestamp FROM expenses WHERE description LIKE ? ORDER BY timestamp DESC",
        (f"%{keyword}%",)
    )
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def get_monthly_expenses(month, year):
    """Retrierives all expenses for a given month and year."""
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, amount, description, category, timestamp FROM expenses WHERE timestamp >= ? AND timestamp < ?",
        (start_date, end_date)
    )
    expenses = cursor.fetchall()
    conn.close()
    return expenses

def get_all_expenses():
    """Retrieves all expenses from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, amount, description, category, timestamp FROM expenses ORDER BY timestamp DESC")
    expenses = cursor.fetchall()
    conn.close()
    return expenses
