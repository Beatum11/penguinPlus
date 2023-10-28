import os
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
# from telebot.types import LabeledPrice
from Services.users_service import UsersService
import asyncio
import openai
import random
from Handlers.start_handler import start_handler
from Handlers.check_credits_handler import check_credits
from Handlers.conversation_loop_handler import conversation_loop
from Handlers.open_and_send_handler import open_and_send_photo

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
openai.api_key = os.environ.get("GPT_KEY")

bot = AsyncTeleBot(BOT_TOKEN)
users_service = UsersService()

user_states = {}

@bot.message_handler(commands=['start'])
async def start_logic(message):
    user_states[message.chat.id] = "in_start"
    r = random.randint(1, 4)
    await open_and_send_photo(bot, message, f'./Assets/hello_pen_{r}.png')
    await start_handler(bot, message)
    user_states[message.chat.id] = "no_state"


@bot.message_handler(commands=['penguin_check'])
async def credits_handler(message):
    user_states[message.chat.id] = "answers_cheking"
    await check_credits(bot, message)
    user_states[message.chat.id] = "no_state"


@bot.message_handler(commands=['penguin_talk'])
async def talk_handler(message):
    user_states[message.chat.id] = "in_conversation"
    text = (f"Со следующего сообщения ты войдешь в режим разговора со мной, твоим ИИ-пингвином 🐧. "
            f"Я здесь, чтобы помочь тебе с ответами на вопросы и предложить решения.\n\n "
            f"Если захочешь прервать беседу, просто напиши 'Пока' или выйди из диалога\n"
            f"Готов начать? Напиши свой вопрос или тему, и я постараюсь помочь! 🧐🐧🤖😂")

    await bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'in_conversation')
async def conversation_handler(message):
    r = str(random.randint(1, 3))
    sent_message = await open_and_send_photo(bot, message, f'./Assets/Thinkin/thinkin_pen_{r}.png')
    await conversation_loop(bot, message, user_states, users_service, openai)
    await bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)


@bot.message_handler(commands=['penguin_pay'])
async def pay_command(message):
    user_states[message.chat.id] = "payment_process"
    await open_and_send_photo(bot, message, './Assets/No_payment_Pen.png')
    user_states[message.chat.id] = "no_state"


@bot.message_handler(content_types=['text'])
async def text_handler(message):
    chat_id = message.chat.id
    user_state = user_states.get(chat_id)
    if user_state == 'no_state':
        await bot.send_message(chat_id, "Я не понимаю. Пожалуйста, используйте одну из команд для взаимодействия со мной.")


asyncio.run(bot.polling())
