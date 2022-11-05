import logging
from dotenv import load_dotenv
import os
from typing import Dict
from telegram import __version__ as TG_VER
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
        ApplicationBuilder,
        ConversationHandler,
        CommandHandler,
        MessageHandler,
        filters,
        PicklePersistence,
    )

from commands import (
    start,
    check_in,
    help_command,
    create_team,
    add_members,
    # choose_show,
    list_members,
    shuffle_members,
    finish,
    unknown
)

load_dotenv()


try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type:ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

CREATING_TEAM, ADDING_MEMBERS, LISTING_MEMBERS, WAITING, CHOOSING, SHUFFLING, CHOOSING_TO_DO, FINISHING, = range(8)


def main() -> None:

    persistence = PicklePersistence(filepath="bot_data")
    application = ApplicationBuilder().token(os.environ.get("TOKEN")).persistence(persistence).build()

    '''Handler Declarations'''

    team_creation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^Создать группу$"),
                    create_team
                ),
            ],
            WAITING: [
                MessageHandler(
                    filters.Regex("^Я жду$"),
                    check_in
                ),
            ],
            CREATING_TEAM: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Создать группу$")),
                    create_team
                ),
                MessageHandler(
                    filters.Regex("^Заново ввести группу$"),
                    create_team
                )
            ],
            ADDING_MEMBERS: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Создать группу$")),
                    add_members
                )
            ],
            LISTING_MEMBERS: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Кто в группе$")),
                    list_members
                )
            ],
            CHOOSING_TO_DO: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Создать группу$")),
                    shuffle_members
                ),
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Создать группу$")),
                    create_team
                ),
            ],
            SHUFFLING: [
                MessageHandler(
                    filters.Regex("^Разослать сантам$"),
                    shuffle_members,
                )
            ],
            FINISHING: [
                MessageHandler(
                    filters.Regex("^Ну как?$"),
                    finish,
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), start)],
        name="my_conversation",
        persistent=True,
    )
    help_handler = MessageHandler(filters.COMMAND, help_command)

    '''ADDING HANDLERS'''
    application.add_handler(team_creation_handler)
    application.add_handler(help_handler)
    # Handles unknown messages, must be the last one
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
