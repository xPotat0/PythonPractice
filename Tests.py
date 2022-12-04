from unittest import TestCase, main
from ismagilovTask import Salary, Vacancy, clean_html_tags

class SalaryTests(TestCase):
    def test_salary_type(self):
        self.assertEqual(type(Salary(10.0, 20.4, 'RUR')).__name__, 'Salary')

    def test_salary_from(self):
        self.assertEqual(Salary(10.0, 20.4, 'RUR').salary_from, 10)

    def test_salary_to(self):
        self.assertEqual(Salary(10.0, 20.4, 'RUR').salary_to, 20)

    def test_salary_currency(self):
        self.assertEqual(Salary(10.0, 20.4, 'RUR').salary_currency, 'RUR')


class VacancyTests(TestCase):
    def test_vacancy_type(self):
        self.assertEqual(type(Vacancy('Prog', Salary(10, 20, 'RUR'), 'Smt', '10/10/10')).__name__, 'Vacancy')

    def test_vacancy_name(self):
        self.assertEqual(Vacancy('Prog', Salary(10, 20, 'RUR'), 'Smt', '10/10/10').name, 'Prog')

    def test_vacancy_salary(self):
        self.assertEqual(type(Vacancy('Prog', Salary(10, 20, 'RUR'), 'Smt', '10/10/10').salary).__name__, 'Salary')

    def test_vacancy_area_name(self):
        self.assertEqual(Vacancy('Prog', Salary(10, 20, 'RUR'), 'Smt', '10/10/10').area_name, 'Smt')

    def test_vacancy_published_at(self):
        self.assertEqual(Vacancy('Prog', Salary(10, 20, 'RUR'), 'Smt', '10/10/10').published_at, '10/10/10')


class CleanTests(TestCase):
    def test_clean_p_tag(self):
        self.assertEqual(clean_html_tags('Hell<p>o</p>'), 'Hello')

    def test_clean_a_tag(self):
        self.assertEqual(clean_html_tags('Some<a>thing</a>'), 'Something')

    def test_clean_double_tag(self):
        self.assertEqual(clean_html_tags('It<a> can<p>not</p> be real!'), 'It cannot be real!')

    def test_clean_text_in_tag(self):
        self.assertEqual(clean_html_tags('You must <not>see this'), 'You must see this')

    def test_clean_no_tag(self):
        self.assertEqual(clean_html_tags('World'), 'World')

if(__name__ == '__main__'):
    main()