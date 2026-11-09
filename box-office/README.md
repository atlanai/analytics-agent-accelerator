# The box office

A second made-up company to practise on, with more going on than the builder's yard: a ticketing
firm, a Tableau dashboard, and a Databricks-style query history. You take the same week-one
steps: start from the dashboard, generate metrics and evals, run your agent, and see the score.

## The firm

TicketMonster sells tickets for six venues in Port Mallory and Little Hampden, from a 60-seat
basement club to a 1,000-capacity field by the river. Sixteen acts play 44 shows between July
2025 and December 2026: The Grumpy Moose sell out the arena twice, Kevin From Accounting gets
postponed, and Velvet Thunder's singer loses their voice three days before the gig. Fans buy
online, in the app or at the box office, and some of them resell. The data runs to 31 October 2026.

## Set up (2 minutes)

In your coding agent, from the repository root:

```text
Set up the box office and show me its dashboard
```

Or by hand:

```bash
python box-office/load.py
python box-office/q.py "SELECT event_name, event_date, status FROM tix.events ORDER BY event_date LIMIT 10"
```

Both use Python's built-in SQLite, so there is nothing to install.

## Build an agent on it

The dashboard is a Tableau workbook saved as a file, `box-office/tableau/box-office-pulse.twb`, so
no Tableau account is needed. With the Atlan Analytics plugin installed, in Claude Code or a
Claude app chat:

```text
Use Atlan Analytics to set up the box-office folder of this repository so I can ask questions about its data:
https://github.com/atlanai/analytics-agent-accelerator
```

The plugin finds the workbook, the CSVs and the query history, loads the data into SQLite,
previews the metrics and SQL, and asks where to publish them. For the week-one score, ask next:

```text
Build an eval set for these metrics, run a baseline with a fresh agent per question, and show me the score.
```

## The question to finish on

**How much of what fans paid last quarter went on fees, and why did it go up?**

## What's in the box office

| Table | Rows | One row is |
|---|---|---|
| `tix.venues` | 7 | a venue |
| `tix.artists` | 17 | an act |
| `tix.events` | 45 | a show |
| `tix.fee_schedule` | 16 | a fee rule, with when it applies and who keeps it |
| `tix.customers` | 2,409 | a TicketMonster account |
| `tix.orders` | 6,506 | one checkout: primary, resale or box office |
| `tix.tickets` | 14,391 | one ticket in an order |
| `tix.refunds` | 491 | money paid back on an order |
| `query.history` | 709 | one statement run on the SQL warehouse, August to October 2026 |
| `atlan.query_shapes` | 57 | one distinct finished SELECT, with its run and user counts |

The dashboard, *Box Office Pulse*, has four tiles (gross sales, fees as a share of what fans
paid, net fee revenue and sell-through) and three charts. Its three data sources are custom
SQL on a Databricks SQL warehouse.

The query history is laid out the way Databricks keeps `system.query.history`: one row per
statement, with who ran it, from which tool, whether it finished, and how long it took. Finance,
the press office, marketing, venue operations, data engineering and the dashboard's own
refreshes all appear. `history/query_history.jsonl` is the export; `q.py` loads it as
`query.history` and groups it as `atlan.query_shapes`, the way the Atlan plugin's one-time admin
view does.

`customers` holds names, email addresses, phone numbers and dates of birth. They are made up
(every address is on an `example` domain and every number is a 555-01xx fiction number), but
treat them the way you would treat the real thing.

The SQL in the history and the workbook is written so it runs on SQLite.
