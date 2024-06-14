from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox, filedialog
import os
import pywhatkit as kit
from tkinter import messagebox
import webbrowser
import sqlite3
import time

class payment:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1206x525+160+183")
        self.root.focus_force()
        self.root.config(bg="#EEEEEE")
        self.root.overrideredirect(True)

        self.name = StringVar()
        self.contact = StringVar()
        self.invoice = StringVar()
        self.amount = StringVar()
        self.date = StringVar()
        self.pdf_path = StringVar()
        self.billsearchvar = StringVar()

        blanktop=Label(self.root,text="",bg="#30336b").place(x=20,y=8,width=1160,height=2)


        notify = Label(self.root, text="P A Y M E N T         N O T I F I C A T I O N S", font=("arial", 18), bg="#EEEEEE", fg="#130f40")
        notify.place(x=20, y=10, width=1155, height=35)

        blank=Label(self.root,text="",bg="#30336b").place(x=20,y=45,width=1160,height=2)

        name_label = Label(self.root, text="Name ", font=("goudy old style", 14), bg="#EEEEEE", fg="#2C3A47").place(x=130, y=100)
        name_text = Entry(self.root, textvariable=self.name, border=0, highlightbackground="#2C3A47", highlightthickness=1,state="readonly").place(x=250, y=105)

        contact_label = Label(self.root, text="Contact ", font=("goudy old style", 14), bg="#EEEEEE", fg="#2C3A47").place(x=130, y=150)
        contact_text = Entry(self.root, textvariable=self.contact, border=0, highlightbackground="#2C3A47", highlightthickness=1).place(x=250, y=155)

        invoice_label = Label(self.root, text="Invoice ", font=("goudy old style", 14), bg="#EEEEEE", fg="#2C3A47").place(x=130, y=200)
        invoice_text = Entry(self.root, textvariable=self.invoice, border=0, highlightbackground="#2C3A47", highlightthickness=1,state="readonly").place(x=250, y=205)

        amount_label = Label(self.root, text="Amount", font=("goudy old style", 14), bg="#EEEEEE", fg="#2C3A47").place(x=130, y=250)
        amount_text = Entry(self.root, textvariable=self.amount, border=0, highlightbackground="#2C3A47", highlightthickness=1,state="readonly").place(x=250, y=255)

        date_label = Label(self.root, text="Date", font=("goudy old style", 14), bg="#EEEEEE", fg="#2C3A47").place(x=130, y=300)
        date_text = Entry(self.root, textvariable=self.date, border=0, highlightbackground="#2C3A47", highlightthickness=1,state="readonly").place(x=250, y=305)

        clear_btn = Button(self.root, text="Clear", font=("arial", 14), fg="white", bg="#4834d4", border=1, command=self.clearbillfield,cursor="hand2").place(x=190, y=360, width=120, height=30)

###################################################################################

# Search frame for bills
        billframe = LabelFrame(self.root, bg="#CAD3C8", text="Search Bills", font=("calibri", 14))
        billframe.place(x=620, y=60, width=580, height=60)
        text_search = Entry(billframe, textvariable=self.billsearchvar).place(x=10, y=0, width=350, height=20)

        search_btn = Button(billframe, text="Search", font=("arial", 12, "bold"), fg="white", bg="#304FFE", border=0, command=self.search_bills,cursor="hand2").place(x=380, y=0, width=85, height=20)

        clear_btn = Button(billframe, text="Clear", font=("arial", 12, "bold"), fg="white", bg="#D50000", border=0, command=self.clearbillframe,cursor="hand2").place(x=480, y=0, width=85, height=20)



        # Frame for bill display
        disp1 = Frame(self.root, bd=2)
        disp1.place(x=620, y=125, height=400, width=580)

        x1scroll = Scrollbar(disp1, orient=HORIZONTAL)
        x1scroll.pack(side=BOTTOM, fill=X)
        y1scroll = Scrollbar(disp1, orient=VERTICAL)
        y1scroll.pack(side=RIGHT, fill=Y)

        self.billtable = ttk.Treeview(disp1, columns=("invoice", "date", "customer", "contact", "amount"), xscrollcommand=x1scroll.set, yscrollcommand=y1scroll.set)
        x1scroll.config(command=self.billtable.xview)
        y1scroll.config(command=self.billtable.yview)

        self.billtable.heading("invoice", text="INVOICE ID")
        self.billtable.heading("date", text="DATE")
        self.billtable.heading("customer", text="CUSTOMER NAME")
        self.billtable.heading("contact", text="CONTACT NUMBER")
        self.billtable.heading("amount", text="AMOUNT")
        self.billtable["show"] = "headings"
        self.billtable.pack(fill=BOTH, expand=1)
        self.billtable.bind("<ButtonRelease-1>",self.get_bill)

        self.billtable.column("invoice", width=50)
        self.billtable.column("date", width=40)
        self.billtable.column("customer", width=100)
        self.billtable.column("contact", width=80)
        self.billtable.column("amount", width=40)



        # Buttons for notifications
        whatsapp_label = Label(self.root, text="Click here to notify via Whatsapp  : ", font=("goudy old style", 14), bg="#EEEEEE", fg="#2C3A47").place(x=80, y=450)
        self.wpbtn = Image.open("notify_whatsapp.png")
        self.wpbtn = self.wpbtn.resize((50, 50), Image.LANCZOS)
        self.wpbtn = ImageTk.PhotoImage(self.wpbtn)
        wp_button = Button(self.root, image=self.wpbtn, border=0, cursor="hand2", command=self.notify_whatsapp).place(x=380, y=435)



  
    def search_bills(self):
        con = sqlite3.connect(database="data.db")
        cur = con.cursor()
        try:
            search_string = self.billsearchvar.get()
            searchquery ="SELECT * FROM bill WHERE invoice LIKE ?  OR amount LIKE ? OR customer LIKE ?"

            cur.execute(searchquery, ('%' + search_string + '%', '%' + search_string + '%', '%' + search_string + '%'))
            rows = cur.fetchall()
            self.billtable.delete(*self.billtable.get_children())
            for row in rows:
                self.billtable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clearbillframe(self):
        self.billsearchvar.set("")
        self.billtable.delete(*self.billtable.get_children())

    def clearbillfield(self):
        self.name.set("")
        self.contact.set("")
        self.invoice.set("")
        self.amount.set("")
        self.date.set("")

    def get_bill(self,ev):
        select=self.billtable.focus()
        content=(self.billtable.item(select))
        row=content['values']
        self.name.set(row[2]),
        self.contact.set("+91" + str(row[3])),
        self.invoice.set(row[0]),
        self.amount.set(row[4]),
        self.date.set(row[1]),


    def notify_whatsapp(self):
        recipient_phone_number = self.contact.get()
        pdf_path = self.pdf_path.get()

        if not recipient_phone_number :
            messagebox.showerror("Error", "Please provide contact number ")
            return

        try:
            message_bill = f"Dear {self.name.get()}, please find the attached invoice for your pending bill of Amount {self.amount.get()}. Kindly make the payment at your earliest convenience. \n Regards, BALAJI HARDWARE AND ELECTRICALS"

            # Open WhatsApp Web and start a chat with the recipient
            kit.sendwhatmsg_instantly(recipient_phone_number, message_bill, wait_time=20, tab_close=False)

            # Wait a few seconds for the WhatsApp Web to load
            time.sleep(20)


        except Exception as e:
            messagebox.showerror("Error", f"Failed to send WhatsApp notification. Error: {str(e)}")





if __name__ == "__main__":
    root = Tk()
    obj = payment(root)
    root.mainloop()
