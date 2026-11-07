# Expense Tracker CLI

A command-line expense tracker built with Python's standard library. This project
implements the [Expense Tracker project on roadmap.sh](https://roadmap.sh/projects/expense-tracker).

Expenses are stored as JSON in `~/.expense_tracker.json`. For isolated testing or
a custom location, set the `EXPENSE_TRACKER_FILE` environment variable.

## Features

- Add expenses with a description and amount
- Update expense descriptions or amounts
- Delete expenses by ID
- List all expenses
- Summarize all expenses or one calendar month
- Validate input and negative or malformed amounts
- Store amounts as integer cents to avoid floating-point rounding errors
- Atomically save JSON data
## Run from source

From this directory:

```bash
python -m expense_tracker add --description "Lunch" --amount 20
python -m expense_tracker list
python -m expense_tracker update --id 1 --amount 12.50
python -m expense_tracker summary
python -m expense_tracker summary --month 11
python -m expense_tracker delete --id 1
```

## Install commands

From the `backend_projects` directory:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
expense-tracker --help
tracker list
```

Both console commands invoke the same application.

## Command reference

### Add an expense

```bash
expense-tracker add --description "Lunch" --amount 20
```

Amounts accept positive whole or two-decimal values such as `20`, `20.50`, or
`0.99`. The JSON representation stores the amount as cents.

### Update an expense

At least one option is required:

```bash
expense-tracker update --id 1 --description "Dinner"
expense-tracker update --id 1 --amount 25.75
expense-tracker update --id 1 --description "Dinner" --amount 25.75
```

### Delete an expense

```bash
expense-tracker delete --id 1
```

### List expenses

```bash
expense-tracker list
```

The table includes the expense ID, date, description, and amount.

### Show a summary

```bash
expense-tracker summary
expense-tracker summary --month 11
```

Months are numbered from 1 (January) through 12 (December).

## Custom storage location

```bash
EXPENSE_TRACKER_FILE="$PWD/expenses.json" expense-tracker list
```

On first use, the application creates the JSON file. Missing data is treated as
an empty expense list.

## Exit codes

- `0`: command completed successfully
- `1`: application or data error
- `2`: invalid command-line arguments

## Project submission

[Expense Tracker project specification and submission](https://roadmap.sh/projects/expense-tracker)
