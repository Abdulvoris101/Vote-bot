from selenium import webdriver
from selenium.webdriver.common.by import By
import time


options = webdriver.ChromeOptions()
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36')

driver = webdriver.Chrome(executable_path='C:\\Users\\User\\Desktop\\Code\\py_bots\\vote_bot\\chromedriver.exe', options=options)
url = "https://openbudget.uz/boards/6/129485/"

try:
    driver.get(url=url)
    btn_elem = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/section/div/div/div[2]/div/div[5]/div[2]/div/a')
    print(btn_elem.text)
    time.sleep(5)

except Exception as ex:
    print(ex)
finally:
    driver.close()