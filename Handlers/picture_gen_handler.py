import io

from Utils.keyboard import get_main_keyboard
import aiohttp
import asyncio
from loguru import logger
import base64
import requests
import os
from Utils.translate_handler import translate_word


async def start_pic_creation(bot, message):

    trans_prompt = await translate_word(message.text)

    url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

    body = {
        "steps": 45,
        "width": 1024,
        "height": 1024,
        "seed": 0,
        "cfg_scale": 8,
        "samples": 1,
        "text_prompts": [
            {
                "text": trans_prompt
            }
        ]
    }

    api_key = 'sk-EW7icLBwffmrRXbHzzQT6gCVBuGexQw20OH3I21nWunKSoUo'
    stable_headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    markup = get_main_keyboard()
    await bot.send_chat_action(message.chat.id, 'typing')

    max_attempts = 3  # Максимальное количество попыток
    attempt = 0  # Текущая попытка
    delay = 2  # Задержка между попытками в секундах

    while attempt < max_attempts:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url=url, json=body, headers=stable_headers) as response:
                    if response.status == 200:
                        answer = await response.json()
                        # image_url = answer['data'][0]['url']

                        image_data = base64.b64decode(answer["artifacts"][0]["base64"])

                        with io.BytesIO(image_data) as image_buffer:
                            await bot.send_photo(message.chat.id, image_buffer.getvalue(), reply_markup=markup)
                        break


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

    # max_attempts = 3  # Максимальное количество попыток
    # attempt = 0  # Текущая попытка
    # delay = 2  # Задержка между попытками в секундах
    #
    # while attempt < max_attempts:
    #     try:
    #         async with aiohttp.ClientSession() as session:
    #             async with session.post(url, json=data, headers=headers) as response:
    #                 if response.status == 200:
    #                     answer = await response.json()
    #                     image_url = answer['data'][0]['url']
    #
    #                     await bot.send_photo(message.chat.id, image_url, reply_markup=markup)
    #                     logger.info(f'Для {message.chat.id} было успешно сгенерированно изображение')
    #                     break  # Выход из цикла, если запрос успешен
    #                 else:
    #                     raise aiohttp.ClientResponseError(response.request_info,
    #                                                       response.history,
    #                                                       status=response.status)
    #     except (TimeoutError, aiohttp.ClientResponseError) as e:
    #         attempt += 1
    #         if attempt < max_attempts:
    #             await asyncio.sleep(delay)  # Ждем перед следующей попыткой
    #             delay *= 2  # Увеличиваем задержку для следующей попытки
    #         else:
    #             await bot.send_message(message.chat.id, 'Проблемы с соединением, попробуйте буквально через минуту.')
    #             logger.error(f'Какие-то проблемы с соединением у {message.chat.id} - {e}')
    #     except Exception as e:
    #         await bot.send_message(message.chat.id, 'Неизвестная ошибка. Попробуй чуть позже.')
    #         logger.error(f'Необработанная ошибка у {message.chat.id} - {e}')
    #         break
