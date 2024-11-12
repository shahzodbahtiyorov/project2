import telebot
from django.core.management.base import BaseCommand
from telebot.types import Message

from v1.gateway import TELEGRAM_ACCESS_TOKEN
from v1.models.errors import Service

bot = telebot.TeleBot(TELEGRAM_ACCESS_TOKEN, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    bot.reply_to(message, "Message receive")


@bot.message_handler(func=lambda m: True)
def echo_all(message: Message):
    global text
    if message.chat.id != 1297756271:
        bot.reply_to(message, "🤌🤌🤌")
        return False
    key = 1
    if message.text == '/0':
        key = 'transfer.transfer.create'
    elif message.text == '/1':
        key = 'payment.transfer.create'
    elif message.text == '/2':
        key = 'mts.transfer.create'
    elif message.text == '/3':
        key = 'mts.payment.create'
    elif message.text == '/4':
        key = 'tcb.transfer.create'
    elif message.text == '/5':
        key = 'tcb.payment.create'
    elif message.text == '/6':
        key = 'tcb.transfer.rf.create'
    elif message.text == '/7_1':
        key = 'visa.conversion.cr.create'
    elif message.text == '/7_2':
        key = 'visa.conversion.dr.create'
    elif message.text == '/8':
        key = 'visa.transfer.create'
    elif message.text == '/11':
        key = 'tj.transfer.create'
    elif message.text == '/12':
        key = 'armenia.transfer.create'
    elif message.text == '/13':
        key = 'turkey.transfer.create'
    elif message.text == '/14':
        key = 'kazakh.transfer.create'
    elif message.text == '/15':
        key = 'azr.transfer.create'
    elif message.text == '/16':
        key = 'sbp.transfer.create'
    elif message.text == '/17':
        key = 'visa.direct.transfer.create'
    elif message.text == '/18':
        key = 'mts.rf_payment.create'
    elif message.text == '/19':
        key = 'paygine.transfer.create'
    elif message.text == '/20':
        key = 'georgia.transfer.create'
    elif message.text == '/21':
        key = 'schools.transfer.create'
    elif message.text == '/22_1':
        key = 'visa.universal.ru.to.visa.transfer.create'
    elif message.text == '/22_2':
        key = 'visa.universal.uz.to.visa.transfer.create'
    elif message.text == '/23':
        key = 'upaygine.transfer.create'
    elif message.text == '/24':
        key = 'payment.by.details'
    elif message.text == '/25':
        key = 'kindergartens.payment.create'
    elif message.text == '/100':
        key = 'card.register.uzcard'
    elif message.text == '/101':
        key = 'card.register.humo'
    elif message.text == '/102':
        key = 'card.register.visa'
    elif message.text == '/103':
        key = 'visa.create'
    elif message.text == '/200':
        key = 'auth.register'
    service = Service.objects.filter(method=key).first()
    if service:
        service.is_active = not service.is_active
        service.save()
        if service.is_active:
            text = 'Service '+message.text+' is ON!'
        else:
            text = 'Service '+message.text+' is OFF!'
    bot.reply_to(message, text)


class Command(BaseCommand):
    help = "Run the bot"

    def handle(self, *args, **options):
        bot.polling()

