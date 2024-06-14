from tkinter import*
from PIL import Image, ImageTk
from tkinter import messagebox
from adddata import add_data
from viewdata import view_data
from update import update_data
from payment import payment
from billing_window import bill
from billupdate import update_bill

class mgmt:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1366x768+0+0")
        self.root.title("EZYtrack v1.0")
        self.root.state('zoomed')
        self.add_window = None
        self.view_window = None
        self.update_window = None
        self.dues_window = None
        self.bill_window = None
        self.billupdate_window = None


#logo
        self.logo = Image.open("logo.png") 
        self.logo = self.logo.resize((160, 160), Image.LANCZOS)  
        self.logo = ImageTk.PhotoImage(self.logo)
        icon = Label(self.root, image=self.logo, border=0,bg="#60a3bc").place(x=0, y=0)
        
#topinfo
        title=Label(self.root,text="Ezytrack   Management   System",font=("copperplate gothic bold",40),bg="#60a3bc",fg="#FFFFFF",anchor="w",padx=80).place(x=160,y=0,width=1366,height=80)

        shop_name=Label(self.root,text="",font=("copperplate gothic bold",25),bg="#60a3bc",fg="#FFFFFF",anchor="w",padx=250).place(x=160,y=80,width=1366,height=80)

        # Create sidebar frame
        menu=Frame(self.root,bg="#82ccdd")
        menu.place(x=0, y=160, width=160 ,height=646)
        #create side buttons

        #add new
        self.add_icon = Image.open("add.png") 
        self.add_icon = self.add_icon.resize((160, 50), Image.LANCZOS)  
        self.add_icon = ImageTk.PhotoImage(self.add_icon)
        add_button=Button(self.root, image=self.add_icon,border=0,cursor="hand2",command=self.add_data).place(x=0, y=160)
       

        #view
        self.view_icon = Image.open("view.png")  
        self.view_icon = self.view_icon.resize((160, 50), Image.LANCZOS) 
        self.view_icon = ImageTk.PhotoImage(self.view_icon)
        view_button = Button(self.root, image=self.view_icon, border=0, cursor="hand2",command=self.view_data).place(x=0, y=210)
        #modify
        self.modify_icon = Image.open("modify.png")  
        self.modify_icon = self.modify_icon.resize((160, 50), Image.LANCZOS) 
        self.modify_icon = ImageTk.PhotoImage(self.modify_icon)
        update_button = Button(self.root, image=self.modify_icon, border=0, cursor="hand2",command=self.update_data).place(x=0, y=260)
        #update_bill
        self.bill_update_icon = Image.open("update_bill.png")  
        self.bill_update_icon = self.bill_update_icon.resize((160, 50), Image.LANCZOS) 
        self.bill_update_icon = ImageTk.PhotoImage(self.bill_update_icon)
        update_button = Button(self.root, image=self.bill_update_icon, border=0, cursor="hand2",command=self.billupdatewindow).place(x=0, y=310)
        #dues
        self.dues_icon = Image.open("dues.png")  
        self.dues_icon = self.dues_icon.resize((160, 50), Image.LANCZOS)  # Resize the image
        self.dues_icon = ImageTk.PhotoImage(self.dues_icon)
        dues_button = Button(self.root, image=self.dues_icon, border=0, cursor="hand2",command=self.view_payment).place(x=0, y=410)
        #bill
        self.bill_icon = Image.open("bill.png") 
        self.bill_icon = self.bill_icon.resize((160, 50), Image.LANCZOS) 
        self.bill_icon = ImageTk.PhotoImage(self.bill_icon)
        bill_button = Button(self.root, image=self.bill_icon,border=0,cursor="hand2",command=self.billing).place(x=0, y=360)        
      
        #exit
        self.exit_icon = Image.open("exit.png")  
        self.exit_icon = self.exit_icon.resize((160, 50), Image.LANCZOS) 
        self.exit_icon = ImageTk.PhotoImage(self.exit_icon)
        exit_button = Button(self.root, image=self.exit_icon, border=0, cursor="hand2",command=self.exit_cmd).place(x=0, y=585)
        #help
        self.help_icon = Image.open("help.png")  
        self.help_icon = self.help_icon.resize((160, 50), Image.LANCZOS) 
        self.help_icon = ImageTk.PhotoImage(self.help_icon)
        help_button = Button(self.root, image=self.help_icon, border=0, cursor="hand2",command=self.help_cmd).place(x=0, y=635)
       
       
        #footer
        footer=Label(self.root,text="Eztrack v1.0 | Developed by Amit Kumar Pandit",font=("arial",10),bg="#079992",fg="#FFFFFF",anchor="center").place(x=0,y=685,width=1366,height=20)
        #greeting
        self.greeting_image = Image.open("greeting.png")  # Replace "logout.png" with your logout button image
        self.greeting_image = self.greeting_image.resize((650, 500), Image.LANCZOS)  # Resize the image
        self.greeting_image = ImageTk.PhotoImage(self.greeting_image)
        greeting=Label(self.root,image=self.greeting_image).place(x=420,y=180)

    def add_data(self):

        if self.add_window is None or not self.add_window.winfo_exists():
            self.add_window = Toplevel(self.root)
            self.add_data_object = add_data(self.add_window)
        else:
            # Bring the existing window to the front
            self.add_window.lift()
    def view_data(self):
        if self.view_window is None or not self.view_window.winfo_exists():
            self.view_window = Toplevel(self.root)
            self.view_data_object = view_data(self.view_window)
        else:
            # Bring the existing window to the front
            self.view_window.lift()

    def update_data(self):
        if self.update_window is None or not self.update_window.winfo_exists():
            self.update_window = Toplevel(self.root)
            self.update_data_object = update_data(self.update_window)
        else:
            # Bring the existing window to the front
            self.update_window.lift()



    def view_payment(self):
        if self.dues_window is None or not self.dues_window.winfo_exists():
            self.dues_window = Toplevel(self.root)
            self.view_payment_object = payment(self.dues_window)
        else:
            # Bring the existing window to the front
            self.dues_window.lift()

    def billing(self):
        if self.bill_window is None or not self.bill_window.winfo_exists():
            self.bill_window = Toplevel(self.root)
            self.bill_window_object = bill(self.bill_window)
        else:
            # Bring the existing window to the front
            self.bill_window.lift()

    def billupdatewindow(self):
        if self.billupdate_window is None or not self.billupdate_window.winfo_exists():
            self.billupdate_window = Toplevel(self.root)
            self.billupdate_window_object = update_bill(self.billupdate_window)
        else:
            # Bring the existing window to the front
            self.billupdate_window.lift()
    
    def help_cmd(self):
        message = ("For help regarding functionalities, refer to the manual.\n\n"
               "For help regarding other issues, contact the developer.\n\n"
               "THANK YOU FOR USING EZYTRACK")
        messagebox.showinfo("Help", message) 
    def exit_cmd(self):
        # Display confirmation dialog
        response = messagebox.askyesno("Exit", "Are you sure you want to exit?")

        if response:
            self.root.destroy() 


