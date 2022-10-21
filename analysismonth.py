import currencyes
from bot import bot
import matplotlib.pyplot as plt
from database.models import User, Transaction
import datetime
import locales


# функция для обработки аналитики и построения диаграмм
def analysis_month(message):
    transactions = Transaction.select().where(
        Transaction.user == User.get(username=message.chat.id),
        Transaction.month == datetime.datetime.today().strftime('%m')
    )
    incomes = 0
    consuptions = 0
    for i in transactions:
        if i.type == 'incom':
            incomes += i.sum
        elif i.type == 'consuption':
            consuptions += i.sum

    vals = [incomes, consuptions]
    labels = []

    if locales.LOCALE == 'ru':
        labels = ['Доходы', 'Расходы']
    elif locales.LOCALE == 'en':
        labels = ['Incomes', 'Consuptions']

    exp = (0.1, 0)
    plt.pie(vals, labels=labels, explode=exp, wedgeprops=dict(width=0.5))
    plt.legend()
    plt.savefig('diagrams/diagramallmonth.png')
    mes = labels[0] + ' : +' + str(vals[0]) + '\n' + labels[1] + ' : -' + str(vals[1]) + '\n'
    with open('diagrams/diagramallmonth.png', 'rb') as diagram:
        bot.send_photo(message.chat.id, diagram)
        bot.send_message(message.chat.id, mes)


def analysis_month_rm(message):
    transactions = Transaction.select().where(
        Transaction.user == User.get(username=message.chat.id),
        Transaction.month == datetime.datetime.now().strftime('%m'),
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

    exp = []
    for _ in labels:
        exp.append(0.1)

    plt.pie(vals, labels=labels, explode=exp, wedgeprops=dict(width=0.5))
    plt.legend()
    plt.savefig('diagrams/rmanalysismonth.png')

    mes = ''
    pos = 0
    for i in labels:
        mes += i + ' : -' + str(vals[pos]) + currencyes.currensyes['ru-ruble'] + '\n'
        pos += 1

    with open('diagrams/rmanalysismonth.png', 'rb') as diagram:
        bot.send_photo(message.chat.id, diagram)
        bot.send_message(message.chat.id, mes)


def have_in_vals(category, labels):
    pos = 0
    for i in labels:
        if i == category:
            return True, pos
        pos += 1
    return False, pos


def analysis_month_add(message):
    transactions = Transaction.select().where(
        Transaction.user == User.get(username=message.chat.id),
        Transaction.month == datetime.datetime.now().strftime('%m'),
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

    exp = []
    for _ in labels:
        exp.append(0.1)

    plt.pie(vals, labels=labels, explode=exp, wedgeprops=dict(width=0.5))
    plt.legend()
    plt.savefig('diagrams/addanalysismonth.png')

    mes = ''
    pos = 0
    for i in labels:
        mes += i + ' : +' + str(vals[pos]) + currencyes.currensyes['ru-ruble'] + '\n'
        pos += 1

    with open('diagrams/addanalysismonth.png', 'rb') as diagram:
        bot.send_photo(message.chat.id, diagram)
        bot.send_message(message.chat.id, mes)
