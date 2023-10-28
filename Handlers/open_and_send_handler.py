import aiofiles


async def open_and_send_photo(bot, message, path):
    try:
        async with aiofiles.open(path, mode='rb') as file:
            photo = await file.read()
            sent_message = await bot.send_photo(message.chat.id, photo)
            return sent_message
    except FileNotFoundError:
        await bot.send_message(message.chat.id, 'Здесь должна быть красивая картинка пингвина...')

