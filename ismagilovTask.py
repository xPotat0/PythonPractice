import csv
import re
import openpyxl
import matplotlib.pyplot as plt
import numpy as np
from openpyxl.styles import Font, Color, Border, Side

global file_name, prof_name
currency_to_rub = {
    "AZN": 35.68,
    "BYR": 23.91,
    "EUR": 59.90,
    "GEL": 21.74,
    "KGS": 0.76,
    "KZT": 0.13,
    "RUR": 1,
    "UAH": 1.64,
    "USD": 60.66,
    "UZS": 0.0055,
}


def request():
    file_name = input('Введите название файла: ')
    prof_name = input('Введите название профессии: ')
    return file_name, prof_name


class DataSet:
    def __init__(self, file_name, vacancies_objects):
        self.file_name = file_name
        self.vacancies_objects = vacancies_objects


class Vacancy:
    def __init__(self, name, salary, area_name, published_at):
        self.name = name
        self.salary = salary
        self.area_name = area_name
        self.published_at = published_at


class Salary:
    def __init__(self, salary_from, salary_to, salary_currency):
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_currency = salary_currency


class Report:
    def __init__(self):
        self.a = 0


clean = re.compile('<.*?>')


def clean_html_tags(html_tags):
    text_without_tags = re.sub(clean, '', html_tags)
    text_without_tags = re.sub(r'\s+', ' ', text_without_tags)
    return text_without_tags.strip()


def csv_reader(file_name):
    file = open(file_name, encoding="UTF-8-SIG")
    reader = csv.reader(file)
    try:
        header = next(reader)
    except:
        print("Пустой файл")
        raise SystemExit
    list_of_vacancies = []
    for row in reader:
        list_of_vacancies.append(row)
    return header, list_of_vacancies


def csv_filer(reader, list_naming, prof_name):
    list_of_dict = []
    list_of_dict_by_name = []
    for row in list_naming:
        dict_of_vac = dict()
        if ((len(row) == len(reader)) and not "" in row):
            for index in range(len(row)):
                dict_of_vac[reader[index]] = clean_html_tags(row[index].replace('\n', ', ')).strip()
            if (prof_name.lower() in dict_of_vac['name'].lower()):
                list_of_dict_by_name.append(Vacancy(dict_of_vac['name'],
                                            Salary(float(dict_of_vac['salary_from']) * float(currency_to_rub[dict_of_vac['salary_currency']]),
                                                   float(dict_of_vac['salary_to']) * float(currency_to_rub[dict_of_vac['salary_currency']]),
                                                   dict_of_vac['salary_currency']),
                                            dict_of_vac['area_name'],
                                            dict_of_vac['published_at']))
            list_of_dict.append(Vacancy(dict_of_vac['name'],
                                            Salary(float(dict_of_vac['salary_from']) * float(currency_to_rub[dict_of_vac['salary_currency']]),
                                                   float(dict_of_vac['salary_to']) * float(currency_to_rub[dict_of_vac['salary_currency']]),
                                                   dict_of_vac['salary_currency']),
                                            dict_of_vac['area_name'],
                                            dict_of_vac['published_at']))
    return list_of_dict, list_of_dict_by_name


def remaker(_list):
    remaked_list = _list
    for key, value in remaked_list.items():
        try:
            remaked_list[key] = value[0]/value[1]
        except:
            remaked_list[key] = value[0]/1
    return remaked_list


def sort_dict(_dict):
    result = {}
    for key, value in _dict:
        result[key] = value
        if(result.__len__() == 10):
            break
    return result


