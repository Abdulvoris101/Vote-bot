import telebot
from telebot import types
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
from fake_useragent import UserAgent


token = '5664019486:AAGdBQKWdic-MVhcZtx11h6wAMGwXnEE900'


bot = telebot.TeleBot(token, parse_mode='HTML')

useragent = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(f'user-agent={useragent.random}')




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
        
        phone_numb = msg_str
        # Selenium 

        

        global driver
        driver = webdriver.Chrome(executable_path='C:\\Users\\User\\Desktop\\Code\\py_bots\\vote_bot\\chromedriver.exe', options=options)
        url = "https://openbudget.uz/boards/6/129485/"
        # url = 'https://www.whatismybrowser.com/detect/what-is-my-user-agent/'

        driver.get(url=url)

        vote_btn = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/section/div/div/div[2]/div/div[5]/div[2]/div/a')
        vote_btn.click()

        time.sleep(2)

        get_sms = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/section/div[2]/div/div[2]/div/a')
        get_sms.click()

        time.sleep(3)
    
        phone_num = driver.find_element(By.ID, 'phone')
        phone_num.send_keys(phone_numb)

        time.sleep(5)


        verif_phone = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/section/div[2]/div/div[2]/form/div[2]/button')
        verif_phone.click()
        

        form = driver.find_element(By.CLASS_NAME, 'form')
        time.sleep(6)
        
        error = form.find_element(By.XPATH, '//*[@id="__layout"]/div/section/div[2]/div/div[2]/form/p')
        
        if error:
            bot.send_message(msg.chat.id, 'Siz ovoz bergansiz!')
            driver.close()
        
        time.sleep(5)


        key = bot.send_message(msg.chat.id, 'Sms kodni kiriting')

        bot.register_next_step_handler(key, sms_verif)


def sms_verif(key):
    input_verif = driver.find_element(By.XPATH, '//*[@id="phone"]').send_keys(key)

    time.sleep(2)

    driver.find_element(By.XPATH, '//*[@id="__layout"]/div/section/div[2]/div/div[2]/form/div[2]/button').click()

    time.sleep(5)

    driver.close()







bot.polling()