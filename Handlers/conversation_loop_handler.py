from Handlers.communication_handler import start_communication


# Эта функция отвечает за процесс общения с ИИ
async def conversation_loop(bot, message, user_states, user_service, openai):
    # Здесь мы проверяем, не ввел ли юзер слово, при котором заверщается цикл разговора
    if message.text.strip().lower() == 'пока':
        user_states.pop(message.chat.id)  # Remove user state
        await bot.send_message(message.chat.id, "Пока! Надеюсь, мы еще пообщаемся 🐧")

        # Если не ввел, то мы начинаем обработку сообщения и уменьшаем credit на 1
    else:
        try:
            await start_communication(bot, message, openai)
            user = await user_service.get_user(message.chat.id)
            user['credits'] -= 1
            await user_service.update_credits(message.chat.id, user['credits'])
        except ConnectionError:
            await bot.send_message(message.chat.id, 'Какие-то проблемы с соединением...')
        except Exception:
            await bot.send_message(message.chat.id, 'Неизвестная ошибка...')
