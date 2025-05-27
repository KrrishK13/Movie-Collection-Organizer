import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
import os
import csv
from PIL import Image, ImageTk

# ---------------------------- Login Page ----------------------------
class LoginPage:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1350x700')
        self.root.title("Login - Movie Collection Organizer")
        self.root.resizable(False, False)
        self.setup_login_ui()

    def setup_login_ui(self):
        bg_image_path = os.path.join("images", "login_3.jpg")
        if not os.path.isfile(bg_image_path):
            messagebox.showerror('Error', 'Login background image not found!')
            self.root.destroy()
            return

        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((1350, 700), Image.LANCZOS)
        self.bgimg = ImageTk.PhotoImage(bg_image)
        bg = tk.Label(self.root, image=self.bgimg)
        bg.place(x=0, y=0, relwidth=1, relheight=1)

        frame = tk.Frame(self.root, bg='white', padx=20, pady=20, bd=7, relief=tk.RIDGE)
        frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        tk.Label(frame, text='Movie Collection Organizer', font=('Helvetica', 20, 'bold'), bg='white', fg='#333').grid(row=0, column=0, columnspan=2, pady=10)
        tk.Label(frame, text='Username:', font=('Helvetica', 14), bg='white').grid(row=1, column=0, pady=5)
        tk.Label(frame, text='Password:', font=('Helvetica', 14), bg='white').grid(row=2, column=0, pady=5)

        self.unameE = tk.Entry(frame, font=('Helvetica', 14))
        self.unameE.grid(row=1, column=1, pady=5)
        self.upassE = tk.Entry(frame, font=('Helvetica', 14), show='*')
        self.upassE.grid(row=2, column=1, pady=5)

        login_btn = tk.Button(frame, text='Login', font=('Helvetica', 14, 'bold'), command=self.login_action)
        login_btn.grid(row=3, column=0, columnspan=2, pady=10)

    def login_action(self):
        username = self.unameE.get()
        password = self.upassE.get()
        if username == 'mahesh' and password == 'mahesh123':
            self.root.destroy()
            root = tk.Tk()
            MovieDashboard(root, username)
            root.mainloop()
        else:
            messagebox.showerror('Error', 'Invalid credentials')