def filter_vac(list_of_vac):
    dict_of_cort = {}
    salary_by_city = {}
    count_of_vac = 0
    for vacancy in list_of_vac:
        publ_year = vacancy.published_at[0:4]
        salary_average = (int(str(vacancy.salary.salary_from).split(sep='.')[0]) +
                          int(str(vacancy.salary.salary_to).split(sep='.')[0]))/2
        city_name = vacancy.area_name
        dict_of_cort[publ_year] = dict_of_cort.get(publ_year, (0, 0))
        dict_of_cort[publ_year] = (dict_of_cort[publ_year][0] + salary_average,
                                   dict_of_cort[publ_year][1] + 1)
        salary_by_city[city_name] = salary_by_city.get(city_name, (0, 0))
        salary_by_city[city_name] = (salary_by_city[city_name][0] + salary_average,
                                            salary_by_city[city_name][1] + 1)
        count_of_vac = count_of_vac + 1

    count_vacancy_by_prof = {}
    for key, value in dict_of_cort.items():
        count_vacancy_by_prof[key] = value[1]

    prosent_vac = {}
    for key, value in salary_by_city.items():
        prosent_vac[key] = value[1]/count_of_vac

    sorted_proc_vac = sort_dict(sorted(prosent_vac.items(), key=lambda item: item[1], reverse=True))
    sorted_vac_by_city = sort_dict(sorted(remaker(salary_by_city).items(), key=lambda item: item[1], reverse=True))
    dict_of_cort = remaker(dict_of_cort)

    return dict_of_cort, count_vacancy_by_prof, sorted_vac_by_city, sorted_proc_vac


def set_default_to_cell(place, title, border, font, is_title):
    cell = place
    cell.value = title
    cell.border = border
    if (is_title):
        cell.font = font


def generate_excel(salary_by_year, vac_by_year, salary_by_prof, vacancy_by_prof, salary_by_city, vacancy_by_city):
    excel_file = openpyxl.Workbook()
    first_sheet = excel_file.active
    first_sheet.title = "Статистика по годам"
    second_sheet = excel_file.create_sheet("Статистика по городам")

    border = Border(left=Side(border_style='thin', color='000000'), top=Side(border_style='thin', color='000000'),
                                                     right=Side(border_style='thin', color='000000'), bottom=Side(border_style='thin', color='000000'))
    font = Font(bold=True)

    titles = ['Год', 'Средняя зарплата', 'Средняя зарплата - ' + prof_name,
              'Количество вакансий', 'Количество вакансий - ' + prof_name,
              'Город', 'Уровень зарплат', '', 'Город', 'Доля вакансий']

    count = 0
    flag = True
    for title in titles:
        if (flag):
            set_default_to_cell(first_sheet[chr(65 + count) + "1"], title, border, font, True)
            first_sheet.column_dimensions[chr(65 + count)].width = title.__len__() + 3
        else:
            if (count != 2):
                cell = set_default_to_cell(second_sheet[chr(65 + count) + "1"], title, border, font, True)
                second_sheet.column_dimensions[chr(65 + count)].width = title.__len__() + 3
            else:
                second_sheet.column_dimensions[chr(65 + count)].width = 3
        count += 1
        if (count == 5):
            flag = False
            count = 0

    flag = True
    letter = 65
    for list_ in [salary_by_year.keys(), salary_by_year.values(),
                  salary_by_prof.values(),
                  vac_by_year.values(),
                  vacancy_by_prof.values(),
                  salary_by_city.keys(), salary_by_city.values(),
                  vacancy_by_city.keys(), vacancy_by_city.values()]:
        _count = 2
        width = 0
        if (flag != True):
            width = len(str(second_sheet[chr(letter)+"1"].value)) + 3

        for value in list_:
            if (flag):
                set_default_to_cell(first_sheet[chr(letter) + str(_count)], value, border, font, False)
            else:
                if(letter == 67):
                    letter += 1
                set_default_to_cell(second_sheet[chr(letter) + str(_count)], value, border, font, False)
                if (len(str(value)) > width):
                    width = len(str(value)) + 3
            _count += 1
        second_sheet.column_dimensions[chr(letter)].width = width
        letter += 1
        if (letter == 70):
            flag = False
            letter = 65

    excel_file.save('report.xlsx')


