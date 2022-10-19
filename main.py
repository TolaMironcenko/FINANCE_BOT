from termcolor import cprint
from bot import bot
import locale
from changelocale import change_locale


def main_bot(messages):
    for message in messages:
        if message.text.split(' ')[0] == '/start' or message.text.split(' ')[0] == '/help':
            mes = None
            if locale.LOCALE == 'ru':
                mes = locale.ru['help_message']
            elif locale.LOCALE == 'en':
                mes = locale.en['help_message']
            bot.send_message(message.chat.id, mes)
        elif message.text.split(' ')[0] == '/ru' or message.text.split(' ')[0] == '/en':
            change_locale(message)
        else:
            mes = None
            if locale.LOCALE == 'ru':
                mes = locale.ru['error404_message']
            elif locale.LOCALE == 'en':
                mes = locale.en['error404_message']
            bot.send_message(message.chat.id, mes)


bot.set_update_listener(main_bot)

try:
    bot.polling(none_stop=True)
except KeyboardInterrupt:
    exit('byby\n')
except Exception as e:
    cprint(str(e), 'red')
    bot.polling(none_stop=True)

while True:
    pass
