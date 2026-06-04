import sys
import os
import subprocess
import logging
import argparse
from datetime import datetime

class CronRunner:
    def __init__(self, script_name, description):
        self.script_name = script_name
        self.description = description
        
        # 1. Parse Arguments
        self.parser = argparse.ArgumentParser(description=description)
        self.parser.add_argument("--dry-run", action="store_true", help="Execute mock tasks without modifying DB or APIs")
        self.args = self.parser.parse_args()
        
        # 2. Setup Logging
        log_dir = "/Users/michaelshaw/Projects/open-design/.od/logs"
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f"{script_name}.log")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(script_name)
        
        self.logger.info(f"=== Starting Cron execution: {script_name} ===")
        if self.args.dry_run:
            self.logger.info("⚠️ DRY-RUN MODE ACTIVE: No live modifications will be made.")
            
    def emit_acmi_event(self, kind, summary, target=None, workflow_id=None):
        """Emits an ACMI event to the live Super Bus relay."""
        source = f"agent:{self.script_name}"
        self.logger.info(f"Publishing ACMI event ({kind}): {summary}")
        
        if self.args.dry_run:
            self.logger.info(f"[Dry-Run] ACMI Event would be: source={source}, kind={kind}, summary='{summary}', target={target}, workflow={workflow_id}")
            return True
            
        relay_path = "/Users/michaelshaw/clawd/acmi-bus-relay/emit-bus-event.sh"
        cmd = [relay_path, source, kind, summary]
        if target:
            cmd.append(target)
        if workflow_id:
            # Ensure target is present if workflow_id is supplied
            if not target:
                cmd.append("")
            cmd.append(workflow_id)
            
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.logger.info(f"ACMI Event emitted successfully: {res.stdout.strip()}")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to emit ACMI event: {e.stderr.strip()}")
            return False
        except Exception as e:
            self.logger.error(f"Exception emitting ACMI event: {e}")
            return False
            
    def run(self, task_function):
        """Executes the cron task wrapped in standard spawn/complete instrumentation."""
        # Pre-execution spawn event
        self.emit_acmi_event(
            kind="task-started",
            summary=f"[task-started] Starting daily cron task: {self.script_name}"
        )
        
        try:
            task_function(self.args.dry_run)
            self.logger.info(f"✓ Daily cron task completed successfully: {self.script_name}")
            
            # Post-execution completion event
            self.emit_acmi_event(
                kind="task-completed",
                summary=f"[task-completed] Successfully executed daily cron task: {self.script_name}"
            )
        except Exception as e:
            self.logger.error(f"✗ Critical failure executing cron task: {e}", exc_info=True)
            
            # Post-execution failure event
            self.emit_acmi_event(
                kind="task-failed",
                summary=f"[task-failed] Error executing daily cron task: {self.script_name} - {str(e)}"
            )
            sys.exit(1)
            
        self.logger.info(f"=== Finished Cron execution: {self.script_name} ===")
