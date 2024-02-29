from Utils.keyboard import get_main_keyboard
import aiohttp
import asyncio
from loguru import logger


async def start_pic_creation(bot, message, openai, user_service):

    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "dall-e-3",  # Используй актуальное название модели DALL·E
        "prompt": message.text,
        "n": 1,  # Количество изображений
        "size": "1024x1024",
        "quality": "standard"
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
                        image_url = answer['data'][0]['url']

                        await bot.send_photo(message.chat.id, image_url, reply_markup=markup)
                        logger.info(f'Для {message.chat.id} было успешно сгенерированно изображение')
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
