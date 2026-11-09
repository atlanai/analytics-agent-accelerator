---
name: box-office
description: Sets up the accelerator's second practice estate, the box office (TicketMonster, a made-up ticketing firm), on the participant's laptop - builds its SQLite database from CSV, shows the Tableau dashboard it starts from, and answers questions on it read-only. Use when the user asks to set up or try the box office, TicketMonster, the ticketing practice data, or the Tableau or Databricks practice estate.
compatibility: Any coding agent with a shell and Python 3.10+. Uses the built-in sqlite3 module; installs nothing.
---

# The box office

Everything lives in `box-office/` (read `box-office/README.md` first). Nothing leaves the laptop.

1. **Build it.** If `box-office/tix.sqlite` is missing, run `python box-office/load.py`. It needs
   no packages. Show the row counts.
2. **Show the dashboard.** Read the workbook `box-office/tableau/box-office-pulse.twb`: its three
   data sources (custom SQL), its calculated fields, and its worksheets with their titles and
   filters. List the four tiles, each with its title, the measure behind it and its value,
   computed with `python box-office/q.py` from the measure's formula over the data source's SQL
   and the sheet's filters. One line per tile.
3. **Hand over to the build.** In one line, say the next step: turn the Tableau workbook into an
   agent with the Atlan analytics plugin, as `box-office/README.md` shows.
4. **Questions.** Answer questions about the box office with `python box-office/q.py` only
   (read-only). State the definition you used in one line under each answer. Do not show
   customer names, email addresses, phone numbers or dates of birth.

Rules: read-only SQL; keep each reply to a status line and one next action.
