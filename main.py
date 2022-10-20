from termcolor import cprint
from bot import bot
import locale
from changelocale import change_locale
from database.models import User


def to_fixed(num_obj, digits=0):
    return f"{num_obj:.{digits}f}"


def main_bot(messages):
    for message in messages:
        if message.text.split(' ')[0] == '/start' or message.text.split(' ')[0] == '/help':
            mes = None
            if locale.LOCALE == 'ru':
                mes = locale.ru['help_message']
            elif locale.LOCALE == 'en':
                mes = locale.en['help_message']
            _, user = User.get_or_create(username=message.chat.id)
            bot.send_message(message.chat.id, mes)
        elif message.text.split(' ')[0] == '/ru' or message.text.split(' ')[0] == '/en':
            change_locale(message)
        elif message.text.split(' ')[0] == '/balance':
            user = User.get(username=message.chat.id)
            bot.send_message(message.chat.id, to_fixed(user.balance, 2))
        elif message.text.split(' ')[0] == '/add' or message.text.split(' ')[0] == '+':
            if len(message.text.split(' ')) < 2:
                mes = None
                if locale.LOCALE == 'ru':
                    mes = 'Используйте /add [сумма] или + [сумма]'
                elif locale.LOCALE == 'en':
                    mes = 'Use /add [sum] or + [sum]'
                bot.send_message(message.chat.id, mes)
            else:
                user = User.get(username=message.chat.id)
                user.balance += float(message.text.split(' ')[1])
                user.save()
                bot.send_message(message.chat.id, to_fixed(user.balance, 2))
        elif message.text.split(' ')[0] == '/rm' or message.text.split(' ')[0] == '-':
            if len(message.text.split(' ')) < 2:
                mes = None
                if locale.LOCALE == 'ru':
                    mes = 'Используйте /rm [сумма] или - [сумма]'
                elif locale.LOCALE == 'en':
                    mes = 'Use /rm [sum] or - [sum]'
                bot.send_message(message.chat.id, mes)
            else:
                user = User.get(username=message.chat.id)
                user.balance -= float(message.text.split(' ')[1])
                user.save()
                bot.send_message(message.chat.id, to_fixed(user.balance, 2))
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
