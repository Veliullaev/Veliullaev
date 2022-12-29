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
    :return: Tuple самой старой вакансии и самой новой вакансии
    """

    dates = frame['published_at'].sort_values()
    earliest = dates[0]
    latest = dates[len(dates) - 1]
    return earliest[0:10], latest[0:10]


def request_sbr(date: str, most_freq_list: list):
    """
    Получает курсы валют за указанный месяц

    :param date: дата в формате YYYY-MM
    :param most_freq_list: список самых встречающихся валют
    :return: возвращает словарь соответствия дата - коэффеценты конвертации
    """
    dates = date.split('-')
    r = requests.get(f'https://www.cbr.ru/scripts/XML_daily_eng.asp?date_req=13/{dates[1]}/{dates[0]}d&d=0')
    dataframe = pd.read_xml(r.text, elems_only=True)
    dataframe = dataframe.drop(columns=['NumCode', 'NumCode', 'Name'])
    dataframe['curr'] = dataframe.apply(lambda row: float(row.Value.replace(',', '.')) / float(row.Nominal), axis=1)
    dataframe = dataframe.drop(columns=['Nominal', 'Value'])
    newest = dataframe[dataframe['CharCode'].apply(lambda x: x in most_freq_list)]
    ech = {date: newest.values}
    return ech


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
    alldates = {}
    for i in getDateRange(dates[0], dates[1]):
        req = request_sbr(i, filter_freqs)
        alldates.update(req)
    for i in alldates.keys():
        values = [sub_list[1] for sub_list in alldates[i]]
        alldates.update({i: values})
    df = pd.DataFrame.from_dict(alldates, orient='index', columns=filter_freqs)
    df.to_csv('monthly_currencies.csv', index_label='Date', index=True)


if __name__ == '__main__':
    get_monthly_currencies(filename='vacancies_dif_currencies.csv', frequency_cap=5000)
