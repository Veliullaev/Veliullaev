"""
Этот модуль предназначен для обработки CSV файла по годам.
"""
import os
from pathlib import Path
from csv import reader
from datetime import datetime

_date_format: str = '%Y'
_original_date_format: str = '%Y-%m-%dT%H:%M:%S+%f'


def splitFiles(years_and_header: (dict, list)):
    """
    Функция, разделяющая файлы CSV по годам.

    Arguments:
        years (dict): Словарь, где ключ - год, значение - список строк-вакансий, принадлежащих этому году.
    """
    currpath = os.path.dirname(__file__) #получаем директорию, где запущен скрипт
    Path(currpath + "/year_splitted_files").mkdir(parents=True, exist_ok=True) #создаем директорию year_splitted_files в папке со скриптом
    newDir = currpath + "/year_splitted_files/"
    for i in years_and_header[0].keys():
        with open(newDir + f'{i}.csv', 'w', encoding="utf-8-sig") as fp:
            fp.write(",".join(years_and_header[1])+"\n")
            for j in years_and_header[0][i]:
                fp.write(','.join(j) + "\n")
    print()


def csv_reader(file_name: str) -> (dict):
    """Данный метод записывает строки вакансий в соответствующие списки для дальнейшего распределения по отдельным CSV
    файлам.

    Parameters:
        file_name (str): Имя файла.
    Returns:
        Словарь, где ключ - год, значение - список строк-вакансий, принадлежащих этому году.
    """
    with open(file_name, 'r', encoding="utf-8-sig") as file:
        data = list(reader(file))
        cooldict = {}
        if len(data) == 0:
            print('Пустой файл')
            exit()
        vacancies = list(filter(lambda x: len(x) == len(data[0])
                                          and not list(x).__contains__('') and list(x) != data[0], data))
        #dictionary = map(lambda x: int(list(x)[len(x)][0:3]), vacancies)
        for i in vacancies:
            #i = list(i)
            date = int(i[len(i)-1][0:4]) #Хак, позволяющий тотально сократить время на обработку файла
            if not cooldict.__contains__(date):
                cooldict[date] = []
                #cooldict.update({date: list(i)})
                cooldict[date].append(list(i))
            else:
                cooldict[date].append(list(i))

        if len(vacancies) == 0:
            print('Нет данных')
            exit()

        return cooldict, data[0]

cooldict = csv_reader("only_statistics.csv")
splitFiles(cooldict)