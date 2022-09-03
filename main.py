import telebot
from telebot import types
import time
import random
from selenium_py.sl import Vote
from Config.config import TOKEN

token = TOKEN # your token


bot = telebot.TeleBot(token, parse_mode='HTML')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Assalomu aleykum <b>{message.from_user.first_name}</b> botimizga xush kelibsiz.\nOvoz berish uchun /vote buyru'gini yuboring")

@bot.message_handler(commands=['vote'])
def send_welcome(message):
    msg = bot.reply_to(message, f"Ovoz berish uchun telefon nomeringizni yuboring\nMasalan: <b>909175555</b>,\nIltimos <b>+998</b> ishlatmang!")
    bot.register_next_step_handler(msg, user_answer)

def user_answer(msg):
    msg_str = str(msg.text)

    if msg_str[0] == '+':
        msg = bot.send_message(msg.chat.id, "Iltimos to'gri nomer kiriting")
        bot.register_next_step_handler(msg, user_answer)
    elif len(msg_str) <  9 or len(msg_str) >= 10:
        bot.send_message(msg.chat.id, 'Iltimos uzb nomer kiriting')
        bot.register_next_step_handler(msg, user_answer)
    else:
        
        phone_numb = msg_str
        
        Vote(phone_number=phone_numb, bot=bot, msg=msg)


bot.polling()