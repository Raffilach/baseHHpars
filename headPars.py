import requests
import pandas as pd
from datetime import datetime
import time
import os

def fetch_vacancies_via_api(city='Москва', search_query='Data Scientist'):
    print("fetch_vacancies_via_api Начала Работу")

    base_url = 'https://api.hh.ru/vacancies' #Базовый URL
    params = {
        'text': search_query,
        'only_with_salary': True,
        #'area': "1",  # Код Москвы - 1; spb - 2; Записал в коментарий, так-как мы не смотрими сейчас какой-то конкретный город
        'page': 0,
        'per_page': 100  # Кол-во вакансий на стр. (максимум 100)
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    vacancies = [] #Сохраняем вакансии в список

    while True:
        print(f"Получение данных со страницы: {params['page']}...")
        try:
            response = requests.get(base_url, headers=headers, params=params)
            print(f"HTTP status code: {response.status_code}")
            data = response.json() # Преобразование ответа в формат JSON
        except Exception as e:
            print(f"Возникло исключение при загрузке страницы {params['page']}: {e}")
            break

        if response.status_code != 200:  # Проверка статуса ответа
            print(f"Не удалось загрузить страницу. {params['page']}, status code: {response.status_code}")
            break

        items = data.get('items', []) # Получение списка вакансий из данных
        if not items:
            print("Больше вакансий не найдено.")
            break

        for item in items:
            title = item.get('name', 'Не указано') # Получаем название вакансии
            salary = item.get('salary')  # Получаем зарплату
            if salary:
                if salary['from'] and salary['to']:
                    coin_salary = f"{salary['from']} - {salary['to']} {salary['currency']}"
                elif salary['from']:
                    coin_salary = f"from {salary['from']} {salary['currency']}"
                elif salary['to']:
                    coin_salary = f"up to {salary['to']} {salary['currency']}"
                else:
                    coin_salary = 'Не указана'
            else:
                coin_salary = 'Не указана'
            company = item['employer'].get('name', 'Не указано') # Получаем название компании
            location = item['area'].get('name', 'Не указано') # Получаем город вакансии
            url = item.get('alternate_url', 'Не указано')  # Получаем ссылку вакансии
            published_date = item.get('published_at', 'Не указано') # Дата публикации вакансии
            professional_roles = ', '.join([role['name'] for role in item.get('professional_roles', [])])
            experience = item['experience'].get('name')
            schedule = item['schedule'].get('name')
            id = item.get('id')
            position = search_query # Записываем поисковой запрос

            converted_salary = converter_salary(salary)
            readable_date = converter_date(published_date)
            readable_time = converter_time(published_date)

            vacancies.append({
                'title': title,
                'salary': coin_salary,
                'rub_salary': converted_salary,
                'professional_roles': professional_roles,
                'experience': experience,
                'schedule': schedule,
                'company': company,
                'location': location,
                'published_date': readable_date,
                'published_time': readable_time,
                'id': id,
                'url': url,
                'position': position
            })

        params['page'] += 1
        if params['page'] >= data['pages']:
            break

    print(f"Всего собрано вакансий: {len(vacancies)}") # Выводим кол-во найденый вакансий
    return vacancies

def converter_salary(salary):
    if salary:
        if salary['from'] and salary['to']:
            down_salary = int(salary['from'])
            up_salary = int(salary['to'])
            currency = salary['currency']
            average_salary = (up_salary + down_salary) / 2
            converted_salary = currency_transfer(average_salary, currency)
        elif salary['from']:
            currency = salary['currency']
            average_salary = int(salary['from'])
            converted_salary = currency_transfer(average_salary, currency)
        elif salary['to']:
            currency = salary['currency']
            average_salary = int(salary['to'])
            converted_salary = currency_transfer(average_salary, currency)
        else:
            converted_salary = 'Не указана'
    else:
        converted_salary = 'Не указана'
    return converted_salary

def currency_transfer(average_salary, currency):

    if currency == 'RUR':
        average_salary = average_salary
    elif currency == 'BYR':
        currency = 'BYN'
        amount = float(average_salary)
        to_currency = 'RUB'

        url = f"https://api.exchangerate-api.com/v4/latest/{currency}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Получаем курс обмена из данных
            exchange_rate = data['rates'][to_currency]
            # Вычисляем конвертированную сумму
            average_salary = amount * exchange_rate
            return average_salary
        else:
            return "Ошибка при получении данных"
    else:
        amount = float(average_salary)
        to_currency = 'RUB'

        url = f"https://api.exchangerate-api.com/v4/latest/{currency}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            # Получаем курс обмена из данных
            exchange_rate = data['rates'][to_currency]
            # Вычисляем конвертированную сумму
            average_salary = amount * exchange_rate
            return average_salary
        else:
            return "Ошибка при получении данных"

    return average_salary

def converter_date(published_date):
    iso_date_str = published_date
    # Парсинг строки даты в объект datetime
    date_obj = datetime.strptime(iso_date_str, "%Y-%m-%dT%H:%M:%S%z")
    # Приведение к читабельному виду
    readable_date = date_obj.strftime("%d.%m.%Y")
    return readable_date
def converter_time(published_date):
    iso_time_str = published_date
    # Парсинг строки даты в объект datetime
    time_obj = datetime.strptime(iso_time_str, "%Y-%m-%dT%H:%M:%S%z")
    # Приведение к читабельному виду
    readable_time = time_obj.strftime("%H:%M")
    return readable_time


def read_existing_vacancies(filename):
    if os.path.exists(filename): # Проверяем наличие файла с вакансиями
        return pd.read_csv(filename) #
    else:
        return pd.DataFrame(columns=['title', 'salary', 'rub_salary', 'professional_roles', 'experience', 'schedule', 'company', 'location','published_date', 'published_time', 'id', 'url', 'position']) #


def save_to_csv(vacancies, filename): # Сохранение в csv
    print("save_to_csv начато")
    if not vacancies:
        print("Нет вакансий, которые можно было бы сохранить.") # Если нет вакансий, выводим это
        return

    df_new = pd.DataFrame(vacancies) # Создаем ДатаФраме из списка вакансий
    df_existing = read_existing_vacancies(filename) # Читаем вакансии с существ. файла

    combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=['title', 'company', 'location', 'url']) # Объединение новых и существующих данных, удаление дубликатов по указанным столбцам(не трогаем последний столб, потому что там одинаково)


    try:
        combined.to_csv(filename, index=False, encoding='utf-8-sig')  # Сохраняем обьедененные данные в csv

        print(f"Данные сохранены в {filename}")
    except Exception as e:
        print(f"Возникло исключение при сохранении в CSV: {e}")


def fetch_and_save_vacancies(search_query, filename):  # Функция для получения и сохранения вакансий
    print(f"Получение данных начинается в {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
    vacancies = fetch_vacancies_via_api(search_query=search_query)  # Получение вакансий по запросу

    if vacancies:
        save_to_csv(vacancies, filename) # Сохранение вакансий в файл
    else:
        print("Вакансий не найдено.")

def main():
    search_query = input("Введите название вакансии: ") # Пользователь вводит название вакансии
    today = datetime.today().strftime('%Y-%m-%d') # Получаем дату
    filename = f'File_Name_{today}.csv' # Создаем файл
    # Мы создаем такое название файла для того, что-бы было понятно с какого дня у нас ведется сбор данных
    fetch_and_save_vacancies(search_query, filename) # Первоначальный запрос и сохранение вакансий

    while True:
        time.sleep(3536)  # 9000 секунд = 2.5 часа
        fetch_and_save_vacancies(search_query, filename) # Периодический запрос и сохранение вакансий
if __name__ == '__main__':
    print("Выполнение скрипта началось")
    main()