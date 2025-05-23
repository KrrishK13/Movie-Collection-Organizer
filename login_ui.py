import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

class LoginPage:
    def __init__(self, root):   
        self.root = root
        self.root.geometry('1350x700')
        self.root.title("Login - Movie Collection Organizer")
        self.root.resizable(False, False)
        self.setup_login_ui()

    def setup_login_ui(self):
        # Path to background image
        bg_image_path = 'images/login_3.jpg'  

        if not os.path.isfile(bg_image_path):
            messagebox.showerror('Error', 'Background image file not found!')
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
            messagebox.showinfo('Success', f'Welcome {username}')
        else:
            messagebox.showerror('Error', 'Invalid credentials')

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginPage(root)
    root.mainloop()
