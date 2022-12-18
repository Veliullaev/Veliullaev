"""
Модуль для мультипроцессорной обработки CSV файлов
"""

# Python program to illustrate the concept
# of threading
# importing the threading module
import multiprocessing
import os
import statistics_creator
import report
import cProfile
import queue


def create_report_card(isConsoleInput: bool, file_name: str, profession_name: str,
                       res: list, queue: multiprocessing.Queue) -> report.Report:
    result = statistics_creator.create_report_card(isConsoleInput=isConsoleInput, file_name=file_name,
                                                   profession_name=profession_name, results=res)
    global results
    queue.put(result)


def compile_result(queue: multiprocessing.Queue, profession: str) -> report.Report:
    """
    Собирает результат со множества процессоров в один

    Arguments:
        queue(multiprocessing.Queue): очередь результатов исполнения программы
        profession(str): название профессии

    Returns:
        Report, готовый для дальнейшей обработки в файл.
    """
    salary_dynamic_by_year = {}
    salary_dynamic_profession = {}
    vacancy_dynamic_by_year = {}
    vacancy_dynamic_profession = {}
    global count
    for other in iter(queue.get, None):
        count -= 1
        salary_dynamic_by_year.update(other.get_salary_dynamic_by_year())
        salary_dynamic_profession.update(other.get_salary_dynamic_profession())
        vacancy_dynamic_by_year.update(other.get_vacancy_dynamic_by_year())
        vacancy_dynamic_profession.update(other.get_vacancy_dynamic_profession())
        if count == 0:
            break

    final = report.Report(profession=profession,
                          salary_dynamic_profession=salary_dynamic_profession,
                          salary_town={}, salary_dynamic_by_year=salary_dynamic_by_year,
                          vacancy_town={}, vacancy_dynamic_profession=vacancy_dynamic_profession,
                          vacancy_dynamic_by_year=vacancy_dynamic_by_year)
    return final


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    currpath = os.path.dirname(__file__)  # получаем директорию, где запущен скрипт
    splittedDir = currpath + "/year_splitted_files/"
    csvList = os.listdir(splittedDir)
    profName = "Программист"

    threads = []
    results = []
    q = multiprocessing.Queue(maxsize=20)
    count = len(csvList)
    for i in csvList:
        t = multiprocessing.Process(target=create_report_card,
                                    args=(False, splittedDir + i, profName,
                                          results, q,))
        t.start()
        threads.append(t)

    for i in threads:
        t.join()

    finalRes = compile_result(queue=q, profession=profName)

    print("Анализ данных завершен!")
    profiler.disable()
    profiler.dump_stats("example.stats")
    import pstats
    stats = pstats.Stats("example.stats").sort_stats("tottime")
    stats.print_stats()
