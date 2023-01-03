import pandas as pd
import requests


def get_freqs(frame: pd.DataFrame):
    """
    Функция, возвращающая частотность валют в выгрузке

    :param frame: датафрейм со всеми данными
    :return: частотность встречи валют в выгрузке
    """
    return frame['salary_currency'].value_counts()


def filter_frequencies(frequencies: pd.Series, count: int, declude: str) -> list:
    """
    Функция, отсеивающая валюты по частотности больше count

    :param frequencies: Серия частот "валюта - число появлений"
    :param count: Число относительно которого производится фильтрация
    :param declude: Валюта, которую требуется исключить
    :return: Отфильтрованная серия
    """
    try:
        freqs = frequencies[frequencies > count].keys().to_list()
        freqs.remove(declude)
        return freqs
    except ValueError:
        return frequencies[frequencies > count].keys().to_list()

def get_dates(frame: pd.DataFrame):
    """
    Функция, получающая даты публикаций вакансий

    :param frame: фрейм данных
    :return: Tuple дат самой старой вакансии и самой новой вакансии
    """
    return frame['published_at'].min()[0:10], frame['published_at'].max()[0:10]


def request_sbr(date: str, most_freq_list: list):
    """
    Получает курсы валют за указанный месяц

    :param date: дата в формате YYYY-MM
    :param most_freq_list: список самых встречающихся валют
    :return: возвращает датафрейм с необходимыми валютами
    """
    dates = date.split('-')
    r = requests.get(f'https://www.cbr.ru/scripts/XML_daily_eng.asp?date_req=13/{dates[1]}/{dates[0]}d&d=0')
    dataframe = pd.read_xml(r.text)
    dataframe = dataframe[['CharCode','Nominal','Value']]
    dataframe['curr'] = dataframe.apply(lambda row: float(row.Value.replace(',', '.')) / float(row.Nominal), axis=1)
    dataframe = dataframe.drop(columns=['Nominal', 'Value'])
    dataframe = dataframe[dataframe['CharCode'].isin(most_freq_list)]
    dataframe['date'] = f'{dates[0]}-{dates[1]}'
    pivoted = dataframe.pivot(index='date', columns='CharCode', values='curr')
    return pivoted


def getDateRange(start: str, end: str):
    """
    Получает серию дат в промежутке от start до end

    :param start: точка отсчёта
    :param end: точка конца
    :return: Серия дат в формате YYYY-MM
    """
    dateRange = pd.date_range(start, end, freq='M').strftime("%Y-%m").tolist()
    return dateRange


def get_monthly_currencies(filename='vacancies_dif_currencies.csv', frequency_cap=5000):
    """

    :param filename: имя csv файла с выгрузкой вакансий
    :param frequency_cap: граница, после которой вакансия является часто встречающейся
    :return:
     None, создает CSV файл с названием monthly_currencies.csv, содержащий курсы валют в каждый месяц в промежутке
     от самой старой вакансии до самой новой вакансии
    """
    main_frame = pd.read_csv(filename)
    dates = get_dates(main_frame)
    freqs = get_freqs(main_frame)
    filter_freqs = filter_frequencies(freqs, 5000, declude='RUR')
    frames = []
    final = pd.DataFrame()
    for i in getDateRange(dates[0], '2022-12'):
    #for i in ['2003-01', '2003-02']:
        req = request_sbr(i, filter_freqs)
        frames.append(req)
    for i in frames:
        final = pd.concat([final, i])

    final.to_csv('monthly_currencies.csv', index_label='Date', index=True)


if __name__ == '__main__':
    get_monthly_currencies(filename='vacancies_dif_currencies.csv', frequency_cap=5000)