# ---------------------------- Dashboard ----------------------------
class MovieDashboard:
    def __init__(self, root, username="mahesh"):
        self.root = root
        self.root.geometry('1280x720+0+0')
        self.root.title('Movie Collection Organizer')
        self.root.resizable(False, False)
        self.username = username
        self.connect_db()
        self.setup_ui()
        self.show_movies()

    def connect_db(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="krrish13@KAU",  # Change this for your DB
                database="movie_collection_organiser"
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Database Error", f"Connection failed: {e}")
            self.root.destroy()

    def setup_ui(self):
        # Background Image for Dashboard
        bg_path = os.path.join("images", "dashboard_bg.jpg")
        if os.path.exists(bg_path):
            bg_image = Image.open(bg_path)
            bg_image = bg_image.resize((1280, 720), Image.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(bg_image)
            self.bg_label = tk.Label(self.root, image=self.bg_img)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_label.lower()

        # Welcome Label
        tk.Label(self.root, text=f'Welcome, {self.username}!', font=('Arial', 20, 'bold'), fg='white', bg='#E22529').pack(pady=4)

        # Menu Frame
        menu_frame = tk.Frame(self.root, bg='lightblue')
        menu_frame.pack(fill=tk.X, padx=10, pady=20)

        button_width = 20
        button_height = 2

        tk.Button(menu_frame, text='Add Movie', width=button_width, height=button_height, command=self.add_movie).pack(side=tk.LEFT, padx=10)
        tk.Button(menu_frame, text='Update Movie', width=button_width, height=button_height, command=self.update_movie).pack(side=tk.LEFT, padx=10)
        tk.Button(menu_frame, text='Delete Movie', width=button_width, height=button_height, command=self.delete_movie).pack(side=tk.LEFT, padx=10)
        tk.Button(menu_frame, text='Export Movies', width=button_width, height=button_height, command=self.export_movies).pack(side=tk.LEFT, padx=10)
        tk.Button(menu_frame, text='Logout', width=button_width, height=button_height, command=self.logout).pack(side=tk.RIGHT, padx=10)

        # Search Frame
        search_frame = tk.Frame(self.root, bg='lightblue')
        search_frame.pack(fill=tk.X, padx=10)

        tk.Label(search_frame, text='Search:', bg='lightblue').pack(side=tk.LEFT, padx=10)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side=tk.LEFT, padx=10)
        tk.Button(search_frame, text='Search', width=15, command=self.search_movies).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text='Show All Movies', width=15, command=self.show_movies).pack(side=tk.LEFT, padx=5)

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

    def show_movies(self):
        self.cur.execute("SELECT * FROM movies")
        rows = self.cur.fetchall()
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert('', tk.END, values=row)

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
                self.show_movies()
            except Exception as e:
                messagebox.showerror('Error', f'Failed to add movie: {e}')

        tk.Button(add_window, text='Save', font=('Helvetica', 12), command=save).pack(pady=10)

    def update_movie(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Select Movie", "Please select a movie to update.")
            return

        values = self.tree.item(selected, 'values')
        if not values:
            return

        update_window = tk.Toplevel(self.root)
        update_window.title('Update Movie')

        fields = ['Title', 'Genre', 'Director', 'Release Year', 'Duration', 'Rating']
        entries = {}

        for i, field in enumerate(fields):
            tk.Label(update_window, text=field, font=('Helvetica', 12)).pack(pady=2)
            entries[field] = tk.Entry(update_window, font=('Helvetica', 12))
            entries[field].pack(pady=2)
            entries[field].insert(0, values[i + 1])

        def save():
            new_values = [entries[field].get() for field in fields]
            if any(v.strip() == '' for v in new_values):
                messagebox.showwarning("Input Error", "All fields are required")
                return
            try:
                self.cur.execute(
                    "UPDATE movies SET title=%s, genre=%s, director=%s, release_year=%s, duration=%s, rating=%s WHERE movie_id=%s",
                    (*new_values, values[0])
                )
                self.conn.commit()
                messagebox.showinfo("Success", "Movie updated successfully!")
                update_window.destroy()
                self.show_movies()
            except Exception as e:
                messagebox.showerror("Error", f"Update failed: {e}")

        tk.Button(update_window, text="Save", font=('Helvetica', 12), command=save).pack(pady=10)

    def delete_movie(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Select Movie", "Please select a movie to delete.")
            return

        values = self.tree.item(selected, 'values')
        if not values:
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete movie ID {values[0]}?")
        if not confirm:
            return

        try:
            self.cur.execute("DELETE FROM movies WHERE movie_id=%s", (values[0],))
            self.conn.commit()
            messagebox.showinfo("Deleted", "Movie deleted successfully!")
            self.show_movies()
        except Exception as e:
            messagebox.showerror("Error", f"Delete failed: {e}")

    def search_movies(self):
        keyword = self.search_var.get()
        if not keyword.strip():
            messagebox.showwarning("Empty Search", "Please enter a search term.")
            return

        query = """
            SELECT * FROM movies
            WHERE title LIKE %s OR genre LIKE %s OR director LIKE %s
            OR release_year LIKE %s OR duration LIKE %s OR rating LIKE %s
        """
        like = f"%{keyword}%"
        self.cur.execute(query, (like,) * 6)
        rows = self.cur.fetchall()

        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert('', tk.END, values=row)

    def export_movies(self):
        rows = self.tree.get_children()
        if not rows:
            messagebox.showinfo("No Data", "No movies to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")],
                                                 title="Save as")
        if not file_path:
            return

        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Title", "Genre", "Director", "Year", "Duration", "Rating"])
                for row_id in rows:
                    row_data = self.tree.item(row_id, 'values')
                    writer.writerow(row_data)
            messagebox.showinfo("Success", f"Movies exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {e}")

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        LoginPage(root)
        root.mainloop()


# ---------------------------- Entry Point ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    LoginPage(root)
    root.mainloop()
