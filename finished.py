from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import requests
import time
import csv
binary = FirefoxBinary('/Applications/Firefox.app')
firefox_path = '/Applications/Firefox.app'
geckodriver_path = '/Users/alex/PycharmProjects/test/geckodriver'

# Создадим функцию для отправки сообщений в телеграм.
def decorator(function_to_decorate):
    def wrapper(arg1):
        print(f'Отправил сообщение в Telegram:  {arg1}')
        function_to_decorate(arg1)
    return wrapper
@decorator
def send_telegram_message(Message: str, ChatID='Default', Token='Default'):
    if ChatID == 'Default':
        ChatID = '@proga_karinaleshabot'

    if Token == 'Default':
        Token = '1736167197:AAGhntG29KrFB3blnjxGF4XeFAyGJ80KDPk'

    r = requests.get(f'https://api.telegram.org/bot{Token}/'
                     f'sendMessage?chat_id={ChatID}&text={Message}')

    return r

# Объявим переменные
count = 0
urls = []  # Ссылки на товары
new_urls = []  # Ссылки на новые товары
file_name_supreme = 'supreme.csv'
file_name_yeezy = 'sites.csv'
errors = 0  # Счетчик ощибок для второй программы

send_telegram_message('Захожу на Supreme')
with open(file_name_supreme, 'r') as filehandle:
    urls = [line[:-1] for line in filehandle]
driver = webdriver.Firefox(executable_path=r'/Users/alex/PycharmProjects/test/'
                                           r'geckodriver')

new_urls.clear()

try:
    driver.get('https://www.supremenewyork.com/shop')

except WebDriverException:
    print('Не нашел магазин')
    errors += 1

try:
    goods_supreme = driver.find_elements_by_xpath('/html/body/div[2]/'
                                                  'div[3]/div/ul/li/a')
    print(f'Я нашел - {str(len(goods_supreme))} товаров')

    with open(file_name_supreme, 'a') as filehandle:
        filehandle.write('\n')
        for element in goods_supreme:
            if not element.get_attribute('href') in urls:
                print(element.get_attribute('href'))
                filehandle.write('%s\n' % element.get_attribute('href'))
                urls.append(element.get_attribute('href'))
                new_urls.append(element.get_attribute('href'))
except NoSuchElementException:
    print('Ничего нет')
    errors += 1
print(f'В списке сейчас {str(len(urls))} товаров')
print(f'Новые товары - {str(len(new_urls))}')
if len(new_urls) > 0:
    for url in new_urls:
        try:
            driver.get(url)
            elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/'
                                                'div/form/fieldset[2]/input')
            elem.click()  # Проверка возможности добавления товара в корзину
            send_telegram_message(url)
            count += 1
        except WebDriverException:
            print(f'Нет в наличии или не нужна {url}')
    driver.get('https://www.supremenewyork.com/shop/cart')
send_telegram_message(f'Закончил с Supreme. Новых вещей {str(count)}')
print(time.asctime())
table = []
# Переход ко второй части
send_telegram_message('Захожу на YEEZY')
with open(file_name_yeezy, 'r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=';')
    table = [site for site in reader]

elements = []
products = []

for row in table:
    try:  # Проверка новых вещей на сайтах разных стран
        driver.get(row[1])
        time.sleep(5)
        elements = driver.find_elements_by_class_name(row[2])
        if not elements:
            driver.refresh
            time.sleep(5)
            elements = driver.find_elements_by_class_name(row[2])
        if len(elements) > 0:
            products.clear()
            products = [str(j.text) for j in elements]
            if not row[3] == str(products) and products[0]:
                row[3] = str(products)
                send_telegram_message(f'Новые товары {str(products)} {row[1]}')
    except WebDriverException:
        send_telegram_message(f'Не нашел на - {row[1]}')


with open(file_name_yeezy, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerows(table)


driver.close()
send_telegram_message('закончил с YEEZY')