class Login:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1366x768+0+0")
        self.root.title("Login")
        self.root.state('zoomed')

        self.username = StringVar()
        self.password = StringVar()


        self.login_image = Image.open("login.png") 
        self.login_image = self.login_image.resize((1366, 768), Image.LANCZOS)  
        self.login_image = ImageTk.PhotoImage(self.login_image)
        icon = Label(self.root, image=self.login_image, border=0).place(x=0, y=0)
        
        Label(self.root, text="Username : ", font=("goudy old style", 18),bg="white").place(x=750, y=300)
        self.username_entry = Entry(self.root, textvariable=self.username, font=("arial", 14),border=2)
        self.username_entry.place(x=900, y=300,height=30)

        Label(self.root, text="Password:", font=("goudy old style", 18),bg="white").place(x=750, y=360)
        self.password_entry = Entry(self.root, textvariable=self.password, font=("arial", 14), show="*",border=2)
        self.password_entry.place(x=900, y=360)

        login_button = Button(self.root, text="Login", font=("arial", 14), command=self.login)
        login_button.place(x=850, y=420,width=200)

    def login(self):
        valid_username = "admin"
        valid_password = "password"

        if self.username.get() == valid_username and self.password.get() == valid_password:
            messagebox.showinfo("Login", "Login Successful!")
            self.root.destroy()
            main_app()
        else:
            messagebox.showerror("Login", "Invalid Credentials")

def main_app():
    root = Tk()
    obj = mgmt(root)
    root.mainloop()

if __name__ == "__main__":
    root = Tk()
    login = Login(root)
    root.mainloop()
