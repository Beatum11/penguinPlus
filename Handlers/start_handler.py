from Services.users_service import UsersService
from Utils.keyboard import get_main_keyboard


# This function sends welcome message.
# Firstly, it checks a user in the database.
# If there is one, we send one type of message.
# If there is no user, we add him to the database and send another type of message.

async def start_handler(bot, message):
    user_service = UsersService()
    user = await user_service.get_user(message.chat.id)

    if user:
        text = (f"Привет, {user['username']}!\nРад снова тебя видеть 🐧\n\n"
                f"Благодаря силе ИИ, я могу помочь с самыми разными вопросами и проблемами.\n\n"
                f"Оставшееся кол-во кредитов: {user['credits']} 🧾\n\n"
                f"Команды:\n"
                f"/penguin_talk - начни разговор и задай мне вопрос.\n"
                f"/penguin_check - проверь, сколько у тебя осталось кредитов.\n"
                f"/penguin_pay - пакеты кредитов на все случаи жизни.\n"
                f"/penguin_pic - создай изображение.\n")

        markup = get_main_keyboard()
        await bot.send_message(message.chat.id, text, reply_markup=markup)
        return
    else:
        user = await user_service.post_user(message.chat.id, message.from_user.username)
        if user:
            text = (f"Привет 🐧\nЯ продвинутая версия @penguin_chat_bot \n\n"
                    f"Я работаю на базе одних из самых мощных моделей ИИ (GPT-4 Turbo | Stable Diffusion XL). "
                    f"Ты можешь задать мне любой вопрос или попросить сгенерировать изображение.\n\n"
                    f"Команды:\n"
                    f"/penguin_talk - начни разговор и задай мне вопрос.\n"
                    f"/penguin_check - проверь, сколько у тебя осталось кредитов.\n"
                    f"/penguin_pay - если нужно БОЛЬШЕ 😄.\n"
                    f"/penguin_pic - создай изображение.\n\n"
                    f"Кол-во кредитов: {user['credits']}\n"
                    f"1 кредит = 1 ответ")

            markup = get_main_keyboard()
            await bot.send_message(message.chat.id, text, reply_markup=markup)
            return
