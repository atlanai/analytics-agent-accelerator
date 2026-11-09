---
name: builders-yard
description: Sets up the accelerator's practice estate, the builder's yard (Fixit & Co., a small made-up building firm), on the participant's laptop - builds its SQLite database from CSV, shows the Power BI dashboard it starts from, and answers questions on it read-only. Use when the user asks to set up or try the builder's yard, the practice data, Fixit, or wants to try the accelerator steps before using their own data.
compatibility: Any coding agent with a shell and Python 3.10+. Uses the built-in sqlite3 module; installs nothing.
---

# The builder's yard

Everything lives in `yard/` (read `yard/README.md` first). Nothing leaves the laptop.

1. **Build the yard.** If `yard/site.sqlite` is missing, run `python yard/load.py`. It needs no
   packages. Show the row counts.
2. **Show the dashboard.** Read the measures in `yard/powerbi/model.bim`. List the four tiles,
   each with its measure and value, computed with `python yard/q.py` from the measure's
   definition and the table's SQL in `yard/powerbi/rowsets.json`. One line per tile.
3. **Hand over to the build.** In one line, say the next step: convert the Power BI report
   `yard/powerbi/hard-hat-area-site-performance.pbit` to an agent with the Atlan analytics plugin, as `yard/README.md` shows.
4. **Questions.** Answer questions about the yard with `python yard/q.py` only (read-only). State
   the definition you used in one line under each answer.

Rules: read-only SQL; keep each reply to a status line and one next action.
