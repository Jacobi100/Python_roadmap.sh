import argparse
import sys

from .errors import DataError, UserError
from .models import format_amount, parse_amount
from .operations import add_expense, delete_expense, list_expenses, summary_expenses, update_expense
from .storage import load_expenses, save_expenses


def build_parser():
    parser = argparse.ArgumentParser(
        prog="expense-tracker",
        description="Track and summarize expenses from the command line.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="add a new expense")
    add_parser.add_argument("--description", required=True, help="expense description")
    add_parser.add_argument("--amount", required=True, help="amount, for example 20 or 12.50")

    update_parser = subparsers.add_parser("update", help="update an existing expense")
    update_parser.add_argument(
        "--id", type=int, required=True, dest="expense_id", help="expense ID"
    )
    update_parser.add_argument("--description", help="new expense description")
    update_parser.add_argument("--amount", help="new amount, for example 20 or 12.50")

    delete_parser = subparsers.add_parser("delete", help="delete an expense")
    delete_parser.add_argument(
        "--id", type=int, required=True, dest="expense_id", help="expense ID"
    )

    subparsers.add_parser("list", help="list all expenses")

    summary_parser = subparsers.add_parser("summary", help="show expense totals")
    summary_parser.add_argument(
        "--month", type=int, choices=range(1, 13), metavar="MONTH",
        help="optional month number (1-12)",
    )

    return parser


def handle_add(args):
    expenses = load_expenses()
    expense = add_expense(
        expenses,
        args.description,
        parse_amount(args.amount),
    )
    expenses.append(expense)
    save_expenses(expenses)
    print(f"Expense added successfully (ID: {expense['id']})")


def handle_update(args):
    description = args.description
    amount = parse_amount(args.amount) if args.amount is not None else None
    expenses = load_expenses()
    update_expense(expenses, args.expense_id, description, amount)
    save_expenses(expenses)
    print(f"Expense updated successfully (ID: {args.expense_id})")


def handle_delete(args):
    expenses = load_expenses()
    delete_expense(expenses, args.expense_id)
    save_expenses(expenses)
    print(f"Expense deleted successfully (ID: {args.expense_id})")


def handle_list(args):
    expenses = list_expenses(load_expenses())
    print(f"{'ID':<5} {'Date':<12} {'Description':<30} Amount")
    print(f"{'--':<5} {'----':<12} {'-----------':<30} ------")
    for expense in expenses:
        print(
            f"{expense['id']:<5} {expense['date']:<12} "
            f"{expense['description']:<30} {format_amount(expense['amount'])}"
        )


def handle_summary(args):
    total = summary_expenses(load_expenses(), args.month)
    if args.month is None:
        print(f"Total expenses: {format_amount(total)}")
    else:
        print(f"Total expenses for month {args.month}: {format_amount(total)}")


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "update":
        if args.description is None and args.amount is None:
            parser.error("update requires --description or --amount")

    handlers = {
        "add": handle_add,
        "update": handle_update,
        "delete": handle_delete,
        "list": handle_list,
        "summary": handle_summary,
    }
    try:
        handlers[args.command](args)
    except (UserError, DataError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())


def run():
    sys.exit(main())