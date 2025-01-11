import os, sys
from tkinter import *
from tkinter import filedialog, font
import tkinter.messagebox as messageBox
from PIL import Image, ImageTk
import importlib
from app.controllers import (branch as branch_controller, remote_repo as remote_repo_controller)
import re
from app.services.initial_backup import new_backup

class BackupPage():
    def __init__(self, root, user_info, open_home):
        self.window = root
        self.user_info = user_info
        self.open_home = open_home
        self.branches = self.get_branches()
        self.render()
    
    def reload_ui(self):
        importlib.reload(sys.modules['app.views.home'])
        for widget in self.window.winfo_children():
            widget.destroy()
        self.render()
    
    def get_branches(self):
        # get the remote information of the current user
        self.remote = remote_repo_controller.get_specific(column="user_id", value=self.user_info.id, limit=1)
        if self.remote in [None, False, '', []]:
            messageBox.showerror("Fetch Error", "No remote repository found")
            self.window.quit
        branches = branch_controller.get_specific(column="remote_repo", value=self.remote.id)
        if branches in [None, False, '', []]:
            return []
        return [value.name for value in branches]
        
    def render(self):
        self.window.title("upGIT Backup")
        homeLabel = Label(self.window, text=f"Backup", font=('Poppins', 14, 'bold'), bg="white")
        homeLabel.pack(padx=20, pady=10)
        
        custom_font=('Poppins', 10)
        
        self.folder_path = StringVar()
        Label(self.window, text="Select Folder to Backup", bg="white", font=custom_font).pack(anchor=W, padx=20, pady=5)
        folder_frame = Frame(self.window, bg="white")
        folder_frame.pack(fill=X, padx=20)
        Entry(folder_frame, textvariable=self.folder_path, width=45, highlightthickness=2, highlightcolor="gray70", bg="white", font=custom_font).pack(side=LEFT, padx=5)
        Button(folder_frame, text="Browse", command=self.browse_folder, cursor="hand2", font=custom_font).pack(side=RIGHT)

        # Backup Frequency Section
        self.frequency_var = StringVar(value="Hours")
        Label(self.window, text="Set Backup Frequency", bg="white", font=custom_font).pack(anchor=W, padx=20, pady=5)
        self.frequencyEntry = Entry(self.window, width=15, highlightthickness=2, highlightcolor="gray70", bg="white")
        self.frequencyEntry.pack(anchor=W, padx=20, pady=5)
        frequency_options = ["Hours", "Days", "Minutes"]
        backupOptions = OptionMenu(self.window, self.frequency_var, *frequency_options)
        backupOptions.config(font=custom_font)
        backupOptions.place(relx=0.33, rely=0.45)

        # Branch Selection Section
        self.branch_var = StringVar(value="None")
        Label(self.window, text="Choose a Branch", bg="white", font=custom_font).pack(anchor=W, padx=20, pady=5)
        branch_options = self.branches if len(self.branches) > 0 else ['None']
        option_menu = OptionMenu(self.window, self.branch_var, *branch_options)
        option_menu.config(width=15, font=custom_font)
        option_menu.pack(anchor=W, padx=20, pady=5)
        Button(self.window, font=custom_font, text="New", bg="RoyalBlue1", bd=0, fg="white", command=self.open_create_branch, width=10, anchor=CENTER, cursor="hand2").place(relx=0.4, rely=0.66)

        # Action Buttons
        Button(self.window, text="Start Backup", font=custom_font, command=self.start_backup, bg="#4CAF50", fg="white", bd=0, width=16, cursor="hand2").pack(anchor=W, padx=20, pady=30)
        Button(self.window, text="Cancel", font=custom_font, command= lambda user_info=self.user_info: self.open_home(user_info), bg="#f44336", fg="white", bd=0, width=16, cursor="hand2").place(relx=0.7, rely=0.84)
        
        self.window.bind('<Control-r>', lambda event: self.reload_ui)

    def open_create_branch(self):
        self.dialog = Toplevel(self.window)
        self.dialog.title("Create New Branch")
        self.dialog.resizable(False, False)
        
        self.dialog.transient(self.window)
        self.dialog.grab_set()

        # Place the dialog at the center of the parent
        par_x = self.window.winfo_rootx()
        par_y = self.window.winfo_rooty()
        x = par_x + 130
        y = par_y + 130
        self.dialog.geometry(f"250x150+{x}+{y}")
        self.dialog.configure(bg="white")
        
        Label(self.dialog, text="Enter Branch Name", bg="white", font=('Poppins', 10)).pack(pady=5)
        self.branch_name = Entry(self.dialog, width=30, highlightthickness=2, highlightcolor="gray70", bg="white", font=('Poppins', 10))
        self.branch_name.pack(pady=5)
        Button(self.dialog, text="Create Branch", font=('Poppins', 10), bg="RoyalBlue1", fg="white", command=self.create_branch).pack(pady=5)
        self.dialog.bind('<Escape>', lambda event: self.dialog.destroy())  
    
    def create_branch(self):
        if self.branch_name not in ['', 'None', None]:
            self.branch_var.set(self.branch_name.get())
        else:
            messageBox.showerror("Error", "Please enter a valid branch name")
        self.dialog.destroy()
    def browse_folder(self):
        self.folder_path.set(filedialog.askdirectory())

    def start_backup(self):
        if self.folder_path.get() in [None, False, '', []]:
            messageBox.showerror("Error", "Please select a folder to backup")
            return
        if self.frequencyEntry.get() == '':
            messageBox.showerror("Error", "Please set backup frequency")
            return
        if not re.match(r'^[1-9][0-9]*', self.frequencyEntry.get()):
            messageBox.showerror("Error", "Frequency value must be a valid number")
            return  
        if self.branch_var.get() == 'None':
            messageBox.showerror("Error", "Please select a branch to backup")
            return
        freq_option = self.frequency_var.get()[0]
        print(freq_option)
        backup_object = {
            'path': self.folder_path.get(),
            'branch_name': self.branch_var.get(),
            'backup_frequency': self.frequencyEntry.get() + freq_option,
        }
        backup_status = new_backup(user = self.user_info, backup_object=backup_object, repo=self.remote)
        if backup_status:
            messageBox.showinfo("Success", "Backup process initiated successfully")
        else:
            messageBox.showerror("Error", "Backup process failed")