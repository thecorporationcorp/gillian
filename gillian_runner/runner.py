#!/usr/bin/env python3
"""
Gillian PC Task Runner
Polls the task queue and executes pending commands

Runs as a separate process from the server
"""

import os
import sys
import time
import sqlite3
import subprocess
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
POLL_INTERVAL = 5  # seconds
DB_PATH = Path.home() / '.gillian' / 'gillian.db'
SAFE_MODE = True  # Set to False to allow risky commands

# Risk level limits
MAX_RISK_LEVEL = 'medium' if SAFE_MODE else 'high'


class TaskRunner:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)

        if not self.db_path.exists():
            logger.error(f"Database not found: {self.db_path}")
            logger.error("Please start the Gillian server first!")
            sys.exit(1)

        logger.info(f"Task runner initialized")
        logger.info(f"Database: {self.db_path}")
        logger.info(f"Safe mode: {SAFE_MODE}")
        logger.info(f"Max risk level: {MAX_RISK_LEVEL}")

    def get_conn(self):
        """Get database connection"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def get_pending_tasks(self):
        """Get pending tasks from database"""
        try:
            conn = self.get_conn()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, task_id, summary, command, risk_level, retries
                FROM tasks
                WHERE status = 'pending'
                ORDER BY queued_time ASC
            ''')

            tasks = cursor.fetchall()
            conn.close()

            return tasks

        except Exception as e:
            logger.error(f"Failed to fetch pending tasks: {e}")
            return []

    def execute_task(self, task):
        """Execute a task"""
        task_id = task['task_id']
        command = task['command']
        risk_level = task['risk_level']
        retries = task['retries']

        logger.info(f"Processing task {task_id}: {task['summary']}")

        # Check risk level
        risk_levels = {'low': 0, 'medium': 1, 'high': 2}
        max_risk = risk_levels.get(MAX_RISK_LEVEL, 1)
        task_risk = risk_levels.get(risk_level, 0)

        if task_risk > max_risk:
            error_msg = f"Risk level {risk_level} exceeds maximum {MAX_RISK_LEVEL}"
            logger.warning(f"Task {task_id} blocked: {error_msg}")
            self.update_task_status(task_id, 'error', error_msg)
            return False

        # Check retry limit
        if retries >= 3:
            error_msg = "Maximum retries exceeded"
            logger.warning(f"Task {task_id} failed permanently: {error_msg}")
            self.update_task_status(task_id, 'failed', error_msg)
            return False

        # Update status to running
        self.update_task_status(task_id, 'running')

        # Execute command
        try:
            logger.info(f"Executing: {command}")

            # Determine shell based on platform
            if sys.platform == 'win32':
                # Windows - use PowerShell
                result = subprocess.run(
                    ['powershell', '-Command', command],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
            else:
                # Linux/Mac - use bash
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=30
                )

            if result.returncode == 0:
                logger.info(f"Task {task_id} completed successfully")
                self.update_task_status(task_id, 'completed')
                return True
            else:
                error_msg = result.stderr[:500] if result.stderr else 'Unknown error'
                logger.error(f"Task {task_id} failed: {error_msg}")
                self.update_task_status(task_id, 'error', error_msg)
                return False

        except subprocess.TimeoutExpired:
            error_msg = "Command timeout (30s)"
            logger.error(f"Task {task_id} timed out")
            self.update_task_status(task_id, 'error', error_msg)
            return False

        except Exception as e:
            error_msg = str(e)[:500]
            logger.error(f"Task {task_id} exception: {error_msg}")
            self.update_task_status(task_id, 'error', error_msg)
            return False

    def update_task_status(self, task_id: str, status: str, error: str = None):
        """Update task status in database"""
        try:
            conn = self.get_conn()
            cursor = conn.cursor()

            if status == 'running':
                cursor.execute('''
                    UPDATE tasks
                    SET status = ?, started_time = CURRENT_TIMESTAMP
                    WHERE task_id = ?
                ''', (status, task_id))

            elif status == 'completed':
                cursor.execute('''
                    UPDATE tasks
                    SET status = ?, completed_time = CURRENT_TIMESTAMP
                    WHERE task_id = ?
                ''', (status, task_id))

            elif status in ['error', 'failed']:
                cursor.execute('''
                    UPDATE tasks
                    SET status = ?, last_error = ?, retries = retries + 1
                    WHERE task_id = ?
                ''', (status, error, task_id))

            else:
                cursor.execute('''
                    UPDATE tasks
                    SET status = ?
                    WHERE task_id = ?
                ''', (status, task_id))

            conn.commit()
            conn.close()

        except Exception as e:
            logger.error(f"Failed to update task status: {e}")

    def run(self):
        """Main runner loop"""
        logger.info("Task runner started")
        logger.info(f"Polling every {POLL_INTERVAL} seconds...")
        logger.info("Press Ctrl+C to stop\n")

        try:
            while True:
                tasks = self.get_pending_tasks()

                if tasks:
                    logger.info(f"Found {len(tasks)} pending task(s)")

                    for task in tasks:
                        self.execute_task(task)

                time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            logger.info("\nTask runner stopped by user")
            sys.exit(0)


if __name__ == '__main__':
    print('\n' + '=' * 60)
    print('  GILLIAN PC TASK RUNNER')
    print('  Executes queued tasks from Gillian server')
    print('=' * 60 + '\n')

    runner = TaskRunner(DB_PATH)
    runner.run()
