from email import message
from urllib import request
import telebot
from telebot import types
import time
import random
from selenium_py.sl import Vote, save_user
from Config.config import TOKEN




import json

token = TOKEN # your token
bot = telebot.TeleBot(token, parse_mode='HTML')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Assalomu aleykum <b>{message.from_user.first_name}</b> botimizga xush kelibsiz. \n\nOvoz berishdan avval telefon nomeringizni yuboring\nMasalan: 973332222,\nIltimos +998 ishlatmang")
    bot.register_next_step_handler(message, user_answer)


@bot.callback_query_handler(func = lambda call: True)
def answer(call):
    if call.data == 'yes':
        Vote(bot=bot, msg=call.message)
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'Ovoz berish bekor qilindi')
    

def user_answer(msg):
    msg_str = str(msg.text)

    if msg_str[0] == '+':
        msg = bot.send_message(msg.chat.id, "Iltimos to'gri nomer kiriting")
    elif len(msg_str) <  9 or len(msg_str) >= 10:
        bot.send_message(msg.chat.id, 'Iltimos uzb nomer kiriting')
    else:
        phone_numb = msg_str
        bot.send_message(msg.chat.id, 'Telefon nomer saqlanmoqda...')
        resp = save_user(phone_number=phone_numb, msg=msg, bot=bot)
        print(resp)

        if resp:
            markup_inline = types.InlineKeyboardMarkup()
            item_yes = types.InlineKeyboardButton(text='Xa', callback_data='yes')
            item_no = types.InlineKeyboardButton(text='Yo\'q', callback_data='no')
            markup_inline.add(item_yes, item_no)

            bot.reply_to(msg, f"Ovoz berasizmi?", reply_markup=markup_inline)

        

    

bot.polling()