# The builder's yard

A small, made-up building firm to practise on before you build on your own data. You take the
same steps as week one: start from a dashboard, generate metrics and evals, run your agent, and
see the score.

## The firm

Fixit & Co. has ten jobs from July to October 2026: a pergola, a barn, a skate park, a cat flap,
and one very expensive wind turbine base. Rob runs the yard, Wanda does the building, and Sprout
"helps". The machines are crew too, and they bill by the hour: Dig digs, Tipper hauls, Whirl
mixes, Flatt rolls and Lanky lifts. Kipper the cat isn't crew, but turns up in the snag log more
than anyone would like.

## Set up (2 minutes)

In your coding agent, from the repository root:

```text
Set up the builder's yard and show me its dashboard
```

Or by hand:

```bash
python yard/load.py
python yard/q.py "SELECT crew_name, catchphrase FROM site.crew"
```

Both use Python's built-in SQLite, so there is nothing to install.

## Build an agent on it

The dashboard is a Power BI report saved as a file, `yard/powerbi/hard-hat-area-site-performance.pbit`, so no
Power BI account is needed. With the Atlan Analytics plugin installed, in Claude Code or a Claude
app chat:

```text
Use Atlan Analytics to set up this repository so I can ask questions about its data:
https://github.com/atlanai/analytics-agent-accelerator
```

The plugin finds the yard's report, CSVs and query history, loads the data into SQLite, previews
the metrics and SQL, and asks where to publish them. It installs nothing, in Claude Code or a
Claude app chat.

It turns the dashboard's four tiles and the query history into metrics and saved SQL. For the
week-one score, ask next:

```text
Build an eval set for these metrics, run a baseline with a fresh agent per question, and show me the score.
```

It writes eval questions and keeps their answers on your laptop, registers your agent, and runs
the baseline. On the yard that takes about 20 minutes.

## The question to finish on

**Which job ate our margin last quarter, and what ate it?**

## What's in the yard

| Table | Rows | One row is |
|---|---|---|
| `site.projects` | 10 | a job |
| `site.crew` | 8 | a person or a machine |
| `site.work_logs` | 746 | one crew member, one job, one day, one task |
| `site.material_orders` | 51 | an order |
| `site.site_snags` | 11 | something that went wrong |
| `account_usage.query_history` | 417 | one query an analyst ran, July to October 2026 |
| `account_usage.query_shapes` (view) | 110 | one distinct query, with its run and user counts |

The dashboard, *Hard Hat Area: Site Performance*, has four tiles: gross margin, rework cost,
material waste and late jobs. It ships as a Power BI template,
`powerbi/hard-hat-area-site-performance.pbit` (report page and model, no data). `powerbi/model.bim` is the same
model as readable JSON, and `powerbi/rowsets.json` holds the SQL each table is built from.

The query history is laid out the way Snowflake keeps it. `account_usage.query_history` has one
row per run with Snowflake's column names, and `account_usage.query_shapes` groups it the way the
Atlan plugin's one-time admin view does. `q.py` builds both from `history/querylog.jsonl`: the
110 queries the yard's analysts ran, with how often and by how many people. The SQL in the
history and the dashboard is written for SQLite.
