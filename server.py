import requests
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import logging
from flask import Flask, request

app = Flask(__name__)

bot_token = "545110014:AAFL9tBt7h93I2fywdCnFU-U7FYeLi77aQY"
updater = Updater(token=bot_token)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
SETUP ,USERNAME = range(2)


def start_method(bot, update):

    msg = "Use /shipping to get an invoice for shipping-payment, "
    msg += "or /noshipping for an invoice without shipping."
    update.message.reply_text(msg)

    # startList = [["Register New Account","Integrate An Account"]]
    # chat_id=update.message.chat_id
    # bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

    # text = "filan bisar"
    # replyText = update.message.text
    # update.message.reply_text(text, parse_mode="Markdown",
# reply_markup=ReplyKeyboardMarkup(startList, one_time_keyboard=True))
    return SETUP

def setup(bot, update):
    if update.message.text == "Register New Account":
        chat_id=update.message.chat_id
        register_text = """Ok.
            Now Send Me Your Bestoon Username.
        """
        update.message.reply_text(register_text, reply_markup=ReplyKeyboardRemove())
        print(update.message.text)
        print ("Going For Username")

        return USERNAME

def regUser(bot, update):
    chat_id = update.message.chat_id
    bot.sendChatAction(chat_id, "TYPING")
    update.message.reply_text("Registering Your Username")
    print (USERNAME)
    return ConversationHandler.END

# dispatcher = updater.dispatcher
# start_handler=CommandHandler('start', start)
# dispatcher.add_handler(start_handler)

# request_handler=CommandHandler('request', request, pass_args=True)
# dispatcher.add_handler(request_handler)

def cancel(bot, update):
    bot.sendMessage(update.message.chat_id, "Bye!")
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points = [CommandHandler('start', start_method)],

    states = {
        SETUP: [MessageHandler(Filters.text, setup)],
        USERNAME: [MessageHandler(Filters.text, regUser)]


    },
    fallbacks = [CommandHandler('cancel', cancel)]
)

updater.dispatcher.add_handler(conv_handler)

# def get_url(method):
#     return "https://api.telegram.org/bot{}/{}".format(bot_token,method)

# def process_message(update):
#     data = {}
#     data["chat_id"] = update["message"]["from"]["id"]
#     data["text"] = "i can hear u"
#     data["reply_markup"]="ReplyKeyboardMarkup"

#     r = requests.post(get_url("sendMessage"), data=data)

# @app.route("/{}".format(bot_token), methods=["POST"])
# def process_update():
#     if request.method == "POST":
#         update = request.get_json()
#         if "message" in update:
#             process_message(update)

#         return "ok!", 200

updater.start_polling()
