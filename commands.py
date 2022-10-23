from uuid import uuid4
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

CHOOSING, CREATING_TEAM, ADDING_MEMBERS, LISTING_MEMBERS, = range(4)


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
        reply_text += f' Ты уже состоишь в группе {context.user_data.get("team_name")}. '

    reply_text += ('Если хочешь создать новую группу, напиши или выбери кнопку "Создать группу". '
                   'Если хочешь получить список людей в группе, напиши или выбери кнопку "Кто в группе". '
                   )
    await update.message.reply_text(reply_text, reply_markup=markup)
    return CHOOSING


async def create_team(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_text = 'Введи название группы, которую хочешь создать:'
    await update.message.reply_text(reply_text)
    team_name = update.message.text
    context.user_data['team_name'] = team_name
    if context.user_data.get(team_name) == team_name:
        reply_text = (
            f"Группа {team_name} уже есть!"
        )
        await update.message.reply_text(reply_text)
        return CHOOSING
    else:
        return ADDING_MEMBERS


async def add_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    update.message.reply_text("Введи список тегов тех, кого хочешь добавить к группе, через запятую:"
    )
    # context.bot.send_message(
    #     text="Введи список тегов тех, кого хочешь добавить к группе, через запятую:",
    #     chat_id=
    # )
    print("Сообщение:", update.message.text)
    team_members = update.message.parse_entities()
    context.user_data['team_members'] = team_members
    print("УЧАСТНИКИ ГРУППЫ:", team_members)
    return LISTING_MEMBERS


async def list_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=context.user_data.get("team_members")
    )
    return CHOOSING


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ничего не понятно, но очень интересно"
    )
