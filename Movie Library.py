import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Файл для хранения данных
DATA_FILE = "movies.json"

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("800x500")

        self.movies = []
        self.load_data()

        # Создание интерфейса
        self.create_widgets()
        self.refresh_table()

    # ------------------ Работа с JSON ------------------
    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.movies = json.load(f)

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    # ------------------ Валидация ввода ------------------
    def validate_input(self, title, genre, year, rating):
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
    def add_movie(self):
        title = self.entry_title.get().strip()
        genre = self.entry_genre.get().strip()
        year = self.entry_year.get().strip()
        rating = self.entry_rating.get().strip()

        if self.validate_input(title, genre, year, rating):
            movie = {
                "title": title,
                "genre": genre,
                "year": int(year),
                "rating": float(rating)
            }
            self.movies.append(movie)
            self.save_data()
            self.refresh_table()

            # Очистка полей
            self.entry_title.delete(0, tk.END)
            self.entry_genre.delete(0, tk.END)
            self.entry_year.delete(0, tk.END)
            self.entry_rating.delete(0, tk.END)

            messagebox.showinfo("Успех", "Фильм добавлен!")

    # ------------------ Фильтрация ------------------
    def refresh_table(self):
        # Получаем фильтры
        genre_filter = self.filter_genre.get().strip()
        year_filter = self.filter_year.get().strip()

        # Фильтруем список
        filtered = self.movies
        if genre_filter:
            filtered = [m for m in filtered if genre_filter.lower() in m["genre"].lower()]
        if year_filter:
            try:
                year_int = int(year_filter)
                filtered = [m for m in filtered if m["year"] == year_int]
            except ValueError:
                pass  # Если год не число, просто игнорируем фильтр

        # Очищаем таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Заполняем таблицу
        for movie in filtered:
            self.tree.insert("", tk.END, values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                movie["rating"]
            ))

    # ------------------ Создание GUI ------------------
    def create_widgets(self):
        # Рамка для ввода данных
        input_frame = tk.LabelFrame(self.root, text="Добавить фильм", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.entry_title = tk.Entry(input_frame, width=30)
        self.entry_title.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(input_frame, text="Жанр:").grid(row=0, column=2, sticky="w")
        self.entry_genre = tk.Entry(input_frame, width=20)
        self.entry_genre.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(input_frame, text="Год:").grid(row=1, column=0, sticky="w")
        self.entry_year = tk.Entry(input_frame, width=10)
        self.entry_year.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        tk.Label(input_frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky="w")
        self.entry_rating = tk.Entry(input_frame, width=10)
        self.entry_rating.grid(row=1, column=3, padx=5, pady=2, sticky="w")

        btn_add = tk.Button(input_frame, text="Добавить фильм", command=self.add_movie, bg="lightgreen")
        btn_add.grid(row=1, column=4, padx=10, pady=2)

        # Рамка для фильтров
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, sticky="w")
        self.filter_genre = tk.Entry(filter_frame, width=20)
        self.filter_genre.grid(row=0, column=1, padx=5, pady=2)
        self.filter_genre.bind("<KeyRelease>", lambda e: self.refresh_table())

        tk.Label(filter_frame, text="Фильтр по году:").grid(row=0, column=2, sticky="w")
        self.filter_year = tk.Entry(filter_frame, width=10)
        self.filter_year.grid(row=0, column=3, padx=5, pady=2)
        self.filter_year.bind("<KeyRelease>", lambda e: self.refresh_table())

        btn_reset = tk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters)
        btn_reset.grid(row=0, column=4, padx=10)

        # Таблица с фильмами
        columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150 if col != "Название" else 250)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def reset_filters(self):
        self.filter_genre.delete(0, tk.END)
        self.filter_year.delete(0, tk.END)
        self.refresh_table()


# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
