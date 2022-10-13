import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    application = ApplicationBuilder().token('TOKEN').build()

    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    # Handles unknown messages, must be the last one
    application.add_handler(unknown_handler)

    application.run_polling()