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
from Utils.keyboard import get_main_keyboard
from Utils.setup_logging import setup_logging
from pathlib import Path
from loguru import logger


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
    await users_service.update_state(message.chat.id, "in_start")
    logger.info(f'Start the conversation by {message.chat.id}')

    r = random.randint(1, 4)
    await open_and_send_photo(bot, message, f'./Assets/hello_pen_{r}.png')
    await start_handler(bot, message)

    await users_service.update_state(message.chat.id, "no_state")


# This command checks user's amount of answers.
@bot.message_handler(commands=['penguin_check'])
async def credits_handler(message):
    await users_service.update_state(message.chat.id, "answers_cheking")
    await check_credits(bot, message)

    await users_service.update_state(message.chat.id, "no_state")


# This command starts the conversation with AI penguin,
# in particular, after that command user will send messages directly to openai
# And important note, that user_state now will hold 'in_conversation' mode.

@bot.message_handler(commands=['penguin_talk'])
async def talk_handler(message):
    await users_service.update_state(message.chat.id, "in_conversation")
    text = (f"Со следующего сообщения ты войдешь в режим разговора 🐧\n\n"
            f"Напиши свой вопрос или тему, и я постараюсь помочь! 🧐")

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


@bot.message_handler(commands=['penguin_pay'])
async def pay_command(message):
    await users_service.update_state(message.chat.id, "payment_process")

    await bot.send_message(message.chat.id, 'Чтобы купить доп. кредиты, напишите сюда: @phineus1\n\n'
                                            'Есть несколько пакетов:\n'
                                            '- 1000 кредитов -  59р.\n'
                                            '- 2000 кредитов - 99р.\n'
                                            '- 4000 кредитов - 169р.\n\n'
                                            '4000 кредитов может хватить на несколько месяцев вперед!')

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

    if message.text == '/penguin_pay':
        await pay_command(message)
    elif message.text == '/penguin_talk':
        await talk_handler(message)
    elif message.text == '/penguin_check':
        await credits_handler(message)

    if user_state == 'no_state':
        markup = get_main_keyboard()
        await bot.send_message(chat_id,
                               "Воспользуйся одной из команд", reply_markup=markup)
    elif user_state == 'in_conversation':
        await conversation_loop(bot, message, openai=openai, user_service=users_service)


asyncio.run(bot.polling())
