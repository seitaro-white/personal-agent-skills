"""Check the practical example's data contracts and user-visible CLI behaviour."""

from datetime import datetime
from pathlib import Path

import pandas as pd
import pytest
from click.testing import CliRunner

from timesheet_report import main, read_sessions, render_report, summarise_projects


@pytest.fixture
def source(tmp_path: Path) -> Path:
    path = tmp_path / "sessions.csv"
    path.write_text(
        "date,project,minutes\n"
        "2026-01-05,Website,90\n"
        "2026-01-06,Documentation,45\n"
        "2026-01-07,Website,30\n"
    )
    return path


def test_summary_groups_projects_without_changing_input(source: Path) -> None:
    sessions = read_sessions(source)
    original = sessions.copy(deep=True)

    summary = summarise_projects(sessions)

    assert summary.to_dict("records") == [
        {"project": "Website", "minutes": 120, "sessions": 2},
        {"project": "Documentation", "minutes": 45, "sessions": 1},
    ]
    pd.testing.assert_frame_equal(sessions, original)


def test_date_bounds_are_inclusive(source: Path) -> None:
    summary = summarise_projects(
        read_sessions(source), since=datetime(2026, 1, 6), until=datetime(2026, 1, 7)
    )

    assert summary["minutes"].sum() == 75
    assert summary["sessions"].sum() == 2


def test_equal_totals_sort_by_project_name(source: Path) -> None:
    source.write_text(
        "date,project,minutes\n2026-01-05,Zebra,30\n2026-01-05,Alpha,30\n"
    )

    summary = summarise_projects(read_sessions(source))

    assert summary["project"].tolist() == ["Alpha", "Zebra"]


def test_project_named_na_is_not_missing_data(source: Path) -> None:
    source.write_text("date,project,minutes\n2026-01-05,NA,20\n")

    summary = summarise_projects(read_sessions(source))

    assert summary.to_dict("records") == [
        {"project": "NA", "minutes": 20, "sessions": 1}
    ]


@pytest.mark.parametrize(
    "row",
    [
        "2026-02-30,Website,30",
        "2026-01-05,,30",
        "2026-01-05,Website,0",
        "2026-01-05,Website,1.5",
        "2026-01-05,Website,1441",
        "2026-01-05,Website",
        "2026-01-05,Website,30,extra",
    ],
    ids=[
        "impossible-date",
        "empty-project",
        "zero-minutes",
        "fractional-minutes",
        "over-one-day",
        "missing-field",
        "extra-field",
    ],
)
def test_invalid_rows_are_rejected_before_filtering(source: Path, row: str) -> None:
    source.write_text("date,project,minutes\n" + row + "\n")

    result = CliRunner().invoke(main, [str(source), "--since", "2027-01-01"])

    assert result.exit_code == 1
    assert "Error:" in result.stderr
    assert "Traceback" not in result.stderr


@pytest.mark.parametrize("content", ["", "project,date,minutes\n"])
def test_empty_or_wrong_header_is_rejected(source: Path, content: str) -> None:
    source.write_text(content)

    with pytest.raises(ValueError):
        read_sessions(source)


def test_no_matching_sessions_gives_an_empty_report(source: Path) -> None:
    summary = summarise_projects(read_sessions(source), since=datetime(2027, 1, 1))

    assert render_report(summary) == "No work sessions in the selected period."


def test_cli_prints_the_report(source: Path) -> None:
    result = CliRunner().invoke(main, [str(source)])

    assert result.exit_code == 0
    assert "Total: 2.75 hours (3 sessions)" in result.stdout


@pytest.mark.parametrize(
    "arguments",
    [
        ["--since", "not-a-date"],
        ["--since", "2026-02-01", "--until", "2026-01-01"],
    ],
)
def test_cli_rejects_invalid_date_options(source: Path, arguments: list[str]) -> None:
    result = CliRunner().invoke(main, [str(source), *arguments])

    assert result.exit_code == 2
    assert "Error:" in result.stderr
