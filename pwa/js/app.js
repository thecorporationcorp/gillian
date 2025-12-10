/**
 * GILLIAN AI - PRODUCTION-GRADE PWA CLIENT
 * Advanced voice recognition, real-time updates, offline support
 */

class GillianAI {
    constructor() {
        this.apiBase = window.location.origin;
        this.sessionId = this.generateSessionId();
        this.isConnected = false;
        this.recognition = null;
        this.isRecording = false;
        this.conversationHistory = [];

        this.init();
    }

    // ========================================================================
    // INITIALIZATION
    // ========================================================================

    async init() {
        this.cacheElements();
        this.attachEventListeners();
        await this.checkConnection();
        this.setupVoiceRecognition();
        this.loadConversationHistory();
        this.startHeartbeat();

        console.log('✅ Gillian AI initialized');
    }

    cacheElements() {
        this.els = {
            conversation: document.getElementById('conversationContainer'),
            textInput: document.getElementById('textInput'),
            sendBtn: document.getElementById('sendBtn'),
            voiceBtn: document.getElementById('voiceBtn'),
            statusIndicator: document.getElementById('statusIndicator'),
            connectionStatus: document.getElementById('connectionStatus'),
            quickActions: document.querySelectorAll('.quick-action'),
            loadingOverlay: document.getElementById('loadingOverlay'),
            toastContainer: document.getElementById('toastContainer')
        };
    }

