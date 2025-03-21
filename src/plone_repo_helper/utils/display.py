from rich import print  # noQA: A004
from rich.table import Table


__all__ = ["print", "table"]


def table(title: str, columns: list[dict], rows: list) -> Table:
    table = Table(title=title)
    for column in columns:
        table.add_column(**column)
    for row in rows:
        table.add_row(*row)
    return table
