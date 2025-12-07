#!/usr/bin/env python3
"""
Gillian-EMRY Hybrid Server
A completely LOCAL voice assistant - NO API COSTS!

Replaces expensive Zapier AI with free local NLP + pattern matching
"""

import os
import sys
import json
import secrets
import logging
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import local modules
from database import GillianDB
from intent_detector import IntentDetector
from response_generator import ResponseGenerator
from task_manager import TaskManager

# Load configuration
CONFIG_PATH = Path(__file__).parent / 'config.json'
with open(CONFIG_PATH, 'r') as f:
    CONFIG = json.load(f)

# Paths
BASE_DIR = Path.home() / '.gillian'
DB_PATH = BASE_DIR / 'gillian.db'
MEMORIES_DIR = BASE_DIR / 'memories'

# Ensure directories exist
BASE_DIR.mkdir(parents=True, exist_ok=True)
MEMORIES_DIR.mkdir(parents=True, exist_ok=True)

# Flask app
app = Flask(__name__)
CORS(app)

# Initialize components
db = GillianDB(str(DB_PATH))
intent_detector = IntentDetector(CONFIG['intents'])
response_gen = ResponseGenerator(CONFIG['personality'])
task_manager = TaskManager(db, CONFIG['task_runner'])

# Security (optional - for external access)
API_KEY = os.environ.get('GILLIAN_API_KEY', '')

def validate_request():
    """Optional API key validation for external requests"""
    if not API_KEY:
        return True  # No security if no key set

    # Allow localhost without auth
    if request.remote_addr in ['127.0.0.1', 'localhost', '::1']:
        return True

    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header.replace('Bearer ', '') == API_KEY

    return False


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'version': CONFIG['version'],
        'personality': CONFIG['personality']['name'],
        'cost': 'FREE (100% local)'
    })


@app.route('/command', methods=['POST'])
def handle_command():
    """
    Main endpoint for voice commands from iPhone Shortcut

    Expects JSON:
    {
        "text": "open chrome",
        "device": "iphone",
        "client_time": "2025-12-07T10:30:00"
    }

    Returns PLAIN TEXT response (what iPhone will speak)
    """
    try:
        if not validate_request():
            return Response("Unauthorized", status=401)

        # Get input
        data = request.get_json()
        if not data or 'text' not in data:
            return Response(
                response_gen.get_error(),
                status=400,
                mimetype='text/plain'
            )

        command_text = data.get('text', '').strip()
        device = data.get('device', 'unknown')
        client_time = data.get('client_time', datetime.now().isoformat())

        if not command_text:
            return Response(
                response_gen.get_error(),
                mimetype='text/plain'
            )

        logger.info(f"Command received: '{command_text}' from {device}")

        # Detect intent (100% LOCAL - no API calls!)
        intent_result = intent_detector.detect(command_text)

        logger.info(f"Intent detected: {intent_result['intent']} (confidence: {intent_result['confidence']})")

        # Log command to database
        command_id = db.log_command(
            utterance=command_text,
            intent=intent_result['intent'],
            confidence=intent_result['confidence'],
            device=device,
            client_time=client_time
        )

        # Handle based on intent
        speak_text = ""

        if intent_result['intent'] == 'pc_task':
            # Queue PC task
            task_data = intent_result.get('task_data', {})
            task_id = task_manager.queue_task(
                summary=f"{intent_result.get('action', 'execute')}: {task_data.get('target', 'unknown')}",
                command=task_data.get('command', ''),
                risk_level=task_data.get('risk_level', 'low')
            )

            speak_text = response_gen.get_confirmation() + f" Task {task_id} queued."

        elif intent_result['intent'] == 'note':
            # Save as a note/memory
            note_content = intent_result.get('note_content', command_text)
            db.save_note(note_content, client_time)

            speak_text = response_gen.get_acknowledgment() + " Note saved."

        elif intent_result['intent'] == 'query':
            # Answer query from memory
            query_type = intent_result.get('query_type', 'unknown')

            if query_type == 'task_status':
                pending = task_manager.get_pending_count()
                speak_text = f"You have {pending} pending tasks, sir."

            elif query_type == 'recent_notes':
                notes = db.get_recent_notes(limit=3)
                if notes:
                    speak_text = f"Your recent notes: {', '.join(notes[:2])}"
                else:
                    speak_text = "No recent notes found."

            else:
                speak_text = "I'm checking on that for you."

        elif intent_result['intent'] == 'system':
            # System commands (be careful!)
            action = intent_result.get('action', '')

            if CONFIG['task_runner']['safe_mode']:
                speak_text = "System commands require safe mode to be disabled."
            else:
                speak_text = f"System {action} initiated."

        else:
            # Fallback
            speak_text = response_gen.get_acknowledgment()

        # Update command log with response
        db.update_command_response(command_id, speak_text)

        logger.info(f"Response: {speak_text}")

        # Return PLAIN TEXT (iPhone will speak this)
        return Response(
            response=speak_text,
            mimetype='text/plain',
            status=200
        )

    except Exception as e:
        logger.error(f"Error handling command: {e}", exc_info=True)
        return Response(
            response=response_gen.get_error(),
            mimetype='text/plain',
            status=500
        )


