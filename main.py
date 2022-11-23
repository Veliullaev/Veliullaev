from csv import reader
from datetime import datetime

import pdfkit
import report
from xlsx2html import xlsx2html
from jinja2 import Environment, FileSystemLoader


class DataSet:
    file_name: str
    vacancies_objects: list

    def __init__(self, file_name: str, vacancies_objects: list):
        self.file_name = file_name
        self.vacancies_objects = vacancies_objects

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
        return datetime.strptime(date, DataSet.original_date_format).strftime(DataSet.date_format)


class Vacancy:
    name: str
    salary_from: float
    salary_to: float
    salary_currency: str
    salary_middle_in_rub: float
    area_name: str
    published_at: int

    def __init__(self, vacDictionary):
        self.name = vacDictionary['name']
        self.salary_from = float(vacDictionary['salary_from'])
        self.salary_to = float(vacDictionary['salary_to'])
        self.salary_currency = vacDictionary['salary_currency']
        self.area_name = vacDictionary['area_name']
        self.published_at = int(DataSet.format_date(vacDictionary['published_at']))
        self.salary_middle_in_rub = (self.salary_from + self.salary_to) / 2 \
                                    * DataSet.currency_to_rub[self.salary_currency]


class UniversalCSVParser:
    __currency_to_rub = {
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

    __headerDict = {}

    def get_currency_to_rub(self):
        return self.__currency_to_rub;

    __date_format = '%Y'
    __original_date_format = '%Y-%m-%dT%H:%M:%S+%f'

    @staticmethod
    def csv_reader(file_name: str, profession_name: str):
        with open(file_name, 'r', encoding="utf-8-sig") as file:
            data = list(reader(file))
            vacancies = list(filter(lambda x: len(x) == len(data[0])
                                              and not list(x).__contains__('') and list(x) != data[0], data))
            return data[0], vacancies

    def csv_filer(self, header_list: list, list_naming: list):
        return list(map(lambda x: self.convert_list_to_dict(list(x), header_list), list_naming))

    @staticmethod
    def convert_list_to_dict(list_: list, header_list: list):
        subDic = {}
        for i in range(len(list_)):
            subDic.update({header_list[i]: list_[i]})
        return subDic

    def format_date(self, date: str):
        return datetime.strptime(date, self.__original_date_format).strftime(self.__date_format)

    @staticmethod
    def throwError(message: str):
        print(message)
        exit()

    def __init__(self, filename, profession):
        self.__isSortReversed = None
        self.__profession = profession
        self.__filename = filename
        self.__dataset = None
        self.__header = None

    def __init__(self):
        self.__filename = None

    def get_filename(self):
        return self.__filename

    def get_reversedDict(self):
        return self.__reversedDict

    def get_boolDict(self):
        return self.__boolDict

    def create_csv_parser_from_input(self):
        self.__filename, self.__profession = InputCorrect.get_parameters(self)
        return self

    def get_profession(self):
        return self.__profession

    def createDataSet(self):
        headerAndVacs = self.csv_reader(self.__filename, self.__profession)
        filedCsv = self.csv_filer(headerAndVacs[0], headerAndVacs[1])
        vacancies_objects = list(map(lambda x: Vacancy(x), filedCsv))
        dataSet = DataSet(self.__filename, vacancies_objects)
        self.__dataset = dataSet
        self.__header = headerAndVacs[0]
        return dataSet

    __salary_dynamic = {}
    __vacancy_dynamic = {}
    __salary_profession_dynamic = {}
    __vacancy_profession_dynamic = {}
    __town_salaries = {}
    __town_vacCounts = {}

    def get_salary_dynamic_by_year(self) -> dict:
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
        return self.__vacancy_dynamic

    def get_salary_dynamic_profession(self) -> dict:
        filtered = list(
            filter(lambda x: x.name.__contains__(self.__profession), self.__dataset.vacancies_objects))
        self.__salary_profession_dynamic = dict(zip(self.__salary_dynamic.keys(), [0]))
        self.__vacancy_profession_dynamic = dict(zip(self.__salary_dynamic.keys(), [0]))
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
        return self.__vacancy_profession_dynamic

    def get_salary_towns_levels(self) -> dict:
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

        finalised = dict(sorted(self.__town_vacCounts.items(), key=lambda x: (-x[1])))
        for vac in finalised:
            finalised[vac] = round((self.__town_vacCounts[vac] / len(self.__dataset.vacancies_objects)), 4)
        return finalised


class InputCorrect:

    @staticmethod
    def throwError(message: str):
        print(message)
        exit()

    @staticmethod
    def get_parameters(csvParser: UniversalCSVParser):
        filename = input("Введите название файла: ")
        profession = input("Введите название профессии: ")
        return filename, profession


def create_report_card() -> report.Report:
    csvParser = UniversalCSVParser().create_csv_parser_from_input()
    csvParser.createDataSet()
    salary_dynamic_by_year = csvParser.get_salary_dynamic_by_year()
    vacancy_dynamic_by_year = csvParser.get_vacancy_dynamic_by_year()
    salary_dynamic_profession = csvParser.get_salary_dynamic_profession()
    vacancy_dynamic_profession = csvParser.get_vacancy_dynamic_profession()
    salary_town = csvParser.get_salary_towns_levels()
    vacancy_town = csvParser.get_vacancies_towns_levels()

    # создание карточки отчёта
    return report.Report(csvParser.get_profession(), salary_dynamic_by_year, vacancy_dynamic_by_year,
                         salary_dynamic_profession, vacancy_dynamic_profession, salary_town, vacancy_town)


if __name__ == '__main__':
    reportCard = create_report_card()
    # печать данных для статистики
    reportCard.print_statistics()
    # генерация эксель-файла
    reportCard.generate_excel()
    # генерация картинки
    reportCard.generate_image()
    # генерация pdf'ки
    reportCard.generate_pdf()
