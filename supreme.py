from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import requests
import time
import csv
binary = FirefoxBinary("/Applications/Firefox.app")
firefox_path = "/Applications/Firefox.app"
geckodriver_path = "/Users/alex/PycharmProjects/test/geckodriver"

# Создадим функцию для отправки сообщений в телеграм.
def send_telegram_message(Message: str, ChatID='Default', Token='Default'):
    if ChatID == 'Default':
        ChatID = '@proga_karinaleshabot'

    if Token == 'Default':
        Token = '1736167197:AAGhntG29KrFB3blnjxGF4XeFAyGJ80KDPk'

    try:
        r = requests.get('https://api.telegram.org/bot' + Token +
                         '/sendMessage?chat_id=' + ChatID + '&text=' + Message)
    except:
        print(r)
    return r

# Объявим переменные
count = 0
urls = []  # Ссылки на товары
new_urls = []  # Ссылки на новые товары
file_name = 'supreme.csv'
file_name1 = 'sites.csv'
error_count = 0  # Счетчик ошибок для первой программы
errors = 0  # Счетчик ощибок для второй программы


with open(file_name, 'r') as filehandle:
    for line in filehandle:
        # удалим заключительный символ перехода строки
        currentPlace = line[:-1]
        # добавим элемент в конец списка
        urls.append(currentPlace)
print(send_telegram_message('Supreme'))
print(send_telegram_message(str(len(urls)) + ' вещей сейчас в списке'))
driver = webdriver.Firefox(executable_path=r'/Users/alex/PycharmProjects/test/geckodriver')

print()
print('------------------------------ ' + str(errors) + ' ошибок')
print(time.asctime())

new_urls.clear()
try:
    driver.get('https://www.supremenewyork.com/')  # Проверка сайта
except:
    print('supremenewyork не работает')
    errors += 1

try:
    driver.get('https://www.supremenewyork.com/shop')

except:
    print('Не нашел магазин')
    errors += 1

try:
    elem2 = driver.find_elements_by_xpath("/html/body/div[2]/div[3]/div/ul/li/a")
    print('Я нашел - ' + str(len(elem2)) + ' товаров')
    for element in elem2:
        if not element.get_attribute('href') in urls:
            print(element.get_attribute('href'))
            with open(file_name, 'a') as filehandle:
                filehandle.write('%s\n' % element.get_attribute('href'))
                urls.append(element.get_attribute('href'))
                new_urls.append(element.get_attribute('href'))
except:
    print('Ничего нет')
    errors += 1

print('В списке сейчас ' + str(len(urls)) + ' товаров')
print('Новые товары - ' + str(len(new_urls)))

if len(new_urls) > 0:
    for url in new_urls:
        try:
            driver.get(url)
            elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/form/fieldset[2]/input')
            elem.click()  # Проверка возможности добавления товара в корзину
            print(send_telegram_message(url))
            count += 1
            name = driver.find_element_by_id("details")
            print(str(name))
        except:
            print('Нет в наличии или не нужна ' + url)
    driver.get('https://www.supremenewyork.com/shop/cart')
print(send_telegram_message("Закончил с Supreme. Новых вещей "+str(count)))
print(send_telegram_message("Yeezy"))
print(time.asctime())
table = []
# Переход ко второй части
with open(file_name1, "r", newline="", encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        table.append(row)

elements = []
products = []

for row in table:
    try:  # Проверка новых вещей на сайтах разных стран
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


with open(file_name1, "w", newline="", encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerows(table)


driver.close()
print(send_telegram_message('закончил с YEEZY'))