class ExpenseTrackerError(Exception):
    """Base class for expected expense tracker errors."""


class UserError(ExpenseTrackerError):
    """Raised when user-provided data is invalid."""


class DataError(ExpenseTrackerError):
    """Raised when persisted expense data cannot be loaded or saved."""
