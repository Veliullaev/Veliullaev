from csv import reader
import re
from typing import Dict, Any, Pattern

from prettytable import PrettyTable
import prettytable
from datetime import datetime

"""Модуль, создающий таблицу с вакансиями"""


class DataSet:
    """Класс для представления данных о вакансиях.
        Attributes:
            file_name (str): Имя обрабатываемого файла.
            vacancies_objects (list): Список объектов типа Vacancy.
        """
    file_name: str
    vacancies_objects: list

    def __init__(self, file_name: str, vacancies_objects: list):
        self.file_name = file_name
        self.vacancies_objects = vacancies_objects


class Salary:
    """Класс для обозначения оклада
    Attributes:
        salary_from (float): Нижняя граница оклада.
        salary_to (float): Верхняя граница оклада.
        salary_currency (str): Название валюты оклада.
        salary_gross (str): Обозначение налогового обложения.
        formatted_salary (str): Отформатированный оклад.
    """
    salary_from: str
    salary_to: str
    salary_gross: str
    salary_currency: str
    formatted_salary: str

    def __init__(self, vac_dict):
        """
            Parameters:
                vac_dict (dict): Словарь, храняющий в себе данные для вставки в поля класса Salary.
        """
        self.salary_from = vac_dict['salary_from']
        self.salary_to = vac_dict['salary_to']
        self.salary_gross = vac_dict['salary_gross']
        self.salary_currency = vac_dict['salary_currency']
        self.formatted_salary = ""


class Vacancy:
    """Класс для представления вакансии.

        Attributes:
            name (str): Название вакансии
            description (str): Описание вакансии
            key_skills (list): Ключевые навыки вакансии
            experience_id (str): Опыт работы
            premium (str): Обозначение премиумности вакансии
            employer_name (str): Имя нанимателя
            salary (Salary): Зарплатный класс
            area_name (str): Название региона вакансии
            published_at (str): Дата публикации вакансии
    """

    name: str
    description: str
    key_skills: list
    experience_id: str
    premium: str
    employer_name: str
    salary: Salary
    area_name: str
    published_at: str

    def __init__(self, vac_dict):
        """
            Parameters:
                vac_dict (dict): Словарь, храняющий в себе данные для вставки в поля класса Vacancy.
        """
        self.name = vac_dict['name']
        self.description = vac_dict['description']
        self.key_skills = vac_dict['key_skills']
        self.experience_id = vac_dict['experience_id']
        self.premium = vac_dict['premium']
        self.employer_name = vac_dict['employer_name']
        self.salary = Salary(vac_dict)
        self.area_name = vac_dict['area_name']
        self.published_at = vac_dict['published_at']


