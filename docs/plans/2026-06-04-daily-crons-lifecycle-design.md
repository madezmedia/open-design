# Plan Design: Daily Crons for Business Lifecycle (FBL-OS)
**Date:** 2026-06-04  
**Author:** Antigravity AI Coding Assistant  
**Co-Authored-By:** aba-bcba-expert <sheveenbrown@gmail.com>  
**Status:** VALIDATED  

This document defines the design and specifications for a local-first micro-cron scheduling system (running locally via crontab first, supporting future Composio triggers) that automates progress across the 10-step business lifecycle of Mad EZ Media Partners: **Discover → Validate → Plan → Build → Test → Launch → Sell → Support → Measure → Iterate**, ending in verified revenue collection.

---

## 1. File Architecture & Layout

We will create a dedicated `scripts/crons/` directory in the `open-design` codebase containing a shared runner class and 4 distinct time-of-day execution scripts:

```
open-design/
  └── scripts/
        └── crons/
              ├── cron_runner.py          # Shared base runner utility class
              ├── morning_discover.py     # 08:00 AM: Market research & trend scraping
              ├── afternoon_build.py      # 01:00 PM: Workspace build, test & deploy
              ├── evening_revenue.py      # 06:00 PM: Square/Whop checkout verify & CS pings
              └── night_measure.py        # 11:00 PM: Daily metrics & ACMI session rollup
```

### Shared base class (`cron_runner.py`):
Handles boilerplate cron tasks:
* Loads environment variables (`OD_PORT`, `UPSTASH_REDIS_REST_URL`, etc.).
* Automated ACMI spawn logging at execution start.
* Unified exception handling and warning notifications on failure.
* Timeline event posting with automatic correlation IDs.

---

## 2. Cron Scheduler Configurations (crontab)

The scripts will be registered under the local user's `crontab` on macOS using absolute path mapping:

```bash
# 1. Morning Discover & Validate (08:00 AM)
0 8 * * * /opt/homebrew/bin/python3.12 /Users/michaelshaw/Projects/open-design/scripts/crons/morning_discover.py >> /Users/michaelshaw/Projects/open-design/.od/logs/morning_discover.log 2>&1

# 2. Afternoon Build, Test & Launch (01:00 PM)
0 13 * * * /opt/homebrew/bin/python3.12 /Users/michaelshaw/Projects/open-design/scripts/crons/afternoon_build.py >> /Users/michaelshaw/Projects/open-design/.od/logs/afternoon_build.log 2>&1

# 3. Evening Sell & Support (06:00 PM)
0 18 * * * /opt/homebrew/bin/python3.12 /Users/michaelshaw/Projects/open-design/scripts/crons/evening_revenue.py >> /Users/michaelshaw/Projects/open-design/.od/logs/evening_revenue.log 2>&1

# 4. Night Measure & Iterate (11:00 PM)
0 23 * * * /opt/homebrew/bin/python3.12 /Users/michaelshaw/Projects/open-design/scripts/crons/night_measure.py >> /Users/michaelshaw/Projects/open-design/.od/logs/night_measure.log 2>&1
```

---

## 3. Data Flow & ACMI Timeline Event Map

Each script publishes standardized events (ACMI Comms v1.5 compliance) to the fleet coordination timeline `acmi:thread:agent-coordination:timeline`:

1. **Morning Discover**:
   * **Event**: `kind: problem-discovered`
   * **Correlation ID**: `cronDiscover-<epochMs>`
   * **Payload**: Market analysis trends and target search volume gaps.
2. **Afternoon Build**:
   * **Event**: `kind: work-update`
   * **Correlation ID**: `cronBuild-<epochMs>`
   * **Payload**: Linter scores, TypeScript checks, and Vercel build details.
3. **Evening Revenue**:
   * **Event**: `kind: work-update`
   * **Correlation ID**: `cronRevenue-<epochMs>`
   * **Payload**: Square checkout health metrics and onboarding logs.
4. **Night Measure**:
   * **Event**: `kind: work-completed`
   * **Correlation ID**: `cronMeasure-<epochMs>`
   * **Payload**: Lighthouse scores, daily database backups, and daily summary rollup.

---

## 4. Spec Verification Plan

* **Lint & Compilation**: The scripts must be validated using `python3.12 -m py_compile` and pass the monorepo linter.
* **Dry-Run Mode**: Each script will support a `--dry-run` flag to execute mock pings and log printouts without executing real API/DB writes.
* **ACMI Telemetry Check**: Dry-run execution will output mock ACMI events to standard console output for verification.

---

## 5. Git Attribution & Comms Compliance
All codebase commits tracking this implementation must be tagged under:
```
Co-Authored-By: aba-bcba-expert <sheveenbrown@gmail.com>
```
Before committing any changes, a pre-commit ACMI bus broadcast (`task.started`) must be sent, followed by a post-commit broadcast (`task.completed`).
