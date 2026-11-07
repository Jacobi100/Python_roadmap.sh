import re
from decimal import Decimal, InvalidOperation

from .errors import UserError


AMOUNT_PATTERN = re.compile(r"^\d+(?:\.\d{1,2})?$")


def parse_amount(text):
    """Convert a decimal amount string to integer cents."""
    if text is None or not AMOUNT_PATTERN.fullmatch(str(text).strip()):
        raise UserError("amount must be a positive number with at most 2 decimal places")

    try:
        amount = Decimal(str(text).strip())
    except InvalidOperation as error:
        raise UserError("amount must be a valid number") from error

    if amount <= 0:
        raise UserError("amount must be greater than zero")
    return int(amount * 100)


def format_amount(cents):
    """Format integer cents as a dollar amount."""
    return f"${cents / 100:.2f}"