class UniversalCSVParser:
    """Класс для работы с CSV файлом"""

    @staticmethod
    def convert_list_to_dict(list_: list, header_list: list):
        """Данный метод преобразует список в словарь по ключам-столбцам CSV файла.

            Parameters:
                list_ (list): список, в котором последовательно содержится информация о вакансии.
                header_list: упорядоченный список столбцов CSV файла.
            Returns:
                Словарь, где ключ - имя столбца из CSV файла.
        """
        subDic = {}
        for i in range(len(list_)):
            if str(list_[i]).__contains__('\n') or header_list[i] == "key_skills":
                element = UniversalCSVParser.clear_excess_from_list(UniversalCSVParser.convert_line_to_list(list_[i]))
                subDic.update({header_list[i]: element})
            else:
                subDic.update({header_list[i]: list_[i]})
        return subDic

    @staticmethod
    def clear_excess_from_list(raw_list: list):
        """Очищает из элементов списка лишние данные.

        Parameters:
            raw_list (str): Список с оригинальными элементами

        Returns:
            Список с очищенными элементами.
        """
        return list(map(lambda x: UniversalCSVParser.remove_excess(x), raw_list))

    @staticmethod
    def remove_excess(raw: str):
        """Удаляет из строки лишние данные

        Parameters:
            raw (str): Оригинальная строка.

        Returns:
            Очищенная строка
        """
        clean = re.sub(UniversalCSVParser.__cleaner, '', str(raw)).strip(" ")
        return re.sub(' +', ' ', clean)

    @staticmethod
    def convert_line_to_list(line: str):
        """Конвертирует строку, содержащую переносы строки в список

            Parameters:
                line (str): Оригинальная строка.

            Returns:
                Список строк, разделенных переносом строки
        """
        return str(line).split('\n')

    __dicNaming: dict[str | Any, str | Any] = {'name': 'Название', 'description': 'Описание', 'key_skills': 'Навыки',
                                               'experience_id': 'Опыт работы',
                                               'premium': 'Премиум-вакансия', 'employer_name': 'Компания',
                                               'Оклад': 'Оклад',
                                               'salary_from': 'Оклад',
                                               'salary_to': 'Верхняя граница вилки оклада',
                                               'salary_gross': 'Оклад указан до вычета налогов',
                                               'salary_currency': 'Идентификатор валюты оклада',
                                               'area_name': 'Название региона',
                                               'published_at': 'Дата публикации вакансии',
                                               'False': 'Нет', 'True': 'Да',
                                               "average_inRub": "Среднее в рублях",
                                               "noExperience": "Нет опыта",
                                               "between1And3": "От 1 года до 3 лет",
                                               "between3And6": "От 3 до 6 лет",
                                               "moreThan6": "Более 6 лет",
                                               "AZN": "Манаты",
                                               "BYR": "Белорусские рубли",
                                               "EUR": "Евро",
                                               "GEL": "Грузинский лари",
                                               "KGS": "Киргизский сом",
                                               "KZT": "Тенге",
                                               "RUR": "Рубли",
                                               "UAH": "Гривны",
                                               "USD": "Доллары",
                                               "UZS": "Узбекский сум",
                                               '': ''}

    __grossDict: dict[str, str] = {'False': 'С вычетом налогов', 'True': 'Без вычета налогов',
                                   'FALSE': 'С вычетом налогов',
                                   'TRUE': 'Без вычета налогов'}

    __currency_to_rub: dict[str, float | int] = {
        "AZN": 35.68,
        "BYR": 23.91,
        "EUR": 59.90,
        "GEL": 21.74,
        "KGS": 0.76,
        "KZT": 0.13,
        "RUR": 1,
        "UAH": 1.64,
        "USD": 60.66,
        "UZS": 0.0055,
    }

    __cleaner: Pattern[str] = re.compile('<.*?>')

    __date_format: str = '%d.%m.%Y'
    __original_date_format: str = '%Y-%m-%dT%H:%M:%S+%f'

    @staticmethod
    def csv_reader(file_name: str) -> (list, list):
        with open(file_name, 'r', encoding="utf-8-sig") as file:
            data = list(reader(file))
            if len(data) == 0:
                print('Пустой файл')
                exit()
            vacancies = list(filter(lambda x: len(x) == len(data[0])
                                              and not list(x).__contains__('') and list(x) != data[0], data))
            if len(vacancies) == 0:
                print('Нет данных')
                exit()
            return data[0], vacancies

    def csv_filer(self, header_list: list, list_naming: list) -> list:
        return list(map(lambda x: self.convert_list_to_dict(self.clear_excess_from_list(x), header_list), list_naming))

    def format_vacancies(self, data_vacancies: list) -> list:
        for i in range(len(data_vacancies)):
            data_vacancies[i] = self.formatter(data_vacancies[i])
        return data_vacancies

    def translate(self, row: dict, key: str, to_ignore: list):
        if not to_ignore.__contains__(key):
            if self.__dicNaming.__contains__(str(row[key])):
                return {self.__dicNaming[key]: ' '.join(self.__dicNaming[str(row[key])].split())}
            elif isinstance(row[key], list):
                return {self.__dicNaming[key]: '\n'.join(row[key])}
            elif key == "salary":
                return {"Оклад": row[key].formatted_salary}
            else:
                return {self.__dicNaming[key]: ' '.join(str(row[key]).split())}

    def format_date(self, date: str):
        return datetime.strptime(date, self.__original_date_format).strftime(self.__date_format)

    def formatter(self, vacancy: Vacancy):
        new_dict = {}
        vacancy.salary.salary_from = format(int(float(vacancy.salary.salary_from)), ',d').replace(',', ' ')
        vacancy.salary.salary_to = format(int(float(vacancy.salary.salary_to)), ',d').replace(',', ' ')
        vacancy.salary.salary_gross = self.__grossDict[vacancy.salary.salary_gross]
        vacancy.salary.salary_currency = self.__dicNaming[vacancy.salary.salary_currency]
        salary = f"{vacancy.salary.salary_from} - {vacancy.salary.salary_to} ({vacancy.salary.salary_currency})" \
                 f" ({vacancy.salary.salary_gross})"
        time = self.format_date(vacancy.published_at)
        vacancy.salary.formatted_salary = salary
        vacancy.published_at = time
        to_ignore = ["salary_to", "salary_gross", "salary_currency"]
        for x in vacancy.__dict__:
            translated = self.translate(vacancy.__dict__, x, to_ignore)
            if translated is not None:
                new_dict.update(translated)
        return new_dict

    @staticmethod
    def setup_table(table: PrettyTable, header_list: list):
        table.field_names = header_list
        table.border = True
        table.hrules = prettytable.ALL
        table.align = "l"
        table.max_width = 20

    @staticmethod
    def cut_long_string(raw: str):
        if isinstance(raw, str) and len(raw) > 100:
            return raw[0:100] + '...'
        return raw

    def get_table_as_string(self, header_list: list, vac_list: list, column_filter: list, borders: list):
        table = PrettyTable()
        counter = 1
        self.setup_table(table, header_list)
        for vacancy in vac_list:
            vacancy = dict(vacancy)
            valueList = list(map(lambda x: self.cut_long_string(x), list(vacancy.values())))
            row = [counter].__add__(valueList)
            table.add_row(row)
            counter += 1
        if len(borders) == 0 or borders is None:
            borders = [1, len(vac_list) + 1]
        elif len(borders) == 1:
            borders.append(len(vac_list) + 1)
        if len(column_filter) == 1:
            column_filter = header_list
        return table.get_string(fields=column_filter, start=borders[0] - 1, end=borders[1] - 1)

    def get_table_borders(self, input_str: str):
        borders = input_str.split()
        for i in borders:
            if not i.isdigit():
                self.throwError("Некорректный формат ввода")
        return list(map(lambda x: int(x), borders))

    def get_filters(self, input_str: str):
        filts = input_str.split(", ")
        return filts if all(filt in self.__reversedDict for filt in filts) else self.throwError(
            "Параметр фильтрации некорректен")

    def get_filtering_parameters(self, args: str):
        if not args.__contains__(": ") and len(args) != 0:
            print("Формат ввода некорректен")
            exit()
        if len(args) == 0:
            return -1, -1
        command_and_args = args.split(": ")
        if not self.__reversedDict.__contains__(command_and_args[0]):
            self.throwError("Параметр поиска некорректен")
        return command_and_args[0], command_and_args[1]

    @staticmethod
    def filter_by_exact_match(parameter: str, argument: str, dataset: DataSet):
        return list(filter(lambda x: x.__dict__[parameter] == argument, dataset.vacancies_objects))

    @staticmethod
    def filter_by_salary_param_match(parameter: str, argument: str, dataset: DataSet):
        return list(filter(lambda x: x.salary.__dict__[parameter] == argument, dataset.vacancies_objects))

    @staticmethod
    def filter_by_salary(parameter: str, salary: str, dataset: DataSet):
        return list(
            filter(lambda x: float(x.salary.__dict__['salary_from']) <= float(salary) <= float(
                x.salary.__dict__['salary_to']),
                   dataset.vacancies_objects))

    def filter_by_date(self, parameter: str, date: str, dataset: DataSet):
        return list(filter(lambda x: self.format_date(x.__dict__[parameter]) == date, dataset.vacancies_objects))

    @staticmethod
    def filter_by_list(parameter: str, args: str, dataset: DataSet):
        return list(filter(lambda x: all(item in x.__dict__[parameter] for item in args.split(", ")),
                           dataset.vacancies_objects))

    def create_filtration_dict(self):
        filtrationDict = {'name': self.filter_by_exact_match, 'description': self.filter_by_exact_match,
                          'employer_name': self.filter_by_exact_match, 'Оклад': self.filter_by_salary,
                          'experience_id': self.filter_by_exact_match,
                          'published_at': self.filter_by_date, 'area_name': self.filter_by_exact_match,
                          'salary_currency': self.filter_by_salary_param_match, 'premium': self.filter_by_exact_match,
                          'key_skills': self.filter_by_list,
                          'salary_gross': self.filter_by_salary_param_match,
                          'salary_from': self.filter_by_salary,
                          'salary_to': self.filter_by_salary_param_match}
        return filtrationDict

    def do_filtration(self, dataset: DataSet, cmd_n_args: tuple):
        cmd = ''
        args = ''
        if cmd_n_args[0] == -1:
            return dataset.vacancies_objects
        if not self.__reversedDict.__contains__(cmd_n_args[0]):
            print("Параметр поиска некорректен")
            exit()
        else:
            cmd = self.__reversedDict[cmd_n_args[0]]
        if self.__reversedDict.__contains__(cmd_n_args[1]):
            args = self.__reversedDict[cmd_n_args[1]]
        else:
            args = cmd_n_args[1]
        filtrationDict = self.create_filtration_dict()
        if not filtrationDict.__contains__(cmd):
            print("Параметр поиска некорректен")
            exit()
        return filtrationDict[cmd](cmd, args, dataset)

    @staticmethod
    def throwError(message: str):
        print(message)
        exit()

    def sort_by_lexicographic(self, vacancies_objects: list, paramName: str, isSortReversed=False) -> list:
        if paramName == '':
            return vacancies_objects
        if not (vacancies_objects[0].__dict__.__contains__(paramName) \
                or vacancies_objects[0].salary.__dict__.__contains__(paramName)):
            self.throwError("Параметр сортировки некорректен")
        else:
            vacancies_objects.sort(key=lambda x: x.__dict__[paramName], reverse=isSortReversed)
            return vacancies_objects

    def sort_by_salary(self, vacancies_objects: list, paramName: str, isSortReversed: bool) -> list:
        vacancies_objects.sort(key=lambda x: float(
            (float(x.salary.__dict__['salary_from']) + float(x.salary.__dict__['salary_to'])) * float(
                self.__currency_to_rub[x.salary.__dict__['salary_currency']]) / 2),
                               reverse=isSortReversed)
        return vacancies_objects

    def sort_by_salary_param(self, vacancies_objects: list, paramName: str, isSortReversed=False) -> list:
        if not vacancies_objects[0].salary.__dict__.__contains__(paramName):
            self.throwError("Параметр сортировки некорректен")
        else:
            vacancies_objects.sort(key=lambda x: float(x.salary.__dict__[paramName])
                                                 * self.__currency_to_rub[x.salary.__dict__['salary_currency']],
                                   reverse=isSortReversed)
            return vacancies_objects

    def sort_by_listCount(self, vacancies_objects: list, paramName: str, isSortReversed=False) -> list:
        vacancies_objects.sort(key=lambda x: len(x.__dict__[paramName])
        if isinstance(x.__dict__[paramName], list) else 1, reverse=isSortReversed)
        return vacancies_objects

    def sort_by_experience(self, vacancies_objects: list, paramName: str, isSortReversed=False) -> list:
        vacancies_objects.sort(key=lambda x: self.__expDict[x.__dict__['experience_id']],
                               reverse=isSortReversed)
        return vacancies_objects

    __sortFuncDict = {'Оклад': sort_by_salary, 'published_at': sort_by_lexicographic,
                      'name': sort_by_lexicographic, 'description': sort_by_lexicographic,
                      'salary_from': sort_by_salary, 'salary_to': sort_by_salary_param,
                      'premium': sort_by_lexicographic, 'area_name': sort_by_lexicographic,
                      'salary_currency': sort_by_lexicographic, 'employer_name': sort_by_lexicographic,
                      'experience_id': sort_by_experience, '': sort_by_lexicographic, 'key_skills': sort_by_listCount}

    __expDict = {"noExperience": 0,
                 "between1And3": 1,
                 "between3And6": 2,
                 "moreThan6": 3}

    __boolDict = {'Да': True, 'Нет': False, '': False}

    __parsedTable = None

    def __init__(self, filename, filterParam, sortParam, isSortReversed_bool, table_borders, filters,
                 reversedDict=None):
        self.__isSortReversed = None
        self.__filename = filename
        self.__filterParam = filterParam
        self.__sortParam = sortParam
        self.__isSortReversed_bool = isSortReversed_bool
        self.__table_borders = table_borders
        self.__filters = filters
        self.__reversedDict = reversedDict

    def __init__(self):
        self.__filename = None
        self.__filterParam = None
        self.__sortParam = None
        self.__isSortReversed = None
        self.__table_borders = None
        self.__filters = None
        self.__reversedDict = None

    def get_filename(self):
        return self.__filename

    def get_reversedDict(self):
        return self.__reversedDict

    def get_boolDict(self):
        return self.__boolDict

    def create_csv_parser_from_input(self):
        self.__reversedDict = {val: key for (key, val) in UniversalCSVParser.__dicNaming.items()}
        self.__filename, self.__filterParam, self.__sortParam, self.__isSortReversed, self.__table_borders, \
        self.__filters = InputCorrect.get_parameters(self)
        self.__filterParam = self.get_filtering_parameters(self.__filterParam)
        self.__filters = ['№'].__add__(list(filter(lambda x: x != '', self.get_filters(self.__filters))))
        self.__table_borders = self.get_table_borders(self.__table_borders)
        return self

    def get_parsed_table(self) -> str:
        if self.__parsedTable is not None:
            return self.__parsedTable
        dataSet = self.createDataSet()
        filtered = self.do_filtration(dataSet, self.__filterParam)
        filtered = self.__sortFuncDict[self.__reversedDict[self.__sortParam]] \
            (self, filtered, self.__reversedDict[self.__sortParam], self.__isSortReversed)
        if len(filtered) == 0:
            return "Ничего не найдено"
        else:
            formatted = self.format_vacancies(filtered)
            header = ['№'].__add__(list(formatted[0].keys()))
            self.__parsedTable = self.get_table_as_string(header, formatted, self.__filters, self.__table_borders)
            if self.__parsedTable is None:
                return ""
            return self.__parsedTable

    def __str__(self):
        if self.get_parsed_table() is None:
            return ""
        return self.get_parsed_table()

    def createDataSet(self):
        headerAndVacs = self.csv_reader(self.__filename)
        filedCsv = self.csv_filer(headerAndVacs[0], headerAndVacs[1])
        vacancies_objects = list(map(lambda x: Vacancy(x), filedCsv))
        dataSet = DataSet(self.__filename, vacancies_objects)
        return dataSet


