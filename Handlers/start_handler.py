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
        text = (f"Привет, {user['username']}! Рад снова тебя видеть 🐧\n"
                f"Благодаря силе ИИ, я могу помочь с самыми разными вопросами и проблемами.\n\n"
                f"На данный момент у тебя {user['credits']} кредитов!\n\n"
                f"Что я умею:\n"
                f"/penguin_talk - начни разговор и задай мне вопрос.\n"
                f"/penguin_check - проверь, сколько у тебя осталось кредитов.\n"
                f"/penguin_pay - пакеты кредитов на все случаи жизни.\n")

        markup = get_main_keyboard()
        await bot.send_message(message.chat.id, text, reply_markup=markup)
        return
    else:
        user = await user_service.post_user(message.chat.id, message.from_user.username)
        if user:
            text = (f"Привет! Я твой новый ИИ друг 🐧\n"
                    f"Хоть пингвины и не умеют летать, но благодаря мощи ИИ, я могу парить по просторам интернета, "
                    f"помогая тебе находить ответы на вопросы и предлагая решения для различных задач. 🌐\n\n"
                    f"Я работаю на базе технологии ChatGPT, что позволяет мне общаться с тобой в естественном и "
                    f"понятном стиле."
                    f"Ты можешь задавать мне вопросы, и я постараюсь помочь тебе в любой ситуации, будь то простой "
                    f"запрос или сложная проблема.\n\n"
                    f"Что я умею:\n"
                    f"/penguin_talk - начни разговор и задай мне вопрос.\n"
                    f"/penguin_check - проверь, сколько у тебя осталось кредитов.\n"
                    f"/penguin_pay - пакеты кредитов на все случаи жизни.\n\n"
                    f"На данный момент у тебя {user['credits']} кредитов, которые ты можешь использовать, чтобы "
                    f"общаться со мной.")

            markup = get_main_keyboard()
            await bot.send_message(message.chat.id, text, reply_markup=markup)
            return
