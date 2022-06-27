from telegram import Update, Bot, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
from game import *

path_file_token = r'C:\Users\Pavel\Desktop\Study\project\token.txt'
with open(path_file_token, 'r') as data:
    for line in data:
        str_token = line

bot = Bot(token=str_token)
updater = Updater(token=str_token, use_context=True)
dispatcher = updater.dispatcher


def info(update, context):
    context.bot.send_message(update.effective_chat.id, "Меня создали в муках")

def unknown(update, context):
    context.bot.send_message(update.effective_chat.id, 'Такая команда мне не знакома.')

conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOICE: [MessageHandler(Filters.regex('^(Человек|Компьютер)$'), message)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

message_handler = MessageHandler(Filters.text, game)
info_handler = CommandHandler('info', info)
unknown_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(conv_handler)
dispatcher.add_handler(message_handler)

dispatcher.add_handler(info_handler)
dispatcher.add_handler(unknown_handler)

# Запуск бота
print("server_started")
updater.start_polling()
updater.idle()
