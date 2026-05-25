import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Имя файла для сохранения
DATA_FILE = "movies.json"

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Личная кинотека")
        self.root.geometry("700x500")

        self.movies = []
        self.load_data()

        # --- Форма ввода ---
        frame_form = ttk.LabelFrame(root, text="Добавить фильм")
        frame_form.pack(pady=10, padx=10, fill="x")

        ttk.Label(frame_form, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_title = ttk.Entry(frame_form)
        self.entry_title.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Жанр:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_genre = ttk.Entry(frame_form)
        self.entry_genre.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_form, text="Год:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_year = ttk.Entry(frame_form)
        self.entry_year.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Рейтинг (0-10):").grid(row=1, column=2, padx=5, pady=5)
        self.entry_rating = ttk.Entry(frame_form)
        self.entry_rating.grid(row=1, column=3, padx=5, pady=5)

        btn_add = ttk.Button(frame_form, text="Добавить", command=self.add_movie)
        btn_add.grid(row=2, column=0, columnspan=4, pady=10)

        # --- Фильтрация ---
        frame_filter = ttk.LabelFrame(root, text="Фильтр")
        frame_filter.pack(pady=5, padx=10, fill="x")

        ttk.Label(frame_filter, text="Жанр:").pack(side="left", padx=5)
        self.filter_genre = ttk.Entry(frame_filter)
        self.filter_genre.pack(side="left", padx=5)

        ttk.Label(frame_filter, text="Год:").pack(side="left", padx=5)
        self.filter_year = ttk.Entry(frame_filter)
        self.filter_year.pack(side="left", padx=5)

        btn_filter = ttk.Button(frame_filter, text="Применить", command=self.display_movies)
        btn_filter.pack(side="left", padx=10)
        btn_clear = ttk.Button(frame_filter, text="Сброс", command=self.clear_filter)
        btn_clear.pack(side="left", padx=5)

        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=("Title", "Genre", "Year", "Rating"), show="headings")
        self.tree.heading("Title", text="Название")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Year", text="Год")
        self.tree.heading("Rating", text="Рейтинг")
        self.tree.pack(pady=10, padx=10, fill="both", expand=True)

        self.display_movies()

    # --- Функционал ---
    def add_movie(self):
        title = self.entry_title.get()
        genre = self.entry_genre.get()
        year = self.entry_year.get()
        rating = self.entry_rating.get()

        # Валидация
        if not (title and genre and year and rating):
            messagebox.showwarning("Ошибка", "Заполните все поля")
            return

        try:
            year = int(year)
            rating = float(rating)
            if not (0 <= rating <= 10):
                raise ValueError
        except ValueError:
            messagebox.showwarning("Ошибка", "Год должен быть числом, рейтинг - число от 0 до 10")
            return

        movie = {"title": title, "genre": genre, "year": year, "rating": rating}
        self.movies.append(movie)
        self.save_data()
        self.display_movies()
        
        # Очистка полей
        self.entry_title.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)
        self.entry_rating.delete(0, tk.END)

    def display_movies(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Фильтрация
        f_genre = self.filter_genre.get().lower()
        f_year = self.filter_year.get()

        for movie in self.movies:
            if f_genre and f_genre not in movie["genre"].lower():
                continue
            if f_year and f_year != str(movie["year"]):
                continue
            
            self.tree.insert("", tk.END, values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))

    def clear_filter(self):
        self.filter_genre.delete(0, tk.END)
        self.filter_year.delete(0, tk.END)
        self.display_movies()

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.movies = json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()