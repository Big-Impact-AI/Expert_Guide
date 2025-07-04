"""
Fixed Telegram Bot for Educational RAG System
Compatible with python-telegram-bot v20+
"""

import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

import telegram_config
from simple_working_coordinator import SimpleWorkingCoordinator
import traceback
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


class EducationalTelegramBot:
    """Telegram bot that uses the educational RAG system."""

    def __init__(self, telegram_token: str):
        self.telegram_token = telegram_token
        self.coordinator = None
        self.user_sessions = {}  # Track user conversation history

    def initialize_coordinator(self):
        """Initialize the educational coordinator synchronously."""
        try:
            self.coordinator = SimpleWorkingCoordinator()
            logger.info("✅ Educational coordinator initialized successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to initialize coordinator: {e}")
            return False

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        user = update.effective_user
        user_id = user.id

        # Initialize user session
        self.user_sessions[user_id] = {
            'started_at': datetime.now(),
            'message_count': 0,
            'last_query': None
        }

        welcome_text = f"""🎓 **Welcome to Educational Assistant Bot!**

Hi {user.first_name}! I'm your AI educational assistant with access to a comprehensive database of courses, tasks, and resources.

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

Use /help anytime for more guidance."""

        # Create quick action buttons
        keyboard = [
            [
                InlineKeyboardButton("📚 List All Courses", callback_data="list_courses"),
                InlineKeyboardButton("📊 Database Stats", callback_data="stats")
            ],
            [
                InlineKeyboardButton("🔍 Search Topics", callback_data="search_help"),
                InlineKeyboardButton("❓ Help", callback_data="help")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            welcome_text,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        help_text = """📚 **Educational Assistant Bot Help**

🎯 **What you can ask me:**

**📊 Database Information:**
• "How many courses are there?"
• "List all courses"
• "What content do you have?"

**🔍 Search for Content:**
• "Find [topic] courses" (e.g., "Find Python courses")
• "Give me [number] [topic] tasks" (e.g., "Give me 5 blockchain tasks")
• "Show me [topic] resources" (e.g., "Show me data science resources")

**📋 Learning Plans:**
• "I want to learn [topic]"
• "Create a learning plan for [topic]"
• "Help me learn [topic] in [timeframe]"

**💡 Example Questions:**
• "Give me 5 machine learning tasks"
• "Find beginner Python courses"  
• "I want to learn web development in 2 months"
• "Show me blockchain resources"
• "What economics courses do you have?"

**⚡ Quick Commands:**
/start - Restart the bot
/help - Show this help
/stats - Database statistics
/courses - List all courses

**🎯 Tips:**
• Be specific about topics you're interested in
• Mention skill level (beginner, intermediate, advanced)
• Ask for specific numbers of items if you want more results
• I search real database content, so I'll show you actual courses and tasks!

Just send me any learning-related question and I'll help! 🚀"""

        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /stats command."""
        await update.message.reply_text("📊 Getting database statistics...")

        try:
            result = self.coordinator.process_query("How many courses are there?")
            await update.message.reply_text(f"📊 **Database Statistics**\n\n{result}", parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Error getting stats: {e}")

    async def courses_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /courses command."""
        await update.message.reply_text("📚 Getting list of all courses...")

        try:
            result = self.coordinator.process_query("List all courses")

            # Split long messages if needed
            if len(result) > 4000:
                chunks = [result[i:i + 3800] for i in range(0, len(result), 3800)]
                for i, chunk in enumerate(chunks):
                    if i == 0:
                        await update.message.reply_text(f"📚 **Available Courses (Part {i + 1})**\n\n{chunk}",
                                                        parse_mode='Markdown')
                    else:
                        await update.message.reply_text(f"**Part {i + 1} (continued)**\n\n{chunk}",
                                                        parse_mode='Markdown')

                    # Small delay between messages
                    if i < len(chunks) - 1:
                        await asyncio.sleep(1)
            else:
                await update.message.reply_text(result, parse_mode='Markdown')

        except Exception as e:
            await update.message.reply_text(f"❌ Error getting courses: {e}")

    async def handle_callback_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks."""
        query = update.callback_query
        await query.answer()

        if query.data == "list_courses":
            await query.message.reply_text("📚 Getting all courses...")
            try:
                result = self.coordinator.process_query("List all courses")
                # Handle long messages
                if len(result) > 3800:
                    result = result[:3800] + "\n\n... (use /courses for full list)"
                await query.message.reply_text(result, parse_mode='Markdown')
            except Exception as e:
                await query.message.reply_text(f"❌ Error: {e}")

        elif query.data == "stats":
            await query.message.reply_text("📊 Getting database statistics...")
            try:
                result = self.coordinator.process_query("How many courses are there?")
                await query.message.reply_text(result, parse_mode='Markdown')
            except Exception as e:
                await query.message.reply_text(f"❌ Error: {e}")

        elif query.data == "search_help":
            help_text = """🔍 **Search Examples:**

**Quick Searches:**
• "blockchain tasks"
• "Python courses"  
• "data science resources"

**Specific Requests:**
• "Give me 5 machine learning tasks"
• "Find beginner web development courses"
• "Show me 10 JavaScript exercises"

**Learning Plans:**
• "I want to learn AI"
• "Help me become a full-stack developer"
• "Create a blockchain learning plan"

Just type any of these or your own question! 🚀"""
            await query.message.reply_text(help_text, parse_mode='Markdown')

        elif query.data == "help":
            await self.help_command(update, context)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages."""
        user = update.effective_user
        user_id = user.id
        message_text = update.message.text

        # Update user session
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = {
                'started_at': datetime.now(),
                'message_count': 0,
                'last_query': None
            }

        self.user_sessions[user_id]['message_count'] += 1
        self.user_sessions[user_id]['last_query'] = message_text

        # Show typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')

        # Log the query
        logger.info(f"User {user_id} ({user.first_name}): {message_text}")

        try:
            # Check if coordinator is available
            if not self.coordinator:
                await update.message.reply_text(
                    "❌ Educational system is not available right now. Please try again later."
                )
                return

            # Process the query
            start_time = time.time()
            result = self.coordinator.process_query(message_text)
            processing_time = time.time() - start_time

            # Handle long responses by splitting them
            max_length = 3800  # Leave some room for formatting

            if len(result) > max_length:
                # Split into chunks
                chunks = []
                lines = result.split('\n')
                current_chunk = ""

                for line in lines:
                    # If adding this line would exceed limit, start new chunk
                    if len(current_chunk + line + '\n') > max_length:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                            current_chunk = line + '\n'
                        else:
                            # Single line is too long, force split
                            chunks.append(line[:max_length])
                            current_chunk = line[max_length:] + '\n'
                    else:
                        current_chunk += line + '\n'

                if current_chunk.strip():
                    chunks.append(current_chunk.strip())

                # Send chunks
                for i, chunk in enumerate(chunks):
                    if i == 0:
                        await update.message.reply_text(
                            f"🤖 **Educational Assistant** (Part {i + 1}/{len(chunks)}):\n\n{chunk}",
                            parse_mode='Markdown'
                        )
                    else:
                        await update.message.reply_text(
                            f"**Part {i + 1}/{len(chunks)} (continued):**\n\n{chunk}",
                            parse_mode='Markdown'
                        )

                    # Small delay between chunks
                    if i < len(chunks) - 1:
                        await asyncio.sleep(1)
            else:
                await update.message.reply_text(
                    f"🤖 **Educational Assistant:**\n\n{result}",
                    parse_mode='Markdown'
                )

            # Add quick action buttons for certain types of responses
            if any(word in message_text.lower() for word in ['course', 'list', 'show', 'find']):
                keyboard = [
                    [
                        InlineKeyboardButton("🔍 Search More", callback_data="search_help"),
                        InlineKeyboardButton("📊 Stats", callback_data="stats")
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text(
                    "💡 What else would you like to explore?",
                    reply_markup=reply_markup
                )

            logger.info(f"Response sent to {user_id} in {processing_time:.2f}s")

        except Exception as e:
            error_msg = f"❌ Sorry, I encountered an error: {str(e)[:100]}..."
            await update.message.reply_text(error_msg)
            logger.error(f"Error processing message from {user_id}: {e}")
            logger.error(traceback.format_exc())

    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors."""
        logger.error(f"Exception while handling an update: {context.error}")

        try:
            if update and update.effective_message:
                await update.effective_message.reply_text(
                    "❌ An unexpected error occurred. Please try again."
                )
        except:
            pass  # Avoid error loops

    def run(self):
        """Run the telegram bot."""
        print("🚀 Starting Educational Telegram Bot...")

        # Initialize coordinator first (synchronously)
        success = self.initialize_coordinator()
        if not success:
            print("❌ Failed to initialize educational coordinator!")
            return

        print("✅ Educational coordinator ready!")

        # Create application
        application = Application.builder().token(self.telegram_token).build()

        # Add handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("stats", self.stats_command))
        application.add_handler(CommandHandler("courses", self.courses_command))
        application.add_handler(CallbackQueryHandler(self.handle_callback_query))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        application.add_error_handler(self.error_handler)

        print("✅ Educational Telegram Bot is running!")
        print("💬 Send messages to your bot to test it!")
        print("🛑 Press Ctrl+C to stop the bot")

        # Run the bot
        try:
            application.run_polling(
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )
        except KeyboardInterrupt:
            print("\n👋 Bot stopped by user")
        except Exception as e:
            print(f"❌ Bot error: {e}")
            logger.error(f"Bot error: {e}")


def main():
    """Main function to run the bot."""
    # You need to set your Telegram Bot Token here
    # Get it from @BotFather on Telegram
    TELEGRAM_TOKEN = telegram_config.TELEGRAM_BOT_TOKEN

    if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("❌ Please set your Telegram Bot Token!")
        print("\n📝 How to get a Telegram Bot Token:")
        print("1. Open Telegram and search for @BotFather")
        print("2. Send /newbot to create a new bot")
        print("3. Follow the instructions to name your bot")
        print("4. Copy the token and replace it in this file")
        print("5. Run this script again")
        return

    try:
        bot = EducationalTelegramBot(TELEGRAM_TOKEN)
        bot.run()
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")
        logger.error(f"Failed to start bot: {e}")


if __name__ == "__main__":
    main()