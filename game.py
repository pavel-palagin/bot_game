from pickle import GLOBAL
from random import randint
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler

game_type = 0
CHOICE = 0

def start(update, _):
    # Список кнопок для ответа
    reply_keyboard = [['Человек', 'Компьютер']]
    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # Начинаем разговор с вопроса
    update.message.reply_text(
        'Начинаем игру! Выберите с кем хотите сыграть?' 
        'Команда /cancel, чтобы прекратить игру.\n\n',
        reply_markup=markup_key,)

    return CHOICE

# Обрабатываем выбор пользователя
def message(update, context):
    # определяем выбор
    global game_type
    game_type = update.message.text
    context.bot.send_message(update.effective_chat.id, 'Поехали! (с)')
    return ConversationHandler.END

def cancel(update, _):
    update.message.reply_text(
        'До свидания',
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

board = list(range(1, 10))

def draw_board(board):
    for i in range(3):
        print("|", board[0 + i * 3], "|", board[1 + i * 3], "|", board[2 + i * 3], "|")

def take_input(player_char):
    valid = False
    while not valid:
        player_answer = int(input("Куда поставим " + player_char + "? "))

        if player_answer >= 1 and player_answer <= 9:
            if (str(board[player_answer - 1]) not in "XO"):
                board[player_answer - 1] = player_char
                valid = True
            else:
                print("Эта клеточка уже занята")

def check_win():
    win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
    for each in win_coord:
        if board[each[0]] == board[each[1]] == board[each[2]]:
            return board[each[0]]
    return False


def game(board):
    # if game_type == 'Человек':
    counter = 0
    win = False
    while not win:
        draw_board(board)
        if counter % 2 == 0:
            take_input("X")
        else:
            take_input("O")
        counter += 1
        if counter > 4:
            tmp = check_win(board)
            if tmp:
                print(tmp, "выиграл!")
                win = True
                break
        if counter == 9:
            print("Ничья!")
            break
    draw_board(board)