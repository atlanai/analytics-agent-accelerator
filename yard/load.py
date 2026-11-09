"""Build the yard's SQLite database from its CSVs: python yard/load.py  (standard library only).

Writes yard/site.sqlite with the five site tables. Column types are inferred from the CSVs:
whole numbers become INTEGER, other numbers REAL, everything else (dates included) TEXT.
The analysts' query history stays in history/querylog.jsonl; q.py loads it on each run.
"""
import csv
import pathlib
import sqlite3

HERE = pathlib.Path(__file__).resolve().parent
DB = HERE / "site.sqlite"  # the file name is the schema name: site.projects, site.crew, ...
TABLES = ("projects", "crew", "work_logs", "material_orders", "site_snags")


def column_type(values) -> str:
    for name, cast in (("INTEGER", int), ("REAL", float)):
        try:
            [cast(v) for v in values if v != ""]
            return name
        except ValueError:
            pass
    return "TEXT"


if DB.exists():
    DB.unlink()
con = sqlite3.connect(DB)
for t in TABLES:
    with (HERE / "data" / f"{t}.csv").open(newline="") as f:
        header, *rows = list(csv.reader(f))
    types = [column_type([r[i] for r in rows]) for i in range(len(header))]
    con.execute(f'CREATE TABLE "{t}" (' + ", ".join(f'"{h}" {ty}' for h, ty in zip(header, types)) + ")")
    con.executemany(f'INSERT INTO "{t}" VALUES ({", ".join("?" * len(header))})',
                    [[None if v == "" else v for v in r] for r in rows])
    print(f"site.{t}: {len(rows)} rows")
con.commit()
con.close()
print(f"built {DB.relative_to(HERE.parent)}")
