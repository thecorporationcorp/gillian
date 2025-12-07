"""
Gillian Intent Detector - 100% LOCAL (NO API COSTS!)

Uses pattern matching + local NLP to detect user intent
Replaces expensive GPT-4 API calls with free local processing
"""

import re
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class IntentDetector:
    def __init__(self, intents_config: dict):
        self.config = intents_config
        self.nlp_available = False

        # Try to load spaCy for better NLP (optional)
        try:
            import spacy
            self.nlp = spacy.load('en_core_web_sm')
            self.nlp_available = True
            logger.info("spaCy NLP engine loaded successfully")
        except:
            logger.warning("spaCy not available - using pattern matching only")
            self.nlp = None

    def detect(self, text: str) -> Dict[str, Any]:
        """
        Detect intent from user text

        Returns:
        {
            'intent': 'pc_task' | 'note' | 'query' | 'system' | 'unknown',
            'confidence': 0.0-1.0,
            'action': str,
            'task_data': {...} or None,
            ...
        }
        """
        text_lower = text.lower().strip()

        # Check PC task intent
        pc_task_result = self._detect_pc_task(text_lower)
        if pc_task_result['confidence'] > 0.6:
            return pc_task_result

        # Check note intent
        note_result = self._detect_note(text_lower)
        if note_result['confidence'] > 0.6:
            return note_result

        # Check query intent
        query_result = self._detect_query(text_lower)
        if query_result['confidence'] > 0.6:
            return query_result

        # Check system intent
        system_result = self._detect_system(text_lower)
        if system_result['confidence'] > 0.6:
            return system_result

        # Fallback
        return {
            'intent': 'unknown',
            'confidence': 0.0,
            'original_text': text
        }

    def _detect_pc_task(self, text: str) -> Dict[str, Any]:
        """Detect PC task commands"""
        pc_config = self.config.get('pc_task', {})
        keywords = pc_config.get('keywords', [])
        apps = pc_config.get('apps', {})

        # Check for action keywords
        action = None
        for keyword in keywords:
            if keyword in text:
                action = keyword
                break

        if not action:
            return {'intent': 'pc_task', 'confidence': 0.0}

        # Check for app names
        target_app = None
        command = None

        for app_name, app_command in apps.items():
            if app_name in text:
                target_app = app_name
                command = app_command
                break

        # If we found both action and target
        if action and target_app:
            return {
                'intent': 'pc_task',
                'confidence': 0.95,
                'action': action,
                'task_data': {
                    'target': target_app,
                    'command': command,
                    'risk_level': self._assess_risk(command)
                }
            }

        # Just action, no specific app
        if action:
            # Extract potential app name from text
            words = text.split()
            potential_target = ' '.join(words[1:3]) if len(words) > 1 else 'unknown'

            return {
                'intent': 'pc_task',
                'confidence': 0.7,
                'action': action,
                'task_data': {
                    'target': potential_target,
                    'command': f'{action} {potential_target}',
                    'risk_level': 'medium'
                }
            }

        return {'intent': 'pc_task', 'confidence': 0.0}

    def _detect_note(self, text: str) -> Dict[str, Any]:
        """Detect note-taking commands"""
        note_config = self.config.get('note', {})
        keywords = note_config.get('keywords', [])

        for keyword in keywords:
            if keyword in text:
                # Extract the content to note
                # e.g., "note that I need milk" -> "I need milk"
                note_content = text

                # Try to extract content after the keyword
                if keyword in text:
                    parts = text.split(keyword, 1)
                    if len(parts) > 1:
                        note_content = parts[1].strip()

                        # Remove common prefixes
                        for prefix in ['that', 'to', 'this:', 'down']:
                            if note_content.startswith(prefix):
                                note_content = note_content[len(prefix):].strip()

                return {
                    'intent': 'note',
                    'confidence': 0.9,
                    'note_content': note_content
                }

        return {'intent': 'note', 'confidence': 0.0}

    def _detect_query(self, text: str) -> Dict[str, Any]:
        """Detect query/question commands"""
        query_config = self.config.get('query', {})
        keywords = query_config.get('keywords', [])

        # Check for question words
        for keyword in keywords:
            if text.startswith(keyword):
                # Determine query type
                query_type = 'general'

                if any(word in text for word in ['task', 'tasks', 'pending', 'queue']):
                    query_type = 'task_status'
                elif any(word in text for word in ['note', 'notes', 'remember']):
                    query_type = 'recent_notes'
                elif any(word in text for word in ['time', 'date', 'day']):
                    query_type = 'datetime'

                return {
                    'intent': 'query',
                    'confidence': 0.85,
                    'query_type': query_type,
                    'question': text
                }

        # Check for status/check keywords (don't need to start with them)
        if any(word in text for word in ['status', 'check on', 'how many']):
            return {
                'intent': 'query',
                'confidence': 0.75,
                'query_type': 'status',
                'question': text
            }

        return {'intent': 'query', 'confidence': 0.0}

    def _detect_system(self, text: str) -> Dict[str, Any]:
        """Detect system commands"""
        system_config = self.config.get('system', {})
        keywords = system_config.get('keywords', [])

        for keyword in keywords:
            if keyword in text:
                return {
                    'intent': 'system',
                    'confidence': 0.95,
                    'action': keyword,
                    'warning': 'System command - requires safe mode off'
                }

        return {'intent': 'system', 'confidence': 0.0}

    def _assess_risk(self, command: str) -> str:
        """Assess risk level of a command"""
        if not command:
            return 'low'

        command_lower = command.lower()

        # High risk commands
        high_risk = ['rm ', 'del ', 'format', 'shutdown', 'restart', 'kill']
        if any(cmd in command_lower for cmd in high_risk):
            return 'high'

        # Medium risk commands
        medium_risk = ['move', 'copy', 'rename', 'mkdir']
        if any(cmd in command_lower for cmd in medium_risk):
            return 'medium'

        # Default to low
        return 'low'

    def extract_entities(self, text: str) -> list:
        """Extract named entities using spaCy (if available)"""
        if not self.nlp_available:
            return []

        try:
            doc = self.nlp(text)
            entities = []

            for ent in doc.ents:
                if ent.label_ in ['PERSON', 'ORG', 'PRODUCT', 'GPE']:
                    entities.append({
                        'text': ent.text,
                        'type': ent.label_
                    })

            return entities
        except Exception as e:
            logger.error(f"Entity extraction failed: {e}")
            return []
