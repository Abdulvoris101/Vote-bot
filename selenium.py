from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# class VoteOpenBudget:
#     def 



options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36')

driver = webdriver.Chrome(executable_path='C:\\Users\\User\\Desktop\\Code\\py_bots\\vote_bot\\chromedriver.exe', options=options)
url = "https://openbudget.uz/boards/6/129485/"



try:
    driver.get(url=url)

    vote_btn = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/section/div/div/div[2]/div/div[5]/div[2]/div/a')
    vote_btn.click()

    time.sleep(2)

    get_sms = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/section/div[2]/div/div[2]/div/a')
    get_sms.click()

    time.sleep(2)

    phone_num = driver.find_element(By.ID, 'phone')
    phone_num.send_keys(phone)
    
    time.sleep(3)
    

    verif_phone = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/section/div[2]/div/div[2]/form/div[2]/button')
    verif_phone.click()

    time.sleep(3)

    time.sleep(2)

    input_verif = driver.find_element(By.XPATH, '//*[@id="phone"]').send_keys(key)
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="__layout"]/div/section/div[2]/div/div[2]/form/div[2]/button').click()

    time.sleep(5)

except Exception as ex:
    print(ex)
finally:
    driver.close()