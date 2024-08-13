
#       ███████╗███████╗██╗     ███████╗███╗  ██╗██╗  ██╗ █████╗     ██████╗ ██╗   ██╗██████╗ ██╗   ██╗
#       ╚════██║██╔════╝██║     ██╔════╝████╗ ██║██║ ██╔╝██╔══██╗   ██╔════╝ ██║   ██║██╔══██╗██║   ██║
#         ███╔═╝█████╗  ██║     █████╗  ██╔██╗██║█████═╝ ███████║   ██║  ██╗ ██║   ██║██████╔╝██║   ██║
#       ██╔══╝  ██╔══╝  ██║     ██╔══╝  ██║╚████║██╔═██╗ ██╔══██║   ██║  ╚██╗██║   ██║██╔══██╗██║   ██║
#       ███████╗███████╗███████╗███████╗██║ ╚███║██║ ╚██╗██║  ██║██╗╚██████╔╝╚██████╔╝██║  ██║╚██████╔╝
#       ╚══════╝╚══════╝╚══════╝╚══════╝╚═╝  ╚══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ 
#        ===================================================================================================
#                       Небольшой тул для экспортирования url:login:pass из логов
#                       Вообщем проверяет все папки на наличие текстового документа Passwords.txt, All_Passwords
#                       Ищет наличие элементов USER,URL,PASSWORDS в этих документах как зачастую бывает
#                       Ну и вписывает результаты в отдельный файл в формате url:login:pass
#                       Файл остаётся в сурсе так-что можете переделать под себя
#                       Сделано на быструю руку юзером https://lolz.live/members/7251982/
#       ====================================================================================================


import os
import re
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

threads = 600 # Количество потоков
root_folder_path = 'D:/'  # Входной путь к папке для поиска
output_file_path = 'extracted_data.txt' # Выходной путь к папке для поиска
pattern = re.compile(r'(?:URL|URL:|url|url:|Url:)\s*(\S+)\s*(?:USER|Username|USERNAME|user|User|Name|name):\s*(\S+)\s*(?:PASS|Password|PASSWORD|password|pass):\s*(\S+)') # Регулярка 

def extract_data_from_file(file_path):
    extracted_data = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
            matches = pattern.findall(content)
            for match in matches:
                url, user, password = match
                result = f'{url}:{user}:{password}\n'
                extracted_data.append(result)
    except Exception as e:
        print(f'Ошибка при чтении {file_path}: {e}')
    return extracted_data

def write_data_to_file(data, output_file_lock):
    with output_file_lock:
        try:
            with open(output_file_path, 'a', encoding='utf-8') as output_file:
                output_file.writelines(data)
        except Exception as e:
            print(f'Ошибка при записи в {output_file_path}: {e}')

def process_file(file_path, output_file_lock):
    extracted_data = extract_data_from_file(file_path)
    if extracted_data:
        write_data_to_file(extracted_data, output_file_lock)

def search_and_extract_data(root_folder):
    output_file_lock = Lock()
    with ThreadPoolExecutor(max_workers=threads) as executor: # Количество потоков
        for root, dirs, files in os.walk(root_folder):
            for file_name in files:
                if 'Passwords' or 'All_Passwords' in file_name:
                    file_path = os.path.join(root, file_name)
                    print(f'Обработка файла: {file_path}')
                    executor.submit(process_file, file_path, output_file_lock)

if __name__ == '__main__':
    search_and_extract_data(root_folder_path)
    print(f'Экспортировано в {output_file_path}')
