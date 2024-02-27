from Services.users_service import UsersService
from Utils.keyboard import get_main_keyboard


# This function gets a user from the database.
# Then it sends a message that shows, how many answers user has.
async def check_credits(bot, message):
    user_service = UsersService()
    user = await user_service.get_user(message.chat.id)

    text = f"Осталось {user['credits']} кредитов 🐧"
    markup = get_main_keyboard()
    await bot.send_message(message.chat.id, text, reply_markup=markup)

