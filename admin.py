import telebot
from Config.config import TOKEN_ADMIN, PASSWORD
from telebot import types
import sqlite3

db = sqlite3.connect('server.db', check_same_thread=False)
sql = db.cursor()


sql.execute("""CREATE TABLE IF NOT EXISTS admins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(250),
    username VARCHAR(250),
    telegram_id BIGINT,
    status BOOLEAN
)""")

db.commit()

token = TOKEN_ADMIN # your token 

bot = telebot.TeleBot(token, parse_mode='HTML')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global admin
    admin = False

    create_user(message)

    if check_user(message):
        admin = True
        markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
        users = types.KeyboardButton('users')
        admins = types.KeyboardButton('admins')
        markup.add(users, admins)

        bot.send_message(message.chat.id, f"Assalomu aleykum <b>admin</b> botga xush kelibsiz", reply_markup=markup)

    else:
        msg = bot.send_message(message.chat.id, f"Assalomu aleykum <b>{message.from_user.first_name}</b> botni ishlatish uchun parolni kiriting")
        bot.register_next_step_handler(msg, check_password)

def check_password(msg):
    if msg.text == PASSWORD:
        
        sql.execute(f" UPDATE admins SET status = 1 WHERE telegram_id = {msg.chat.id};")
        db.commit()

        markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
        users = types.KeyboardButton('users')
        admins = types.KeyboardButton('admins')
        markup.add(users, admins)

        bot.send_message(msg.chat.id, f"Botimizga xush kelibsiz", reply_markup=markup)
    else:
        bot.send_message(msg.chat.id, f"Parol notog'ri, boshqatan urinib ko'ring /start")

def create_user(message):
    telegram_id = message.chat.id
    first_name = message.chat.first_name
    username = message.chat.username
    status = 0
    values = first_name, username, telegram_id, status

    use = sql.execute(f"SELECT id FROM admins WHERE telegram_id={telegram_id}")

    print(use)

    if use.fetchone() is None:
        sql.execute(f"INSERT INTO admins(first_name, username, telegram_id, status) VALUES(?, ?, ?, ?)", values) 
        db.commit()
    else:
        print('Have this user')

@bot.message_handler(content_types=['text'])
def text_handler(message):
    if check_user(message):
        if message.text == 'users':
            get_users(message)
        elif message.text == 'admins':
            get_admins(message)
    else:
        bot.send_message(message.chat.id, 'Iltimos ro\'yhatdan o\'ting! /start')

def get_users(message):
    users = sql.execute("SELECT * from users")
    
    for user in users:
        id = user[0]
        first_name = user[1]
        username = user[2]
        telegram_id = user[3]
        status = user[4]
        phone_number = user[5]

        if status == 1:
            status_m = 'Ovoz bergan'
        else:
            status_m = 'Ovoz bermagan'

        bot.send_message(message.chat.id, f"{first_name} #{id} \n\nid: {id}, \nusername: {username}, \ntelegram_id: {telegram_id}, \nphone: {phone_number}, \nstatus: {status_m}")

def get_admins(message):
    admins = sql.execute("SELECT * from admins")

    for admin in admins:
        status = admin[4]
        if status == 1:
            id = admin[0]
            first_name = admin[1]
            username = admin[2]
            telegram_id = admin[3]
            bot.send_message(message.chat.id, f"{first_name} #{id} \n\nid:{id}, \nusername:{username}, \ntelegram_id:{telegram_id}")

def check_user(message):
    status = sql.execute(f"SELECT status FROM admins WHERE telegram_id={message.chat.id}")

    status_f = str(status.fetchone()).replace('(', '').replace(')', '').replace(',', '')
    print(status_f)
    print(status.fetchone())

    global admin
    admin = False

    if status_f == '1':
        admin = True
        return True
    
    return False

bot.polling()