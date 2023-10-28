from Utils.keyboard import get_main_keyboard
import aiohttp
import asyncio


async def start_communication(bot, message, openai):

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo-16k",
        "messages": [
            {
                "role": "user",
                "content": message.text
            }
        ],
        "temperature": 1,
        "max_tokens": 800,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0
    }
    markup = get_main_keyboard()

    await bot.send_chat_action(message.chat.id, 'typing')
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                answer = await response.json()
                send_msg = answer['choices'][0]['message']['content'].strip()
                await bot.send_message(message.chat.id, send_msg, reply_markup=markup)
    except TimeoutError:
        await bot.send_message(message.chat.id, 'В Антарктике 2 сервера. Оба сломались. Пойду починю. Попробуй еще раз через минуту.')
    except aiohttp.ClientResponseError as e:
        await bot.send_message(message.chat.id, f':{e.status} | В Антарктике 2 сервера. '
                                                f'Оба сломались. Пойду починю. '
                                                f'Попробуй еще раз через минуту.')
    except Exception:
        await bot.send_message(message.chat.id, 'Неизвестная ошибка.')

