import os, sys
from tkinter import *
from tkinter import filedialog, font
import tkinter.messagebox as messageBox
from PIL import Image, ImageTk
from app.auth.user import UserAuthentication

class Login():
    def __init__(self, root, on_register, open_home):
        self.window = root
        self.on_register = on_register
        self.open_home = open_home
        self.render()
    
    def render(self):
        self.window.title("upGIT Login")
        # input frames
        FormFrame = Frame(self.window, bg="white", width="400", height="450")
        FormFrame.place(relx=0.5, rely=0.5, anchor=CENTER)
        customFont = font.Font(family="Poppins", size=11)
        
        loginLabel = Label(FormFrame, text="Login", font=('Poppins', 18, 'bold'), bg="white")
        loginLabel.place(relx=0.4, rely=0.15)
        # email entry and frame
        self.emailEntry = Entry(FormFrame, width=45, font= customFont, bg="#fff", bd=0)
        self.emailEntry.place(relx=0.1, rely=0.3)
        self.emailEntry.insert(3, 'Enter email')
        self.emailFrame = Frame(FormFrame, width=320, height=1.5, bg="gray50")
        self.emailFrame.place(relx=0.09, rely=0.357)
        self.emailEntry.bind('<FocusIn>', lambda event: self.on_enter(event, self.emailEntry, "Enter email", self.emailFrame))
        self.emailEntry.bind('<FocusOut>', lambda event: self.on_leave(event, self.emailEntry, "Enter email", self.emailFrame))

        # password entry and frame
        self.passwordEntry = Entry(FormFrame, width=45, font= customFont, bg="#fff", bd=0)
        self.passwordEntry.place(relx=0.1, rely=0.41)
        self.passwordEntry.insert(3, 'Enter password')
        passwordFrame = Frame(FormFrame, width=320, height=1.5, bg="gray50")
        passwordFrame.place(relx=0.09, rely=0.467)
        self.passwordEntry.bind('<FocusIn>', lambda event: self.on_enter(event, self.passwordEntry, "Enter password", passwordFrame))
        self.passwordEntry.bind('<KeyPress>', self.on_keypress)
        self.passwordEntry.bind('<FocusOut>', lambda event: self.on_leave(event, self.passwordEntry, "Enter password", passwordFrame))
        
        eye_path = os.path.join(os.getcwd(), 'app', 'assets', 'eye.png')
        eye = Image.open(eye_path)
        eye = eye.resize((21, 16), Image.Resampling.LANCZOS)
        self.eye = ImageTk.PhotoImage(eye)
        
        passwordVisibilityBtn = Button(FormFrame, bd=0, bg="white", image=self.eye, command=self.togglePasswordVisibility, cursor="hand2")
        passwordVisibilityBtn.place(relx=0.82, rely=0.42)
        
        loginBtn = Button(FormFrame, bg="purple1", height=1, width=31, font=('Poppins', 12, 'bold'), fg="white", text="Login", bd=0, command = self.checkValues, cursor="hand2")
        loginBtn.place(relx=0.09, rely=0.55)
        
        # register label
        registerLabel = Label(FormFrame, text="Don't have an account?", font=('Poppins', 10), bg="white")
        registerLabel.place(relx=0.09, rely=0.68)
        
        # register button
        registerBtn = Button(FormFrame, text="Register", font=('Poppins', 10), bg="white", fg="purple1", bd=0, cursor="hand2", command=self.on_register)
        registerBtn.place(relx=0.475, rely=0.673)
        pass
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
    
    def checkValues(self):
        if self.emailEntry.get() in ["", 'Enter email']:
            messageBox.showerror('email error', "email entry required")
            return
        elif self.passwordEntry.get() in ["", 'Enter password']:
            messageBox.showerror('password error', "password entry required")
            return
        # Verify credentials
        user_object = {
            'email': self.emailEntry.get(),
            'password': self.passwordEntry.get()
        }
        user_auth = UserAuthentication()
        status, value = user_auth.login(user_object)
        if not status:
            messageBox.showerror('login error', value)
            return
        else:
            messageBox.showinfo('success', "Login Successful")
            self.user_info = value
            # open home
            self.open_home(value)

    def togglePasswordVisibility(self):
        if self.passwordEntry.cget("show") == "*":
            self.passwordEntry.config(show="")
        else:
            self.passwordEntry.config(show="*")
            
    # centralize the root window

    