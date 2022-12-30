import pandas as pd
import numpy as np
from sqlalchemy import create_engine


def createDataBaseCurrencies():
    engine = create_engine('sqlite:///Vacancies.db', echo=False)


def insert_currencies(filename='monthly_currency.csv'):
    df = pd.read_csv(filename, delimiter=',')
    engine = create_engine('sqlite:///Vacancies.db', echo=False)
    df.to_sql('currencies', con=engine, index=False)


def getCurrencyForMonth(engine, month):
    """
    Обращение к базе данных с таблицей валют за месяцы

    :param engine: Движок взаимодействия с базой данных SQLite
    :param month: Дата в формате YYYY-MM
    :return: Dataframe с валютами за один месяц
    """
    return pd.read_sql(f"SELECT * FROM 'currencies' where Date = '{month}'", engine)


def example(engine, month):
    """
    Пример обращения к базе данных с таблицей валют за месяцы

    :param engine: Движок взаимодействия с базой данных SQLite
    :param month: Дата в формате YYYY-MM
    :return: Dataframe с валютами
    """
    return getCurrencyForMonth(engine, month)


engine = create_engine('sqlite:///Vacancies.db', echo=False)

example_row = example(engine, '2005-01')
print(example_row)
# createDataBaseCurrencies()
# insert_currencies()
print('Работа выполнена студентом: Велиуллаев Владислав Маратович')