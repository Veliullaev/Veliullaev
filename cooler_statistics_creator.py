import pandas as pd
import numpy as np
import currencty_convertator
import report


def prepare_data(vac_file_path: str, currencies_file_path = '', noconvert = True):

    vacancies = pd.read_csv(vac_file_path, delimiter=',')
    if not noconvert:
        currencies = pd.read_csv(currencies_file_path, delimiter=',').set_index('Date').transpose().to_dict(orient='dict')
        work_frame = vacancies[['name', 'salary_from', 'salary_to', 'salary_currency', 'area_name', 'published_at']]
        work_frame = currencty_convertator.addSalaryInFrame(work_frame, currencies)
        work_frame = work_frame[work_frame['Salary'].notnull()]
        return work_frame
    return vacancies[vacancies['Salary'].notnull()]


# if __name__ == '__main__':
# filename = input("Введите название файла: ", end='')
# profession = input("Введите название профессиии: ", end='')

# Фрейм для вообще всех вакансий из CSVшки(с зарпалатами

def getSalariesYear(prepared: pd.DataFrame):
    groups = prepared.groupby('published_at')
    salaries = {}
    for n, g in groups:
        salaries.update({g['published_at'].max(): round(g['Salary'].mean())})
    return salaries


def getVaccountsYear(prepared: pd.DataFrame):
    vaccounts = prepared['published_at'].value_counts()
    vaccounts = vaccounts.sort_index()
    vacDynamics = vaccounts.to_dict()
    return vacDynamics


def getProfessionalSalary(professional: pd.DataFrame):
    # Динамика уровня зарплат по годам для выбранной профессии
    prof_groups = professional.groupby('published_at')
    prof_salaries = {}
    for n, g in prof_groups:
        prof_salaries.update({g['published_at'].max(): round(g['Salary'].mean())})
    return prof_salaries


def getProfessionalVaccounts(professional: pd.DataFrame):
    # Динамика количества вакансий по годам для выбранной профессии
    prof_vaccounts = professional['published_at'].value_counts()
    prof_vaccounts = prof_vaccounts.sort_index()
    prof_vaccounts_dict = prof_vaccounts.to_dict()
    return prof_vaccounts_dict


def getTownSalaries(prepared: pd.DataFrame):
    # Уровень зарплат по городам (в порядке убывания) для городов с числом вакансий > 1%)
    town_counts = prepared['area_name'].value_counts()  # подсчёт всех городов
    total = town_counts.sum()  # подсчёт всего числа городов
    precentages_ = town_counts / total  # процентовка содержания городов
    precentages_ = precentages_[precentages_ > 0.01]  # фильтруем по правилу '>1%'
    townnames = precentages_.keys().tolist()  # Получаем города, у которых надо учитывать значения
    townsalaries = precentages_.copy() * 0
    for town in townnames:
        meantown = prepared[prepared['area_name'] == town]['Salary'].mean()
        townsalaries[town] = round(meantown)
    townsalaries = townsalaries.sort_values(ascending=False)[0:10]
    return townsalaries.to_dict()


def getTownVacancies(prepared: pd.DataFrame):
    # Доля вакансий по городам (в порядке убывания, топ-10)
    town_counts = prepared['area_name'].value_counts()  # подсчёт всех городов
    total = town_counts.sum()  # подсчёт всего числа городов
    town_counts.head(10)
    precentages = town_counts / total
    precentages = precentages.sort_values(ascending=False)
    return precentages[0:10].to_dict()


filename = input("Введите название файла: ")
profession = input("Введите название профессии: ")

#использовать если нет сформированного фрейма с зарплатой
#prepared = prepare_data(filename, 'monthly_currency.csv', noconvert=False)

prepared = prepare_data(filename, noconvert=True)

prepared['published_at'] = prepared['published_at'].apply(lambda x: int(str(x[0:4])))
professional = prepared[prepared['name'].str.contains(profession, case=False)].copy()

salYear = getSalariesYear(prepared)
vacYear = getVaccountsYear(prepared)
profSal = getProfessionalSalary(professional)
profVac = getProfessionalVaccounts(professional)
townSal = getTownSalaries(prepared)
townVac = getTownVacancies(prepared)
print(salYear, vacYear, profSal, profVac, townSal, townVac, sep='\n')
reportCard = report.Report(profession, salYear, vacYear, profSal, profVac, townSal, townVac)
reportCard.generate_excel()
reportCard.generate_image()
reportCard.generate_pdf()
