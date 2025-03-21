import json
import requests
from bs4 import BeautifulSoup
import os
import re
import psycopg2

DB_PARAMS = {
    "dbname": "food_ru_db",
    "user": "postgres",
    "password": "a33900400",
    "host": "localhost",
    "port": "5432"
}

# Підключення до бази даних
conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()

# 🔹 1. Створюємо єдину таблицю dish, якщо її ще немає
cur.execute("""
    CREATE TABLE IF NOT EXISTS dish (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        ingredients JSONB,
        steps JSONB
    )
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS dish_images (
        id SERIAL PRIMARY KEY,
        dish_id INTEGER REFERENCES dish(id) ON DELETE CASCADE,
        image BYTEA NOT NULL,
        image_index INTEGER, -- `count` для сортування
        is_main BOOLEAN NOT NULL DEFAULT FALSE
    )
""")
conn.commit()

headers = {
    "Accept": '*/*',
    "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

# Створюємо необхідні папки
os.makedirs("data", exist_ok=True)
os.makedirs("dish", exist_ok=True)
os.makedirs("media", exist_ok=True)

# Завантажуємо список страв
with open("all_food_dict.json", "r") as file:
    all_foods = json.load(file)

count = 0
for all_food_name, all_food_href in all_foods.items():
    if count == 0:  # Обробляємо лише одну страву для тесту
        req = requests.get(url=all_food_href, headers=headers)
        src = req.text

        safe_name = re.sub(r'[\\/*?:"<>|]', "_", all_food_name)

        # Зберігаємо HTML сторінку
        with open(f"data/food{count + 1}_{safe_name}.html", "w") as file:
            file.write(src)

        soup = BeautifulSoup(src, "lxml")

        # 🔹 Отримуємо головне зображення
        img_main = soup.find("table", class_="main_image")
        img_main_src = None
        if img_main:
            img_main_src = img_main.find("img").get("src")
            if img_main_src and img_main_src.startswith("//"):
                img_main_src = "https:" + img_main_src

        # 🔹 Опис страви
        description_food = soup.find("td", class_="padding_l padding_r")
        description_food_text = description_food.find("p").text.strip() if description_food else "Немає опису"

        # 🔹 Інгредієнти
        goods_food = soup.find("table", class_="ingr")
        goods_food_text = [td.text.strip() for td in goods_food.find_all("td", class_="padding_l padding_r")]

        # 🔹 Кроки приготування
        step_of_cooking = soup.find("div", class_="step_images_n")
        step_of_cooking_text = [p.text.strip() for p in step_of_cooking.find_all("p")] if step_of_cooking else []

        # 🔹 Завантажуємо зображення кроків
        step_img = step_of_cooking.find_all("img") if step_of_cooking else []
        z = 0
        for i in step_img:
            img_url = i.get("src")
            if img_url.startswith("//"):
                img_url = "https:" + img_url  # Додаємо протокол

            req_ = requests.get(url=img_url)
            response = req_.content

            with open(f"media/{count}_{z}.jpg", "wb") as file:
                file.write(response)
            z += 1

        # 🔹 Завантажуємо головне зображення, якщо є
        if img_main_src:
            img_main_url = img_main_src if img_main_src.startswith("http") else "https://www.russianfood.com" + img_main_src
            img_data = requests.get(img_main_url).content
            with open(f"media/main_{count}.jpg", "wb") as file:
                file.write(img_data)

        # 🔹 Створюємо JSON-дані страви
        dish_data = {
            "name": all_food_name,
            "description": description_food_text,
            "ingredients": goods_food_text,
            "steps": step_of_cooking_text
        }

        # 🔹 Зберігаємо JSON-дані у файл
        with open(f"dish/{count}.json", "w", encoding="utf-8") as file:
            json.dump(dish_data, file, indent=4, ensure_ascii=False)

        # 🔹 Вставляємо в єдину таблицю dish
        cur.execute(
            "INSERT INTO dish (name, description, ingredients, steps) VALUES (%s, %s, %s, %s)",
            (all_food_name, description_food_text, json.dumps(goods_food_text), json.dumps(step_of_cooking_text))
        )
        conn.commit()

        count += 1  # Обробляємо лише першу страву для тесту

# Закриваємо підключення до бази
cur.close()
conn.close()


#            (all_food_name, description_food_text, json.dumps(goods_food_text), json.dumps(step_of_cooking_text))

# url = "https://www.russianfood.com/"
#
# headers = {
#     "Accept" : '*/*',
#
#     "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
# }
#
#
# req = requests.get(url)
# src = req.text
# print(src)
#
# with open("index.html" , "w" )as file:
#     file.write(src)
#
# with open("index.html", "r") as file:
#     src = file.read()
#
#
# soup = BeautifulSoup(src, "lxml")
#
#
# all_food_start = soup.find_all("table", class_="top")
# all_food_title = soup.find_all("a", class_="title")
#
# all_food_dict = {}
#
#
# for i in all_food_title:
#     all_food_text = i.text
#     all_food_href = "https://www.russianfood.com/" + i.get("href")
#     all_food_dict[all_food_text] = all_food_href
#
#     with open("all_food_dict.json", "a") as file:
#         json.dump(all_food_dict, file, indent=4, ensure_ascii=False)

