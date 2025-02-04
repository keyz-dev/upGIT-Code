import os, sys
from tkinter import *
from tkinter import filedialog, font
import tkinter.messagebox as messageBox
from PIL import Image, ImageTk
from app.auth.user import UserAuthentication

class Register():
    def __init__(self, root, on_login):
        self.window = root
        self.on_login = on_login
        self.render()
    
    def render(self):
        self.window.title("upGIT Registration")        
        # input frame
        FormFrame = Frame(self.window, bg="white", width="400", height="450")
        FormFrame.place(relx=0.5, rely=0.5, anchor=CENTER)
        customFont = font.Font(family="Poppins", size=11)
        
        loginLabel = Label(FormFrame, text="Create Account", font=('Poppins', 18, 'bold'), bg="white")
        loginLabel.place(relx=0.25, rely=0.05)
        # name entry
        self.nameEntry = Entry(FormFrame, width=45, font= customFont, bg="#fff", bd=0)
        self.nameEntry.place(relx=0.1, rely=0.2)
        self.nameEntry.insert(3, 'Enter username')
        self.nameFrame = Frame(FormFrame, width=320, height=1.5, bg="gray50")
        self.nameFrame.place(relx=0.09, rely=0.257)
        self.nameEntry.bind('<FocusIn>', lambda event: self.on_enter(event, self.nameEntry, "Enter username", self.nameFrame))
        self.nameEntry.bind('<FocusOut>', lambda event: self.on_leave(event, self.nameEntry, "Enter username", self.nameFrame))
        # email entry
        self.emailEntry = Entry(FormFrame, width=45, font= customFont, bg="#fff", bd=0)
        self.emailEntry.place(relx=0.1, rely=0.31)
        self.emailEntry.insert(3, 'Enter email')
        self.emailFrame = Frame(FormFrame, width=320, height=1.5, bg="gray50")
        self.emailFrame.place(relx=0.09, rely=0.367)
        self.emailEntry.bind('<FocusIn>', lambda event: self.on_enter(event, self.emailEntry, "Enter email", self.emailFrame))
        self.emailEntry.bind('<FocusOut>', lambda event: self.on_leave(event, self.emailEntry, "Enter email", self.emailFrame))
        # password entry
        self.passwordEntry = Entry(FormFrame, width=45, font= customFont, bg="#fff", bd=0)
        self.passwordEntry.place(relx=0.1, rely=0.42)
        self.passwordEntry.insert(3, 'Enter password')
        passwordFrame = Frame(FormFrame, width=320, height=1.5, bg="gray50")
        passwordFrame.place(relx=0.09, rely=0.477)
        self.passwordEntry.bind('<FocusIn>', lambda event: self.on_enter(event, self.passwordEntry, "Enter password", passwordFrame))
        self.passwordEntry.bind('<KeyPress>', self.on_keypress)
        self.passwordEntry.bind('<FocusOut>', lambda event: self.on_leave(event, self.passwordEntry, "Enter password", passwordFrame))
        # password confirmation entry
        self.cpasswordEntry = Entry(FormFrame, width=45, font= customFont, bg="#fff", bd=0)
        self.cpasswordEntry.place(relx=0.1, rely=0.53)
        self.cpasswordEntry.insert(3, 'Confirm Password')
        cpasswordFrame = Frame(FormFrame, width=320, height=1.5, bg="gray50")
        cpasswordFrame.place(relx=0.09, rely=0.607)
        self.cpasswordEntry.bind('<FocusIn>', lambda event: self.on_enter(event, self.cpasswordEntry, "Confirm Password", cpasswordFrame))
        self.cpasswordEntry.bind('<KeyPress>', self.on_keypress)
        self.cpasswordEntry.bind('<FocusOut>', lambda event: self.on_leave(event, self.cpasswordEntry, "Confirm Password", cpasswordFrame))
        
        eye_path = os.path.join(os.getcwd(), 'app', 'assets', 'eye.png')
        eye = Image.open(eye_path)
        eye = eye.resize((20, 16), Image.Resampling.LANCZOS)
        self.eye = ImageTk.PhotoImage(eye)
        
        passwordVisibilityBtn = Button(FormFrame, bd=0, bg="white", image=self.eye, command=lambda field=self.passwordEntry: self.togglePasswordVisibility(field), cursor="hand2")
        passwordVisibilityBtn.place(relx=0.82, rely=0.42)
        
        cpasswordVisibilityBtn = Button(FormFrame, bd=0, bg="white", image=self.eye, command=lambda field=self.cpasswordEntry: self.togglePasswordVisibility(field), cursor="hand2")
        cpasswordVisibilityBtn.place(relx=0.82, rely=0.53)
        
        registerBtn = Button(FormFrame, bg="purple1", height=1, width=31, font=('Poppins', 12, 'bold'), fg="white", text="Create", bd=0, command = self.checkValues, cursor="hand2")
        registerBtn.place(relx=0.09, rely=0.65)
        
        # login link label
        loginLabel = Label(FormFrame, text="Already have an account?", font=('Poppins', 10), bg="white")
        loginLabel.place(relx=0.09, rely=0.8)
        
        # login link button
        loginBtn = Button(FormFrame, text="Login", font=('Poppins', 10), bg="white", fg="purple1", bd=0, cursor="hand2", command=self.on_login)
        loginBtn.place(relx=0.53, rely=0.79)
        
    def on_enter(self, event, field, value, frame=None):
        if field.get() == value:   
            field.delete(0, END)
            if field == self.passwordEntry:
                field.config(show="")
            field.unbind('<FocusIn>')
            if frame:
                frame.config(bg="purple1") 
    
    def on_leave(self, event, field, value, frame=None):
        if field.get() == '':   
            field.insert(0, value)
            field.bind('<FocusIn>', lambda event: self.on_enter(event, field, value, frame))        
            if field == self.passwordEntry and field.get() not in ['', 'Enter password']:
                field.config(show="*")
            if frame:
                frame.config(bg="gray50")

    def on_keypress(self, event):
        self.passwordEntry.config(show="*")
        self.cpasswordEntry.config(show="*")
    
    def checkValues(self):
        if self.nameEntry.get() in ["", 'Enter username']:
            messageBox.showerror('username error', "username entry required")
            return
        if self.emailEntry.get() in ["", 'Enter email']:
            messageBox.showerror('email error', "email entry required")
            return
        if self.passwordEntry.get() in ["", 'Enter password']:
            messageBox.showerror('password error', "password entry required")
            return
        if self.cpasswordEntry.get() in ["", 'Confirm Password']:
            messageBox.showerror('confirm password error', "confirm entry required")
            return
        if self.cpasswordEntry.get() != self.passwordEntry.get():
            messageBox.showerror('password error', "passwords do not match")
            return
        
        user_object = {
            "name": self.nameEntry.get(),
            "email": self.emailEntry.get(),
            "password": self.passwordEntry.get(),
            "confirm_password": self.cpasswordEntry.get()
        }
        user_auth = UserAuthentication()
        status, value = user_auth.handle_acc_creation(user_object)
        if status:
            messageBox.showinfo('success', "Registration successful")
            self.on_login()
        # Verify credentials
        else:
            messageBox.showerror('registration error', value)
            return
    def togglePasswordVisibility(self, field):
        if field.cget("show") == "*":
            field.config(show="")
        else:
            field.config(show="*")
            
    # centralize the root window

    