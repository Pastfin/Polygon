from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver

from telegram import Bot, Update
from telegram.ext import Updater

import pandas as pd
import datetime
import inspect
import pickle

import time
import sys
import re


CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
WINDOW_SIZE = "1920,1080"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                          chrome_options=chrome_options
                         )

def get_auth():

    link = driver.get('https://steamcommunity.com/login/home/?goto=')

    login = driver.find_element_by_id('steamAccountName')
    password = driver.find_element_by_id('steamPassword')
    entire = driver.find_element_by_id('SteamLogin')

    login.send_keys('')
    time.sleep(0.5)
    password.send_keys('')
    time.sleep(0.5)
    entire.click()
    code = input('Введите код: ')

    auth = driver.find_element_by_id('twofactorcode_entry')
    auth.send_keys(code)

    finish = driver.find_element(By.XPATH, 'html[1]/body[1]/div[3]/div[3]/div[1]/div[1]/div[1]/form[1]/div[4]/div[1]/div[1]/div[1]')
    finish.click()
    time.sleep(6)

    driver.get('https://steamcommunity.com/openid/login?openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.mode=checkid_setup&openid.return_to=http%3A%2F%2F79.174.12.1'
               '15%2Fauthorization.php%3Flogin%26domain_new_1&openid.realm=http%3A%2F%2F79.174.12.115&openid.ns.sreg=http%3A%2F%2Fopenid.net%2Fextensions%2Fsreg%2F1.1&openid.claimed'
               '_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select')
    element = driver.find_element_by_id('imageLogin')

    element.click()
    time.sleep(5)


def check_time_round():
    global a, data_quantity, list1
    try:
        while True:
            try:
                while True:
                    page = driver.page_source
                    timer = re.findall('progress_timer.*?in (..)', page)

                    if str(timer) == "['2.', '2.']":
                        break
                    elif str(timer) == '[]' or str(timer) == "['0.', '0.']":
                        print('Error_check_time_1')
                        text = 'Error_check_time_1' + '\n' + f'Индекс в базе: {a}'
                        driver.refresh()
                        time.sleep(4)
                        main(text)
                    time.sleep(0.5)
            except:
                print('Error_check_time_2')
                driver.refresh()
                time.sleep(4)
                text = 'Error_check_time_2' + '\n' + f'Индекс в базе: {a}'
                main(text)
                check_time_round()
                time.sleep(4)

            page = driver.page_source
            bet = re.findall('class="total">(.*?)<', str(page))
            date = datetime.datetime.today().strftime("%d-%m-%Y")
            timee = datetime.datetime.today().strftime('%X')
            online = re.findall('online">(.*?)<', str(page))[-1]
            time.sleep(20)
            page1 = driver.page_source
            paragraph = re.findall('<li class="ball".*?<.li><.ul>', str(page1))
            balls = re.findall('class="([^"ball"].*?)">(.*?)<', str(paragraph))
            ball = balls[-1]

            color_result = ball[0]
            number_result = ball[1]
            bet_red = bet[0]
            bet_green = bet[1]
            bet_black = bet[2]

            try:
                a += 1
                data_quantity += 1

                df.loc[a] = 0

                df['date'].iloc[a] = date
                df['time'].iloc[a] = timee

                df['color_result'].iloc[a] = color_result
                df['number_result'].iloc[a] = number_result

                df['red_bet'].iloc[a] = bet_red
                df['green_bet'].iloc[a] = bet_green
                df['black_bet'].iloc[a] = bet_black

                df['online'].iloc[a] = online


            except:
                print('Error_find')
                text = 'Error_find' + '\n' + f'Индекс в базе: {a}'
                main(text)
                check_time_round()

            print('\ndata_quantity: ', data_quantity)
            if data_quantity % 10 == 0:
                list1.append(balls)
                pickle.dump(list1, open("numbers.txt", "wb"))
                print('Прошла запись листа')

                df.to_csv('data_poly')
                print('Прошла запись базы')
                # print (df['number_result'])
                time.sleep(1)
                if data_quantity % 100 == 0:
                    text = f'{a}'
                    main(text)

    except:
        text = f'Было записано {a} строк.\nCrash'
        main(text)
        sys.exit()




def main(text):
    bot = Bot(
        token="",
        base_url="https://telegg.ru/orig/bot",)
    
    updater = Updater(
        bot=bot,)

    bot.send_message(
        chat_id=194990305,
        text=text)

    updater.start_polling()


if __name__ == '__main__':
    a = -1
    data_quantity = -1
    list1 = []

    df = pd.DataFrame(
        {
            'date': [], 'time': [], 'color_result': [], 'number_result': [], 'red_bet': [], 'green_bet': [],
            'black_bet': [], 'online': []
        }
    )

    get_auth()
    check_time_round()
    sys.exit()