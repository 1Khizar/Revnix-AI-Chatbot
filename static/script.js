// Configuration
const API_BASE_URL = window.location.origin;
const ENDPOINTS = {
    chat: `${API_BASE_URL}/api/chat`,
    health: `${API_BASE_URL}/api/health`
};

// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const typingIndicator = document.getElementById('typing-indicator');
const clearChatBtn = document.getElementById('clear-chat');
const statusText = document.getElementById('status-text');
const charCount = document.getElementById('char-count');
const toastEl = document.getElementById('toast');

// State
let isProcessing = false;
let conversationHistory = [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
    checkHealth();
});

// Initialize application
function initializeApp() {
    // Auto-resize textarea
    userInput.addEventListener('input', () => {
        autoResizeTextarea();
        updateCharCount();
    });
    
    // Load conversation history
    loadConversationHistory();
    
    // Focus input
    userInput.focus();
}

// Setup event listeners
function setupEventListeners() {
    // Form submission
    chatForm.addEventListener('submit', handleSubmit);
    
    // Clear chat
    clearChatBtn.addEventListener('click', handleClearChat);
    
    // Quick action buttons
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('quick-btn')) {
            const question = e.target.getAttribute('data-question');
            if (question) {
                userInput.value = question;
                handleSubmit(e);
            }
        }
    });
    
    // Enter key handling
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });
}

// Check API health
async function checkHealth() {
    try {
        const response = await fetch(ENDPOINTS.health);
        const data = await response.json();
        
        if (data.status === 'healthy' && data.agent_ready) {
            updateStatus('online', 'Ready to chat');
        } else {
            updateStatus('warning', 'Initializing...');
            setTimeout(checkHealth, 2000);
        }
    } catch (error) {
        console.error('Health check failed:', error);
        updateStatus('error', 'Connection error');
        showToast('Unable to connect to the server. Please refresh the page.', 'error');
    }
}

// Update status indicator
function updateStatus(status, text) {
    const statusDot = document.querySelector('.status-dot');
    statusText.textContent = text;
    
    statusDot.classList.remove('online', 'warning', 'error');
    if (status === 'online') {
        statusDot.classList.add('online');
    }
}

// Handle form submission
async function handleSubmit(e) {
    e.preventDefault();
    
    const question = userInput.value.trim();
    
    if (!question || isProcessing) return;
    
    // Disable input
    isProcessing = true;
    sendBtn.disabled = true;
    userInput.disabled = true;
    
    // Add user message
    addMessage(question, 'user');
    
    // Clear input
    userInput.value = '';
    updateCharCount();
    autoResizeTextarea();
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        // Send request
        const response = await fetch(ENDPOINTS.chat, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Hide typing indicator
        hideTypingIndicator();
        
        // Add bot response
        addMessage(data.answer, 'bot');
        
        // Save conversation
        saveConversation(question, data.answer);
        
    } catch (error) {
        console.error('Error:', error);
        hideTypingIndicator();
        
        const errorMessage = 'Sorry, I encountered an error. Please try again.';
        addMessage(errorMessage, 'bot');
        showToast('Failed to get response. Please try again.', 'error');
    } finally {
        // Enable input
        isProcessing = false;
        sendBtn.disabled = false;
        userInput.disabled = false;
        userInput.focus();
    }
}

// Add message to chat
function addMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = `message-avatar ${type}-avatar`;
    
    const avatarSvg = type === 'bot' 
        ? `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
             <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
             <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
           </svg>`
        : `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
             <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
             <circle cx="12" cy="7" r="4"></circle>
           </svg>`;
    
    avatarDiv.innerHTML = avatarSvg;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    
    // Format text (preserve line breaks, make links clickable)
    const formattedText = formatMessageText(text);
    textDiv.innerHTML = formattedText;
    
    contentDiv.appendChild(textDiv);
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom with animation
    scrollToBottom();
}

// Format message text
function formatMessageText(text) {
    // Convert URLs to links
    text = text.replace(
        /(https?:\/\/[^\s]+)/g,
        '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
    );
    
    // Convert line breaks
    text = text.replace(/\n/g, '<br>');
    
    // Convert **bold** to <strong>
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Convert *italic* to <em>
    text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
    
    return text;
}

// Show typing indicator
function showTypingIndicator() {
    typingIndicator.style.display = 'flex';
    scrollToBottom();
}

// Hide typing indicator
function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

// Scroll to bottom
function scrollToBottom() {
    setTimeout(() => {
        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    }, 100);
}

// Auto-resize textarea
function autoResizeTextarea() {
    userInput.style.height = 'auto';
    userInput.style.height = Math.min(userInput.scrollHeight, 120) + 'px';
}

// Update character count
function updateCharCount() {
    const count = userInput.value.length;
    charCount.textContent = `${count}/500`;
    
    if (count > 450) {
        charCount.style.color = 'var(--warning)';
    } else if (count > 480) {
        charCount.style.color = 'var(--error)';
    } else {
        charCount.style.color = 'var(--text-muted)';
    }
}

// Clear chat
function handleClearChat() {
    if (confirm('Are you sure you want to clear the conversation?')) {
        // Remove all messages except welcome message
        const messages = chatMessages.querySelectorAll('.message:not(.welcome-message)');
        messages.forEach(msg => msg.remove());
        
        // Clear storage
        conversationHistory = [];
        localStorage.removeItem('revnix_conversation');
        
        showToast('Conversation cleared!', 'success');
        userInput.focus();
    }
}

// Save conversation
function saveConversation(question, answer) {
    conversationHistory.push({
        question,
        answer,
        timestamp: new Date().toISOString()
    });
    
    // Keep only last 50 exchanges
    if (conversationHistory.length > 50) {
        conversationHistory = conversationHistory.slice(-50);
    }
    
    try {
        localStorage.setItem('revnix_conversation', JSON.stringify(conversationHistory));
    } catch (e) {
        console.warn('Could not save conversation history:', e);
    }
}

// Load conversation history
function loadConversationHistory() {
    try {
        const saved = localStorage.getItem('revnix_conversation');
        if (saved) {
            conversationHistory = JSON.parse(saved);
            
            // Restore messages (limit to last 10 exchanges)
            const recentHistory = conversationHistory.slice(-10);
            recentHistory.forEach(({ question, answer }) => {
                addMessage(question, 'user');
                addMessage(answer, 'bot');
            });
        }
    } catch (e) {
        console.warn('Could not load conversation history:', e);
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    toastEl.textContent = message;
    toastEl.className = `toast ${type}`;
    
    // Trigger reflow
    void toastEl.offsetWidth;
    
    toastEl.classList.add('show');
    
    setTimeout(() => {
        toastEl.classList.remove('show');
    }, 3000);
}

// Add CSS for links in messages
const style = document.createElement('style');
style.textContent = `
    .message-text a {
        color: var(--primary-light);
        text-decoration: underline;
        transition: color var(--transition-base);
    }
    .message-text a:hover {
        color: var(--primary);
    }
    .user-message .message-text a {
        color: rgba(255, 255, 255, 0.9);
    }
    .user-message .message-text a:hover {
        color: white;
    }
    .message-text strong {
        font-weight: 600;
        color: var(--text-primary);
    }
    .message-text em {
        font-style: italic;
        color: var(--text-secondary);
    }
`;
document.head.appendChild(style);