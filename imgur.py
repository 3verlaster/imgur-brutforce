import requests
import random
import os
from PIL import Image
import io
from colorama import Fore, Style

# Создаем папку "images", если ее еще нет
if not os.path.exists('images'):
    os.makedirs('images')

# Список буквенно-цифровых символов, используемых в Imgur идентификаторах
CHARACTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

# Функция для генерации случайного идентификатора длиной n
def generate_id(n):
    return ''.join(random.choice(CHARACTERS) for _ in range(n))

# Функция для проверки, что полученный ответ содержит изображение
def is_image(content):
    try:
        image = Image.open(io.BytesIO(content))
        image.verify()
        return True
    except:
        return False

# Запрашиваем случайный идентификатор и проверяем наличие картинки на Imgur
count = int(input("Сколько картинок нужно скачать? "))
for i in range(count):
    found_image = False
    while not found_image:
        image_id = generate_id(5)
        url = f'https://i.imgur.com/{image_id}.jpg'
        response = requests.get(url)
        if response.status_code == 200 and is_image(response.content) and len(response.content) > 2000:
            found_image = True

    # Сохраняем картинку в папку "images"
    with open(os.path.join('images', f'{image_id}.jpg'), 'wb') as f:
        f.write(response.content)
        print(f'{Fore.GREEN}{Style.BRIGHT}Картинка {image_id}.jpg сохранена в папку images{Style.RESET_ALL}')