@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all pending tasks (for debugging)"""
    if not validate_request():
        return jsonify({'error': 'Unauthorized'}), 401

    tasks = task_manager.get_all_tasks()
    return jsonify({'tasks': tasks})


@app.route('/stats', methods=['GET'])
def get_stats():
    """Get usage statistics"""
    if not validate_request():
        return jsonify({'error': 'Unauthorized'}), 401

    stats = db.get_stats()
    return jsonify(stats)


@app.route('/history', methods=['GET'])
def get_history():
    """Get command history"""
    if not validate_request():
        return jsonify({'error': 'Unauthorized'}), 401

    limit = int(request.args.get('limit', 20))
    history = db.get_command_history(limit)
    return jsonify({'history': history})


def start_server():
    """Start the Gillian server"""
    host = CONFIG['server']['host']
    port = CONFIG['server']['port']
    use_ngrok = CONFIG['server']['use_ngrok']

    print('\n' + '=' * 70)
    print('  GILLIAN-EMRY HYBRID SERVER v1.0')
    print('  💯 100% LOCAL - ZERO API COSTS')
    print('=' * 70)
    print(f'\n🚀 Server starting on http://{host}:{port}')

    # Start ngrok if enabled
    ngrok_url = None
    if use_ngrok:
        try:
            from pyngrok import ngrok as ngrok_lib

            # Set auth token if provided
            auth_token = CONFIG['server'].get('ngrok_authtoken', '')
            if auth_token:
                ngrok_lib.set_auth_token(auth_token)

            # Start tunnel
            ngrok_url = ngrok_lib.connect(port, bind_tls=True)
            print(f'\n🌐 ngrok tunnel active: {ngrok_url}')
            print('   Use this URL in your iPhone Shortcut!')
            print(f'   Command endpoint: {ngrok_url}/command')

        except Exception as e:
            logger.warning(f'ngrok failed to start: {e}')
            print('\n⚠️  ngrok not available - using local-only mode')
            print('   iPhone must be on same network')

    print(f'\n🧠 Intelligence: Local NLP (spaCy) - FREE!')
    print(f'💾 Database: SQLite at {DB_PATH}')
    print(f'🎭 Personality: {CONFIG["personality"]["name"]} ({CONFIG["personality"]["accent"]})')

    if API_KEY:
        print(f'🔐 Security: API Key enabled')
        print(f'   Key: {API_KEY[:10]}...')

    print('\n📝 Endpoints:')
    print('   POST /command  - Voice command input (for iPhone)')
    print('   GET  /health   - Health check')
    print('   GET  /tasks    - View task queue')
    print('   GET  /stats    - Usage statistics')
    print('   GET  /history  - Command history')

    print('\n✅ Ready! Press Ctrl+C to stop.\n')

    # Start Flask
    app.run(
        host=host,
        port=port,
        debug=False
    )


if __name__ == '__main__':
    start_server()
