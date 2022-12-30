import pandas as pd
import numpy as np
from sqlalchemy import create_engine


def createDataBaseCurrencies():
    engine = create_engine('sqlite:///Vacancies.db', echo=False)


def insert_currencies(filename='monthly_currency.csv'):
    df = pd.read_csv(filename, delimiter=',')
    engine = create_engine('sqlite:///Vacancies.db', echo=False)
    df.to_sql('currencies', con=engine, index=False)

createDataBaseCurrencies()
insert_currencies()