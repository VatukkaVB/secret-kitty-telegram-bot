from random import choice
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    )
import MyLogger
import logging
import re

CREATING_TEAM, ADDING_MEMBERS, LISTING_MEMBERS, WAITING, CHOOSING, SHUFFLING, CHOOSING_TO_DO, FINISHING, = range(8)

logging.basicConfig(
    filename='santa_bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def show_members(user_data):
    return " \n".join(user_data['team_members'].values())


def shuffle(people):
    pairs = {}
    for santa in people:
        potential_recipients = [person for person in people if person != santa and person not in pairs.values()]
        recipient = choice(potential_recipients)
        pairs[santa] = recipient
    return pairs


def get_logged_users():
    with open('santa_bot.log', 'r') as log_file:
        logs = log_file.read()
        users = re.findall(r"([A-Z|a-z|0-9]* : \d*)", logs)
        users_info = {}
        for user in users:
            un_id = user.split(" : ")
            users_info[un_id[0]] = un_id[1]
    return users_info


def get_needed_users(users_info, needed_uns):
    un_id = {}
    for key in users_info.keys():
        if key in needed_uns:
            un_id[key] = users_info[key]
    return un_id


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
    user = update.message.from_user
    logger.info("Started the conversation USER: " + str(user.username) + " : " + str(user.id))
    reply_text = ('Привет! Это бот для тайного санты имени трусов хэллоу китти. '
                  'Если хочешь создать новую группу, напиши или выбери кнопку "Создать группу". '
                  'Если ты ждешь, пока тебя распределят, нажми "Я жду"'
                  )
    try:
        del context.user_data
    except AttributeError:
        pass
    user = update.message.from_user
    await update.message.reply_text(reply_text, reply_markup=markup)
    return CHOOSING


async def check_in(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("\tWaiting user:", update.effective_message.chat_id)
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
    print("\tcontext: ", context.user_data)
    print("\tUSER DATA:", (context.user_data['team_members'].values() is not None))

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
    buttons = [
        ["Разослать сантам"],
        ["Заново ввести группу"],
    ]
    markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    reply_text = ('Вот кого удалось добавить: \n'
                  + show_members(context.user_data) +
                  '\n Все верно? Тогда жми "Разослать", чтобы санты узнали, кому они дарят подарки!'
                  '\n Или ты кого-то забыла? Тогда придется начать с начала :(')
    # await update.message.reply_text(reply_text, ", ".join(context.user_data.get('team_members').values()))
    await update.message.reply_text(reply_text, reply_markup=markup)
    return SHUFFLING


def show_pairs(pairs):
    return " ".join(pairs.items())


async def shuffle_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("SHUFFLE_MEMBERS")
    reply_keyboard = [["Ну как?"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    people = list(context.user_data['team_members'].values())
    try:
        pairs = shuffle(people)
        reply_text = "Успешно сгенерировали пары!"
    except IndexError:
        pairs = shuffle(people)
        reply_text = "Уф, это было нелегко, но мы сгенерировали пары!" + show_pairs(pairs)
    print("\tСформированные пары:", pairs)
    await update.message.reply_text(reply_text, reply_markup=markup)
    # await update.message.reply_text(reply_text)

    for key in pairs.keys():
        recipient = pairs[key]


    photo = "https://icdn.lenta.ru/images/2021/10/21/11/20211021110546130/square_320_2ae978183310b7a3e921e8628b2c3314.jpeg"
    await update.message.reply_photo(photo)
    return ConversationHandler.END


# async def finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     print("END")
#     photo = "https://icdn.lenta.ru/images/2021/10/21/11/20211021110546130/square_320_2ae978183310b7a3e921e8628b2c3314.jpeg"
#     await update.message.reply_photo(photo)
#     return ConversationHandler.END


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Ничего не понятно, но очень интересно"
    )

