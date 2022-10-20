import datetime

from termcolor import cprint
from bot import bot
import locales
from changelocale import change_locale
from database.models import User, Transaction


# функция ограничения количества знаков после запятой
def to_fixed(num_obj, digits=0):
    return f"{num_obj:.{digits}f}"


# основной обработчик для бота
def main_bot(messages):
    for message in messages:
        if message.text.split(' ')[0] == '/start' or message.text.split(' ')[0] == '/help':
            mes = None
            if locales.LOCALE == 'ru':
                mes = locales.ru['help_message']
            elif locales.LOCALE == 'en':
                mes = locales.en['help_message']
            _, user = User.get_or_create(username=message.chat.id)
            bot.send_message(message.chat.id, mes)
        elif message.text.split(' ')[0] == '/ru' or message.text.split(' ')[0] == '/en':
            change_locale(message)  # функция для изменения языка
        elif message.text.split(' ')[0] == '/balance':
            user = User.get(username=message.chat.id)
            mes = ''
            if locales.LOCALE == 'ru':
                mes = 'Баланс: '
            elif locales.LOCALE == 'en':
                mes = 'Balance: '
            mes += to_fixed(user.balance, 2)
            bot.send_message(message.chat.id, mes)
        elif message.text.split(' ')[0] == '/add' or message.text.split(' ')[0] == '+':
            if len(message.text.split(' ')) < 2:
                mes = None
                if locales.LOCALE == 'ru':
                    mes = locales.ru['erradd']
                elif locales.LOCALE == 'en':
                    mes = locales.en['erradd']
                bot.send_message(message.chat.id, mes)
            else:
                user = User.get(username=message.chat.id)
                user.balance += float(message.text.split(' ')[1])
                user.save()
                if len(message.text.split(' ')) == 3:
                    Transaction.create(
                        sum=int(message.text.split(' ')[1]),
                        type='incom',
                        user=User.get(username=message.chat.id),
                        category=message.text.split(' ')[2]
                    )
                else:
                    Transaction.create(
                        sum=int(message.text.split(' ')[1]),
                        type='incom',
                        user=User.get(username=message.chat.id)
                    )
                bot.send_message(message.chat.id, to_fixed(user.balance, 2))
        elif message.text.split(' ')[0] == '/rm' or message.text.split(' ')[0] == '-':
            if len(message.text.split(' ')) < 2:
                mes = None
                if locales.LOCALE == 'ru':
                    mes = locales.ru['errrm']
                elif locales.LOCALE == 'en':
                    mes = locales.en['errrm']
                bot.send_message(message.chat.id, mes)
            else:
                user = User.get(username=message.chat.id)
                user.balance -= float(message.text.split(' ')[1])
                user.save()
                if len(message.text.split(' ')) == 3:
                    Transaction.create(
                        sum=int(message.text.split(' ')[1]),
                        type='consuption',
                        user=User.get(username=message.chat.id),
                        category=message.text.split(' ')[2]
                    )
                else:
                    Transaction.create(
                        sum=int(message.text.split(' ')[1]),
                        type='consuption',
                        user=User.get(username=message.chat.id)
                    )
                bot.send_message(message.chat.id, to_fixed(user.balance, 2))
        elif message.text.split(' ')[0] == '/addtoday':
            transactions = Transaction.select().where(
                Transaction.type == 'incom',
                Transaction.date == datetime.datetime.today(),
                Transaction.user == User.get(username=message.chat.id).id
            )
            mes = ''
            if locales.LOCALE == 'ru':
                mes = 'Ваши доходы за сегодня:\n\n'
            elif locales.LOCALE == 'en':
                mes = 'Your incomes today:\n\n'
            iteration = 1
            for i in transactions:
                mes += str(iteration) + '. 􀅼' + str(i.sum) + '􁑆   ' + i.category + '\n\n'
                iteration += 1

            bot.send_message(message.chat.id, mes)
        elif message.text.split(' ')[0] == '/rmtoday':
            transactions = Transaction.select().where(
                Transaction.type == 'consuption',
                Transaction.date == datetime.datetime.today(),
                Transaction.user == User.get(username=message.chat.id).id
            )
            mes = ''
            if locales.LOCALE == 'ru':
                mes = 'Ваши расходы за сегодня:\n\n'
            elif locales.LOCALE == 'en':
                mes = 'Your consuptions today:\n\n'
            iteration = 1
            for i in transactions:
                mes += str(iteration) + '. 􀅽' + str(i.sum) + '􁑆   ' + i.category + '\n\n'
                iteration += 1

            bot.send_message(message.chat.id, mes)
        elif message.text.split(' ')[0] == '/rmall':
            transactions = Transaction.select().where(
                Transaction.type == 'consuption',
                Transaction.user == User.get(username=message.chat.id).id
            )
            mes = ''
            if locales.LOCALE == 'ru':
                mes = 'Ваши расходы за все время:\n\n'
            elif locales.LOCALE == 'en':
                mes = 'Your all consuptions:\n\n'
            iteration = 1
            for i in transactions:
                mes += str(iteration) + '. 􀅽' + str(i.sum) + '􁑆   ' + i.category + '\n\n'
                iteration += 1

            bot.send_message(message.chat.id, mes)
        elif message.text.split(' ')[0] == '/addall':
            transactions = Transaction.select().where(
                Transaction.type == 'incom',
                Transaction.user == User.get(username=message.chat.id).id
            )
            mes = ''
            if locales.LOCALE == 'ru':
                mes = 'Ваши доходы за все время:\n\n'
            elif locales.LOCALE == 'en':
                mes = 'Your all incomes:\n\n'
            iteration = 1
            for i in transactions:
                mes += str(iteration) + '. 􀅼' + str(i.sum) + '􁑆   ' + i.category + '\n\n'
                iteration += 1

            bot.send_message(message.chat.id, mes)
        else:
            mes = None
            if locales.LOCALE == 'ru':
                mes = locales.ru['error404_message']
            elif locales.LOCALE == 'en':
                mes = locales.en['error404_message']
            bot.send_message(message.chat.id, mes)


bot.set_update_listener(main_bot)

try:
    bot.polling(none_stop=True)
    while True:
        pass
except KeyboardInterrupt:
    cprint('\ngoodbye', 'green')
    exit()
except Exception as e:
    cprint(str(e), 'red')
    bot.polling(none_stop=True)