    attachEventListeners() {
        // Send button
        this.els.sendBtn.addEventListener('click', () => this.sendMessage());

        // Text input
        this.els.textInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Voice button
        this.els.voiceBtn.addEventListener('mousedown', () => this.startVoiceRecording());
        this.els.voiceBtn.addEventListener('mouseup', () => this.stopVoiceRecording());
        this.els.voiceBtn.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.startVoiceRecording();
        });
        this.els.voiceBtn.addEventListener('touchend', (e) => {
            e.preventDefault();
            this.stopVoiceRecording();
        });

        // Quick actions
        this.els.quickActions.forEach(btn => {
            btn.addEventListener('click', () => {
                const command = btn.getAttribute('data-command');
                this.els.textInput.value = command;
                this.sendMessage();
            });
        });

        // Install prompt
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            this.deferredPrompt = e;
            this.showInstallPrompt();
        });
    }

    // ========================================================================
    // CONNECTION MANAGEMENT
    // ========================================================================

    async checkConnection() {
        try {
            const response = await fetch(`${this.apiBase}/health`);
            const data = await response.json();

            if (data.status === 'online') {
                this.isConnected = true;
                this.updateConnectionStatus('Connected', true);
                this.showToast('Connected to Gillian AI', 'success');
            } else {
                this.updateConnectionStatus('Server error', false);
            }
        } catch (error) {
            this.isConnected = false;
            this.updateConnectionStatus('Offline', false);
            console.error('Connection error:', error);
        }
    }

    updateConnectionStatus(text, connected) {
        const statusDot = this.els.connectionStatus.querySelector('.status-dot');
        const statusText = this.els.connectionStatus.querySelector('.status-text');

        statusDot.style.background = connected ? 'var(--success)' : 'var(--error)';
        statusText.textContent = text;
    }

    startHeartbeat() {
        setInterval(() => this.checkConnection(), 30000); // Every 30 seconds
    }

    // ========================================================================
    // VOICE RECOGNITION
    // ========================================================================

    setupVoiceRecognition() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.warn('Speech recognition not supported');
            this.els.voiceBtn.style.opacity = '0.5';
            this.els.voiceBtn.style.cursor = 'not-allowed';
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US';

        this.recognition.onstart = () => {
            this.isRecording = true;
            this.els.voiceBtn.classList.add('active');
            this.updateVoiceStatus('Listening...');
            this.showToast('Listening...', 'info');
        };

        this.recognition.onresult = (event) => {
            const transcript = Array.from(event.results)
                .map(result => result[0])
                .map(result => result.transcript)
                .join('');

            this.els.textInput.value = transcript;

            // If final result, send automatically
            if (event.results[0].isFinal) {
                setTimeout(() => this.sendMessage(), 500);
            }
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.isRecording = false;
            this.els.voiceBtn.classList.remove('active');
            this.updateVoiceStatus('Hold to speak');

            if (event.error !== 'no-speech') {
                this.showToast(`Voice error: ${event.error}`, 'error');
            }
        };

        this.recognition.onend = () => {
            this.isRecording = false;
            this.els.voiceBtn.classList.remove('active');
            this.updateVoiceStatus('Hold to speak');
        };
    }

    startVoiceRecording() {
        if (!this.recognition || this.isRecording) return;

        try {
            this.recognition.start();
        } catch (error) {
            console.error('Failed to start recording:', error);
        }
    }

    stopVoiceRecording() {
        if (!this.recognition || !this.isRecording) return;

        try {
            this.recognition.stop();
        } catch (error) {
            console.error('Failed to stop recording:', error);
        }
    }

    updateVoiceStatus(text) {
        const status = this.els.voiceBtn.querySelector('.voice-status');
        if (status) status.textContent = text;
    }

    // ========================================================================
    // MESSAGE HANDLING
    // ========================================================================

    async sendMessage() {
        const text = this.els.textInput.value.trim();

        if (!text) return;

        if (!this.isConnected) {
            this.showToast('Not connected to server', 'error');
            return;
        }

        // Clear input immediately
        this.els.textInput.value = '';

        // Add user message to UI
        this.addMessage('user', text);

        // Show loading
        this.showLoading();

        try {
            const response = await fetch(`${this.apiBase}/api/command`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: text,
                    session_id: this.sessionId,
                    device: this.getDeviceInfo()
                })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const data = await response.json();

            // Hide loading
            this.hideLoading();

            // Add assistant response
            if (data.response) {
                this.addMessage('assistant', data.response, data.intent);
                this.speak(data.response);
            }

            // Save to history
            this.saveToHistory({
                user: text,
                assistant: data.response,
                intent: data.intent,
                timestamp: new Date().toISOString()
            });

        } catch (error) {
            console.error('Send message error:', error);
            this.hideLoading();
            this.addMessage('assistant', "I apologize, but I'm having trouble processing that right now. Please try again.", null);
            this.showToast('Failed to send message', 'error');
        }
    }

    addMessage(role, text, metadata = null) {
        // Remove welcome message if present
        const welcome = this.els.conversation.querySelector('.welcome-message');
        if (welcome) {
            welcome.remove();
        }

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        textDiv.textContent = text;

        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = this.formatTime(new Date());

        contentDiv.appendChild(textDiv);

        // Add intent badge if present
        if (metadata && metadata.intent) {
            const intentBadge = document.createElement('div');
            intentBadge.className = 'intent-badge';
            intentBadge.textContent = metadata.intent;
            intentBadge.style.cssText = `
                display: inline-block;
                padding: 4px 8px;
                background: rgba(108, 99, 255, 0.2);
                border-radius: 12px;
                font-size: 10px;
                margin-top: 8px;
                color: var(--primary-light);
            `;
            contentDiv.appendChild(intentBadge);
        }

        contentDiv.appendChild(timeDiv);
        messageDiv.appendChild(contentDiv);
        this.els.conversation.appendChild(messageDiv);

        // Scroll to bottom
        this.els.conversation.scrollTop = this.els.conversation.scrollHeight;
    }

    // ========================================================================
    // TEXT-TO-SPEECH
    // ========================================================================

    speak(text) {
        if (!('speechSynthesis' in window)) {
            console.warn('Speech synthesis not supported');
            return;
        }

        // Cancel any ongoing speech
        speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-GB'; // British accent
        utterance.rate = 1.0;
        utterance.pitch = 1.0;

        // Try to find a British voice
        const voices = speechSynthesis.getVoices();
        const britishVoice = voices.find(v => v.lang.startsWith('en-GB'));
        if (britishVoice) {
            utterance.voice = britishVoice;
        }

        speechSynthesis.speak(utterance);
    }

    // ========================================================================
    // HISTORY MANAGEMENT
    // ========================================================================

    loadConversationHistory() {
        try {
            const history = localStorage.getItem('gillian_history');
            if (history) {
                this.conversationHistory = JSON.parse(history);
                console.log('📜 Loaded conversation history:', this.conversationHistory.length);
            }
        } catch (error) {
            console.error('Failed to load history:', error);
        }
    }

    saveToHistory(entry) {
        this.conversationHistory.push(entry);

        // Keep last 100 entries
        if (this.conversationHistory.length > 100) {
            this.conversationHistory = this.conversationHistory.slice(-100);
        }

        try {
            localStorage.setItem('gillian_history', JSON.stringify(this.conversationHistory));
        } catch (error) {
            console.error('Failed to save history:', error);
        }
    }

    // ========================================================================
    // UI HELPERS
    // ========================================================================

    showLoading() {
        this.els.loadingOverlay.classList.add('active');
    }

    hideLoading() {
        this.els.loadingOverlay.classList.remove('active');
    }

    showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;

        this.els.toastContainer.appendChild(toast);

        // Auto-remove after 3 seconds
        setTimeout(() => {
            toast.style.animation = 'slideInRight 0.3s ease-out reverse';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    showInstallPrompt() {
        const toast = document.createElement('div');
        toast.className = 'toast info';
        toast.innerHTML = `
            <span>Install Gillian AI for offline use</span>
            <button id="installBtn" style="margin-left: auto; padding: 8px 16px; background: var(--primary); border: none; border-radius: 8px; color: white; cursor: pointer;">Install</button>
        `;

        this.els.toastContainer.appendChild(toast);

        document.getElementById('installBtn').addEventListener('click', async () => {
            if (this.deferredPrompt) {
                this.deferredPrompt.prompt();
                const { outcome } = await this.deferredPrompt.userChoice;
                console.log('Install outcome:', outcome);
                this.deferredPrompt = null;
                toast.remove();
            }
        });
    }

    // ========================================================================
    // UTILITIES
    // ========================================================================

    generateSessionId() {
        return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    getDeviceInfo() {
        const ua = navigator.userAgent;
        if (/mobile/i.test(ua)) return 'mobile';
        if (/tablet/i.test(ua)) return 'tablet';
        return 'desktop';
    }

    formatTime(date) {
        return date.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}

// ========================================================================
// INITIALIZE
// ========================================================================

document.addEventListener('DOMContentLoaded', () => {
    window.gillian = new GillianAI();
});
