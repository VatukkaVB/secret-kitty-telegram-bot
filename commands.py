from uuid import uuid4
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

CHOOSING, CREATING_TEAM, ADDING_MEMBERS, LISTING_MEMBERS,  = range(4)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Помощь"
    )
    return CHOOSING


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    reply_keyboard = [
        ["Создать группу", "Кто в группе"],
        ["Помощь"],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    reply_text = "Привет! Это бот для тайного санты имени трусов хэллоу китти. "

    if context.user_data.get("team_name"):
        print("team_name:", context.user_data.get("team_name"))
        reply_text += (
            f' Ты уже состоишь в группе {context.user_data.get("team_name")}. '
            'Если хочешь создать новую группу, напиши "Создать группу". '
            'Если хочешь получить список людей в группе, напиши "Кто в группе". '
        )
        await update.message.reply_text(reply_text, reply_markup=markup)
        return CHOOSING
    else:
        reply_text += (
            'Ты не принадлежишь ни к какой группе! '
            'Для создания новой группы введи название: '
        )
    await update.message.reply_text(reply_text, reply_markup=None)
    return CREATING_TEAM


async def create_team(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    await update.callback_query.answer()
    team_name = update.message.text
    context.user_data['team_name'] = team_name
    if context.user_data.get(team_name) == team_name:
        reply_text = (
            f"Группа {team_name} уже есть!"
        )
    else:
        reply_text = f'{team_name}? Отличное название! Давай введем список участников. Напиши "Ввести".'
    await update.message.reply_text(reply_text)

    return ADDING_MEMBERS


async def add_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Введи список тегов тех, кого хочешь добавить к группе, через запятую:"
    )
    team_members = update.message.parse_entities()
    print("УЧАСТНИКИ ГРУППЫ:", team_members)
    context.user_data['team_members'] = team_members
    return LISTING_MEMBERS


async def list_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    team_name = update.message.text
    return CHOOSING


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ничего не понятно, но очень интересно"
    )