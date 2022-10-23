from uuid import uuid4
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

CREATING_TEAM, LISTING_MEMBERS, HELP, CHOOSING, SHUFFLING, = range(5)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Помощь"
    )
    return CREATING_TEAM


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [
        ["Создать группу", "Кто в группе"],
        ["Помощь"],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    reply_text = ('Привет! Это бот для тайного санты имени трусов хэллоу китти. '
                  'Если хочешь создать новую группу, напиши или выбери кнопку "Создать группу". '
                  'Если хочешь получить список людей в группе, напиши или выбери кнопку "Кто в группе". '
                  )
    await update.message.reply_text(reply_text, reply_markup=markup)
    return CHOOSING


async def create_team(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_text = "Введи список тегов тех, кого хочешь добавить к группе, через запятую:"
    await update.message.reply_text(reply_text)
    # context.bot.send_message(
    #     text="Введи список тегов тех, кого хочешь добавить к группе, через запятую:",
    #     chat_id=
    # )
    message = update.message
    team_members = message.parse_entities()
    context.user_data['team_members'] = team_members
    return LISTING_MEMBERS


async def list_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("УЧАСТНИКИ ГРУППЫ:", context.user_data.get('team_members'))
    await update.message.reply_text(context.user_data['team_members'])
    # chat_id=update.effective_chat.id,
    return CHOOSING


async def shuffling_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ничего не понятно, но очень интересно"
    )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ничего не понятно, но очень интересно"
    )

