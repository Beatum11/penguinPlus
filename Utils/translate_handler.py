import os
import aiohttp
import asyncio
from loguru import logger


async def translate_word(message):
    api_key = os.environ.get('GPT_3_KEY')
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo-0125",
        "messages": [{
            "content": f'Переведи данный текст на английский. Без каких-то дополнительных слов в ответе, только перевод '
                       f'текста и все. Вот текст: {message}',
            "role": "user"
        }],
        "temperature": 1,
        "max_tokens": 650,
        "top_p": 1,
        "frequency_penalty": 0.5,
        "presence_penalty": 0.5
    }

    max_attempts = 3  # Максимальное количество попыток
    attempt = 0  # Текущая попытка
    delay = 2  # Задержка между попытками в секундах

    while attempt < max_attempts:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, headers=headers) as response:
                    if response.status == 200:
                        answer = await response.json()
                        translate_msg = answer['choices'][0]['message']['content']
                        return translate_msg
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
                return ''
        except Exception as e:
            return ''