def generate_image(salary_by_year, vac_by_year, salary_by_prof, vacancy_by_prof, salary_by_city, vacancy_by_city):
    '''Двойная диаграмма з/п'''
    cat_par_1 = list(salary_by_year.keys())
    year_val = list(salary_by_year.values())
    prof_val = list(salary_by_prof.values())
    width = 0.3
    x = np.arange(len(cat_par_1))
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(plt.subplot(2, 2, 1))
    rects1 = ax.bar(x - width / 2, year_val, width, label='Средняя з/п')
    rects2 = ax.bar(x + width / 2, prof_val, width, label='з/п ' + prof_name)
    ax.set_title('Уровень зарплат по годам')
    ax.grid(axis='y')
    ax.set_xticks(x, fontsize=8)
    ax.set_xticklabels(cat_par_1, rotation=90, fontsize=8)
    ax.legend(loc='upper left', fontsize=8)

    '''Двойная диаграмма вакансия/год'''
    cat_par_2 = list(salary_by_year.keys())
    year_vac = list(vac_by_year.values())
    prof_vac = list(vacancy_by_prof.values())
    width = 0.3
    x = np.arange(len(cat_par_2))
    ay = fig.add_subplot(plt.subplot(2, 2, 2))
    rects3 = ay.bar(x - width / 2, year_vac, width, label='Количество вакансий')
    rects4 = ay.bar(x + width / 2, prof_vac, width, label='Количество вакансий ' + prof_name)
    ay.set_title('Количество вакансий по годам')
    ay.grid(axis='y')
    ay.set_xticks(x, fontsize=8)
    ay.set_xticklabels(cat_par_2, rotation=90, fontsize=8)
    ay.legend(loc='upper left')

    '''Боковая диаграмма'''
    bx = plt.subplot(2, 2, 3)
    labels = list(salary_by_city.keys())
    values = list(salary_by_city.values())
    plt.barh(labels, values)
    bx.set_title('Уровень зарплат по городам')
    bx.grid(axis='x')

    '''Круговая диаграмма'''
    num = 1.0
    for value in list(vacancy_by_city.values()):
        num -= value
    vacancy_by_city['Другие'] = num
    cx = plt.subplot(2, 2, 4)
    vals = list(vacancy_by_city.values())
    labels = list(vacancy_by_city.keys())
    cx.pie(vals, labels=labels)
    cx.axis("equal")
    cx.set_title('Доля вакансий по городам')

    fig.savefig('Graphs.png', dpi=300)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)
    plt.show()


data_to_show = input('Введите данные для печати:')
show = (False, False)
if(data_to_show.lower() == 'Вакансии'.lower()):
    show = (True, True)
elif(data_to_show.lower() == 'Статистика'.lower()):
    show = (True, False)
else:
    raise SystemExit('Неверный ввод')

request = request()
file_name = request[0]
prof_name = request[1]
get_reader = csv_reader(file_name)
get_filer = csv_filer(get_reader[0], get_reader[1], prof_name)
result = filter_vac(get_filer[0])
result_by_prof = filter_vac((get_filer[1]))
'''print(f'Динамика уровня зарплат по годам: {result[0]}')
    print(f'Динамика количества вакансий по годам: {result[1]}')
    print()
    print(f'Динамика уровня зарплат по годам для выбранной профессии: {result_by_prof[0]}')
    print(f'Динамика количества вакансий по годам для выбранной профессии: {result_by_prof[1]}')
    print()
    print(f'Уровень зарплат по городам (в порядке убывания): {result[2]}')
    print()
print(f'Доля вакансий по городам (в порядке убывания): {result[3]}')'''
if(show[0]):
    if(show[1]):
        generate_excel(result[0], result[1], result_by_prof[0], result_by_prof[1], result[2], result[3])
    else:
        generate_image(result[0], result[1], result_by_prof[0], result_by_prof[1], result[2], result[3])
