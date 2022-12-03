import statistics_creator
import table_creator

"""
Программа для запуска подпрограмм с обработкой CSV файлов
Вакансии - запускает подпрограмму table_creator, выводящую табличку с описанием вакансий
Статистика - запускает подпрограмму statistics_creator, создающую xlsx,png,pdf файлы со статистикой о вакансиях
"""
if __name__ == '__main__':
    correct = ['Вакансии', 'Статистика']
    datatype = input("Введите данные для печати: ")
    if not(datatype in correct):
        raise("Некорректный ввод. Введите либо \"Вакансии\", либо \"Статистика\"");
    else:
        if datatype == 'Вакансии':
            table_creator.create_table()
        else:
            statistics_creator.create_report_card()
