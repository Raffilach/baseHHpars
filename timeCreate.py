import pandas as pd
import requests
from datetime import datetime
import time
from tqdm import tqdm
from colorama import Fore, init

init(autoreset=True)  # Инициализация colorama для автоматического сброса цвета


def check_vacancy(df, js_url, index):
    time.sleep(0.5)
    try:
        response = requests.get(js_url)
        response.raise_for_status()

        item = response.json()
        actchek = item.get("type", {}).get("id", "Нет:(")

        if actchek == "open":
            df.at[index, 'status'] = "Открыта"
            df.at[index, 'check_Time'] = datetime.now().strftime('%d.%m.%Y - %H:%M:%S')
            df.at[index, 'error_attempts'] = 0
            df.at[index, 'error_Message'] = 0
        else:
            df.at[index, 'status'] = "Закрыта"
            df.at[index, 'closing_Date'] = datetime.now().strftime('%d.%m.%Y - %H:%M:%S')
            df.at[index, 'closing_Year'] = datetime.now().year
            df.at[index, 'closing_Month'] = datetime.now().month
            df.at[index, 'closing_Day'] = datetime.now().day
            df.at[index, 'check_Time'] = datetime.now().strftime('%d.%m.%Y - %H:%M:%S')
            df.at[index, 'error_attempts'] = 0
            df.at[index, 'error_Message'] = 0
    except requests.RequestException as e:
        df.at[index, 'status'] = "Ошибка"
        error_attempts = df.at[index, 'error_attempts'] + 1 if not pd.isna(df.at[index, 'error_attempts']) else 1
        df.at[index, 'error_attempts'] = error_attempts
        df.at[index, 'error_Message'] = str(e)
        df.at[index, 'check_Time'] = datetime.now().strftime('%d.%m.%Y - %H:%M:%S')

        if error_attempts >= 2:  # Если две проверки закончились ошибкой, закрываем вакансию
            df.at[index, 'status'] = "Закрыта"
            df.at[index, 'closing_Date'] = datetime.now().strftime('%d.%m.%Y - %H:%M:%S')
            df.at[index, 'closing_Year'] = datetime.now().year
            df.at[index, 'closing_Month'] = datetime.now().month
            df.at[index, 'closing_Day'] = datetime.now().day
            df.at[index, 'error_attempts'] = 2
            df.at[index, 'error_Message'] = 0



def check_columns(df):
    columns = ['status', 'closing_Date', 'closing_Year', 'closing_Month', 'closing_Day', 'check_Time',
               'error_Message', 'error_attempts']
    for col in columns:
        if col not in df.columns:
            df[col] = None


def main():
    file_path = 'TEST_ParsHH_21-07-2024.csv'

    while True:
        df = pd.read_csv(file_path)
        print(f"{Fore.CYAN}Подключение к файлу выполнено")

        check_columns(df)

        for index, row in tqdm(df.iterrows(),
                               desc="\033[31m Проверка вакансий: \033[0m",
                               total=len(df),
                               colour='white'):
            js_url = row['js_url']
            status = row['status']

            if pd.isna(status) or status != "Закрыта":
                check_vacancy(df, js_url, index)

        print("Время")
        df.to_csv(file_path, index=False)
        print(f"{Fore.CYAN}Проверка завершена и данные сохранены в {file_path}")

        wait_time_seconds = 21600  # 6 часов в секундах

        with tqdm(total=wait_time_seconds,
                  desc="До повторной проверки",
                  colour='green') as pbar:
            for _ in range(wait_time_seconds):
                time.sleep(1)
                pbar.update(1)


if __name__ == "__main__":
    # ПРИМЕРНЫЕ РАСЧЕТЫ, БЕЗ УЧЕТА ЗАКРЫТЫХ ВАКАНСИЙ!!!
    # Для более точного расчета нужна проба на практике
    # До 86400 вакансий дни будут точными
    # До 2500000 вакансий месяца будут точными
    # До 30000000 вакансий года будут точными
    main()
