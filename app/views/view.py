from app.views.home import HomePage
from app.views.backup import BackupPage
from app.views.recover import RecoverPage
from app.views.auth.register import Register
from app.views.auth.login import Login
from tkinter import *
from PIL import Image, ImageTk
import os
from app.controllers import user as user_controller

class MainApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("upGIT")
        self.root.resizable(False, False)
        icon_path = os.path.join(os.getcwd(), 'app', 'assets', 'icon.png')
        icon = Image.open(icon_path)
        icon = ImageTk.PhotoImage(icon)
        self.root.iconphoto(True, icon)
        self.root.configure(bg="#fff")
        
        # Check if the user has an account
        user_info = self.get_user()
        if not user_info:
            self.open_login()
        else:
            self.open_home(user_info)

        self.root.mainloop()

    def get_user(self):
        dir_path = os.path.dirname(__file__)
        id_path = os.path.join(
            dir_path, '..', 'auth', 'user_id.txt'
        )
        try:
            """Get the user information if an account exists already"""
            with open(id_path, 'r') as fb:
                id = fb.read()
                
            return user_controller.get(id)
        except Exception as e:
            return False
            
    def set_dimensions(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = width
        window_height = height
        # dimension calculation
        x = (screen_width/2) - (window_width/2)
        y = (screen_height/2) - (window_height/2)
        self.root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')
        
    def open_login(self):
        self.clear_frame()
        self.set_dimensions(width=450, height=420)
        Login(self.root, self.open_register, self.open_home)

    def open_register(self):
        self.clear_frame()
        self.set_dimensions(width=450, height=470)
        Register(self.root, self.open_login)
    
    def open_home(self, user_info=None):
        self.clear_frame()
        self.set_dimensions(width=300, height=200)
        HomePage(self.root, user_info, self.open_backup, self.open_recover)
    
    def open_backup(self, user_info=None):
        self.clear_frame()
        self.set_dimensions(width=500, height=400)
        BackupPage(self.root, user_info, self.open_home)
    
    def open_recover(self, user_info=None):
        self.clear_frame()
        self.set_dimensions(width=380, height=300)
        RecoverPage(self.root, user_info, self.open_home)
    
    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
