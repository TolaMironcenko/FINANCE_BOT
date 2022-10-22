from bot import bot
from database.models import Transaction, User
import matplotlib.pyplot as plt
import locales
import datetime
import currencyes
from analysismonth import have_in_vals


def analysis_today(message):
    transactions = Transaction.select().where(
        Transaction.user == User.get(username=message.chat.id),
        Transaction.month == datetime.datetime.today().strftime('%m'),
        Transaction.year == datetime.datetime.today().strftime('%Y'),
        Transaction.day == datetime.datetime.today().strftime('%d')
    )
    incomes = 0
    consuptions = 0
    for i in transactions:
        if i.type == 'incom':
            incomes += i.sum
        elif i.type == 'consuption':
            consuptions += i.sum
    mes = ''
    if len(transactions) == 0:
        if locales.LOCALE == 'ru':
            mes += 'Нет транзакций за сегодня\n'
        elif locales.LOCALE == 'en':
            mes += 'No transactions today\n'
        bot.send_message(message.chat.id, mes)
    else:
        vals = [incomes, consuptions]
        labels = []

        if locales.LOCALE == 'ru':
            labels = ['Доходы', 'Расходы']
        elif locales.LOCALE == 'en':
            labels = ['Incomes', 'Consuptions']

        exp = (0.1, 0)
        plt.pie(vals, labels=labels, explode=exp, wedgeprops=dict(width=0.5))
        plt.legend()
        plt.savefig('diagrams/today/diagramalltoday.png')
        mes = labels[0] + ' : +' + str(vals[0]) + '\n' + labels[1] + ' : -' + str(vals[1]) + '\n'
        with open('diagrams/today/diagramalltoday.png', 'rb') as diagram:
            bot.send_photo(message.chat.id, diagram)
            bot.send_message(message.chat.id, mes)


def analysis_today_rm(message):
    transactions = Transaction.select().where(
        Transaction.user == User.get(username=message.chat.id),
        Transaction.month == datetime.datetime.now().strftime('%m'),
        Transaction.year == datetime.datetime.today().strftime('%Y'),
        Transaction.day == datetime.datetime.today().strftime('%d'),
        Transaction.type == 'consuption'
    )
    vals = []
    labels = []
    for i in transactions:
        if have_in_vals(i.category, labels)[0]:
            pos = have_in_vals(i.category, labels)[1]
            vals[pos] += i.sum
        else:
            labels.append(i.category)
            vals.append(i.sum)
    mes = ''
    if len(transactions) == 0:
        if locales.LOCALE == 'ru':
            mes += 'Нет расходов за сегодня\n'
        elif locales.LOCALE == 'en':
            mes += 'No сonsuptions today\n'
        bot.send_message(message.chat.id, mes)
    else:
        exp = []
        for _ in labels:
            exp.append(0.1)

        plt.pie(vals, labels=labels, explode=exp, wedgeprops=dict(width=0.5))
        plt.legend()
        plt.savefig('diagrams/today/rmanalysistoday.png')

        mes = ''
        pos = 0
        for i in labels:
            mes += i + ' : -' + str(vals[pos]) + currencyes.currensyes['ru-ruble'] + '\n'
            pos += 1

        with open('diagrams/today/rmanalysistoday.png', 'rb') as diagram:
            bot.send_photo(message.chat.id, diagram)
            bot.send_message(message.chat.id, mes)


def analysis_today_add(message):
    transactions = Transaction.select().where(
        Transaction.user == User.get(username=message.chat.id),
        Transaction.month == datetime.datetime.now().strftime('%m'),
        Transaction.year == datetime.datetime.today().strftime('%Y'),
        Transaction.day == datetime.datetime.today().strftime('%d'),
        Transaction.type == 'incom'
    )
    vals = []
    labels = []
    for i in transactions:
        if have_in_vals(i.category, labels)[0]:
            pos = have_in_vals(i.category, labels)[1]
            vals[pos] += i.sum
        else:
            labels.append(i.category)
            vals.append(i.sum)
    mes = ''
    if len(transactions) == 0:
        if locales.LOCALE == 'ru':
            mes += 'Нет доходов за сегодня\n'
        elif locales.LOCALE == 'en':
            mes += 'No incomes today\n'
        bot.send_message(message.chat.id, mes)
    else:
        exp = []
        for _ in labels:
            exp.append(0.1)

        plt.pie(vals, labels=labels, explode=exp, wedgeprops=dict(width=0.5))
        plt.legend()
        plt.savefig('diagrams/today/addanalysistoday.png')

        mes = ''
        pos = 0
        for i in labels:
            mes += i + ' : +' + str(vals[pos]) + currencyes.currensyes['ru-ruble'] + '\n'
            pos += 1

        with open('diagrams/today/addanalysistoday.png', 'rb') as diagram:
            bot.send_photo(message.chat.id, diagram)
            bot.send_message(message.chat.id, mes)
