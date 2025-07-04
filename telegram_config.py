"""
Configuration file for Telegram Bot
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Bot Settings
BOT_USERNAME = os.getenv('BOT_USERNAME')
MAX_MESSAGE_LENGTH = 4000  # Telegram's limit is 4096
RESPONSE_TIMEOUT = 30  # seconds

# Feature Toggles
ENABLE_INLINE_KEYBOARDS = True
ENABLE_USER_SESSIONS = True
ENABLE_ANALYTICS = True
ENABLE_ERROR_REPORTING = True

# Rate Limiting (to prevent spam)
MAX_REQUESTS_PER_MINUTE = 20
MAX_REQUESTS_PER_HOUR = 100

# Admin Configuration (optional)
ADMIN_USER_IDS = []  # Add admin Telegram user IDs here

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_TO_FILE = True
LOG_FILE = 'telegram_bot.log'

# Welcome Message Customization
WELCOME_MESSAGE_TEMPLATE = """
🎓 **Welcome to Expert Guide Bot!**

Hi {user_name}! I'm your AI expert guide with access to a comprehensive database of courses, tasks, and resources.

🤖 **What I can help you with:**
• Find courses on any topic
• Get practice tasks and exercises  
• Discover learning resources
• Create personalized learning plans
• Answer questions about available content

💬 **Try asking me:**
• "How many courses do you have?"
• "Give me 5 blockchain tasks"
• "Find machine learning courses"
• "I want to learn web development"
• "Show me Python resources"

🚀 **Just send me a message and I'll help you learn!**

Use /help anytime for more guidance.
"""

# Error Messages
ERROR_MESSAGES = {
    'coordinator_not_available': "❌ Educational system is not available right now. Please try again later.",
    'processing_error': "❌ Sorry, I encountered an error processing your request. Please try again.",
    'rate_limit_exceeded': "⏰ You're sending messages too quickly. Please wait a moment and try again.",
    'invalid_token': "❌ Bot token is not configured. Please contact the administrator.",
    'timeout_error': "⏰ Request timed out. Please try a simpler query or try again later."
}

# Quick Reply Templates
QUICK_REPLIES = {
    'more_courses': "📚 Show me more courses",
    'different_topic': "🔄 Search different topic",
    'create_plan': "📋 Create learning plan",
    'get_resources': "🔗 Find resources",
    'get_tasks': "📝 Get practice tasks"
}

# Analytics Events (if enabled)
ANALYTICS_EVENTS = {
    'bot_started': 'bot_started',
    'help_requested': 'help_requested',
    'query_processed': 'query_processed',
    'error_occurred': 'error_occurred',
    'course_listed': 'course_listed',
    'stats_requested': 'stats_requested'
}