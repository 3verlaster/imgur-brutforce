import requests
import random
import os
import tkinter as tk
from tkinter import messagebox

def download_images(num_images):
    if not os.path.exists('imgur_images'):
        os.makedirs('imgur_images')
        
    valid_images = []
    url = 'https://api.imgur.com/3/gallery/random/random/0'
    headers = {'Authorization': 'Client-ID 9e57cb1c4791cea'}
    response = requests.get(url, headers=headers)
    data = response.json()['data']

    for item in data:
        if 'images' in item:
            for image in item['images']:
                if 'type' in image and image['type'] == 'image/jpeg':
                    valid_images.append(image['id'])

    num_images = min(num_images, len(valid_images))

    for i in range(num_images):
        while True:
            image_id = random.choice(valid_images)
            url = f"https://i.imgur.com/{image_id}.jpg"
            response = requests.get(url)
            if response.status_code == 200:
                break
            else:
                valid_images.remove(image_id)

        image_path = os.path.join('imgur_images', f"{image_id}.jpg")
        with open(image_path, 'wb') as f:
            f.write(response.content)

        if os.path.getsize(image_path) < 2 * 1024:
            os.remove(image_path)
        else:
            print(f"Сохранено: {image_path}")
    
    tk.messagebox.showinfo("Готово!", f"Скачано {num_images} изображений")
    
def show_log():
    log_path = os.path.join('imgur_images', 'download_log.txt')
    if os.path.exists(log_path):
        with open(log_path, 'r') as f:
            log = f.read()
            tk.messagebox.showinfo("Лог", log)
    else:
        tk.messagebox.showerror("Ошибка", "Лог еще не создан")

root = tk.Tk()
root.title("Скачать случайные изображения с imgur")
root.geometry("300x200")

num_images_label = tk.Label(root, text="Количество изображений")
num_images_entry = tk.Entry(root)
num_images_label.pack()
num_images_entry.pack()

download_button = tk.Button(root, text="Скачать", command=lambda: download_images(int(num_images_entry.get())))
download_button.pack()

log_button = tk.Button(root, text="Посмотреть лог", command=show_log)
log_button.pack()

root.mainloop()
