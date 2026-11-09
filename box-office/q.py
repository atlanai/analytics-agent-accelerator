"""Read-only SQL on the box office: python box-office/q.py "SELECT ..."  (standard library only).

Tables are tix.* (from box-office/tix.sqlite, built by load.py). The query history is loaded in
memory the way Databricks keeps it: query.history has one row per statement with the columns of
system.query.history (compute flattened to compute_warehouse_id), and atlan.query_shapes groups
the finished SELECTs the way the Atlan plugin's one-time admin view does. Prints columns and up
to 50 rows as JSON.
"""
import json
import pathlib
import sqlite3
import sys

HERE = pathlib.Path(__file__).resolve().parent
DB = HERE / "tix.sqlite"
COLUMNS = ("workspace_id", "statement_id", "executed_by", "executed_by_user_id", "execution_status",
           "statement_type", "statement_text", "error_message", "client_application",
           "compute_warehouse_id", "start_time", "end_time", "total_duration_ms", "read_rows",
           "produced_rows")


def history_rows():
    for line in (HERE / "history" / "query_history.jsonl").open():
        r = json.loads(line)
        r["compute_warehouse_id"] = (r.pop("compute", None) or {}).get("warehouse_id")
        yield tuple(r.get(c) for c in COLUMNS)


if not DB.exists():
    sys.exit("No box office yet: run python box-office/load.py first.")
sql = sys.argv[1]
if not sql.lstrip().lower().startswith(("select", "with")):
    sys.exit("Read-only: SELECT or WITH only.")
con = sqlite3.connect(":memory:", uri=True)
con.execute("ATTACH DATABASE ? AS tix", (f"file:{DB}?mode=ro",))
con.execute("ATTACH DATABASE ':memory:' AS query")
con.execute("CREATE TABLE query.history (" + ", ".join(COLUMNS) + ")")
con.executemany(f"INSERT INTO query.history VALUES ({', '.join('?' * len(COLUMNS))})", history_rows())
# The same grouping as the plugin's one-time admin view, without a rolling window: the history is fixed.
con.execute("ATTACH DATABASE ':memory:' AS atlan")
con.execute("""CREATE TABLE atlan.query_shapes AS
    SELECT statement_text AS sql, COUNT(*) AS exec, COUNT(DISTINCT executed_by_user_id) AS users,
           MAX(start_time) AS last_run
    FROM query.history
    WHERE execution_status = 'FINISHED' AND statement_type = 'SELECT'
    GROUP BY statement_text""")
con.execute("PRAGMA query_only = ON")
cur = con.execute(sql)
print(json.dumps({"columns": [d[0] for d in cur.description], "rows": cur.fetchmany(50)}, default=str))
