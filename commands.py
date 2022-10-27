from uuid import uuid4
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

CREATING_TEAM, ADDING_MEMBERS, LISTING_MEMBERS, HELP, CHOOSING, SHUFFLING, CHOOSING_TO_DO, = range(7)


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

    reply_text = ('Привет! Это бот для тайного санты имени трусов хэллоу китти. '
                  'Если хочешь создать новую группу, напиши или выбери кнопку "Создать группу". '
                  'Если хочешь получить список людей в группе, напиши или выбери кнопку "Кто в группе". '
                  )
    if context.user_data:
        del context.user_data
    text = update.message.text.lower()
    context.user_data['choice'] = text
    await update.message.reply_text(reply_text, reply_markup=markup)
    return CHOOSING


async def create_team(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # reply_text = "Введи список тегов тех, кого хочешь добавить к группе, через запятую:"
    # await update.message.reply_text(reply_text)
    await context.bot.send_message(
        text="Введи список тегов тех, кого хочешь добавить к группе, через запятую:",
        chat_id=update.effective_message.chat_id
    )

    return ADDING_MEMBERS


async def add_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    team_members = update.message.parse_entities(types=["user"])
    print(update.message.parse_entities(types=["user"]))
    context.user_data['team_members'] = team_members
    print("context: ", context.user_data)
    if context.user_data['team_members']:
        return LISTING_MEMBERS
    else:
        await context.bot.send_message(
            text="Что-то пошло не так!",
            chat_id=update.effective_message.chat_id
        )
        return ADDING_MEMBERS



async def list_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.lower()
    context.user_data['choice'] = text
    # team_members = update.message.parse_entities(types=["user"])
    # print('team_members', team_members)
    # context.user_data[ADDING_MEMBERS] = team_members
    # print(context.user_data[ADDING_MEMBERS])
    reply_text = "Вот кого удалось добавить:" + context.user_data['team_members']
    # await update.message.reply_text(reply_text, ", ".join(context.user_data.get('team_members').values()))
    await context.bot.send_message(
        text=reply_text,
        chat_id=update.effective_message.chat_id
    )
    # chat_id=update.effective_chat.id,
    return CHOOSING_TO_DO


async def shuffle_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ничего не понятно, но очень интересно"
    )


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ничего не понятно, но очень интересно"
    )

