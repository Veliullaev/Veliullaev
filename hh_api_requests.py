import requests
import pandas as pd


def request_vacancies(request=''):
    """
    Функция обработки данных с api.hh.ru

    :param request: строка запроса к API
    :return: Dataframe с форматированными вакансиями
    """
    conn = ''
    if request == '':
        conn = requests.get("https://api.hh.ru/vacancies?specialization=1&date_from=2022-12-28&date_to=2022-12-28")
    else:
        conn = requests.get(request)

    vacancies_dict = pd.DataFrame.from_dict(conn.json())
    records_df = pd.DataFrame.from_records(vacancies_dict['items'])
    try:
        first_step = records_df[['name', 'salary', 'area', 'published_at']]
    except KeyError:
        return pd.DataFrame()
    first_step = pd.concat([first_step.drop(['salary'], axis=1), first_step['salary'].apply(pd.Series)], axis=1)
    first_step = pd.concat([first_step.drop(['area'], axis=1), first_step['area'].apply(pd.Series)], axis=1)
    first_step.columns.values[7] = "area_name"
    experimental = first_step[['name', 'from', 'to', 'currency', 'area_name', 'published_at']]
    experimental.columns.values[1] = 'salary_from'
    experimental.columns.values[2] = 'salary_to'
    experimental.columns.values[3] = 'salary_currency'
    return experimental


"""
https://api.hh.ru/vacancies?specialization=1&date_from=YYYY-MM-DD&date_to=YYYY-MM-DD&per_page=100&page=1 - тело реквеста

https://api.hh.ru/vacancies?specialization=1&date_from=2022-12-28&date_to=2022-12-28&per_page=100&page=1 - пример реквеста

"""


def get_requests_for_day(date: str):
    """
    Функция, составляющая список запросов на день для последующего обращения на api.hh.ru

    :param date: Дата в формате YYYY-MM-DD
    :return: Список запросов на день в промежутках между ['00:00','04:00','08:00','12:00','16:00','20:00','23:59']
    """
    # дата в формате YYYY-MM-DD
    # segments = ['00:00','04:00','08:00','12:00','16:00','20:00','23:59']
    time_segments = \
        [('00:00', '04:00'), ('04:00', '08:00'), ('08:00', '12:00'), ('12:00', '16:00'), ('16:00', '20:00'),
         ('20:00', '23:59')]
    daily_requests = []
    for segment in time_segments:
        segment_request = []
        for i in range(1, 19):
            segment_request.append(
                f'https://api.hh.ru/vacancies?specialization=1&date_from={date}T{segment[0]}&date_to={date}T{segment[1]}&per_page=100&page={i}')
        daily_requests.append(segment_request)
    return daily_requests


def get_stats_in_request_list(subrequests: list, queue=None):
    """
    Функция, которая должна была обращаться в многопроцессе к api.hh.ru

    :param subrequests: список запросов
    :param queue: очередь для мультипроцессинга
    :return: обработанные запросы в формате списка DataFrame'ов
    """
    results = []
    for request in subrequests:
        results.append(request_vacancies(request))
    if not (queue is None):
        queue.put(results)
    return results


def get_stats_mono(request_list: list):
    """
    Посылает запрос на все реквесты в списке

    :param request_list: список запросов
    :return: Список датафреймов с вакансиями
    """
    result = []
    for i in request_list:
        result.append(get_stats_in_request_list(i))
    return result


def unite_frames(framelist: list):
    """
    Функция, объединяющая фреймы и отсеивающая те, которые пустые.

    :param framelist: список датафреймов вакансий
    :return: объединенный фрейм
    """
    fin_frame = pd.DataFrame()
    filtered_frames = list(filter(lambda x: x.empty == False, framelist))
    for i in filtered_frames:
        fin_frame = pd.concat([fin_frame, i], ignore_index=True)
    return fin_frame


if __name__ == '__main__':
    stats = get_stats_mono(get_requests_for_day('2022-12-28'))
    frames_ = []
    for segment in stats:
        frames_.append(unite_frames(segment))

    filtered_frames = list(filter(lambda x: x.empty == False, frames_))
    final_frame_yay = pd.DataFrame()
    for i in filtered_frames:
        final_frame_yay = pd.concat([final_frame_yay, i])
    final_frame_yay.to_csv('vacancies_recent.csv', index=False)
