
import csv
import re

symbols = 0
spaces = 0
words = 0
punctuation = 0
sentences = 0
symb_without_sp = 0
symb_without_punc = 0

with open ('steam_description_data.csv', encoding='utf-8') as file:
    for line in file:
        symbols += len(line)
        spaces += line.count (' ')
        punctuation += len(re.findall(r"[!?:;.,—]", line))
        words += len(line.split())
        sentences += len(re.findall(r"([A-Z][^\.!?]*[\.!?])", line))

symb_without_sp = symbols - spaces # Количество символов без пробелов
symb_without_punc += symbols - punctuation # Количество символов без знаков препинания
print ('Количество символов: ', symbols)
print ('Количество символов без пробелов: ', symb_without_sp)
print ('Количество символов без знаков препинания: ', symb_without_punc)
print('Количество слов: ', words)
print('Количество предложений: ', sentences)


