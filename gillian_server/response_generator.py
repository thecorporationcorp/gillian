"""
Gillian Response Generator - British Personality
NO API NEEDED - all responses are pre-generated templates
"""

import random
from typing import List


class ResponseGenerator:
    def __init__(self, personality_config: dict):
        self.config = personality_config
        self.name = personality_config.get('name', 'Gillian')
        self.accent = personality_config.get('accent', 'british')

        # Load response templates
        self.acknowledgments = personality_config.get('acknowledgments', ['Understood.'])
        self.confirmations = personality_config.get('confirmations', ['Done.'])
        self.errors = personality_config.get('errors', ['I did not understand that.'])

    def get_acknowledgment(self) -> str:
        """Get a random acknowledgment phrase"""
        return random.choice(self.acknowledgments)

    def get_confirmation(self) -> str:
        """Get a random confirmation phrase"""
        return random.choice(self.confirmations)

    def get_error(self) -> str:
        """Get a random error phrase"""
        return random.choice(self.errors)

    def format_task_response(self, task_id: str, action: str) -> str:
        """Format a response for a task"""
        templates = [
            f"Right away. Task {task_id} is queued.",
            f"Consider it done. Task {task_id} pending.",
            f"I'll see to it. Task {task_id} ready.",
            f"Very good. Task {task_id} in the queue."
        ]
        return random.choice(templates)

    def format_note_response(self) -> str:
        """Format a response for a note"""
        templates = [
            "Noted, sir.",
            "I've made a note of that.",
            "Logged and ready.",
            "All sorted."
        ]
        return random.choice(templates)

    def format_query_response(self, answer: str) -> str:
        """Format a response for a query"""
        return answer  # Answer is already formatted

    def format_greeting(self) -> str:
        """Format a greeting"""
        templates = [
            f"At your service.",
            f"Good day, sir.",
            f"{self.name} here.",
            f"How may I assist you?"
        ]
        return random.choice(templates)
