from main import vote_to
import telebot
from telebot import types

token = '5664019486:AAGdBQKWdic-MVhcZtx11h6wAMGwXnEE900'


bot = telebot.TeleBot(token, parse_mode='HTML')

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, f"Assalomu aleykum <b>{message.from_user.first_name}</b> botimizga xush kelibsiz.\nOvoz berish uchun /vote buyru'gini yuboring")

@bot.message_handler(commands=['vote'])
def send_welcome(message):
	# msg = bot.reply_to(message, f"Ovoz berishdan avval telefon nomeringizni yuboring  Masalan: 909175555")
    msg = bot.reply_to(message, f"Ovoz berishdan avval telefon nomeringizni yuboring\nMasalan: <b>909175555</b>,\nIltimos <b>+998</b> ishlatmang!")
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
        kb = types.InlineKeyboardMarkup()
        item_yes = types.InlineKeyboardButton(text='Xa', callback_data='yes')
        item_no = types.InlineKeyboardButton(text='Yoq', callback_data='no')
        kb.add(item_yes, item_no)

        global phone_num
        phone_num = msg_str

        msg = bot.send_message(msg.chat.id, 'Ovoz berish uchun <b>Xa</b> ni bosing', reply_markup=kb)

@bot.callback_query_handler(func= lambda call:True)
def answer(call):
    if call.data == 'yes':
        vote_to(phone_num)
        bot.send_message(call.message.chat.id, 'Ovoz berganingiz uchun raxmat')
    elif call.data == 'no':
        bot.send_message(call.message.chat.id, 'Ovoz berish bekor qilindi')


bot.polling()