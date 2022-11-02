from uuid import uuid4
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

CREATING_TEAM, ADDING_MEMBERS, LISTING_MEMBERS, WAITING, CHOOSING, SHUFFLING, CHOOSING_TO_DO, = range(7)


def show_members(user_data):
    return " \n".join(user_data['team_members'].values())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Помощь"
    )
    return CHOOSING


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [
        ["Создать группу"], ["Я жду"]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    reply_text = ('Привет! Это бот для тайного санты имени трусов хэллоу китти. '
                  'Если хочешь создать новую группу, напиши или выбери кнопку "Создать группу". '
                  'Если ты ждешь, пока тебя распределят, нажми "Я жду"'
                  )
    del context.user_data
    await update.message.reply_text(reply_text, reply_markup=markup)
    return CHOOSING


async def check_in(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Waiting user:", update.effective_message.chat_id)
    if context.bot_data['users'] is None:
        context.bot_data['users'] = [update.effective_message.chat_id]
    else:
        context.bot_data['users'] = context.bot_data['users'].append(update.effective_message.chat_id)


async def create_team(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # user = update.message.from_user
    reply_text = "Введи список тегов тех, кого хочешь добавить к группе, через запятую:"
    await update.message.reply_text(reply_text)

    return ADDING_MEMBERS


async def add_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("ADD_MEMBERS")
    # user = update.message.from_user
    team_members = update.message.parse_entities()
    print(team_members)
    context.user_data['team_members'] = team_members
    print("context: ", context.user_data)
    print("USER DATA:", (context.user_data['team_members'].values() is not None))

    reply_keyboard = [
        ["Показать!"],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    reply_text = "Проверим, все ли указанные тобой теги верные"
    await update.message.reply_text(reply_text, reply_markup=markup)

    if context.user_data['team_members'].values() is not None:
        return LISTING_MEMBERS

    # else:
    #     await context.bot.send_message(
    #         text="Что-то пошло не так!",
    #         chat_id=update.effective_message.chat_id
    #     )
    #     return ADDING_MEMBERS


async def list_members(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print("LIST_MEMBERS")
    reply_keyboard = [
        InlineKeyboardButton(text="Разослать сантам", callback_data=str(SHUFFLING)),
        InlineKeyboardButton(text="Заново ввести группу", callback_data=str(ADDING_MEMBERS)),
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    reply_text = ('Вот кого удалось добавить: \n'
                  + show_members(context.user_data) +
                  '\n Все верно? Тогда жми "Разослать", чтобы санты узнали, кому они дарят подарки!'
                  '\n Или ты кого-то забыла? Тогда придется начать с начала :(')
    # await update.message.reply_text(reply_text, ", ".join(context.user_data.get('team_members').values()))
    await update.message.reply_text(reply_text, reply_markup=markup)
    return SHUFFLING


async def shuffle_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    people_safe = context.user_data['team_members'].items()
    people = people_safe
    santa_s = people
    pairs = {}
    for santa in santa_s:
        potential_recipients = people
        potential_recipients.remove(santa)

        recipient = choice(potential_recipients)
        pairs[santa] = recipient

        people.remove(recipient)

        people = people + [santa]


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ничего не понятно, но очень интересно"
    )

