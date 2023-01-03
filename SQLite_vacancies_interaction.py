import pandas as pd
import numpy as np
from sqlalchemy import create_engine


def createDataBaseCurrencies():
    engine = create_engine('sqlite:///Vacancies.db', echo=False)


def insert_table(filename='monthly_currency.csv', tablename='currencies'):
    """
    Вставка таблицы, прямое преобразование из csv в таблицу SQlite

    :param filename: имя файла
    :param tablename: название таблицы
    :return: None
    """
    df = pd.read_csv(filename, delimiter=',')
    engine = create_engine('sqlite:///Vacancies.db', echo=False)
    df.to_sql(tablename, con=engine, index=False)


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


def read_from_sql(engine, profession=''):
    # Динамика уровня зарплат по годам
    df = pd.read_sql(
        "Select substr(published_at,1,4) as date, round(avg(Salary),3) as average from vacancies where salary not "
        "null group by substr(published_at,1,4);",
        engine)

    # Динамика количества вакансий по годам
    df1 = pd.read_sql(
        "Select substr(published_at,1,4) as date, count(Salary) as cnt from vacancies where salary not null group by "
        "substr(published_at,1,4);",
        engine)

    # Динамика уровня зарплат по годам для выбранной профессии
    df2 = pd.read_sql(f"Select substr(published_at,1,4) as date, round(avg(Salary),3) \
     as average from vacancies where (salary not null and name like '{profession}') group by substr(published_at,1,4);",
                      engine)

    # Динамика количества вакансий по годам для выбранной профессии
    df3 = pd.read_sql("Select substr(published_at,1,4) as date, count(Salary) \
           as cnt from vacancies where (salary not null and name = 'Программист') group by substr(published_at,1,4);",
                      engine)

    # Средняя з/п по городам
    df4 = pd.read_sql("Select area_name,\
      round(avg(Salary),3) as average\
       from vacancies\
        where (salary not null)\
         group by area_name\
          having 1.0 * count(*) / (select count(*) from vacancies where (salary not null)) > 0.01\
           order by average DESC\
           LIMIT 10;", engine)

    # Доля вакансий по городам
    df5 = pd.read_sql("Select area_name,\
                      round(1.0 * count(*) / (SELECT COUNT(*) FROM vacancies where (salary not null)),4) as percentage\
       from vacancies\
        where (salary not null)\
         group by area_name\
           order by percentage DESC\
           LIMIT 10;", engine)
    return df, df1, df2, df3, df4, df5


engine = create_engine('sqlite:///Vacancies.db', echo=False)

#example_row = example(engine, '2005-01')
#print(example_row)
# createDataBaseCurrencies()
# insert_currencies()
#frames = read_from_sql(engine, 'Программист')
#for i in frames:
#    print(i.head(2))
insert_table('monthly_currencies.csv')
print('Работа выполнена студентом: Велиуллаев Владислав Маратович')
