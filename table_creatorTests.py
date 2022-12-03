import unittest
from table_creator import Salary
from table_creator import Vacancy


class SalaryTest(unittest.TestCase):
    testcase = Salary({'salary_from': 10, 'salary_to': 20, 'salary_gross': 'true',
                       'salary_currency': 'RUR'})

    def test_type(self):
        self.assertEqual(type(self.testcase).__name__, 'Salary')

    def test_from(self):
        self.assertEqual(self.testcase.salary_from, 10)

    def test_to(self):
        self.assertEqual(self.testcase.salary_to, 20)

    def test_gross(self):
        self.assertEqual(self.testcase.salary_gross, 'true')

    def test_currency(self):
        self.assertEqual(self.testcase.salary_currency, 'RUR')


class VacancyTest(unittest.TestCase):
    testcase = Vacancy({'name': 'Тестовая ситуация', 'description': 'Пирожок с корицей',
                        'key_skills': 'Жабист, Питонист', 'experience_id': 'От 3 до 6 лет',
                        'premium': 'true', 'employer_name': 'Очередь за забором',
                        'salary_from': 10, 'salary_to': 20, 'salary_gross': 'true',
                        'salary_currency': 'RUR', 'area_name': 'Кибердянск',
                        'published_at': '2007-12-04T15:06:07+0300'})

    def test_type(self):
        self.assertEqual(type(self.testcase).__name__, 'Vacancy')

if __name__ == '__main__':
    unittest.main()
