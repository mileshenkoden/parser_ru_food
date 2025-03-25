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

conn = psycopg2.connect(**DB_PARAMS)
cur = conn.cursor()

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
        image_index INTEGER, -- count для сортування
        is_main BOOLEAN NOT NULL DEFAULT FALSE
    )
""")
conn.commit()

# Функція для перевірки, чи існує страва
def dish_exists(name):
    cur.execute("SELECT id FROM dish WHERE name = %s", (name,))
    return cur.fetchone()

# Функція для додавання страви
def add_dish(name, description, ingredients, steps):
    cur.execute("""
        INSERT INTO dish (name, description, ingredients, steps) 
        VALUES (%s, %s, %s, %s) RETURNING id
    """, (name, description, json.dumps(ingredients), json.dumps(steps)))

    dish_id = cur.fetchone()[0]
    conn.commit()
    print(f"✅ Додано страву '{name}' з ID {dish_id}")
    return dish_id

# Функція для додавання зображень
def add_image_to_db(dish_id, image_path, image_index, is_main=False):
    with open(image_path, "rb") as file:
        img_data = file.read()

    cur.execute("""
        INSERT INTO dish_images (dish_id, image, image_index, is_main) 
        VALUES (%s, %s, %s, %s)
    """, (dish_id, psycopg2.Binary(img_data), image_index, is_main))

    conn.commit()
    print(f"📷 Додано зображення {image_index} для страви ID {dish_id} (Main: {is_main})")

headers = {
    "Accept": "*/*",
    "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}
os.makedirs("data", exist_ok=True)
os.makedirs("media", exist_ok=True)
os.makedirs("dish", exist_ok=True)
os.makedirs("link", exist_ok=True)

url = "https://www.russianfood.com/"


req = requests.get(url)
src = req.text

with open("index.html" , "w" )as file:
    file.write(src)

with open("index.html", "r") as file:
    src = file.read()


soup = BeautifulSoup(src, "lxml")


all_food_start = soup.find_all("div", class_="annonce annonce_orange")

all_food_dict = {}

for food_block in all_food_start:  # Ітерація по всіх знайдених блоках
    all_food_title = food_block.find_all("a", class_="title")  # Пошук у кожному блоці

    for i in all_food_title:
        all_food_text = i.text.strip()
        all_food_href = "https://www.russianfood.com/" + i.get("href")
        all_food_dict[all_food_text] = all_food_href

with open("link/all_food_dict.json", "w", encoding="utf-8") as file:
    json.dump(all_food_dict, file, indent=4, ensure_ascii=False)




with open("link/all_food_dict.json", "r") as file:
    all_foods = json.load(file)

for count, (food_name, food_href) in enumerate(all_foods.items()):
    if dish_exists(food_name):
        print(f"⏩ Страва '{food_name}' вже існує, пропускаємо...")
        continue

    req = requests.get(url=food_href, headers=headers)
    src = req.text
    safe_name = re.sub(r'[\\/*?:"<>|]', "_", food_name)

    with open(f"data/food_{safe_name}.html", "w") as file:
        file.write(src)

    soup = BeautifulSoup(src, "lxml")

    img_main = soup.find("table", class_="main_image")
    img_main_src = None
    if img_main:
        img_main_src = img_main.find("img").get("src")
        if img_main_src and img_main_src.startswith("//"):
            img_main_src = "https:" + img_main_src

    description_food = soup.find("td", class_="padding_l padding_r")
    description_food_text = description_food.find("p").text.strip() if description_food else "Немає опису"

    goods_food = soup.find("table", class_="ingr")
    goods_food_text = [td.text.strip() for td in goods_food.find_all("td", class_="padding_l padding_r")]

    step_of_cooking = soup.find("div", class_="step_images_n")
    step_of_cooking_text = [p.text.strip() for p in step_of_cooking.find_all("p")] if step_of_cooking else []

    step_img = step_of_cooking.find_all("img") if step_of_cooking else []

    dish_data = {
        "name": food_name,
        "description": description_food_text,
        "ingredients": goods_food_text,
        "steps": step_of_cooking_text
    }

    with open(f"dish/{safe_name}.json", "w", encoding="utf-8") as file:
        json.dump(dish_data, file, indent=4, ensure_ascii=False)

    dish_id = add_dish(food_name, description_food_text, goods_food_text, step_of_cooking_text)

    if img_main_src:
        img_main_url = img_main_src if img_main_src.startswith("http") else "https://www.russianfood.com" + img_main_src
        img_data = requests.get(img_main_url).content
        main_image_path = f"media/main_{safe_name}.jpg"

        with open(main_image_path, "wb") as file:
            file.write(img_data)

        add_image_to_db(dish_id, main_image_path, image_index=0, is_main=True)

    for idx, img in enumerate(step_img):
        img_url = img.get("src")
        if img_url.startswith("//"):
            img_url = "https:" + img_url

        image_path = f"media/{safe_name}_{idx}.jpg"

        img_data = requests.get(img_url).content
        with open(image_path, "wb") as file:
            file.write(img_data)

        add_image_to_db(dish_id, image_path, image_index=idx + 1, is_main=False)

cur.close()
conn.close()






