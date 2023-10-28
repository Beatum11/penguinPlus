from Services.users_service import UsersService
from Utils.keyboard import get_main_keyboard


async def check_credits(bot, message):
    user_service = UsersService()
    user = await user_service.get_user(message.chat.id)

    text = f"Барабанная дробь... Оставшееся кол-во ответов: {user['credits']}"
    markup = get_main_keyboard()
    await bot.send_message(message.chat.id, text, reply_markup=markup)

