from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import requests
import time

binary = FirefoxBinary("/Applications/Firefox.app")
# profile = FirefoxProfile("C:\\Users\\Administrator\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\hs9pwqm9.Selenium")
# driver = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary, executable_path="C:\\Python\\geckodriver.exe")


firefox_path = "/Applications/Firefox.app"
geckodriver_path = "/Users/alex/PycharmProjects/test/geckodriver"

# from proxy_requests import ProxyRequests
# import os
# os.startfile(r'C:\Users\vitaly-hp\Desktop\Tor Browser\Browser\firefox.exe')
"""
def send_telegram_message(Message:str, ChatID='Default', Socks5Proxi='127.0.0.1:9150', Token='Default'):

    #https://habr.com/ru/post/306222/

    if ChatID == 'Default':
        ChatID = '292623451'
        #ChatID = '170004524

    if Token == 'Default':
        Token = '1171143469:AAEsKOQddICOGF34stUYO0FK99QqvoaugPI'

    proxies = {
        "http": f'socks5://' + Socks5Proxi,
        "https": f'socks5://' + Socks5Proxi
    }

    #r = ProxyRequests('https://api.ipify.org')
    r = ProxyRequests('https://api.telegram.org/bot' + Token + '/sendMessage?chat_id=' + ChatID + '&text=' + Message)
    try:
        r.get()
    except:
        print(r)
    return r
"""


def send_telegram_message(Message: str, ChatID='Default', Token='Default'):
    if ChatID == 'Default':
        ChatID = '@proga_karinaleshabot'
        # ChatID = '170004524

    if Token == 'Default':
        Token = '1736167197:AAGhntG29KrFB3blnjxGF4XeFAyGJ80KDPk'

    # r = ProxyRequests('https://api.ipify.org')
    # r = ProxyRequests('https://api.telegram.org/bot' + Token + '/sendMessage?chat_id=' + ChatID + '&text=' + Message)

    try:
        r = requests.get('https://api.telegram.org/bot' + Token + '/sendMessage?chat_id=' + ChatID + '&text=' + Message)
    except:
        print(r)
    return r


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
print(str(len(urls)) + ' goods are in the list')
"""
binary = FirefoxBinary(firefox_path)
driver = webdriver.Firefox(firefox_binary=firefox_path, executable_path=geckodriver_path)

driver.implicitly_wait(1)
"""
driver = webdriver.Firefox(executable_path=r'/Users/alex/PycharmProjects/test/geckodriver')
while errors < 10:
    print()
    print('------------------------------ ' + str(errors) + ' errors')
    print(time.asctime())

    new_urls.clear()
    try:
        driver.get('https://www.supremenewyork.com/')
    except:
        print('supremenewyork isnt work')
        errors += 1

    try:
        # elem = driver.find_element_by_partial_link_text('shop')
        # driver.get(elem.get_attribute('href'))

        driver.get('https://www.supremenewyork.com/shop')

    except:
        print('I dont find shop')
        errors += 1

    try:
        elem2 = driver.find_elements_by_xpath("/html/body/div[2]/div[3]/div/ul/li/a")
        # /html/body/div[2]/div[3]/div/ul/li[1]
        print('I found - ' + str(len(elem2)) + ' goods')
        for element in elem2:
            if not element.get_attribute('href') in urls:
                print(element.get_attribute('href'))
                with open(file_name, 'a') as filehandle:
                    filehandle.write('%s\n' % element.get_attribute('href'))
                urls.append(element.get_attribute('href'))
                new_urls.append(element.get_attribute('href'))
    except:
        print('I dont find goods')
        errors += 1

    print('In the list are ' + str(len(urls)) + ' goods')
    print('New goods - ' + str(len(new_urls)))

    if len(new_urls) > 0:
        for url in new_urls:
            try:
                print(send_telegram_message(url))
                print(url)
                driver.get(url)
                elem = driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/form/fieldset[2]/input')
                # /html/body/div[2]/div/div[2]/div/form/fieldset[2]/input
                elem.click()
            except:
                print('Already finished - ' + url)
                # errors += 1
        driver.get('https://www.supremenewyork.com/shop/cart')
    print(send_telegram_message("I had a lot of mistakes. I've had enough."))
    time.sleep(1800)
"""
    for url in new_urls:
        print(send_telegram_message(url))    
        print(url)

"""

print(send_telegram_message("I had a lot of mistakes. I've had enough."))
driver.close
driver.quit