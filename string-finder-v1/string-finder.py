import os
import re
from datetime import datetime

def search_text_in_files(folder_path, search_text):
    report_data = {
        'search_text': search_text,
        'search_date': datetime.now().strftime('%Y-%m-%d'),
        'search_time': datetime.now().strftime('%H:%M:%S'),
        'search_folder': folder_path,
        'scanned_folders': {},
        'matches': []
    }

    for root, dirs, files in os.walk(folder_path):
        folder_match_count = 0
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        if re.search(search_text, line):
                            match = {
                                'text': line.strip(),
                                'line_number': line_num,
                                'file_path': file_path
                            }
                            report_data['matches'].append(match)
                            folder_match_count += 1
            except (UnicodeDecodeError, PermissionError):
                continue
        
        report_data['scanned_folders'][root] = folder_match_count

    return report_data

def generate_report(report_data):
    # Создаем папку reports, если ее нет
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    # Генерируем имя файла отчета
    folder_name = os.path.basename(report_data['search_folder'])
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    report_filename = f"{folder_name}-report-{timestamp}.txt"
    report_path = os.path.join('reports', report_filename)
    
    with open(report_path, 'w', encoding='utf-8') as report_file:
        # Заголовок отчета
        # report_file.write("="*50 + "\n")
        report_file.write("SEARCH REPORT\n")
        # report_file.write("="*50 + "\n\n")
        
        # Информация о поиске
        report_file.write(f"Search text: {report_data['search_text']}\n")
        report_file.write(f"Date: {report_data['search_date']}\n")
        report_file.write(f"Time: {report_data['search_time']}\n")
        report_file.write(f"Search folder: {report_data['search_folder']}\n\n")
        
        # Просмотренные папки и количество совпадений
        # report_file.write("="*50 + "\n")
        report_file.write("SCANNED FOLDERS AND MATCH COUNTS\n")
        # report_file.write("="*50 + "\n")
        for folder, count in report_data['scanned_folders'].items():
            report_file.write(f"{folder}: {count} matches\n")
        report_file.write("\n")
        
        # Найденные совпадения
        # report_file.write("="*50 + "\n")
        report_file.write("FOUND MATCHES\n")
        # report_file.write("="*50 + "\n")
        for match in report_data['matches']:
            report_file.write(f"Text: {match['text']}\n")
            report_file.write(f"Line: {match['line_number']}\n")
            report_file.write(f"File: {match['file_path']}\n")
            report_file.write("-"*50 + "\n")
    
    return report_path

def main():
    print("Text Search Tool")
    # print("="*50)
    
    # Запрашиваем у пользователя данные
    folder_path = input("Enter the folder path to search in: ")
    while not os.path.isdir(folder_path):
        print("Error: The specified path is not a valid directory.")
        folder_path = input("Enter the folder path to search in: ")
    
    search_text = input("Enter the text to search for: ")
    
    # Выполняем поиск
    print("\nSearching...")
    report_data = search_text_in_files(folder_path, search_text)
    
    # Генерируем отчет
    report_path = generate_report(report_data)
    
    print(f"\nSearch completed. Report saved to: {report_path}")
    print(f"Total matches found: {len(report_data['matches'])}")

if __name__ == "__main__":
    main()