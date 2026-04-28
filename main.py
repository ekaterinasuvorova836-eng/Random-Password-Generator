import tkinter as tk
from tkinter import messagebox, ttk
import random
import string
import json
import os

# --- Настройки ---
HISTORY_FILE = "password_history.json"
MIN_LENGTH = 4
MAX_LENGTH = 32


# --- Функции логики ---

def generate_password(length, use_digits, use_letters, use_special):
    """Генерирует пароль на основе выбранных параметров."""
    if length < MIN_LENGTH or length > MAX_LENGTH:
        raise ValueError(f"Длина должна быть от {MIN_LENGTH} до {MAX_LENGTH}.")

    char_pool = ""
    if use_digits:
        char_pool += string.digits
    if use_letters:
        char_pool += string.ascii_letters
    if use_special:
        char_pool += string.punctuation

    if not char_pool:
        raise ValueError("Выберите хотя бы один тип символов.")

    return ''.join(random.choices(char_pool, k=length))


def load_history():
    """Загружает историю из файла JSON. Возвращает пустой список при любой ошибке."""
    try:
        # Проверяем, является ли файл обычным файлом (не директорией и т.д.)
        if os.path.isfile(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                # Пытаемся загрузить JSON. Если файл пуст или поврежден,
                # json.load() может вызвать ValueError или другие исключения.
                data = json.load(f)
                # Проверяем, что загруженные данные - это список
                if isinstance(data, list):
                    return data
    except Exception:
        # Любая ошибка (чтения, декодирования, неверный формат) приводит к возврату пустого списка.
        # Это самый надежный способ избежать краха приложения.
        pass
    return []


def save_history(history):
    """Сохраняет историю в файл JSON. Игнорирует ошибки записи."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        # Если не удалось сохранить (например, нет прав на запись), просто игнорируем.
        # Приложение продолжит работать.
        pass


def add_to_history(password):
    """Добавляет новый пароль в историю и обновляет файл."""
    history = load_history()
    history.insert(0, password)
    if len(history) > 20:
        history = history[:20]
    save_history(history)
    update_history_display()


# --- Функции GUI ---

def on_generate():
    """Обработчик нажатия кнопки 'Сгенерировать'."""
    try:
        length = int(scale_length.get())
        use_digits = var_digits.get()
        use_letters = var_letters.get()
        use_special = var_special.get()

        password = generate_password(length, use_digits, use_letters, use_special)

        entry_password.delete(0, tk.END)
        entry_password.insert(0, password)

        add_to_history(password)

    except ValueError as e:
        messagebox.showwarning("Ошибка ввода", str(e))


def update_history_display():
    """Обновляет виджет истории в окне."""
    history = load_history()
    listbox_history.delete(0, tk.END)
    for pwd in history:
        listbox_history.insert(tk.END, pwd)


# --- Создание главного окна ---
root = tk.Tk()
root.title("Генератор случайных паролей")
root.geometry("500x450")
root.resizable(False, False)

# --- Визуальные элементы ---

# Ползунок длины пароля
frame_length = tk.Frame(root)
frame_length.pack(pady=10)
tk.Label(frame_length, text="Длина пароля:").pack(side=tk.LEFT)
scale_length = tk.Scale(frame_length, from_=MIN_LENGTH, to=MAX_LENGTH, orient=tk.HORIZONTAL, length=250)
scale_length.set(12)
scale_length.pack(side=tk.LEFT, padx=10)

# Чекбоксы выбора символов
frame_options = tk.Frame(root)
frame_options.pack(pady=5)
var_digits = tk.BooleanVar(value=True)
var_letters = tk.BooleanVar(value=True)
var_special = tk.BooleanVar(value=True)
tk.Checkbutton(frame_options, text="Цифры (0-9)", variable=var_digits).pack(side=tk.LEFT)
tk.Checkbutton(frame_options, text="Буквы (a-z, A-Z)", variable=var_letters).pack(side=tk.LEFT)
tk.Checkbutton(frame_options, text="Спецсимволы (!@#$)", variable=var_special).pack(side=tk.LEFT)

# Кнопка генерации и поле вывода
frame_generate = tk.Frame(root)
frame_generate.pack(pady=15)
entry_password = tk.Entry(frame_generate, font=('Arial', 14), width=30)
entry_password.pack(side=tk.LEFT)
btn_generate = tk.Button(frame_generate, text="Сгенерировать", font=('Arial', 12), command=on_generate)
btn_generate.pack(side=tk.LEFT, padx=10)

# История паролей
frame_history = tk.Frame(root)
frame_history.pack(pady=10, fill=tk.BOTH, expand=True)
label_history = tk.Label(frame_history, text="История генераций:")
label_history.pack()
scrollbar = ttk.Scrollbar(frame_history)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox_history = tk.Listbox(frame_history, yscrollcommand=scrollbar.set, height=8, width=60)
listbox_history.pack(padx=5, pady=5)
scrollbar.config(command=listbox_history.yview)

# --- Инициализация ---
update_history_display()
root.mainloop()
