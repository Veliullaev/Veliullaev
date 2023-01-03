import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def fasterSalaryFromPositions(df: pd.DataFrame, currs):
    df['published_at'] = df['published_at'].str[0:7]
    eng = create_engine('sqlite:///Vacancies.db', echo=False)
    currencies = pd.read_sql('select * from currencies', eng)
    currencies = currencies.rename(columns={'Date':'published_at'})

    print(currencies.head(5))

    
    #Определяем, что у нас nullValues на зарплатах от и до
    
    null_sal_to = df['salary_to'].isnull()
    null_sal_from = df['salary_from'].isnull()
    corr_sals = ~(df['salary_from'].isnull() | df['salary_to'].isnull())

    df.loc[null_sal_to, 'Salary'] = df.loc[null_sal_to, 'salary_from']
    df.loc[null_sal_from, 'Salary'] = df.loc[null_sal_from, 'salary_to']
    df.loc[corr_sals, 'Salary'] = (df.loc[corr_sals, 'salary_from'] + df.loc[corr_sals, 'salary_to']) / 2 
    df = pd.merge(df, currencies, how='inner',on='published_at')
    print(df.head(5))
    bread = df.to_dict(orient='records')
    for i in bread:
        if i['salary_currency'] in currs:
            i['Salary'] = i['Salary'] * i[i['salary_currency']]
    ech = pd.DataFrame.from_records(bread)
    ech = ech[['name','Salary','area_name','published_at']]
    return ech


engine = create_engine('sqlite:///Vacancies.db', echo=False)

if __name__ == '__main__':  
    print('Reading vacancies csv...')
    raw_vacs = pd.read_csv('vacancies_dif_currencies.csv', delimiter=',')

    print('Completed! Length: ' + str(len(raw_vacs)))


    currs = pd.read_sql("PRAGMA table_info(currencies)",engine)['name']
    currs = currs[currs != 'Date'].to_list()

    print('inserting column and removing null from salary_currency...')
    raw_vacs = raw_vacs[raw_vacs['salary_currency'].notnull()]
    print('Completed! Length: ' + str(len(raw_vacs)))
    print('Converting vacancies to wholesome data')
    reformed = fasterSalaryFromPositions(raw_vacs, currs)
    print('Completed!')
    reformed.to_csv('wholesome_vacancies_data.csv', index=False)
