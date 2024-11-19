# Необходимо реализовать скрипт, который будет получать с русскоязычной википедии список всех животных
# (https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту) и записывать в файл в формате beasts.csv количество
# животных на каждую букву алфавита. Содержимое результирующего файла:
# А,642
# Б,412
# В, ....

# Примечание:
# анализ текста производить не нужно, считается любая запись из категории (в ней может быть не только название,
# но и, например, род)

import requests
from bs4 import BeautifulSoup
import csv
from collections import defaultdict

# URL категории "Животные по алфавиту"
BASE_URL = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"


def get_animals_count_by_letter(base_url):
    # Словарь для хранения количества животных на каждую букву
    animals_count = defaultdict(int)
    session = requests.Session()

    # Проходим по всем страницам категории
    while base_url:
        print(f"Processing: {base_url}")
        response = session.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим всех животных на текущей странице
        animals = soup.select("#mw-pages .mw-category.mw-category-columns  li a")
        for animal in animals:
            first_letter = animal.text[0].upper()
            if first_letter.isalpha():
                animals_count[first_letter] += 1

        # Ищем ссылку на следующую страницу
        next_page = soup.find("a", string="Следующая страница")
        base_url = f"https://ru.wikipedia.org{next_page['href']}" if next_page else None

    return animals_count


def save_to_csv(animals_count, filename="beasts.csv"):
    # Сортируем по алфавиту и сохраняем в CSV
    with open(filename, mode="w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Буква", "Количество"])
        for letter, count in sorted(animals_count.items()):
            writer.writerow([letter, count])
    print(f"Данные сохранены в {filename}")


if __name__ == "__main__":
    animals_count = get_animals_count_by_letter(BASE_URL)
    save_to_csv(animals_count)
