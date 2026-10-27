# Python style examples

Two examples apply the same principles in different ways. Take the ideas that fit
the task, not the exact dependencies or number of classes.

- `timesheet_report.py` lets established tools handle solved problems: pandas
  for tabular data and Click for the CLI. Our code owns only the input contract
  and the report.
- `order_fulfilment.py` uses classes where state and rules belong together:
  `Inventory` owns stock and reservation transitions, with no CLI, persistence
  layer or invented extension points.

The tests in `tests/` describe each example's behaviour.

## Running

Use Python 3.12 or newer. From this directory:

```bash
printf 'date,project,minutes\n2026-01-05,Website,90\n' > /tmp/sessions.csv
uv run --no-project --with click --with pandas timesheet_report.py /tmp/sessions.csv

uv venv
uv pip install click pandas pandas-stubs pytest ruff ty
source .venv/bin/activate
pytest
ruff check .
ruff format --check .
ty check .
```
