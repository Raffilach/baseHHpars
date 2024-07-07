import pandas as pd
import requests
from datetime import datetime
import time
from tqdm import tqdm
from colorama import Fore, init


def check_vacancy(df, id, index):
    try:
        url = f'https://api.hh.ru/vacancies/{id}'
        response = requests.get(url)
        response.raise_for_status()

        item = response.json()
        actchek = item.get("type", {}).get("name", "Нет:(")

        if actchek == "Открытая":
            df.at[index, 'status'] = "Открыта"
            df.at[index, 'check_Time'] = datetime.now().strftime('%d.%м.%Y - %H:%М:%S')
        else:
            df.at[index, 'status'] = "Закрыта"
            df.at[index, 'closing_Date'] = datetime.now().strftime('%d.%m.%Y - %H:%М:%S')
            df.at[index, 'closing_Year'] = datetime.now().strftime('%Y')
            df.at[index, 'closing_Month'] = datetime.now().strftime('%m')
            df.at[index, 'closing_Day'] = datetime.now().strftime('%d')
            df.at[index, 'check_Time'] = datetime.now().strftime('%d.%м.%Y - %H:%М:%S')
    except requests.RequestException as e:
        df.at[index, 'status'] = "Закрыта"
        df.at[index, 'closing_Date'] = datetime.now().strftime('%d.%m.%Y - %H:%М:%S')
        df.at[index, 'closing_Year'] = datetime.now().strftime('%Y')
        df.at[index, 'closing_Month'] = datetime.now().strftime('%m')
        df.at[index, 'closing_Day'] = datetime.now().strftime('%d')
        df.at[index, 'check_Time'] = datetime.now().strftime('%d.%м.%Y - %H:%М:%S')

def main():
    input_file_path = 'OFFresParsHH_2024-06-15.csv'
    output_file_path = 'OFFresParsHH_2024-06-15.csv'

    while True:
        df = pd.read_csv(input_file_path)
        print(f"{Fore.CYAN}Подключение к файлу выполнено")

        if 'status' not in df.columns:
            df['status'] = pd.NA
        if 'closing_Date' not in df.columns:
            df['closing_Date'] = pd.NA
        if 'closing_Year' not in df.columns:
            df['closing_Year'] = pd.NA
        if 'closing_Month' not in df.columns:
            df['closing_Month'] = pd.NA
        if 'closing_Day' not in df.columns:
            df['closing_Day'] = pd.NA
        if 'check_Time' not in df.columns:
            df['check_Time'] = pd.NA

        for index, row in tqdm(df.iterrows(),
                               desc="\033[31m Проверка вакансий: \033[0m",
                               total=len(df),
                               colour='white'):
            id = row['id']
            status = row['status']

            if status != "Закрыта":
                check_vacancy(df, id, index)

        df.to_csv(output_file_path, index=False)
        print(f"{Fore.CYAN}Проверка завершена и данные сохранены в {output_file_path}")

        wait_time_seconds = 21600  # 6 часов в секундах

        with tqdm(total=wait_time_seconds, desc="До повторной проверки", colour='green') as pbar:
            for _ in range(wait_time_seconds):
                time.sleep(1)
                pbar.update(1)

if __name__ == "__main__":
    main()
