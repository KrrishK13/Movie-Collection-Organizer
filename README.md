# 🎬 Movie Collection Organiser

A Python-based desktop application to manage your personal movie collection using a graphical interface built with **Tkinter**, and data storage handled through **MySQL**. This project allows users to add, update, delete, search, and export movie records. It also includes a login system and a clean, image-enhanced user interface.

---

## ✅ Features

- 🔐 **Login System** with username and password validation
- 📝 **Add, Update, and Delete** movie records
- 🔍 **Search** movies by title, genre, director, etc.
- 📂 **Export** movie list to `.csv`
- 📊 **Display** data in a TreeView table with scrollbar
- 🎨 Visually styled UI with **Tkinter** and background images

---

## 🗓️ Daily Upload Progress

- ✅ Day 1: Initialized repository and added README
- ✅ Day 2: Added login screen with background image and validation
- ✅ Day 3: Added main dashboard layout with menu buttons and TreeView
- ✅ Day 4: Added Add Movie form and integrated database insert functionality
- ✅ Day 5: Added Update and Delete movie functionality

---

## 🧰 Tech Stack

| Technology | Purpose                            |
|------------|-------------------------------------|
| Python 3   | Programming Language                |
| Tkinter    | GUI Framework                       |
| MySQL      | Database backend                    |
| mysql-connector-python | MySQL connection from Python |
| Pillow     | Display background images in Tkinter |
| csv module | Export data to `.csv` format        |

---

## 🔐 Default Login Credentials

| Username | Password   |
|----------|------------|
| mahesh   | mahesh123  |

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/KrrishK13/movie-collection-organizer.git
cd movie-collection-organizer
```

### 2. Install Dependencies
```bash
pip install mysql-connector-python Pillow
```

### 3. Set up MySQL database

Start your MySQL server.
Open your MySQL command line or a GUI tool (like MySQL Workbench) and execute the commands to create the database and tables.

### 4.  Configure Database Connection

Open the file `config.py` (or the Python script where the database connection is set).
Update the database credentials to match your MySQL setup.

```python3
db_config = {
    'host': 'localhost',
    'user': 'your_mysql_username',
    'password': 'your_mysql_password',
    'database': 'movie_collection_organiser'
}
```

### 5.  Run the Application

In the terminal or command prompt (inside the project folder), run:
```bash
python main.py
```  
