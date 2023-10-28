from telebot import types


# Функция отвечает за рендер клавиатуры
def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    pen_talk = types.KeyboardButton('/penguin_talk')
    pen_check = types.KeyboardButton('/penguin_check')
    pen_pay = types.KeyboardButton('/penguin_pay')
    markup.add(pen_talk, pen_check, pen_pay)
    return markup
