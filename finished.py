from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import requests
import time
import csv
binary = FirefoxBinary('/Applications/Firefox.app')
firefox_path = '/Applications/Firefox.app'
geckodriver_path = '/Users/alex/PycharmProjects/test/geckodriver'

# Создадим функцию для отправки сообщений в телеграм.
def send_telegram_message(Message: str, ChatID='Default', Token='Default'):
    if ChatID == 'Default':
        ChatID = '@proga_karinaleshabot'

    if Token == 'Default':
        Token = '1736167197:AAGhntG29KrFB3blnjxGF4XeFAyGJ80KDPk'

    r = requests.get(f'https://api.telegram.org/bot{Token}/sendMessage?chat_id={ChatID}&text={Message}')

    return r

# Объявим переменные
count = 0
urls = []  # Ссылки на товары
new_urls = []  # Ссылки на новые товары
file_name_supreme = 'supreme.csv'
file_name_yeezy = 'sites.csv'
errors = 0  # Счетчик ощибок для второй программы


with open(file_name_supreme, 'r') as filehandle:
    for line in filehandle:
        # удалим заключительный символ перехода строки
        currentPlace = line[:-1]
        # добавим элемент в конец списка
        urls.append(currentPlace)
print(send_telegram_message('Supreme'))
print(send_telegram_message(str(len(urls)) + ' вещей сейчас в списке'))
driver = webdriver.Firefox(executable_path=r'/Users/alex/PycharmProjects/test/geckodriver')

new_urls.clear()
try:
    driver.get('https://www.supremenewyork.com/')  # Проверка сайта
except WebDriverException:
    print('supremenewyork не работает')
    errors += 1

try:
    driver.get('https://www.supremenewyork.com/shop')

except WebDriverException:
    print('Не нашел магазин')
    errors += 1

try:
    goods_supreme = driver.find_elements_by_xpath('/html/body/div[2]/div[3]/div/ul/li/a')
    print('Я нашел - ' + str(len(goods_supreme)) + ' товаров')

    with open(file_name_supreme, 'a') as filehandle:
        for element in goods_supreme:
            if not element.get_attribute('href') in urls:
                print(element.get_attribute('href'))
                filehandle.write('%s\n' % element.get_attribute('href'))
                urls.append(element.get_attribute('href'))
                new_urls.append(element.get_attribute('href'))
except NoSuchElementException:
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
        except WebDriverException:
            print('Нет в наличии или не нужна ' + url)
    driver.get('https://www.supremenewyork.com/shop/cart')
print(send_telegram_message('Закончил с Supreme. Новых вещей '+str(count)))
print(send_telegram_message('Yeezy'))
print(time.asctime())
table = []
# Переход ко второй части
with open(file_name_yeezy, 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    for site in reader:
        table.append(site)

elements = []
products = []

for site in table:
    try:  # Проверка новых вещей на сайтах разных стран
        driver.get(site[1])
        time.sleep(5)
        elements = driver.find_elements_by_class_name(site[2])
        if not elements:
            driver.refresh
            time.sleep(5)
            elements = driver.find_elements_by_class_name(site[2])
        if len(elements) > 0:
            products.clear()
            products = [str(j.text) for j in elements]
            if not site[3] == str(products) and products[0]:
                site[3] = str(products)
                print('Новые товары ' + str(products), site[1], sep='\n')
                print(send_telegram_message('Новые товары ' + str(products) + '\n' + site[1]))
    except WebDriverException:
        print('Не нашел на - ' + site[1])
        print(send_telegram_message('Не нашел на - ' + site[1]))


with open(file_name_yeezy, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerows(table)


driver.close()
print(send_telegram_message('закончил с YEEZY'))