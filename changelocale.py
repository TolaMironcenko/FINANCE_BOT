from bot import bot
import locales


def change_locale(message):
    if message.text.split(' ')[0] == '/ru':
        locales.LOCALE = 'ru'
        bot.send_message(message.chat.id, 'Выбран русский язык')
    elif message.text.split(' ')[0] == '/en':
        locales.LOCALE = 'en'
        bot.send_message(message.chat.id, 'Selected language: english')
