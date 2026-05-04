import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Файл для хранения данных
DATA_FILE = "movies.json"

# Глобальные переменные
movies = []
entry_title = None
entry_genre = None
entry_year = None
entry_rating = None
filter_genre = None
filter_year = None
tree = None

# ------------------ Работа с JSON ------------------
def load_data():
    global movies
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            movies = json.load(f)

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=4)

# ------------------ Валидация ввода ------------------
def validate_input(title, genre, year, rating):
    if not title or not genre:
        messagebox.showerror("Ошибка", "Название и жанр не могут быть пустыми.")
        return False
    try:
        year_int = int(year)
        if year_int < 1888 or year_int > 2100:
            messagebox.showerror("Ошибка", "Год должен быть от 1888 до 2100.")
            return False
    except ValueError:
        messagebox.showerror("Ошибка", "Год должен быть числом.")
        return False

    try:
        rating_float = float(rating)
        if rating_float < 0 or rating_float > 10:
            messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10.")
            return False
    except ValueError:
        messagebox.showerror("Ошибка", "Рейтинг должен быть числом.")
        return False

    return True

# ------------------ Добавление фильма ------------------
def add_movie():
    global movies, entry_title, entry_genre, entry_year, entry_rating

    title = entry_title.get().strip()
    genre = entry_genre.get().strip()
    year = entry_year.get().strip()
    rating = entry_rating.get().strip()

    if validate_input(title, genre, year, rating):
        movie = {
            "title": title,
            "genre": genre,
            "year": int(year),
            "rating": float(rating)
        }
        movies.append(movie)
        save_data()
        refresh_table()

        # Очистка полей
        entry_title.delete(0, tk.END)
        entry_genre.delete(0, tk.END)
        entry_year.delete(0, tk.END)
        entry_rating.delete(0, tk.END)

        messagebox.showinfo("Успех", "Фильм добавлен!")

# ------------------ Фильтрация и обновление таблицы ------------------
def refresh_table(event=None):
    global movies, tree, filter_genre, filter_year

    # Получаем фильтры
    genre_filter = filter_genre.get().strip()
    year_filter = filter_year.get().strip()

    # Фильтруем список
    filtered = movies
    if genre_filter:
        filtered = [m for m in filtered if genre_filter.lower() in m["genre"].lower()]
    if year_filter:
        try:
            year_int = int(year_filter)
            filtered = [m for m in filtered if m["year"] == year_int]
        except ValueError:
            pass  # Если год не число, просто игнорируем фильтр

    # Очищаем таблицу
    for row in tree.get_children():
        tree.delete(row)

    # Заполняем таблицу
    for movie in filtered:
        tree.insert("", tk.END, values=(
            movie["title"],
            movie["genre"],
            movie["year"],
            movie["rating"]
        ))

def reset_filters():
    global filter_genre, filter_year
    filter_genre.delete(0, tk.END)
    filter_year.delete(0, tk.END)
    refresh_table()

# ------------------ Создание GUI ------------------
def create_widgets(root):
    global entry_title, entry_genre, entry_year, entry_rating, filter_genre, filter_year, tree

    # Рамка для ввода данных
    input_frame = tk.LabelFrame(root, text="Добавить фильм", padx=10, pady=10)
    input_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w")
    entry_title = tk.Entry(input_frame, width=30)
    entry_title.grid(row=0, column=1, padx=5, pady=2)

    tk.Label(input_frame, text="Жанр:").grid(row=0, column=2, sticky="w")
    entry_genre = tk.Entry(input_frame, width=20)
    entry_genre.grid(row=0, column=3, padx=5, pady=2)

    tk.Label(input_frame, text="Год:").grid(row=1, column=0, sticky="w")
    entry_year = tk.Entry(input_frame, width=10)
    entry_year.grid(row=1, column=1, padx=5, pady=2, sticky="w")

    tk.Label(input_frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky="w")
    entry_rating = tk.Entry(input_frame, width=10)
    entry_rating.grid(row=1, column=3, padx=5, pady=2, sticky="w")

    btn_add = tk.Button(input_frame, text="Добавить фильм", command=add_movie, bg="lightgreen")
    btn_add.grid(row=1, column=4, padx=10, pady=2)

    # Рамка для фильтров
    filter_frame = tk.LabelFrame(root, text="Фильтрация", padx=10, pady=10)
    filter_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, sticky="w")
    filter_genre = tk.Entry(filter_frame, width=20)
    filter_genre.grid(row=0, column=1, padx=5, pady=2)
    filter_genre.bind("<KeyRelease>", refresh_table)

    tk.Label(filter_frame, text="Фильтр по году:").grid(row=0, column=2, sticky="w")
    filter_year = tk.Entry(filter_frame, width=10)
    filter_year.grid(row=0, column=3, padx=5, pady=2)
    filter_year.bind("<KeyRelease>", refresh_table)

    btn_reset = tk.Button(filter_frame, text="Сбросить фильтры", command=reset_filters)
    btn_reset.grid(row=0, column=4, padx=10)

    # Таблица с фильмами
    columns = ("Название", "Жанр", "Год", "Рейтинг")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150 if col != "Название" else 250)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

# ------------------ Запуск приложения ------------------
def main():
    global movies
    root = tk.Tk()
    root.title("Movie Library - Личная кинотека")
    root.geometry("800x500")

    load_data()
    create_widgets(root)
    refresh_table()

    root.mainloop()

if __name__ == "__main__":
    main()
