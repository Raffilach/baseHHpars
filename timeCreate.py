import pandas as pd
import requests
from datetime import datetime
import time
from tqdm import tqdm
from colorama import Fore

while True:
    file_path = '<Your_file_name.csv>'
    df = pd.read_csv(file_path)
    print(f"{Fore.CYAN}Подключение к файлу выполнено")

    def check_vacancy(id, nowDate):
        try:
            url = f'https://api.hh.ru/vacancies/{id}'
            response = requests.get(url)
            response.raise_for_status()

            item = response.json()
            actchek = item.get("type", {}).get("name", "Нет:(")
            if actchek == "Открытая":
               df.at[index, 'status'] = f"Открыта"
               df.at[index, 'closing_Date'] = f"{nowDate}"
               return True
            else:
                df.at[index, 'status'] = f"Закрыта"
                df.at[index, 'closing_Date'] = f"{nowDate}"
                return False
        except requests.RequestException:
            df.at[index, 'status'] = f"Закрыта"
            df.at[index, 'closing_Date'] = f"{nowDate}"
            return False

    df['status'] = pd.NaT
    df['closing_Date'] = pd.NaT

    for index, row in tqdm(df.iterrows(), desc="\033[31m Проверка вакансий: \033[0m", total=len(df), colour='white'):
        id = row['id']
        status = row['status']

        if status == "Закрыта":
            pass
        else:
            nowDate = datetime.now().strftime('%d.%m.%Y')
            check_vacancy(id, nowDate)

    output_path = '<Your_file_name.csv>'
    df.to_csv(output_path, index=False)
    print(f"{Fore.CYAN}Проверка завершена и данные сохранены в", output_path)

    wait_time_seconds = 21600  # 6 часов в секундах

    with tqdm(total=wait_time_seconds, desc="До повторной проверки") as pbar:
        for remaining_seconds in range(wait_time_seconds, 0, -1):
            time.sleep(1)
            pbar.update(1)
