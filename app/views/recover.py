import os, sys
import tkinter as tk
from tkinter import *
import tkinter.messagebox as messageBox
import importlib
from app.controllers import (
    branch as branch_controller, 
    remote_repo as remote_repo_controller, 
    local_repo as local_repo_controller
)
from app.services.pull import pull


class RecoverPage():
    def __init__(self, root, user_info, open_home):
        self.window = root
        self.user_info = user_info
        self.open_home = open_home
        self.local_repo_names = self.get_repos()
        
        self.render()
    
    def reload_ui(self):
        importlib.reload(sys.modules['app.views.home'])
        for widget in self.window.winfo_children():
            widget.destroy()
        self.render()
    
    def get_repos(self):
        self.local_repos = local_repo_controller.get_specific(column="user_id", value=self.user_info.id)
        if self.local_repos in [None, False, '', []]:
            messageBox.showerror("Fetch Error", "No Local repositories found to recover from")
            self.open_home(self.user_info)
        return [value.name for value in self.local_repos]
        
    def render(self):
        self.window.title("upGIT Recovery")
        homeLabel = Label(self.window, text=f"Recover", font=('Poppins', 14, 'bold'), bg="white")
        homeLabel.pack(padx=20, pady=10)
        custom_font=('Poppins', 10)
        
        def update_width(*args):
            """Adjust the OptionMenu width dynamically based on the longest item."""
            longest_item = max(folder_options, key=len)  # Find the longest string in options
            folder_options_menu.config(width=len(longest_item))
        
        # Folder Selection Section
        self.folder_var = StringVar(value="None")
        self.folder_var.trace_add("write", update_width)
        Label(self.window, text="Select Folder", bg="white", font=custom_font).pack(padx=20, pady=10)
        folder_options = self.local_repo_names if len(self.local_repo_names) > 0 else ['None']
        folder_options_menu = OptionMenu(self.window, self.folder_var, *folder_options)
        folder_options_menu.config(font=custom_font)
        folder_options_menu.pack(padx=20, pady=10)

        self.result_label = Label(self.window, text="", font=custom_font, bg="white")
        self.result_label.pack(padx=10, pady=10)
        
        # Action Buttons
        Button(self.window, text="Recover", font=custom_font, command=self.start_recover, bg="#4CAF50", fg="white", bd=0, width=16, cursor="hand2").place(relx=0.028, rely=0.8)
        Button(self.window, text="Cancel", font=custom_font, command= lambda user_info=self.user_info:self.open_home(user_info), bg="#f44336", fg="white", bd=0, width=16, cursor="hand2").place(relx=0.7, rely=0.8)
        
        self.window.bind('<Control-r>', lambda event: self.reload_ui())    

    def start_recover(self):
        self.result_label.configure(text="Recovering your data..., Please wait.")
        self.window.update_idletasks()
    
        folder_name = self.folder_var.get()
        for folder in self.local_repos:
            if folder.name == folder_name:
                folder_id = folder.id
                branch_id = folder.branch_id
        
        branch = branch_controller.get(branch_id)
        branch_name = branch.name
        remote = remote_repo_controller.get_specific(column='user_id', value=self.user_info.id, limit=1)
        if remote in [None, False, '', []]:
            messageBox.showerror("Fetch Error", "No remote repository found")
            self.window.quit
        
        remote_url = remote.clone_url
        pull_status = pull(remote_url=remote_url, local_dir=folder_name, branch_name=branch.name)
        
        if pull_status:
            # messageBox.showinfo("Recover Successful", "Recovery completed successfully!")
            self.result_label.configure(text="Data Recovery Successful!", fg="green")
        else:
            messageBox.showerror("Recover Failed", "Failed to recover repository. Please try again.")
            self.result_label.configure(text="Recovery Failed!", fg="red")
        
        
        