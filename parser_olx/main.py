import os
import json
import requests
from bs4 import BeautifulSoup
import re

# Створення папок для збереження даних
os.makedirs("dish", exist_ok=True)
os.makedirs("media", exist_ok=True)  # Папка для всіх зображень

# URL сайту
url = "https://www.olx.ua/uk/list/q-%D1%84%D0%B5%D0%BD/"

# Заголовки для запиту
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,uk;q=0.6,zh-TW;q=0.5,zh;q=0.4",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Connection": "keep-alive"
}

# Отримання HTML-коду сторінки
req = requests.get(url=url, headers=headers)
src = req.text

# Збереження сторінки у файл (для перевірки)
with open("index.html", "w", encoding="utf-8") as file:
    file.write(src)

# Парсинг HTML
soup = BeautifulSoup(src, "lxml")

# Пошук оголошень
ads = soup.find_all("div", class_="css-1g5933j")
text_all = {}

for index, ad in enumerate(ads):
    all_title = ad.find("h4")
    all_price = ad.find("p", class_="css-6j1qjp")
    all_status = ad.find("span", class_="css-iudov9")
    all_place_time = ad.find("p", class_="css-1mwdrlh")

    # Перевірка, чи елементи знайдені
    all_title_text = all_title.text.strip() if all_title else f"Оголошення_{index}"
    all_price_text = all_price.text.strip() if all_price else "Ціна не вказана"
    all_status_text = all_status.text.strip() if all_status else "Немає статусу"
    all_place_time_text = all_place_time.text.strip() if all_place_time else "Місце і час не вказані"

    # Очищення імені файлу
    safe_name = re.sub(r'[\\/*?:"<>|]', "_", all_title_text)

    text_all[safe_name] = {
        "price": all_price_text,
        "status": all_status_text,
        "place_and_time": all_place_time_text,
        "images": []  # Тут зберігатимемо посилання на зображення
    }

    # Пошук зображень у кожному оголошенні
    img_container = ad.find("div", class_="css-gl6djm")
    if img_container:
        img_tags = img_container.find_all("img")

        for img_index, img_tag in enumerate(img_tags):
            img_src = img_tag.get("src")
            if img_src:
                if img_src.startswith("//"):
                    img_src = "https:" + img_src
                elif not img_src.startswith("http"):
                    img_src = "https://www.olx.ua" + img_src

                # Завантаження зображення
                img_data = requests.get(img_src).content
                img_filename = os.path.join("media", f"{safe_name}_{img_index}.jpg")

                with open(img_filename, "wb") as file:
                    file.write(img_data)

                # Додаємо шлях до файлу в JSON
                text_all[safe_name]["images"].append(img_filename)

# Запис у JSON
json_path = os.path.join("dish", "index.json")
with open(json_path, "w", encoding="utf-8") as file:
    json.dump(text_all, file, ensure_ascii=False, indent=4)

print(f"Дані успішно збережено у {json_path}")
print("Зображення збережені у папці media/")
