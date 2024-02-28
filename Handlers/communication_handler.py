from Utils.keyboard import get_main_keyboard
import aiohttp
from aiohttp import ClientResponseError
import asyncio
from loguru import logger


async def start_communication(bot, message, openai, user_service):

    chat_history = await user_service.get_chat_history(message.chat.id)

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo-0125",
        "messages": chat_history,
        "temperature": 1,
        "max_tokens": 700,
        "top_p": 1,
        "frequency_penalty": 0.5,
        "presence_penalty": 0.5
    }
    markup = get_main_keyboard()

    await bot.send_chat_action(message.chat.id, 'typing')

    max_attempts = 3  # Максимальное количество попыток
    attempt = 0  # Текущая попытка
    delay = 2  # Задержка между попытками в секундах

    while attempt < max_attempts:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, headers=headers) as response:
                    if response.status == 200:
                        answer = await response.json()
                        send_msg = answer['choices'][0]['message']['content']

                        await user_service.create_chat_history(chat_id=message.chat.id,
                                                               role='system', message=send_msg)

                        await bot.send_message(message.chat.id, send_msg, reply_markup=markup, parse_mode='Markdown')
                        logger.info(f'Для {message.chat.id} было успешно сгенерированно сообщение')
                        break  # Выход из цикла, если запрос успешен
                    else:
                        raise aiohttp.ClientResponseError(response.request_info,
                                                          response.history,
                                                          status=response.status)
        except (TimeoutError, aiohttp.ClientResponseError) as e:
            attempt += 1
            if attempt < max_attempts:
                await asyncio.sleep(delay)  # Ждем перед следующей попыткой
                delay *= 2  # Увеличиваем задержку для следующей попытки
            else:
                await bot.send_message(message.chat.id, 'Проблемы с соединением, попробуйте буквально через минуту.')
                logger.error(f'Какие-то проблемы с соединением у {message.chat.id} - {e}')
        except Exception as e:
            await bot.send_message(message.chat.id, 'Неизвестная ошибка. Попробуй чуть позже.')
            logger.error(f'Необработанная ошибка у {message.chat.id} - {e}')
            break
