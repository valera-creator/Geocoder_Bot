from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters
from image_code import check_get_image

BOT_TOKEN = '7134752919:AAGCqQM82B3rswT_BgYjxb84hgs3HjkHqFA'


async def start(update, context):
    await update.message.reply_text('Для того, чтобы я прислала карту, напишите:\nПокажи {название местности}.'
                                    '\n\nЧтобы посмотреть пример запроса, нажмите /example')


async def help_info(update, context):
    await update.message.reply_text('Для того, чтобы я прислала карту, напишите:\nПокажи {название местности}')


async def example(update, context):
    await update.message.reply_text('Покажи Аллин Михайловск')
    await send_message(update, context, text='Покажи Аллин Михайловск', text_check="Аллин Михайловск")


async def send_message(update, context, text='Покажи Ярославль', text_check='Ярославль'):
    result = check_get_image(text_check)
    if result:
        await context.bot.send_photo(
            update.message.chat_id,
            'image.png',
            caption=f'Вот, что я нашла по запросу "{text[7:]}"'
        )
    else:
        await update.message.reply_text(f'По результату "{text[7:]}" ничего не было найдено')


async def check_text(update, context):
    text = update.message.text
    if 'покажи' not in text.lower() or len(text) <= 7 or text.lower().strip()[0:7] != 'покажи ':
        await update.message.reply_text(
            'Я вас не поняла.\n\nДля просмотра примера нажмите на /example')
        return
    text_check = text.lower().strip()
    text_check = text_check.split('покажи')[1:]
    await send_message(update, context, text, text_check)


async def stop(update, context):
    await update.message.reply_text(f"Пока, пока)")
    context.user_data.clear()  # очищаем словарь с пользовательскими данными
    return ConversationHandler.END


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler(["start"], start))
    application.add_handler(CommandHandler(["help"], help_info))
    application.add_handler(CommandHandler(["example"], example))
    application.add_handler(CommandHandler(["stop"], stop))
    text_handler = MessageHandler(filters.TEXT, check_text)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == '__main__':
    main()
