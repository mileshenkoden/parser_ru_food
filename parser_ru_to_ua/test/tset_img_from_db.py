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

def get_dish_images(dish_id):
    cur.execute("SELECT image, image_index, is_main FROM dish_images WHERE dish_id = %s ORDER BY image_index", (dish_id,))
    images = cur.fetchall()

    if not images:
        print(f"⚠️ Немає зображень для страви ID {dish_id}")
        return

    os.makedirs("test_img", exist_ok=True)

    for img_data, index, is_main in images:
        filename = f"test_img/output_{dish_id}_{index}.jpg"
        with open(filename, "wb") as file:
            file.write(img_data)
        print(f"📷 Зображення збе`режено у файл {filename} (Main: {is_main})")

get_dish_images(dish_id=3)
