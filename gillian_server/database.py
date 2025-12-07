"""
Gillian Database - SQLite storage (replaces Google Sheets)
NO QUOTA LIMITS, 100% LOCAL
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class GillianDB:
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        logger.info(f"Database initialized: {self.db_path}")

    def _get_conn(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Initialize database schema"""
        conn = self._get_conn()
        conn.executescript('''
            -- Command history (replaces Behavior Log sheet)
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                utterance TEXT NOT NULL,
                intent TEXT,
                confidence REAL,
                response TEXT,
                device TEXT,
                client_time TEXT,
                metadata TEXT
            );

            -- PC Tasks queue (replaces PC Tasks sheet)
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id TEXT UNIQUE NOT NULL,
                summary TEXT NOT NULL,
                command TEXT NOT NULL,
                risk_level TEXT DEFAULT 'low',
                status TEXT DEFAULT 'pending',
                queued_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                started_time TIMESTAMP,
                completed_time TIMESTAMP,
                last_error TEXT,
                retries INTEGER DEFAULT 0
            );

            -- Notes/Memories
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                content TEXT NOT NULL,
                tags TEXT,
                client_time TEXT
            );

            -- Entities (people, places, things mentioned)
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                type TEXT,
                first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                mention_count INTEGER DEFAULT 1,
                contexts TEXT
            );

            CREATE INDEX IF NOT EXISTS idx_commands_timestamp ON commands(timestamp);
            CREATE INDEX IF NOT EXISTS idx_commands_intent ON commands(intent);
            CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
            CREATE INDEX IF NOT EXISTS idx_notes_timestamp ON notes(timestamp);
        ''')
        conn.commit()
        conn.close()

    def log_command(self, utterance: str, intent: str, confidence: float,
                    device: str = 'unknown', client_time: str = None) -> int:
        """Log a voice command"""
        try:
            conn = self._get_conn()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO commands (utterance, intent, confidence, device, client_time)
                VALUES (?, ?, ?, ?, ?)
            ''', (utterance, intent, confidence, device, client_time))

            conn.commit()
            command_id = cursor.lastrowid
            conn.close()

            return command_id
        except Exception as e:
            logger.error(f"Failed to log command: {e}")
            return -1

    def update_command_response(self, command_id: int, response: str):
        """Update command with response"""
        try:
            conn = self._get_conn()
            cursor = conn.cursor()

            cursor.execute('''
                UPDATE commands SET response = ? WHERE id = ?
            ''', (response, command_id))

            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to update command response: {e}")

    def save_note(self, content: str, client_time: str = None) -> int:
        """Save a note/memory"""
        try:
            conn = self._get_conn()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO notes (content, client_time)
                VALUES (?, ?)
            ''', (content, client_time))

            conn.commit()
            note_id = cursor.lastrowid
            conn.close()

            return note_id
        except Exception as e:
            logger.error(f"Failed to save note: {e}")
            return -1

    def get_recent_notes(self, limit: int = 10) -> list:
        """Get recent notes"""
        try:
            conn = self._get_conn()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT content FROM notes
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))

            notes = [row[0] for row in cursor.fetchall()]
            conn.close()

            return notes
        except Exception as e:
            logger.error(f"Failed to get notes: {e}")
            return []

    def get_command_history(self, limit: int = 20) -> list:
        """Get command history"""
        try:
            conn = self._get_conn()
            cursor = conn.cursor()

            cursor.execute('''
                SELECT timestamp, utterance, intent, confidence, response, device
                FROM commands
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,))

            history = []
            for row in cursor.fetchall():
                history.append({
                    'timestamp': row[0],
                    'utterance': row[1],
                    'intent': row[2],
                    'confidence': row[3],
                    'response': row[4],
                    'device': row[5]
                })

            conn.close()
            return history
        except Exception as e:
            logger.error(f"Failed to get history: {e}")
            return []

    def get_stats(self) -> dict:
        """Get usage statistics"""
        try:
            conn = self._get_conn()
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM commands')
            total_commands = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = "pending"')
            pending_tasks = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM tasks WHERE status = "completed"')
            completed_tasks = cursor.fetchone()[0]

            cursor.execute('SELECT COUNT(*) FROM notes')
            total_notes = cursor.fetchone()[0]

            cursor.execute('''
                SELECT intent, COUNT(*) as count
                FROM commands
                WHERE intent IS NOT NULL
                GROUP BY intent
            ''')
            intents = {row[0]: row[1] for row in cursor.fetchall()}

            conn.close()

            return {
                'total_commands': total_commands,
                'total_notes': total_notes,
                'pending_tasks': pending_tasks,
                'completed_tasks': completed_tasks,
                'intents_breakdown': intents,
                'api_cost': 0.00  # FREE!
            }
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {}
