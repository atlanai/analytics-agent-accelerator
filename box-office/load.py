"""Build the box office's SQLite database from its CSVs: python box-office/load.py  (standard library only).

Writes box-office/tix.sqlite with the eight tix tables. Column types are inferred from the CSVs:
whole numbers become INTEGER, other numbers REAL, everything else (dates and timestamps included)
TEXT. Identifier columns (`*_id`) stay TEXT. The query history stays in history/query_history.jsonl;
q.py loads it on each run.
"""
import csv
import pathlib
import sqlite3

HERE = pathlib.Path(__file__).resolve().parent
DB = HERE / "tix.sqlite"  # the file name is the schema name: tix.events, tix.orders, ...
TABLES = ("venues", "artists", "events", "fee_schedule", "customers", "orders", "tickets", "refunds")


def column_type(name, values) -> str:
    if name.endswith("_id"):
        return "TEXT"
    for kind, cast in (("INTEGER", int), ("REAL", float)):
        try:
            [cast(v) for v in values if v != ""]
            return kind
        except ValueError:
            pass
    return "TEXT"


if DB.exists():
    DB.unlink()
con = sqlite3.connect(DB)
for t in TABLES:
    with (HERE / "data" / f"{t}.csv").open(newline="") as f:
        header, *rows = list(csv.reader(f))
    types = [column_type(h, [r[i] for r in rows]) for i, h in enumerate(header)]
    con.execute(f'CREATE TABLE "{t}" (' + ", ".join(f'"{h}" {ty}' for h, ty in zip(header, types)) + ")")
    con.executemany(f'INSERT INTO "{t}" VALUES ({", ".join("?" * len(header))})',
                    [[None if v == "" else v for v in r] for r in rows])
    print(f"tix.{t}: {len(rows)} rows")
con.commit()
con.close()
print(f"built {DB.relative_to(HERE.parent)}")
