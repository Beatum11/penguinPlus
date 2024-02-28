from Handlers.communication_handler import start_communication
from Utils.keyboard import get_main_keyboard
from loguru import logger


# Эта функция отвечает за процесс общения с ИИ
async def conversation_loop(bot, message, user_service, openai):
    try:
        user = await user_service.get_user(message.chat.id)
        users_credits = user['credits']
        if users_credits <= 0:
            markup = get_main_keyboard()
            await bot.send_message(message.chat.id,
                                   'Не хватает кредитов, чтобы продолжить купите один из пакетов',
                                   reply_markup=markup)

            logger.info(f'Для {message.chat.id} не хватает кредитов')
            await user_service.update_state(message.chat.id, "no_state")
            return

        await user_service.create_chat_history(chat_id=message.chat.id,
                                               role='user', message=message.text)

        await start_communication(bot, message, openai, user_service)
        user['credits'] -= 1
        await user_service.update_credits(message.chat.id, user['credits'])
    except ConnectionError as e:
        await bot.send_message(message.chat.id, 'Какие-то проблемы с соединением...')
        logger.error(f"Проблемы с соединением для {message.chat.id} - {e}")
        return
    except Exception as e:
        await bot.send_message(message.chat.id, 'Неизвестная ошибка...')
        logger.error(f"Какая-то необработанная ошибка для {message.chat.id} - {e}")
        return
