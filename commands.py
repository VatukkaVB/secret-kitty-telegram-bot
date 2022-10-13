from uuid import uuid4
from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет! Это бот для тайного санты имени трусов хэллоу китти."
    )


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Чтобы корректно распределить дарителей и получателей, все они должны активировать этого бота, иначе не получат уведомление! \
             Чтобы указать тех, кто участвует в распределении, используй команду /create_team."
    )


async def create_team(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Введи название группы:"
    )
    team_name = update.message.text


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ничего не понятно, но очень интересно"
    )