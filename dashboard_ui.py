import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class MovieDashboard:
    def __init__(self, root, username="mahesh"):
        self.root = root
        self.root.geometry('1280x720+0+0')
        self.root.title('Movie Collection Organizer')
        self.root.resizable(False, False)
        self.username = username
        self.connect_db()
        self.setup_ui()

    def connect_db(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="krrish13@KAU",
                database="movie_collection_organiser"
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Database Error", f"Connection failed: {e}")
            self.root.destroy()

    def setup_ui(self):
        # Welcome Label
        tk.Label(self.root, text=f'Welcome, {self.username}!', font=('Arial', 20, 'bold'), fg='white', bg='#E22529').pack(pady=4)

        # Menu Frame
        menu_frame = tk.Frame(self.root, bg='lightblue')
        menu_frame.pack(fill=tk.X, padx=10, pady=20)

        button_width = 20
        button_height = 2

        tk.Button(menu_frame, text='Add Movie', width=button_width, height=button_height, command=self.add_movie).pack(side=tk.LEFT, padx=10)
        tk.Button(menu_frame, text='Update Movie', width=button_width, height=button_height).pack(side=tk.LEFT, padx=10)
        tk.Button(menu_frame, text='Delete Movie', width=button_width, height=button_height).pack(side=tk.LEFT, padx=10)
        tk.Button(menu_frame, text='Export Movies', width=button_width, height=button_height).pack(side=tk.LEFT, padx=10)
        tk.Button(menu_frame, text='Logout', width=button_width, height=button_height).pack(side=tk.RIGHT, padx=10)

        # Search Frame
        search_frame = tk.Frame(self.root, bg='lightblue')
        search_frame.pack(fill=tk.X, padx=10)

        tk.Label(search_frame, text='Search:', bg='lightblue').pack(side=tk.LEFT, padx=10)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT, padx=10)
        tk.Button(search_frame, text='Search', width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text='Show All Movies', width=15).pack(side=tk.LEFT, padx=5)

        # Treeview Frame
        list_frame = tk.Frame(self.root)
        list_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(list_frame, columns=('ID', 'Title', 'Genre', 'Director', 'Year', 'Duration', 'Rating'), show='headings')
        for col in self.tree['columns']:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

    def add_movie(self):
        add_window = tk.Toplevel(self.root)
        add_window.title('Add Movie')

        fields = ['Title', 'Genre', 'Director', 'Release Year', 'Duration', 'Rating']
        entries = {}

        for field in fields:
            tk.Label(add_window, text=field, font=('Helvetica', 12)).pack(pady=2)
            entries[field] = tk.Entry(add_window, font=('Helvetica', 12))
            entries[field].pack(pady=2)

        def save():
            values = [entries[field].get() for field in fields]
            if any(v.strip() == '' for v in values):
                messagebox.showwarning("Input Error", "All fields are required")
                return
            try:
                self.cur.execute(
                    "INSERT INTO movies (title, genre, director, release_year, duration, rating) VALUES (%s, %s, %s, %s, %s, %s)",
                    values
                )
                self.conn.commit()
                messagebox.showinfo('Success', 'Movie added successfully!')
                add_window.destroy()
            except Exception as e:
                messagebox.showerror('Error', f'Failed to add movie: {e}')

        tk.Button(add_window, text='Save', font=('Helvetica', 12), command=save).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieDashboard(root)
    root.mainloop()
