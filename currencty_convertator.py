import pandas as pd
import numpy as np


def setSalaryInDict(vacancy: dict, monthly_currencies: dict):
    date = vacancy['published_at'][0:7]
    if pd.isnull(vacancy['salary_currency']):
        return
    coef = 1
    if vacancy['salary_currency'] in ['USD', 'KZT', 'BYR', 'UAH', 'EUR']:
        coef = monthly_currencies[date][vacancy['salary_currency']]
    # print(coef)
    if pd.isnull(vacancy['salary_from']):
        vacancy['Salary'] = vacancy['salary_to'] * coef
        return
    if pd.isnull(vacancy['salary_to']):
        vacancy['Salary'] = vacancy['salary_from'] * coef
        return
    vacancy['Salary'] = (vacancy['salary_to'] + vacancy['salary_from']) / 2 * coef


def addSalaryInFrame(vacancies: pd.DataFrame, monthly_currencies: pd.DataFrame):
    vacancies.insert(1, 'Salary', value=[np.nan] * len(vacancies))
    dicts = vacancies.transpose(copy=False).to_dict(orient='dict')
    for i in dicts.keys():
        setSalaryInDict(dicts[i], monthly_currencies=monthly_currencies)
    reformed = pd.DataFrame.from_dict(dicts).transpose(copy=False).drop(
        columns=['salary_from', 'salary_to', 'salary_currency'])
    return reformed


if __name__ == '__main__':
    raw_vacs = pd.read_csv('vacancies_dif_currencies.csv', delimiter=',')
    monthly_currencies = pd.read_csv('monthly_currency.csv', delimiter=',')

    raw_vacs.insert(1, 'Salary', value=[np.nan] * len(raw_vacs))
    dicts = raw_vacs.transpose(copy=False)
    monthly_dict = monthly_currencies.set_index('Date').transpose().to_dict(orient='dict')
    for i in dicts.keys():
        setSalaryInDict(dicts[i], monthly_currencies=monthly_dict)
    reformed = pd.DataFrame.from_dict(dicts).transpose(copy=False) \
        .drop(columns=['salary_from', 'salary_to', 'salary_currency'])
    reformed.to_csv('wholesome_vacancies_data.csv', index=False)
