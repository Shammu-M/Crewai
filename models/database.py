"""SQLite model and deterministic demo-data initialization."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parent.parent / "bank_data.db"


def initialize_database(db_path: Path = DB_PATH) -> None:
    """Create the synthesized banking database on startup."""
    with sqlite3.connect(db_path) as connection:
        connection.executescript(
            """
            DROP TABLE IF EXISTS accounts;
            DROP TABLE IF EXISTS transactions;
            DROP TABLE IF EXISTS service_requests;
            CREATE TABLE accounts (
                account_id TEXT PRIMARY KEY, user_id TEXT NOT NULL,
                customer_name TEXT NOT NULL, account_type TEXT NOT NULL,
                balance REAL NOT NULL, currency TEXT NOT NULL, branch TEXT NOT NULL,
                opened_on TEXT NOT NULL
            );
            CREATE TABLE transactions (
                transaction_id INTEGER PRIMARY KEY, account_id TEXT NOT NULL,
                transaction_date TEXT NOT NULL, description TEXT NOT NULL,
                category TEXT NOT NULL, amount REAL NOT NULL,
                transaction_type TEXT NOT NULL,
                FOREIGN KEY (account_id) REFERENCES accounts(account_id)
            );
            CREATE TABLE service_requests (
                request_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL,
                request_type TEXT NOT NULL, details TEXT NOT NULL,
                status TEXT NOT NULL, created_at TEXT NOT NULL
            );
            """
        )
        connection.executemany(
            "INSERT INTO accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [
                ("ACCT-1001", "DEMO-USER-001", "Jordan Lee", "Checking", 4250.75, "USD", "Downtown", "2021-04-12"),
                ("ACCT-1002", "DEMO-USER-001", "Jordan Lee", "Savings", 12800.00, "USD", "Downtown", "2022-09-03"),
                ("ACCT-1003", "DEMO-USER-002", "Avery Smith", "Checking", 1890.40, "USD", "Riverside", "2020-11-28"),
                ("ACCT-1004", "DEMO-USER-003", "Casey Brown", "Credit", -340.15, "USD", "Northside", "2023-02-14"),
                ("ACCT-1005", "DEMO-USER-004", "Morgan Patel", "Checking", 765.20, "USD", "Lakeside", "2024-01-19"),
                ("ACCT-1006", "DEMO-USER-005", "Taylor Chen", "Savings", 22150.90, "USD", "Market Street", "2019-07-07"),
            ],
        )
        connection.executemany(
            """INSERT INTO transactions
            (transaction_id, account_id, transaction_date, description, category, amount, transaction_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                (1, "ACCT-1001", "2026-08-29", "Payroll deposit", "Income", 3200.00, "credit"),
                (2, "ACCT-1001", "2026-08-30", "Green Market", "Groceries", -86.42, "debit"),
                (3, "ACCT-1001", "2026-09-01", "Metro Utilities", "Bills", -142.18, "debit"),
                (4, "ACCT-1001", "2026-09-04", "Harbor Coffee", "Dining", -12.75, "debit"),
                (5, "ACCT-1002", "2026-08-15", "Interest payment", "Interest", 18.70, "credit"),
                (6, "ACCT-1002", "2026-08-20", "Rent transfer", "Housing", -1200.00, "debit"),
                (7, "ACCT-1003", "2026-08-27", "Bookstore", "Shopping", -54.99, "debit"),
                (8, "ACCT-1005", "2026-09-02", "Fuel station", "Transport", -48.30, "debit"),
                (9, "ACCT-1006", "2026-08-31", "Investment transfer", "Savings", 500.00, "credit"),
            ],
        )
        connection.executemany(
            """INSERT INTO service_requests
            (user_id, request_type, details, status, created_at)
            VALUES (?, ?, ?, ?, ?)""",
            [
                ("DEMO-USER-001", "KYC update", "Phone number verification", "Open", "2026-08-18"),
                ("DEMO-USER-001", "Cheque book", "Standard 25-leaf cheque book", "Completed", "2026-07-21"),
                ("DEMO-USER-002", "Address change", "Moved to 18 River Lane", "In review", "2026-09-01"),
                ("DEMO-USER-003", "KYC update", "Tax residency document", "Open", "2026-08-30"),
                ("DEMO-USER-004", "Cheque book", "Urgent delivery requested", "Open", "2026-08-25"),
            ],
        )


def query_rows(sql: str, parameters: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    with sqlite3.connect(DB_PATH) as connection:
        connection.row_factory = sqlite3.Row
        return [dict(row) for row in connection.execute(sql, parameters).fetchall()]
