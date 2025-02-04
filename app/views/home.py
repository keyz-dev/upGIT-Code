import os, sys
from tkinter import *

class HomePage():
    def __init__(self, root, user_info, open_backup, open_recover):
        self.window = root
        self.user_info = user_info
        self.open_recover = open_recover
        self.open_backup = open_backup
        self.render()
        
    def render(self):
        self.window.title("upGIT Dashboard")
        homeLabel = Label(self.window, text=f"Choose an option", font=('Poppins', 14, 'bold'), bg="white")
        homeLabel.pack(padx=10, pady=10)
        
        custom_font=('Poppins', 10)
        backupBtn = Button(self.window, text="Back up", font=custom_font, cursor="hand2", command=self.open_backup_page)
        backupBtn.place(relx=0.2, rely=0.4)
        
        recoverBtn = Button(self.window, text="Recover", font=custom_font, cursor="hand2", command=self.open_recover_page)
        recoverBtn.place(relx=0.6, rely=0.4)
    
    def open_backup_page(self):
        self.open_backup(self.user_info)
    
    def open_recover_page(self):
        print(self.user_info)
        self.open_recover(self.user_info)