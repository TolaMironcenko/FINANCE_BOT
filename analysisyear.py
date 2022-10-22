from bot import bot
from database.models import Transaction, User
import locales
import matplotlib.pyplot as plt
import datetime
from analysismonth import have_in_vals
import currencyes


def analysis_year(message):
    transactions = Transaction.select().where(
        Transaction.user == User.get(username=message.chat.id),
        Transaction.year == datetime.datetime.today().strftime('%Y')
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
            mes += 'Нет транзакций за этот год\n'
        elif locales.LOCALE == 'en':
            mes += 'No transactions for this year\n'
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
        plt.savefig('diagrams/year/diagramallyear.png')
        mes = labels[0] + ' : +' + str(vals[0]) + '\n' + labels[1] + ' : -' + str(vals[1]) + '\n'
        with open('diagrams/year/diagramallyear.png', 'rb') as diagram:
            bot.send_photo(message.chat.id, diagram)
            bot.send_message(message.chat.id, mes)


def analysis_year_rm(message):
    transactions = Transaction.select().where(
        Transaction.user == User.get(username=message.chat.id),
        Transaction.year == datetime.datetime.today().strftime('%Y'),
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
            mes += 'Нет расходов за этот год\n'
        elif locales.LOCALE == 'en':
            mes += 'No consuptions for this year\n'
        bot.send_message(message.chat.id, mes)
    else:
        exp = []
        for _ in labels:
            exp.append(0.1)

        plt.pie(vals, labels=labels, explode=exp, wedgeprops=dict(width=0.5))
        plt.legend()
        plt.savefig('diagrams/year/rmanalysisyear.png')

        mes = ''
        pos = 0
        for i in labels:
            mes += i + ' : -' + str(vals[pos]) + currencyes.currensyes['ru-ruble'] + '\n'
            pos += 1

        with open('diagrams/year/rmanalysisyear.png', 'rb') as diagram:
            bot.send_photo(message.chat.id, diagram)
            bot.send_message(message.chat.id, mes)


def analysis_year_add(message):
    transactions = Transaction.select().where(
        Transaction.user == User.get(username=message.chat.id),
        Transaction.year == datetime.datetime.today().strftime('%Y'),
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
            mes += 'Нет доходов за этот год\n'
        elif locales.LOCALE == 'en':
            mes += 'No incomes for this year\n'
        bot.send_message(message.chat.id, mes)
    else:
        exp = []
        for _ in labels:
            exp.append(0.1)

        plt.pie(vals, labels=labels, explode=exp, wedgeprops=dict(width=0.5))
        plt.legend()
        plt.savefig('diagrams/year/addanalysisyear.png')

        mes = ''
        pos = 0
        for i in labels:
            mes += i + ' : +' + str(vals[pos]) + currencyes.currensyes['ru-ruble'] + '\n'
            pos += 1

        with open('diagrams/year/addanalysisyear.png', 'rb') as diagram:
            bot.send_photo(message.chat.id, diagram)
            bot.send_message(message.chat.id, mes)
