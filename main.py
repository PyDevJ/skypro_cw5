from src.class_hh_api import HhAPI
from src.class_DBManager import DBManager
from src.utils import load_companies, config
from src.class_vacancy import Vacancy
import os


def main():
    database_name = 'hh_vacancies'
    companies_name = os.path.join('data', 'companies.json')
    companies = load_companies(companies_name)  # загрузка компаний из файла
    params = config()  # загрузка параметров для подключения к базе данных из database.ini
    db_manager = DBManager(database_name, params)  # экземпляр класса DBManager, создание базы данных
    print(f'База SQL {db_manager.name} создана')
    hh_api = HhAPI()  # экземпляр класса для получения данных с hh.ru

    for company in companies:
        # получение информации от компании по 'id' идентификатору
        vacancies_info = hh_api.get_all_vacancies(company['id'])

        # загрузка информации о компании в базу данных
        db_manager.insert_data_company(vacancies_info[0])

        # создание списка вакансий
        vacancies = []
        for vacancy_info in vacancies_info:
            vacancy = Vacancy.create_vacancy_from_hh(vacancy_info)
            vacancies.append(vacancy)

        # загрузка вакансий в базу данных
        db_manager.insert_data_vacancy(vacancies)

        print(f"Компания {company['name']} - количество вакансий", len(vacancies_info))
    print('Данные по вакансиям выбранных работодателей добавлены в базу данных SQL')

    # пользовательский интерфейс для выбора запроса к базе данных
    while True:
        print('''
    Выберите один запрос из пунктов:
1 - получить список всех компаний и количество вакансий у каждой компании
2 - получить список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию
3 - получить среднюю зарплату по вакансиям
4 - получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
5 - получить список всех вакансий, в названии которых содержится слово "python"
0 - выход''')

        user_input = input()
        if user_input == "1":
            db_manager.get_companies_and_vacancies_count()
        elif user_input == "2":
            db_manager.get_all_vacancies()
        elif user_input == "3":
            db_manager.get_avg_salary()
        elif user_input == "4":
            db_manager.get_vacancies_with_higher_salary()
        elif user_input == "5":
            db_manager.get_vacancies_with_keyword('python')
        elif user_input == "0":
            break
        else:
            print('Неверная команда')


if __name__ == "__main__":
    main()
