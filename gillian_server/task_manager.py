"""
Gillian Task Manager - Queue and execute PC tasks
"""

import uuid
import logging
from datetime import datetime
import sqlite3

logger = logging.getLogger(__name__)


class TaskManager:
    def __init__(self, db, config: dict):
        self.db = db
        self.config = config

    def queue_task(self, summary: str, command: str, risk_level: str = 'low') -> str:
        """
        Queue a new PC task

        Returns task_id
        """
        try:
            task_id = str(uuid.uuid4())[:8]

            conn = self.db._get_conn()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO tasks (task_id, summary, command, risk_level, status, queued_time)
                VALUES (?, ?, ?, ?, 'pending', CURRENT_TIMESTAMP)
            ''', (task_id, summary, command, risk_level))

            conn.commit()
            conn.close()

            logger.info(f"Task queued: {task_id} - {summary}")
            return task_id

        except Exception as e:
            logger.error(f"Failed to queue task: {e}")
            return 'error'

    def get_pending_tasks(self) -> list:
        """Get all pending tasks"""
        try:
            conn = self.db._get_conn()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, task_id, summary, command, risk_level, queued_time
                FROM tasks
                WHERE status = 'pending'
                ORDER BY queued_time ASC
            ''')

            tasks = []
            for row in cursor.fetchall():
                tasks.append({
                    'id': row[0],
                    'task_id': row[1],
                    'summary': row[2],
                    'command': row[3],
                    'risk_level': row[4],
                    'queued_time': row[5]
                })

            conn.close()
            return tasks

        except Exception as e:
            logger.error(f"Failed to get pending tasks: {e}")
            return []

    def get_all_tasks(self) -> list:
        """Get all tasks (for debugging)"""
        try:
            conn = self.db._get_conn()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT task_id, summary, command, status, risk_level, queued_time, completed_time, last_error
                FROM tasks
                ORDER BY queued_time DESC
                LIMIT 50
            ''')

            tasks = []
            for row in cursor.fetchall():
                tasks.append({
                    'task_id': row[0],
                    'summary': row[1],
                    'command': row[2],
                    'status': row[3],
                    'risk_level': row[4],
                    'queued_time': row[5],
                    'completed_time': row[6],
                    'last_error': row[7]
                })

            conn.close()
            return tasks

        except Exception as e:
            logger.error(f"Failed to get tasks: {e}")
            return []

    def get_pending_count(self) -> int:
        """Get count of pending tasks"""
        try:
            conn = self.db._get_conn()
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = "pending"')
            count = cursor.fetchone()[0]

            conn.close()
            return count

        except Exception as e:
            logger.error(f"Failed to get pending count: {e}")
            return 0

    def update_task_status(self, task_id: str, status: str, error: str = None):
        """Update task status"""
        try:
            conn = self.db._get_conn()
            cursor = conn.cursor()

            if status == 'completed':
                cursor.execute('''
                    UPDATE tasks
                    SET status = ?, completed_time = CURRENT_TIMESTAMP
                    WHERE task_id = ?
                ''', (status, task_id))
            elif status == 'error':
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

            logger.info(f"Task {task_id} status updated to {status}")

        except Exception as e:
            logger.error(f"Failed to update task status: {e}")
