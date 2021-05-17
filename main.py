import csv
from selenium import webdriver
import time
import requests


def send_telegram_message(Message: str, ChatID='Default', Token='Default'):
    if ChatID == 'Default':
        ChatID = '@proga_karinaleshabot'

    if Token == 'Default':
        Token = '1736167197:AAGhntG29KrFB3blnjxGF4XeFAyGJ80KDPk'

    try:
        r = requests.get('https://api.telegram.org/bot' + Token + '/sendMessage?chat_id=' + ChatID + '&text=' + Message)
    except:
        print(r)
    return r


file_name = 'sites.csv'
error_count = 0

driver = webdriver.Firefox(executable_path=r'/Users/alex/PycharmProjects/test/geckodriver')

driver.implicitly_wait(5)

while 1 == 1:
    print(time.asctime())
    table = []

    with open(file_name, "r", newline="", encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        for row in reader:
            table.append(row)

    elements = []
    products = []

    for row in table:
        # print('-----------------------------')
        try:
            driver.get(row[1])
            time.sleep(5)
            elements = driver.find_elements_by_class_name(row[2])
            if len(elements) == 0:
                driver.refresh
                time.sleep(5)
                elements = driver.find_elements_by_class_name(str(row[2]))
            if len(elements) > 0:
                products.clear()
                for j in elements:
                    products.append(str(j.text))
                if not str(row[3]) == str(products) and not str(products[0]) == "":
                    row[3] = str(products)
                    print('-----------------------------')
                    print('Новые товары ' + str(products), str(row[1]), sep='\n')
                    print(send_telegram_message('Новые товары ' + str(products) + '\n' + str(row[1])))
        except:
            print('-----------------------------')
            print("Не нашел на - " + str(row[1]))
            print(send_telegram_message("Не нашел на - " + str(row[1])))


    with open(file_name, "w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(table)

    time.sleep(3600)

driver.close()