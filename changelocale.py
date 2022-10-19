from bot import bot
import locale


def change_locale(message):
    if message.text.split(' ')[0] == '/ru':
        locale.LOCALE = 'ru'
        bot.send_message(message.chat.id, 'Выбран русский язык')
    elif message.text.split(' ')[0] == '/en':
        locale.LOCALE = 'en'
        bot.send_message(message.chat.id, 'Selected language: english')
