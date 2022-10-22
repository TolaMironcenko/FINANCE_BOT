import datetime
from termcolor import cprint
from bot import bot
import locales
from changelocale import change_locale
from database.models import User, Transaction
from currencyes import currensyes
from multiprocessing import Process
from analysismonth import analysis_month, analysis_month_rm, analysis_month_add
from analysisyear import analysis_year, analysis_year_rm, analysis_year_add
from analysistoday import analysis_today, analysis_today_rm, analysis_today_add


# функция ограничения количества знаков после запятой
def to_fixed(num_obj, digits=0):
    return f"{num_obj:.{digits}f}"


def main():
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
                mes += to_fixed(user.balance, 2) + currensyes['ru-ruble']
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
                    bot.send_message(message.chat.id, to_fixed(user.balance, 2) + currensyes['ru-ruble'])
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
                    bot.send_message(message.chat.id, to_fixed(user.balance, 2) + currensyes['ru-ruble'])
            elif message.text.split(' ')[0] == '/addtoday':
                transactions = Transaction.select().where(
                    Transaction.type == 'incom',
                    Transaction.day == datetime.datetime.today().strftime('%d'),
                    Transaction.user == User.get(username=message.chat.id).id
                )
                mes = ''
                if locales.LOCALE == 'ru':
                    mes = 'Ваши доходы за сегодня:\n\n'
                elif locales.LOCALE == 'en':
                    mes = 'Your incomes today:\n\n'
                iteration = 1
                if len(transactions) == 0:
                    if locales.LOCALE == 'ru':
                        mes += 'Нет доходов за сегодня\n'
                    elif locales.LOCALE == 'en':
                        mes += 'No incomes today\n'
                for i in transactions:
                    mes += '-------------------------------------\n'
                    mes += str(iteration) + '  ||  +' + str(i.sum) + currensyes['ru-ruble'] + '  ||  ' + i.category \
                        + '  ||  ' + str(i.day) + '-' + str(i.month) + '-' + str(i.year) \
                        + '  ||  ' + i.time.strftime('%H:%M:%S') + '  ||\n'
                    iteration += 1
                mes += '-------------------------------------\n'
                bot.send_message(message.chat.id, mes)
            elif message.text.split(' ')[0] == '/rmtoday':
                transactions = Transaction.select().where(
                    Transaction.type == 'consuption',
                    Transaction.day == datetime.datetime.today().strftime('%d'),
                    Transaction.user == User.get(username=message.chat.id).id
                )
                mes = ''
                if locales.LOCALE == 'ru':
                    mes = 'Ваши расходы за сегодня:\n\n'
                elif locales.LOCALE == 'en':
                    mes = 'Your consuptions today:\n\n'
                iteration = 1
                if len(transactions) == 0:
                    if locales.LOCALE == 'ru':
                        mes += 'Нет расходов за сегодня\n'
                    elif locales.LOCALE == 'en':
                        mes += 'No consuptions today\n'
                for i in transactions:
                    mes += '-------------------------------------\n'
                    mes += str(iteration) + '  ||  -' + str(i.sum) + currensyes['ru-ruble'] + '  ||  ' + i.category \
                        + '  ||  ' + str(i.day) + '-' + str(i.month) + '-' + str(i.year) \
                        + '  ||  ' + i.time.strftime('%H:%M:%S') + '  ||\n'
                    iteration += 1
                mes += '-------------------------------------\n'
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
                if len(transactions) == 0:
                    if locales.LOCALE == 'ru':
                        mes += 'Нет расходов за все время\n'
                    elif locales.LOCALE == 'en':
                        mes += 'No consuptions for all time\n'
                for i in transactions:
                    mes += '-------------------------------------\n'
                    mes += str(iteration) + '  ||  -' + str(i.sum) + currensyes['ru-ruble'] + '  ||  ' + i.category \
                        + '  ||  ' + str(i.day) + '-' + str(i.month) + '-' + str(i.year) \
                        + '  ||  ' + i.time.strftime('%H:%M:%S') + '  ||\n'
                    iteration += 1
                mes += '-------------------------------------\n'
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
                if len(transactions) == 0:
                    if locales.LOCALE == 'ru':
                        mes += 'Нет доходов за все время\n'
                    elif locales.LOCALE == 'en':
                        mes += 'No incomes for all time\n'
                for i in transactions:
                    mes += '-------------------------------------\n'
                    mes += str(iteration) + '  ||  +' + str(i.sum) + currensyes['ru-ruble'] + '  ||  ' + i.category \
                        + '  ||  ' + str(i.day) + '-' + str(i.month) + '-' + str(i.year) \
                        + '  ||  ' + i.time.strftime('%H:%M:%S') + '  ||\n'
                    iteration += 1
                mes += '-------------------------------------\n'
                bot.send_message(message.chat.id, mes)
            elif message.text.split(' ')[0] == '/rmmonth':
                transactions = Transaction.select().where(
                    Transaction.user == User.get(username=message.chat.id),
                    Transaction.month == datetime.datetime.now().strftime('%m'),
                    Transaction.type == 'consuption'
                )
                mes = ''
                if locales.LOCALE == 'ru':
                    mes = 'Ваши расходы за этот месяц:\n\n'
                elif locales.LOCALE == 'en':
                    mes = 'Your consuptions for this month:\n\n'
                iteration = 1
                if len(transactions) == 0:
                    if locales.LOCALE == 'ru':
                        mes += 'Нет расходов за этот месяц\n'
                    elif locales.LOCALE == 'en':
                        mes += 'No consuptions for this month\n'

                for i in transactions:
                    mes += '-------------------------------------\n'
                    mes += str(iteration) + '  ||  -' + str(i.sum) + currensyes['ru-ruble'] + '  ||  ' + i.category \
                        + '  ||  ' + str(i.day) + '-' + str(i.month) + '-' + str(i.year) \
                        + '  ||  ' + i.time.strftime('%H:%M:%S') + '  ||\n'
                    iteration += 1
                mes += '-------------------------------------\n'
                bot.send_message(message.chat.id, mes)
            elif message.text.split(' ')[0] == '/addmonth':
                transactions = Transaction.select().where(
                    Transaction.user == User.get(username=message.chat.id),
                    Transaction.month == datetime.datetime.now().strftime('%m'),
                    Transaction.type == 'incom'
                )
                mes = ''
                if locales.LOCALE == 'ru':
                    mes = 'Ваши доходы за этот месяц:\n\n'
                elif locales.LOCALE == 'en':
                    mes = 'Your incomes for this month:\n\n'
                iteration = 1
                if len(transactions) == 0:
                    if locales.LOCALE == 'ru':
                        mes += 'Нет доходов за этот месяц\n'
                    elif locales.LOCALE == 'en':
                        mes += 'No incomes for this month\n'

                for i in transactions:
                    mes += '-------------------------------------\n'
                    mes += str(iteration) + '  ||  +' + str(i.sum) + currensyes['ru-ruble'] + '  ||  ' + i.category \
                        + '  ||  ' + str(i.day) + '-' + str(i.month) + '-' + str(i.year) \
                        + '  ||  ' + i.time.strftime('%H:%M:%S') + '  ||\n'
                    iteration += 1
                mes += '-------------------------------------\n'
                bot.send_message(message.chat.id, mes)
            elif message.text.split(' ')[0] == '/analysismonth':
                Process(target=analysis_month, args=(message,)).start()
            elif message.text.split(' ')[0] == '/rmanalysismonth':
                Process(target=analysis_month_rm, args=(message, )).start()
            elif message.text.split(' ')[0] == '/addanalysismonth':
                Process(target=analysis_month_add, args=(message,)).start()
            elif message.text.split(' ')[0] == '/analysisyear':
                Process(target=analysis_year, args=(message, )).start()
            elif message.text.split(' ')[0] == '/rmanalysisyear':
                Process(target=analysis_year_rm, args=(message, )).start()
            elif message.text.split(' ')[0] == '/addanalysisyear':
                Process(target=analysis_year_add, args=(message, )).start()
            elif message.text.split(' ')[0] == '/analysistoday':
                Process(target=analysis_today, args=(message,)).start()
            elif message.text.split(' ')[0] == '/rmanalysistoday':
                Process(target=analysis_today_rm, args=(message,)).start()
            elif message.text.split(' ')[0] == '/addanalysistoday':
                Process(target=analysis_today_add, args=(message,)).start()
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


if __name__ == '__main__':
    main()
