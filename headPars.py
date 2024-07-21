import requests
import pandas as pd
from datetime import datetime
import time
import os
from tqdm import tqdm

def fetch_vacancies_via_api():
    print("Функция fetch_vacancies_via_api запущена")

    base_url = 'https://api.hh.ru/vacancies'
    params = {
        'only_with_salary': True,
        'page': 0,
        'per_page': 100
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    vacancies = [] #Сохраняем вакансии в список

    while True:
        print(f"Получаем страницу {params['page']}...")
        try:
            response = requests.get(base_url, headers=headers, params=params)
            print(f"Код состояния HTTP: {response.status_code}")
            data = response.json() # Преобразование ответа в формат JSON
        except Exception as e:
            print(f"Произошла ошибка при получении страницы {params['page']}: {e}")
            break

        if response.status_code != 200:  # Проверка статуса ответа
            print(f"Не удалось получить страницу {params['page']}, код состояния: {response.status_code}")
            break

        items = data.get('items', []) # Получение списка вакансий из данных
        if not items:
            print("Больше вакансий не найдено.")
            break

        for item in items:
            title = item.get('name', 'Не указано') # Получаем название вакансии
            salary = item.get('salary')  # Получаем зарплату
            coin_salary = get_salary(salary)
            company = item['employer'].get('name', 'Не указано') # Получаем название компании
            location = item['area'].get('name', 'Не указано') # Получаем город вакансии
            url = item.get('alternate_url', 'Не указано')  # Получаем ссылку вакансии
            js_url = item.get('url', 'Не указано')  # Получаем ссылку api вакансии
            published_date = item.get('published_at', 'Не указано') # Дата публикации вакансии
            professional_roles = ', '.join([role['name'] for role in item.get('professional_roles', [])])
            experience = item['experience'].get('name')
            schedule = item['schedule'].get('name')
            id = item.get('id')
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
                'js_url': js_url,
            })

        params['page'] += 1
        if params['page'] >= data['pages']:
            break

    print(f"Всего найдено вакансий: {len(vacancies)}") # Выводим кол-во найденных вакансий
    return vacancies


def get_salary(salary):
    if salary:
        if salary['from'] and salary['to']:
            coin_salary = f"{salary['from']} - {salary['to']} {salary['currency']}"
        elif salary['from']:
            coin_salary = f"от {salary['from']} {salary['currency']}"
        elif salary['to']:
            coin_salary = f"до {salary['to']} {salary['currency']}"
        else:
            coin_salary = 'Не указана'
    else:
        coin_salary = 'Не указана'
    return coin_salary

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
    time_obj = datetime.strptime(iso_time_str, "%Y-%m-%dT%H:%M:%S%z")
    readable_time = time_obj.strftime("%H:%M")
    return readable_time


def read_existing_vacancies(filename):
    if os.path.exists(filename): # Проверяем наличие файла с вакансиями
        return pd.read_csv(filename) #
    else:
        return pd.DataFrame(columns=['title', 'salary', 'rub_salary',
                                     'professional_roles', 'experience', 'schedule',
                                     'company', 'location','published_date',
                                     'published_time', 'id', 'url', 'js_url',
                                     ])


def save_to_csv(vacancies, filename):  # Сохранение в csv
    print("Функция save_to_csv запущена")
    if not vacancies:
        print("Нет вакансий для сохранения.")  # Если нет вакансий, выводим это
        return

    df_new = pd.DataFrame(vacancies)  # Создаем DataFrame из списка вакансий
    df_existing = read_existing_vacancies(filename)  # Читаем вакансии из существующего файла

    # Исключаем пустые или полностью NA DataFrame-ы
    if df_existing.empty:
        combined = df_new
    elif df_new.empty:
        combined = df_existing
    else:
        combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=['title', 'company', 'location', 'url'])  # Объединение новых и существующих данных, удаление дубликатов по указанным столбцам

    try:
        combined.to_csv(filename, index=False, encoding='utf-8-sig')  # Сохраняем объединенные данные в csv
        print(f"Данные сохранены в {filename}")
    except Exception as e:
        print(f"Произошла ошибка при сохранении в CSV: {e}")


def fetch_and_save_vacancies(filename):  # Функция для получения и сохранения вакансий
    print(f"Начало получения данных {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}...")
    vacancies = fetch_vacancies_via_api()  # Получение вакансий по запросу

    if vacancies:
        save_to_csv(vacancies, filename) # Сохранение вакансий в файл
    else:
        print("Вакансии не найдены.")

def main():
    filename = f'TEST_ParsHH_21-07-2024.csv'
    fetch_and_save_vacancies(filename)

    while True:
        wait_time_seconds = 3536  # 1 час в секундах

        with tqdm(total=wait_time_seconds,
                  desc="До повторной проверки",
                  colour='green') as pbar:
            for _ in range(wait_time_seconds):
                time.sleep(1)
                pbar.update(1)
        fetch_and_save_vacancies(filename) # Периодический запрос и сохранение вакансий


if __name__ == '__main__':
    print("Запуск скрипта")
    main()
