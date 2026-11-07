import argparse


def build_parser():
    parser = argparse.ArgumentParser(prog="expense-tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add")
    add_parser.add_argument("--description", required=True)
    add_parser.add_argument("--amount", required=True)

    update_parser = subparsers.add_parser("update")
    update_parser.add_argument(
        "--id", type=int, required=True, dest="expense_id"
    )
    update_parser.add_argument("--description")
    update_parser.add_argument("--amount")

    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument(
        "--id", type=int, required=True, dest="expense_id"
    )

    subparsers.add_parser("list")

    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--month", type=int, choices=range(1, 13))

    return parser


def handle_add(args):
    print("add not implemented")


def handle_update(args):
    print("update not implemented")


def handle_delete(args):
    print("delete not implemented")


def handle_list(args):
    print("list not implemented")


def handle_summary(args):
    print("summary not implemented")


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
    handlers[args.command](args)
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())