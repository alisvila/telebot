import requests
from osticket import *
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, RegexHandler
from flask import Flask, request
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


bot_token = "545110014:AAFL9tBt7h93I2fywdCnFU-U7FYeLi77aQY"
updater = Updater(token=bot_token)

app = Flask(__name__)
NAMEENTRY, EMAILENTRY, FIRST_CHOICE =range(3)
SETUP, NEWACC, USERNAME=range(3)
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

start_keyboard = [['shop', 'contact support']]
markup_start = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True, resize_keyboard=True)

reply_keyboard = [['name', 'message'],
                  ['email', 'phone number'],
                  ['Done']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data):
    facts = list()

    for key, value in user_data.items():
        facts.append('{} - {}'.format(key, value))

    return "\n".join(facts).join(['\n', '\n'])


def start(bot, update):

    update.message.reply_text(
        "plz tell us how can we help u",
        reply_markup=markup_start)

    return CHOOSING
    # register_text="ok"
    # update.message.reply_text(register_text, reply_markup=ReplyKeyboardRemove())
    # bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

    # text="another ok"
    # update.message.reply_text(text, parse_mode="Markdown", reply_markup=ReplyKeyboardMarkup(startList, one_time_keyboard=True,resize_keyboard=True))

def setup(bot, update):
    text="folan"
    bot.send_message(chat_id=update.message.chat_id, text=text )

def newacc(bot, update, user_data):
    text="filan"
    print(user_data['choice'])
    bot.send_message(chat_id=update.message.chat_id, text=text)

def cancel(bot, update):
    text="filan"
    bot.send_message(chat_id=update.message.chat_id, text=text)

def regular_choice(bot, update, user_data):
    text = update.message.text
    user_data['choice'] = text
    print(user_data)
    update.message.reply_text(
        'Your {}? Yes, I would love to hear about that!'.format(text.lower()))


    return TYPING_REPLY

def form(bot, update):
    update.message.reply_text(
        "plz fill ur information",
        reply_markup=markup)
    return CHOOSING

def send_info(bot, update):
    update.message.reply_text('u need some kind of authentication', reply_markup=markup_start)
    return CHOOSING


def custom_choice(bot, update):
    update.message.reply_text('Alright, please send me the category first, '
                              'for example "Most impressive skill"')

    return TYPING_CHOICE


def received_information(bot, update, user_data):
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text("Neat! Just so you know, this is what you already told me:"
                              "{}"
                              "You can tell me more, or change your opinion on something.".format(
                                  facts_to_str(user_data)), reply_markup=markup)

    return CHOOSING


def received_name(bot, update, user_data):
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text("plz enter ur name", reply_markup=markup)

    return EMAILENTRY


def received_email(bot, update, user_data):
    text = update.message.text
    category = user_data['choice']
    user_data[category] = text
    del user_data['choice']

    update.message.reply_text("plz enter ur email", reply_markup=markup)

    return CHOOSING

conv_handler=ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={

        CHOOSING: [RegexHandler('^(name|email|phone number)$',
                                regular_choice,
                                pass_user_data=True),
                   RegexHandler('^message$',
                                custom_choice),
                   RegexHandler('^shop$',
                                send_info),

                   RegexHandler('^contact support$',
                                form),
                   ],

	TYPING_CHOICE: [MessageHandler(Filters.text,
				regular_choice,
				pass_user_data=True),
		 ],

	TYPING_REPLY: [MessageHandler(Filters.text,
			       received_information,
			       pass_user_data=True),
		],

	EMAILENTRY: [MessageHandler(Filters.text,
				received_email,
				pass_user_data=True)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

dispatcher = updater.dispatcher
dispatcher.add_handler(conv_handler)

updater.start_polling()
