from datetime import date

from .errors import UserError


def _find_expense(expenses, expense_id):
    for expense in expenses:
        if expense["id"] == expense_id:
            return expense
    raise UserError(f"no expense with ID {expense_id}")


def _valid_description(description):
    if description is None:
        raise UserError("description cannot be empty")
    description = description.strip()
    if not description:
        raise UserError("description cannot be empty")
    return description


def next_id(expenses):
    return max((expense["id"] for expense in expenses), default=0) + 1


def add_expense(expenses, description, amount_cents):
    if not isinstance(amount_cents, int) or amount_cents <= 0:
        raise UserError("amount must be greater than zero")
    return {
        "id": next_id(expenses),
        "date": date.today().isoformat(),
        "description": _valid_description(description),
        "amount": amount_cents,
    }


def update_expense(expenses, expense_id, description=None, amount_cents=None):
    if description is None and amount_cents is None:
        raise UserError("update requires --description or --amount")

    expense = _find_expense(expenses, expense_id)
    if description is not None:
        expense["description"] = _valid_description(description)
    if amount_cents is not None:
        if not isinstance(amount_cents, int) or amount_cents <= 0:
            raise UserError("amount must be greater than zero")
        expense["amount"] = amount_cents
    return expense


def delete_expense(expenses, expense_id):
    expense = _find_expense(expenses, expense_id)
    expenses.remove(expense)
    return expense


def list_expenses(expenses):
    return sorted(expenses, key=lambda expense: expense["id"])


def summary_expenses(expenses, month=None):
    if month is None:
        return sum(expense["amount"] for expense in expenses)

    if isinstance(month, int) and not 1 <= month <= 12:
        raise UserError("month must be between 1 and 12")

    total = 0
    for expense in expenses:
        expense_month = date.fromisoformat(expense["date"]).month
        if expense_month == month:
            total += expense["amount"]
    return total