class InputCorrect:

    @staticmethod
    def throwError(message: str):
        print(message)
        exit()

    @staticmethod
    def get_parameters(csvParser: UniversalCSVParser):
        filename = input("Введите название файла: ")
        filterParam = input("Введите параметр фильтрации: ")
        sortParam = input("Введите параметр сортировки: ")
        sortParam = sortParam if csvParser.get_reversedDict().__contains__(sortParam) else -1
        isSortReversed = input("Обратный порядок сортировки (Да / Нет): ")
        is_sort_reversed_bool = csvParser.get_boolDict()[isSortReversed] \
            if csvParser.get_boolDict().__contains__(isSortReversed) else -1
        table_borders = input("Введите диапазон вывода: ")
        filters = input("Введите требуемые столбцы: ")
        if sortParam == -1:
            InputCorrect.throwError("Параметр сортировки некорректен")
        if is_sort_reversed_bool == -1:
            InputCorrect.throwError("Порядок сортировки задан некорректно")
        return filename, filterParam, sortParam, is_sort_reversed_bool, table_borders, filters


def create_table():
    parser = UniversalCSVParser().create_csv_parser_from_input()
    print(parser.get_parsed_table())


if __name__ == '__main__':
    csvParser = UniversalCSVParser().create_csv_parser_from_input()
    print(csvParser.get_parsed_table())
