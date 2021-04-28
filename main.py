import csv
from selenium import webdriver
import time
import requests


def send_telegram_message(Message: str, ChatID='Default', Token='Default'):
    if ChatID == 'Default':
        ChatID = '@proga_karinaleshabot'
        # ChatID = '170004524

    if Token == 'Default':
        Token = '1736167197:AAGhntG29KrFB3blnjxGF4XeFAyGJ80KDPk'

    #r = ProxyRequests('https://api.ipify.org')

    try:
        r = requests.get('https://api.telegram.org/bot' + Token + '/sendMessage?chat_id=' + ChatID + '&text=' + Message)
    except:
        print(r)
    return r


file_name = 'sites.csv'
# table=[]
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
            time.sleep(20)
            elements = driver.find_elements_by_class_name(row[2])
            if len(elements) == 0:
                driver.refresh
                time.sleep(20)
                elements = driver.find_elements_by_class_name(str(row[2]))
            if len(elements) > 0:
                products.clear()
                for j in elements:
                    products.append(str(j.text))
                if not str(row[3]) == str(products) and not str(products[0]) == "":
                    row[3] = str(products)
                    print('-----------------------------')
                    print('changed products ' + str(products), str(row[1]), sep='\n')
                    print(send_telegram_message('changed products ' + str(products) + '\n' + str(row[1])))

                    # else:
                #    print("without changes on the " + str(row[1]))
        except:
            # error_count += 1
            # print (str(error_count) + ' ошибок')
            print('-----------------------------')
            print("I didn't find it in the - " + str(row[1]))


    with open(file_name, "w", newline="", encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(table)

    time.sleep(3600)

driver.close()