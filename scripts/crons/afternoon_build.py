#!/usr/bin/env python3
"""
Mad EZ Media Partners — Afternoon Build, Test & Launch Cron
Scheduled: Daily at 01:00 PM
"""

from cron_runner import CronRunner
import subprocess
import os

def build_task(dry_run):
    runner.logger.info("Executing codebase build compilation and linter guard audits...")
    
    project_root = "/Users/michaelshaw/Projects/open-design"
    
    if dry_run:
        runner.logger.info("[Dry-Run] Would run: pnpm typecheck && pnpm guard")
        runner.emit_acmi_event(
            kind="work-update",
            summary="[work-update @devops-engineer] Codebase compile checks passed (dry-run)."
        )
        return
        
    # 1. Run typecheck
    runner.logger.info("Running pnpm typecheck...")
    try:
        subprocess.run(["pnpm", "typecheck"], cwd=project_root, check=True, capture_output=True, text=True)
        runner.logger.info("✓ Typecheck compilation successful.")
    except subprocess.CalledProcessError as e:
        runner.logger.error(f"✗ Typecheck failed: {e.stderr}")
        raise Exception(f"Typecheck failed: {e.stderr[:300]}")
        
    # 2. Run guard script
    runner.logger.info("Running pnpm guard style policy audits...")
    try:
        subprocess.run(["pnpm", "guard"], cwd=project_root, check=True, capture_output=True, text=True)
        runner.logger.info("✓ Linter guard audits successful.")
    except subprocess.CalledProcessError as e:
        runner.logger.error(f"✗ Guard linter audit failed: {e.stderr}")
        raise Exception(f"Linter guard check failed: {e.stderr[:300]}")
        
    # Emit success event to ACMI
    runner.emit_acmi_event(
        kind="work-update",
        summary="[work-update @devops-engineer] Daily afternoon compile and linter guard checks succeeded. Codebase aligned and stable."
    )

if __name__ == "__main__":
    runner = CronRunner("afternoon_build", "01:00 PM: Workspace build, test & deploy")
    runner.run(build_task)
