import logging
from dotenv import load_dotenv
import os

load_dotenv()

from typing import Dict

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
        ApplicationBuilder,
        ConversationHandler,
        CommandHandler,
        MessageHandler,
        filters,
        PicklePersistence,
    )
from commands import start, help_command, create_team, add_members, list_members, unknown

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

CHOOSING, CREATING_TEAM, ADDING_MEMBERS, LISTING_MEMBERS,  = range(4)
# reply_keyboard = [
#     ["Создать группу", "Кто в группе"],
#     ["Помощь"],
# ]
# markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

if __name__ == '__main__':
    #persistence = PicklePersistence(filepath="conversationbot")
    application = ApplicationBuilder().token(os.environ.get("TOKEN")).build()


    '''Handler Declarations'''

    team_creation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^Создать группу$"),
                    create_team
                ),
                MessageHandler(
                    filters.Regex("^Кто в группе$"),
                    list_members),
            ],
            CREATING_TEAM: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Стоп!$")),
                    create_team
                )
            ],
            ADDING_MEMBERS: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                    add_members,
                )
            ],
            LISTING_MEMBERS: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                    list_members,
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), start)],
        name="my_conversation",
        persistent=False,
    )
    help_handler = MessageHandler(filters.COMMAND, help_command)

    '''ADDING HANDLERS'''
    application.add_handler(team_creation_handler)
    application.add_handler(help_handler)
    # Handles unknown messages, must be the last one
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()
