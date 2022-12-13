"""
Модуль для мультипроцессорной обработки CSV файлов
"""

# Python program to illustrate the concept
# of threading
# importing the threading module
import threading
import os
import statistics_creator
import report


def compile_result(threads: list, profession: str) -> report.Report:
    """
    Собирает результат со множества потоков в один

    Arguments:
        threads(list): список потоков
        profession(str): название профессии

    Returns:
        Report, готовый для дальнейшей обработки в файл.
    """
    final = report.Report(profession=profession,
                          salary_dynamic_profession={},
                          salary_town={}, salary_dynamic_by_year={},
                          vacancy_town={}, vacancy_dynamic_profession={}, vacancy_dynamic_by_year={})
    for i in threads:
        final = report.merge_reports(final, i)
    return final


if __name__ == "__main__":
    currpath = os.path.dirname(__file__)  # получаем директорию, где запущен скрипт
    splittedDir = currpath + "/year_splitted_files/"
    csvList = os.listdir(splittedDir)
    profName = "Программист"

    threads = []
    results = []
    # creating thread
    for i in csvList:
        # t = threading.Thread(target=statistics_creator.create_report_card(False, profession_name=profName,
        #                                                                  file_name=splittedDir+i,))
        # parser_ = statistics_creator.CSVParser(filename=splittedDir+i, profession=profName)

        t = threading.Thread(target=statistics_creator.create_report_card, args=(False, splittedDir + i, profName,
                                                                                 results))
        t.start()
        threads.append(t)

    for i in threads:
        t.join()

    finalRes = compile_result(threads=results, profession=profName)

    # both threads completely executed
    print("Done!")
