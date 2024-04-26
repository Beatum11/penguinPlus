import os
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from Services.users_service import UsersService
import asyncio
import openai
import random
from Handlers.start_handler import start_handler
from Handlers.check_credits_handler import check_credits
from Handlers.conversation_loop_handler import conversation_loop
from Handlers.open_and_send_handler import open_and_send_photo
from Utils.keyboard import get_main_keyboard, get_price_keyboard
from Utils.setup_logging import setup_logging
from pathlib import Path
from loguru import logger
from Handlers.pic_loop import picture_loop


app_root = Path(__file__).parent
load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
openai.api_key = os.environ.get("GPT_KEY")

bot = AsyncTeleBot(BOT_TOKEN)
users_service = UsersService()

setup_logging(app_root)


# This command is responsible for starting the conversation.
# It changes user state to in_start, generates welcome image and sends a start message
# based on user's data. In the end it changes user_state to 'no_state'

@bot.message_handler(commands=['start'])
async def start_logic(message):
    logger.info(f'Start the conversation by {message.chat.id}')

    r = random.randint(1, 3)
    await open_and_send_photo(bot, message, f'./Assets/hello_pen_{r}.png')
    await start_handler(bot, message)


# This command checks user's amount of answers.
@bot.message_handler(commands=['check'])
async def credits_handler(message):
    await check_credits(bot, message)
    await users_service.update_state(message.chat.id, "no_state")


# This command starts the conversation with AI penguin,
# in particular, after that command user will send messages directly to openai
# And important note, that user_state now will hold 'in_conversation' mode.

@bot.message_handler(commands=['speak'])
async def talk_handler(message):
    await users_service.update_state(message.chat.id, "in_conversation")
    text = (f"Со следующего сообщения ты войдешь в режим разговора 🐧\n\n"
            f"Напиши свой вопрос или тему, и я постараюсь помочь! 🧐")
    await bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['create'])
async def picture_handler(message):
    await users_service.update_state(message.chat.id, "in_pic_creation")
    text = (f"ВАЖНО: каждая новая картинка - это новый запрос. Я не помню, что рисовал до этого 😄\n\n"
            f"Что мне нарисовать:")

    await bot.send_message(message.chat.id, text)


# This function will work only if a user will be in 'in_conversation' state.
# It means that user will receive messages only if he used previous command that changed the state.

# @bot.message_handler()
# async def conversation_handler(message):
#     state = await users_service.get_current_state(message.chat.id)
#     if state == 'no_state':
#         await bot.send_message(message.chat.id, 'GO TO /penguin_pay')
#         return
#     print(state)


@bot.message_handler(commands=['buy'])
async def pay_command(message):
    await users_service.update_state(message.chat.id, "payment_process")
    markup = get_price_keyboard()
    await bot.send_message(message.chat.id,
                           "Сколько покупаем кредитов:", reply_markup=markup)

    await users_service.update_state(message.chat.id, "no_state")

    # prices = [LabeledPrice(label=invoice["TITLE"], amount=invoice["PRICE"])]
    #
    # await bot.send_invoice(message.chat.id,
    #                        title="Оплата ответов от AI Penguin | 100 кред.",
    #                        description=invoice["DESCRIPTION"],
    #                        invoice_payload=invoice["PAYLOAD"],
    #                        provider_token=invoice["PROVIDER_TOKEN"],
    #                        start_parameter=invoice["START_PARAMETER"],
    #                        currency=invoice["CURRENCY"],
    #                        prices=prices)


# @bot.pre_checkout_query_handler(func=lambda query: True)
# async def checkout(pre_checkout_query):
#     await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


# @bot.message_handler(content_types=['successful_payment'])
# async def got_payment(message):
#     chat_id = message.chat.id
#     await users_service.update_credits(chat_id, 100)
#
#     await bot.send_message(chat_id, f"Спасибо за покупку! Вам добавлено 100 ответов.")
#
#     # Обновляем состояние пользователя после завершения процесса покупки
#     user_states[chat_id] = 'no_state'


# The idea of this command is that if user has 'no_state', it means that he communicates
# with bot and doesn't use any command.
# So, we send a message that tells user to use some commands instead.
# But we're checking every message out there.

@bot.message_handler(content_types=['text'])
async def text_handler(message):

    chat_id = message.chat.id
    user_state = await users_service.get_current_state(chat_id)

    if message.text == '/buy':
        await pay_command(message)
    elif message.text == '/speak':
        print(user_state)
        await talk_handler(message)
    elif message.text == '/check':
        await users_service.update_state(message.chat.id, "answers_cheking")
        await credits_handler(message)
    elif message.text == '/create':
        await picture_handler(message)
    elif message.text == '10 кредитов - 49р.':
        await bot.send_message(chat_id,
                               '🛑<b>ВАЖНО</b>🛑\n'
                               'Необходимо будет переслать сгенерированный чек сюда: @phineus1\n\n'
                               '<a href="https://pro.selfwork.ru/kassa/10_credits">Ссылка для оплаты</a>\n\n'
                               'P.S. Для удобства, сейчас произойдет автоматический переход в стандартный режим выбора '
                               'команд 🐧',
                               parse_mode='HTML', disable_web_page_preview=True)
    elif message.text == '50 кредитов - 219р.':
        await bot.send_message(chat_id,
                               '🛑<b>ВАЖНО</b>🛑\n'
                               'Необходимо будет переслать сгенерированный чек сюда: @phineus1\n\n'
                               '<a href="https://pro.selfwork.ru/kassa/50_credits">Ссылка для оплаты</a>\n\n'
                               'P.S. Для удобства, сейчас произойдет автоматический переход в стандартный режим выбора '
                               'команд 🐧',
                               parse_mode='HTML', disable_web_page_preview=True)
    elif message.text == '100 кредитов - 399р.':
        await bot.send_message(chat_id,
                               '🛑<b>ВАЖНО</b>🛑\n'
                               'Необходимо будет переслать сгенерированный чек сюда: @phineus1\n\n'
                               '<a href="https://pro.selfwork.ru/kassa/100_credits">Ссылка для оплаты</a>\n\n'
                               'P.S. Для удобства, сейчас произойдет автоматический переход в стандартный режим выбора '
                               'команд 🐧',
                               parse_mode='HTML', disable_web_page_preview=True)

    if user_state == 'no_state':
        markup = get_main_keyboard()
        await bot.send_message(chat_id,
                               "Воспользуйся одной из команд", reply_markup=markup)
    elif user_state == 'in_conversation':
        await conversation_loop(bot, message, openai=openai, user_service=users_service)
    elif user_state == 'in_pic_creation':
        await picture_loop(bot, message, user_service=users_service)


asyncio.run(bot.polling())
