"""Mock MCP model endpoints backed by the SQLite model."""

from __future__ import annotations

import json
from typing import Any

from tenacity import retry, stop_after_attempt, wait_exponential

from models.database import query_rows


@retry(wait=wait_exponential(multiplier=0.2, min=0.2, max=2), stop=stop_after_attempt(3), reraise=True)
def _query_with_retry(sql: str, parameters: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    return query_rows(sql, parameters)


def accounts_mcp(query: str) -> str:
    """Mock Accounts MCP endpoint for balances, types, and profiles."""
    rows = _query_with_retry(
        """SELECT account_id, customer_name, account_type, balance, currency, branch, opened_on
        FROM accounts WHERE user_id = ? OR account_id = ? ORDER BY account_id""",
        ("DEMO-USER-001", query.strip()),
    )
    return _format_rows(rows, "No account matched the demo user or supplied account id.")


def transactions_mcp(query: str) -> str:
    """Mock Transactions MCP endpoint for history and spending analysis."""
    rows = _query_with_retry(
        """SELECT t.transaction_date, t.account_id, t.description, t.category,
        t.amount, t.transaction_type FROM transactions t JOIN accounts a
        ON a.account_id = t.account_id WHERE a.user_id = ? OR a.account_id = ?
        ORDER BY t.transaction_date DESC""",
        ("DEMO-USER-001", query.strip()),
    )
    return _format_rows(rows, "No transactions matched the demo user or supplied account id.")


def services_mcp(query: str) -> str:
    """Mock Services MCP endpoint for address, cheque book, and KYC requests."""
    rows = _query_with_retry(
        """SELECT request_id, request_type, details, status, created_at
        FROM service_requests WHERE user_id = ? OR request_type LIKE ?
        ORDER BY created_at DESC""",
        ("DEMO-USER-001", f"%{query.strip()}%"),
    )
    return _format_rows(rows, "No service requests matched the demo user or request type.")


def _format_rows(rows: list[dict[str, Any]], empty_message: str) -> str:
    if not rows:
        return json.dumps({"count": 0, "records": [], "message": empty_message})
    return json.dumps({"count": len(rows), "records": rows}, default=str)
