from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import requests
import time
binary = FirefoxBinary("/Applications/Firefox.app")
firefox_path = "/Applications/Firefox.app"
geckodriver_path = "/Users/alex/PycharmProjects/test/geckodriver"
def send_telegram_message(Message: str, ChatID='Default', Token='Default'):
    if ChatID == 'Default':
        ChatID = '@proga_karinaleshabot'
        # ChatID = '170004524

    if Token == 'Default':
        Token = '1736167197:AAGhntG29KrFB3blnjxGF4XeFAyGJ80KDPk'

    try:
        r = requests.get('https://api.telegram.org/bot' + Token + '/sendMessage?chat_id=' + ChatID + '&text=' + Message)
    except:
        print(r)
    return r
count=0
urls = []
new_urls = []
file_name = 'supreme.csv'
errors = 0

with open(file_name, 'r') as filehandle:
    for line in filehandle:
        # удалим заключительный символ перехода строки
        currentPlace = line[:-1]
        # добавим элемент в конец списка
        urls.append(currentPlace)
print(send_telegram_message(str(len(urls)) + ' вещей сейчас в списке'))
driver = webdriver.Firefox(executable_path=r'/Users/alex/PycharmProjects/test/geckodriver')
while errors < 10:
    print()
    print('------------------------------ ' + str(errors) + ' ошибок')
    print(time.asctime())

    new_urls.clear()
    try:
        driver.get('https://www.supremenewyork.com/')
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
                elem.click()
                print(send_telegram_message(url))
                count += 1
            except:
                print('Закончил - ' + url)
        driver.get('https://www.supremenewyork.com/shop/cart')
    print(send_telegram_message("Закончил. Новых вещей "+str(count)))
    time.sleep(1800)
print(send_telegram_message("Слишком много ошибок"))
driver.close
driver.quit