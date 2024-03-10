from telebot import types


# Функция отвечает за рендер клавиатуры
def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    pen_talk = types.KeyboardButton('/penguin_talk')
    pen_check = types.KeyboardButton('/penguin_check')
    pen_pay = types.KeyboardButton('/penguin_pay')
    pic_pen = types.KeyboardButton('/penguin_pic')
    markup.add(pen_talk, pen_check, pen_pay, pic_pen)
    return markup


def get_price_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    thous_credits = types.KeyboardButton('10 кредитов - 49р.')
    two_thous_credits = types.KeyboardButton('50 кредитов - 219р.')
    three_thous_credits = types.KeyboardButton('100 кредитов - 399р.')
    markup.add(thous_credits, two_thous_credits, three_thous_credits)
    return markup
