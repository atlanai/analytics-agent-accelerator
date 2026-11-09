# Atlan Analytics Agent Accelerator · starter kit

A skill for your coding agent that checks whether your laptop is ready for the
[Atlan](https://atlan.com) Analytics Agent Accelerator, signs you in or helps you connect where
something is missing, and writes a short readiness report to send to us.

During the accelerator we build an agent together, with you, for one use case of your own:
a question your team asks of its data again and again. The check starts by asking what that
use case is. Everything after it (your coding agent, your warehouse access, the dashboard you
would start from) is so we can come to kickoff ready to build that agent with you, not to
spend the first session on setup.

It follows the [Agent Skills](https://agentskills.io) format, so it works in Claude Code,
Codex, Cursor, Windsurf, Gemini CLI, GitHub Copilot CLI, OpenCode and other agents that read
`SKILL.md` files. About ten minutes. No Atlan account needed.

## Get started

Open your coding agent on your laptop (Claude Code, Codex, Cursor, or similar) and paste:

```text
Help me get started with https://github.com/atlanai/analytics-agent-accelerator
```

Your agent reads the [readiness skill](skills/accelerator-readiness/SKILL.md) and its
references from this repository, then guides you through the check in the same conversation.
You don't need to install the skill separately or send another prompt to run it.

The agent asks about your use case and walks you through six short steps with only a handful
of questions. Apart from the use case, each one is a choice you click rather than a sentence
to type. It asks before it runs anything against your warehouse, and it asks again before it
sends the report.

## Practise first

No warehouse connected yet? Two made-up firms let you try the week-one steps on your laptop:

- The [builder's yard](yard/): a small building firm with five tables, a Power BI dashboard and
  a Snowflake-style query history. Paste: `Set up the builder's yard and show me its dashboard`.
- The [box office](box-office/): a ticketing firm with ten tables, a Tableau dashboard and a
  Databricks-style query history, with more to untangle. Paste:
  `Set up the box office and show me its dashboard`.

To look round either firm first, take its [tour](https://atlanai.github.io/analytics-agent-accelerator/).

## What the agent does

| Step | What happens |
|---|---|
| Use case | Asks what you want to build an agent for during the accelerator, in a sentence or two |
| 1. Coding agent | Names the agent you are in, lists the others installed, and the MCP server names each has configured |
| 2. Warehouse route | Looks for your warehouse in its own tools and in the CLIs on your machine: Snowflake, Databricks, BigQuery, Redshift, Postgres and others. With your yes, runs one read-only statement to prove the connection, and if a sign-in has expired, opens the browser sign-in for you from the same session |
| 3. Connect | If no route works, walks you through installing the CLI and signing in, then checks again. Only commands that ask for a password or token go to your own terminal |
| 4. BI | Finds BI apps and MCP servers, counts local BI files, and asks which BI tool and dashboard you would start from and whether you know the tables behind it. No screenshots or exports are requested; BI access is not verified |
| 5. Who you are | Reads your name and work email from the machine (your warehouse sign-in, git, the OS account) and confirms them in one line |
| 6. Report | Writes `atlan-readiness-report.md` in your home folder, shows the summary, and with your yes posts it to Atlan's collection form, then thanks you and says the Atlan team will be in touch with next steps |

The accelerator needs one way for your agent to run SQL as you. A warehouse CLI or an MCP
server, either works. If neither is set up yet, step 3 is the point: the agent gets you
connected before kickoff, or records exactly where it got stuck so we can help.

## Why we ask and where your answers go

**Why.** During the accelerator we build an agent with you for your use case. The report
tells us, before kickoff, what you want to build, how your agent can reach your warehouse, and
which dashboard and tables to start from. We use it only to prepare for the accelerator with
you.

**Where it's stored.**

- **On your laptop:** the agent writes the report to `atlan-readiness-report.md` in your home
  folder. It stays there until you delete it.
- **With Atlan, only if you choose Send:** the report, your name and your work email go to a
  Google Form owned by Atlan. Responses stay within Atlan, are not public, and only the
  accelerator team can see them.
- **If sending fails:** you email the file yourself, to an Atlan address the agent gives you.

Your coding agent handles your answers the way it handles any conversation, under your own
agreement with its provider. Atlan receives nothing unless you choose Send.

**How long we keep it.** For the length of the accelerator. To see or delete your report,
email [ailabs@atlan.com](mailto:ailabs@atlan.com).

## What leaves your machine

Only the report, and only when you say yes. It contains tool names and versions, the names of
your warehouse, BI and Atlan MCP servers and a count of the others, connection and profile
names, the signed-in user and role, the outcome of each check, BI tool names and file counts,
your name and work email, your use case, your BI answers, and any table names you give. A connection or server name that looks like an
account identifier is replaced with a neutral label before it is written. It never contains
credentials, tokens, hostnames, account identifiers, file names or data rows. The skill reads
configuration files only to list names, and every command it runs on its own is read-only.
Read the report before you send it.

## Requirements

- A coding agent on your laptop. The browser versions of Claude and ChatGPT are not enough.
- A warehouse account you can sign in to (Snowflake, Databricks, BigQuery, Redshift, Postgres
  or another).
- A BI tool and a starting dashboard in mind for week one. No screenshots or exports needed.
- Python 3.10 or newer if you need to install the Snowflake CLI during step 3.

## Layout

```
skills/accelerator-readiness/
  SKILL.md                      the six steps and the rules the agent follows
  references/coding-agents.md   agents, version commands, where MCP servers are configured
  references/snowflake.md       Snowflake CLI, Cortex Code and MCP: check, sign in, connect, errors
  references/databricks.md      Databricks CLI and MCP: check, sign in, connect, errors
  references/bigquery.md        gcloud, bq and the BigQuery MCP server
  references/redshift.md        AWS CLI, the Redshift Data API and the Redshift MCP server
  references/other-warehouses.md Postgres, ClickHouse, Fabric and SQL Server, Trino, DuckDB
  references/bi-tools.md        what to look for and the two questions
  references/report.md          the report template and where it goes
  references/builder.md         the Builder: start frame, quips, site pass and inspection
skills/builders-yard/SKILL.md   set up the practice yard and show its dashboard
skills/box-office/SKILL.md      set up the practice box office and show its dashboard
yard/                           the builder's yard: data, dashboard, query history
box-office/                     the box office: data, Tableau workbook, Databricks query history
```

## Contact us

Questions about the accelerator or the readiness check: email
[ailabs@atlan.com](mailto:ailabs@atlan.com).

## License

Apache 2.0. See [LICENSE](LICENSE).
