from csv import reader
from datetime import datetime
import report
import doctest


class DataSet:
    """Класс для представления данных о вакансиях.
    Attributes:
        file_name (str): Имя обрабатываемого файла.
        vacancies_objects (list): Список объектов типа Vacancy.
        currency_to_rub (dict): Словарь валютной конвертации.
        date_format (str): Формат даты после преобразования.
        original_date_format (str): Формат даты до преобразования, оригинальный.
    """
    file_name: str
    vacancies_objects: list

    def __init__(self, file_name: str, vacancies_objects: list):
        """ Инициализация объекта Dataset для дальнейшей работы с ним посредством класса CSVParser
            Args:
                file_name (str): имя обрабатываемого файла.
                vacancies_objects (list): список объектов типа Vacancy.
        """
        self.file_name = file_name
        self.vacancies_objects = vacancies_objects
        self.currency_to_rub = self.currency_to_rub
        self.date_format = self.date_format
        self.original_date_format = self.original_date_format

    currency_to_rub = {
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

    date_format = '%Y'
    original_date_format = '%Y-%m-%dT%H:%M:%S+%f'

    @staticmethod
    def format_date(date: str):
        """
        Метод, преобразующий дату в виде original_date_format и возвращающий дату в виде date_format.

        Arguments:
            date (str): оригинальная дата.
        Returns:
             Преобразованная дата.
        """
        return datetime.strptime(date, DataSet.original_date_format).strftime(DataSet.date_format)


class Vacancy:
    """Класс для представления вакансии.

    Attributes:
        name (str): Название вакансии.
        salary_from (float): Нижняя граница оклада.
        salary_to (float): Верхняя граница оклада.
        salary_currency (str): Название валюты оклада.
        salary_middle_in_rub (float): Среднее значеие оклада в рублях.
        area_name (str): Название региона вакансии.
        published_at (int): Дата публикации вакансии, год.
    """
    name: str
    salary_from: float
    salary_to: float
    salary_currency: str
    salary_middle_in_rub: float
    area_name: str
    published_at: int

    def __init__(self, vac_dict: dict):
        """
        Parameters:
            vac_dict (dict): Словарь, храняющий в себе данные для вставки в поля класса Vacancy.
        """
        self.name = vac_dict['name']
        self.salary_from = float(vac_dict['salary_from'])
        self.salary_to = float(vac_dict['salary_to'])
        self.salary_currency = vac_dict['salary_currency']
        self.area_name = vac_dict['area_name']
        self.published_at = int(DataSet.format_date(vac_dict['published_at']))
        self.salary_middle_in_rub = (self.salary_from + self.salary_to) / 2 \
                                    * DataSet.currency_to_rub[self.salary_currency]


class CSVParser:
    """ Класс для работы с CSV файлом.
        Attributes:
            _profession (str): Название профессии.
            __filename (str): Имя файла.
            __dataset (DataSet): Датасет, используемый в обработке данных.
            __salary_dynamic (dict): Словарь, описывающий годовую динамику зарплат.
            __vacancy_dynamic (dict): Словарь, описывающий годовую динамику вакансий.
            __salary_profession_dynamic (dict): Словарь, описывающий годовую динамику зарплаты КОНКРЕТНОЙ вакансии.
            __vacancy_profession_dynamic (dict): Словарь, описывающий годовую динамику КОНКРЕТНОЙ вакансии.
            __town_salaries (dict): Словарь, описывающий средние зарплаты в городах.
            __town_vacCounts (dict): Словарь, описывающий число вакансий в городах.
    """

    @staticmethod
    def csv_reader(file_name: str) -> (list, list):
        """Данный метод считывает файл и проводит фильтрацию на соответствие заголовочному списку - столбцов CSV файла.
        Parameters:
            file_name (str): Имя файла.
        Returns:
            Заголовочный список c именами столбцов и список вакансий в виде подсписков.
        """
        with open(file_name, 'r', encoding="utf-8-sig") as file:
            data = list(reader(file))
            vacancies = list(filter(lambda x: len(x) == len(data[0])
                                              and not list(x).__contains__('') and list(x) != data[0], data))
            return data[0], vacancies

    def csv_filer(self, header_list: list, list_naming: list):
        """Данный метод преобразует список вакансий в виде подсписков в список вакансий в виде словарей
        Parameters:
            header_list (list): Список столбцов CSV файла.
            list_naming (list): Список списков, содержащих в себе информацию о вакансиях.
        Returns:
            Список вакансий в виде словарей с ключами-столбцами CSV файла и соответствующими значениями.
        """
        return list(map(lambda x: self.convert_list_to_dict(list(x), header_list), list_naming))

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
            subDic.update({header_list[i]: list_[i]})
        return subDic

    @staticmethod
    def throwError(message: str):
        """Данный метод кидает ошибку.
        Parameters:
            message (str): Текст ошибки.
        """
        raise message

    def __init__(self, filename, profession):
        """Инициализация CSV-Парсера
        Parameters:
            filename (str): Название файла
            profession (str): Имя профессии
        """
        self._profession = profession
        self.__filename = filename
        self.__dataset = None
        self.__salary_dynamic = {}
        self.__vacancy_dynamic = {}
        self.__salary_profession_dynamic = {}
        self.__vacancy_profession_dynamic = {}
        self.__town_salaries = {}
        self.__town_vacCounts = {}

    __salary_dynamic = {}
    __vacancy_dynamic = {}
    __salary_profession_dynamic = {}
    __vacancy_profession_dynamic = {}
    __town_salaries = {}
    __town_vacCounts = {}

    # def __init__(self):
    #    """Пустой __init__ для заполнения полей с помощью create_csv_parser_from_input"""
    #    self.__filename = None

    def get_filename(self):
        """Получение имени обрабатываемого файла"""
        return self.__filename

    def create_csv_parser_from_input(self):
        """Заполняет поля класса через консольный ввод из класса ConsoleInput

        Returns:
            CSVParser instance.
        """
        self.__filename, self._profession = ConsoleInput.get_parameters(self)
        return self

    def get_profession(self):
        """
        Returns:
            Название профессии.
        """
        return self._profession

    def set_profession(self, new_profession: str):
        self._profession = new_profession

    def createDataSet(self):
        """Данный метод создает датасет, в процессе получая объект класса DataSet.

        Returns:
            Объект класса DataSet.
        """
        headerAndVacs = self.csv_reader(self.__filename)
        """Получаем заголовок - список столбцов и вакансии в виде списка списков"""
        filedCsv = self.csv_filer(headerAndVacs[0], headerAndVacs[1])
        """Формируем список словарей-вакансий"""
        vacancies_objects = list(map(lambda x: Vacancy(x), filedCsv))
        """Преобразуем список словарей в список Vacancy"""
        dataSet = DataSet(self.__filename, vacancies_objects)
        self.__dataset = dataSet
        return dataSet

    def get_salary_dynamic_by_year(self) -> dict:
        """Данный метод создает словарь динамики зарплат по годам вида {год: средняя зарплата}

        Returns:
            Словарь динамики зарплат по годам вида {год: средняя зарплата}
        """
        """Также заполняет словарь динамики вакансий по годам"""
        for vacancy in self.__dataset.vacancies_objects:
            if self.__vacancy_dynamic.__contains__(vacancy.published_at) \
                    and self.__salary_dynamic.__contains__(vacancy.published_at):
                self.__vacancy_dynamic[vacancy.published_at] += 1
                self.__salary_dynamic[vacancy.published_at] += vacancy.salary_middle_in_rub
            else:
                self.__vacancy_dynamic[vacancy.published_at] = 1
                self.__salary_dynamic[vacancy.published_at] = vacancy.salary_middle_in_rub
        for year in self.__salary_dynamic:
            self.__salary_dynamic[year] = int(self.__salary_dynamic[year] / self.__vacancy_dynamic[year])
        return self.__salary_dynamic

    def get_vacancy_dynamic_by_year(self) -> dict:
        """Возвращает словарь динамики вакансий по годам вида {год: число вакансий}"""
        if self.__salary_dynamic == {}:
            self.get_salary_dynamic_by_year()
        return self.__vacancy_dynamic

    def get_salary_dynamic_profession(self) -> dict:
        """Возвращает словарь динамики зарплат для конкретной профессии и
        заполняет словарь динамики числа вакансий для конкретной профессии

        Returns:
              Готовый словарь с годовой динамикой зарплат для конкретной профессии.
        """

        """Фильтруем список всех вакансий по имени конкретной профессии"""
        filtered = list(
            filter(lambda x: x.name.__contains__(self._profession), self.__dataset.vacancies_objects))
        """Создаем словари по годовому распределению из общих данных (забираем ключи-года)"""
        self.__salary_profession_dynamic = dict(zip(self.__salary_dynamic.keys(), [0]))
        self.__vacancy_profession_dynamic = dict(zip(self.__salary_dynamic.keys(), [0]))

        """Заполняем словари __salary_profession_dynamic и __vacancy_profession_dynamic"""
        for vacancy in filtered:
            if self.__vacancy_profession_dynamic.__contains__(vacancy.published_at) \
                    and self.__salary_profession_dynamic.__contains__(vacancy.published_at):
                self.__vacancy_profession_dynamic[vacancy.published_at] += 1
                self.__salary_profession_dynamic[vacancy.published_at] += vacancy.salary_middle_in_rub
            else:
                self.__vacancy_profession_dynamic[vacancy.published_at] = 1
                self.__salary_profession_dynamic[vacancy.published_at] = vacancy.salary_middle_in_rub
        for year in self.__salary_profession_dynamic:
            if self.__vacancy_profession_dynamic[year] != 0:
                self.__salary_profession_dynamic[year] = int(self.__salary_profession_dynamic[year] / \
                                                             self.__vacancy_profession_dynamic[year])
        return self.__salary_profession_dynamic

    def get_vacancy_dynamic_profession(self) -> dict:
        """Возвращает словарь динамики числа вакансий для конкретной профессии"""
        return self.__vacancy_profession_dynamic

    def get_salary_towns_levels(self) -> dict:
        """Возвращает словарь средних зарплат по городам и заполняет словарь долей вакансий по городам.

        Returns:
            Отсортированный словарь средних зарплат по городам, число вакансий которых составляет более и равно 1%
        """
        for vacancy in self.__dataset.vacancies_objects:
            if self.__town_vacCounts.__contains__(vacancy.area_name):
                self.__town_salaries[vacancy.area_name] += vacancy.salary_middle_in_rub
                self.__town_vacCounts[vacancy.area_name] += 1
            else:
                self.__town_salaries[vacancy.area_name] = vacancy.salary_middle_in_rub
                self.__town_vacCounts[vacancy.area_name] = 1
        for town in self.__town_salaries:
            self.__town_salaries[town] = int(self.__town_salaries[town] / self.__town_vacCounts[town])
        self.__town_vacCounts = dict(filter(lambda x: x[1] >= len(self.__dataset.vacancies_objects) / 100,
                                            self.__town_vacCounts.items()))
        self.__town_salaries = dict(
            filter(lambda x: self.__town_vacCounts.__contains__(x[0]), self.__town_salaries.items()))
        return dict(sorted(self.__town_salaries.items(), key=lambda x: x[1], reverse=True))

    def get_vacancies_towns_levels(self) -> dict:
        """Преобразует и форматирует словарь долей вакансий по городам

        Returns:
            Отсортированный словарь долей вакансий по городам с обрезанными значениями до четвертого знака.
        """
        finalised = dict(sorted(self.__town_vacCounts.items(), key=lambda x: (-x[1])))
        for vac in finalised:
            finalised[vac] = round((self.__town_vacCounts[vac] / len(self.__dataset.vacancies_objects)), 4)
        return finalised


class ConsoleInput:
    """Класс для ввода параметров обработки CSV с консоли"""

    @staticmethod
    def get_parameters(csvParser: CSVParser):
        """Получает данные для CSV парсинга с консоли

        Returns:
            Кортеж с названием файла и именем профессии.
        """
        filename = input("Введите название файла: ")
        profession = input("Введите название профессии: ")
        return filename, profession


def create_report_card(isConsoleInput: bool, file_name: str, profession_name: str,
                       results : list) -> report.Report:
    """Метод, создающий карточку отчёта класса Report

    Arguments:
        isConsoleInput(bool): отвечает за то, нужно ли будет пользователю вводить аргументы для команды
        file_name(str): имя файла если не нужно вводить с консоли
        profession_name(str): название профессии
        results(list): quick hack для мультитрединга

    Returns:
        Объект класса Report с готовыми данными для статистики.
    """
    if isConsoleInput:
        csvParser = CSVParser().create_csv_parser_from_input()
    else:
        csvParser = CSVParser(filename=file_name, profession=profession_name)
    csvParser.createDataSet()
    salary_dynamic_by_year = csvParser.get_salary_dynamic_by_year()
    vacancy_dynamic_by_year = csvParser.get_vacancy_dynamic_by_year()
    salary_dynamic_profession = csvParser.get_salary_dynamic_profession()
    vacancy_dynamic_profession = csvParser.get_vacancy_dynamic_profession()
    salary_town = csvParser.get_salary_towns_levels()
    vacancy_town = csvParser.get_vacancies_towns_levels()

    result = report.Report(csvParser.get_profession(), salary_dynamic_by_year, vacancy_dynamic_by_year,
                           salary_dynamic_profession, vacancy_dynamic_profession, salary_town, vacancy_town)
    results.append(result)

    # создание карточки отчёта
    return result


def generate_statistics():
    """Метод, генерирующий Excel файл, графики и pdf файл со статистикой из полученных данных в ходе
    работы create_report_card
    """
    reportCard = create_report_card()
    # печать данных для статистики
    reportCard.print_statistics()
    # генерация эксель-файла
    reportCard.generate_excel()
    # генерация картинки
    reportCard.generate_image()
    # генерация pdf'ки
    reportCard.generate_pdf()
