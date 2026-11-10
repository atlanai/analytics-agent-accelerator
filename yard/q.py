"""Read-only SQL on the yard: python yard/q.py "SELECT ..."  (standard library only).

Tables are site.* (from yard/site.sqlite, built by load.py). The analysts' query history is
loaded in memory beside them: query.history has one row per run, and query.query_shapes groups
it the way the Atlan plugin's one-time admin view does. Prints columns and up to 50 rows as JSON.
"""
import datetime
import hashlib
import json
import pathlib
import sqlite3
import sys

HERE = pathlib.Path(__file__).resolve().parent
DB = HERE / "site.sqlite"
# Who ran the queries: job titles in the yard office, not people.
USERS = ("YARD_OFFICE", "QUANTITY_SURVEYOR", "SITE_PLANNER", "BOOKKEEPER", "ESTIMATOR")
START = datetime.datetime(2026, 7, 1, 8, 0)  # history spans 1 July to 31 October 2026


def pick(*key) -> int:
    """A stable number from a key, so every run gives the same history."""
    return int(hashlib.sha256(repr(key).encode()).hexdigest()[:12], 16)


def history_rows():
    """Expand each {sql, exec, users} line into exec runs by exactly `users` distinct users."""
    for i, line in enumerate((HERE / "history" / "querylog.jsonl").open()):
        q = json.loads(line)
        who = [USERS[(pick("user", i) + k) % len(USERS)] for k in range(q["users"])]
        for run in range(q["exec"]):
            start = START + datetime.timedelta(days=pick("day", i, run) % 123, hours=pick("hour", i, run) % 10,
                                               seconds=pick("sec", i, run) % 3600)
            elapsed_ms = 120 + pick("ms", i, run) % 2900
            end = start + datetime.timedelta(milliseconds=elapsed_ms)
            yield (f"{pick('id', i, run):012x}", q["sql"], "SELECT", who[run % len(who)], "SUCCESS",
                   start.isoformat(sep=" "), end.isoformat(sep=" "), elapsed_ms)


if not DB.exists():
    sys.exit("No yard yet: run python yard/load.py first.")
sql = sys.argv[1]
if not sql.lstrip().lower().startswith(("select", "with")):
    sys.exit("Read-only: SELECT or WITH only.")
con = sqlite3.connect(":memory:", uri=True)
con.execute("ATTACH DATABASE ? AS site", (f"file:{DB}?mode=ro",))
con.execute("ATTACH DATABASE ':memory:' AS query")
con.execute("""CREATE TABLE query.history (
    query_id TEXT, query_text TEXT, query_type TEXT, user_name TEXT, execution_status TEXT,
    start_time TEXT, end_time TEXT, duration_ms INTEGER)""")
con.executemany("INSERT INTO query.history VALUES (?, ?, ?, ?, ?, ?, ?, ?)", history_rows())
# The same grouping as the plugin's one-time admin view, without a rolling window: the yard's history is fixed.
con.execute("""CREATE VIEW query.query_shapes AS
    SELECT query_text AS sql, COUNT(*) AS exec, COUNT(DISTINCT user_name) AS users, MAX(start_time) AS last_run
    FROM history
    WHERE execution_status = 'SUCCESS' AND query_type = 'SELECT'
    GROUP BY query_text""")
con.execute("PRAGMA query_only = ON")
cur = con.execute(sql)
print(json.dumps({"columns": [d[0] for d in cur.description], "rows": cur.fetchmany(50)}, default=str))
