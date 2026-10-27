"""Report time spent per project, using pandas for tables and Click for the CLI.

Run with: python timesheet_report.py sessions.csv --since 2026-01-01
Input: a CSV with date,project,minutes columns. Dates use YYYY-MM-DD; minutes
are whole numbers from 1 to 1440 (one day).
"""

from datetime import datetime
from pathlib import Path

import click
import pandas as pd

MINUTES_PER_DAY = 1440


def read_sessions(source: Path) -> pd.DataFrame:
    """Load a timesheet, rejecting it if any row has an invalid field.

    Raises:
        ValueError: The CSV is malformed, has the wrong columns or invalid rows.
    """
    # Keep every field as text, so a project named "NA" is not read as missing.
    sessions = pd.read_csv(source, dtype="string", keep_default_na=False)
    if list(sessions.columns) != ["date", "project", "minutes"]:
        raise ValueError("expected columns: date,project,minutes")
    # pandas silently shifts the columns into the index when rows have extra fields.
    if not isinstance(sessions.index, pd.RangeIndex):
        raise ValueError("each row must contain exactly three fields")

    dates = pd.to_datetime(sessions["date"], format="%Y-%m-%d", errors="coerce")
    minutes = pd.to_numeric(sessions["minutes"], errors="coerce")
    valid_rows = (
        dates.notna()
        & (sessions["project"] != "")
        & sessions["minutes"].str.fullmatch(r"[0-9]+")
        & minutes.between(1, MINUTES_PER_DAY)
    )
    if not valid_rows.all():
        row_numbers = ", ".join(str(index + 1) for index in sessions.index[~valid_rows])
        raise ValueError(f"invalid date, project or minutes in row(s): {row_numbers}")

    return sessions.assign(date=dates, minutes=minutes.astype("int64"))


def summarise_projects(
    sessions: pd.DataFrame,
    *,
    since: datetime | None = None,
    until: datetime | None = None,
) -> pd.DataFrame:
    """Total the minutes and sessions per project within inclusive date bounds.

    Returns:
        Project, minutes and sessions columns, ordered by decreasing time and
        then project name.
    """
    selected = sessions
    if since is not None:
        selected = selected.loc[selected["date"] >= since]
    if until is not None:
        selected = selected.loc[selected["date"] <= until]

    return (
        selected.groupby("project", as_index=False)
        .agg(minutes=("minutes", "sum"), sessions=("minutes", "size"))
        .sort_values(["minutes", "project"], ascending=[False, True], ignore_index=True)
    )


def render_report(totals: pd.DataFrame) -> str:
    """Format a project summary as a text table with a grand total."""
    if totals.empty:
        return "No work sessions in the selected period."

    table = totals.assign(hours=(totals["minutes"] / 60).round(2))
    total_minutes = int(totals["minutes"].sum())
    total_sessions = int(totals["sessions"].sum())
    return (
        table[["project", "hours", "sessions"]].to_string(index=False)
        + f"\n\nTotal: {total_minutes / 60:.2f} hours ({total_sessions} sessions)"
    )


@click.command()
@click.argument("source", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--since", type=click.DateTime(formats=["%Y-%m-%d"]), help="First date.")
@click.option("--until", type=click.DateTime(formats=["%Y-%m-%d"]), help="Last date.")
def main(source: Path, since: datetime | None, until: datetime | None) -> None:
    """Print a report of time spent per project in a CSV timesheet."""
    if since is not None and until is not None and since > until:
        raise click.UsageError("--since must be on or before --until")
    try:
        sessions = read_sessions(source)
    except (OSError, ValueError) as error:
        raise click.ClickException(str(error)) from error

    click.echo(render_report(summarise_projects(sessions, since=since, until=until)))


if __name__ == "__main__":
    main()
