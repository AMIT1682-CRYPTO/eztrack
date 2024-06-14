from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
class update_bill:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1206x525+160+183")
        self.root.focus_force()
        self.root.config(bg="#EEEEEE")
        self.root.overrideredirect(True)

        self.name = StringVar()
        self.contact = StringVar()
        self.invoice = StringVar()
        self.amount = StringVar()
        self.date = StringVar()
        self.billsearchvar = StringVar()
#############################################################################



        finditem=Label(self.root,text="U P D A T E     B I L L S",font=("arial",20),bg="#EEEEEE",fg="#30336b")
        finditem.place(x=50,y=10,width=1100,height=30)
        #searchframe
        searchframe=LabelFrame(self.root,bg="#9E9E9E")
        searchframe.place(x=210,y=60,width=800,height=40)
        text_search=Entry(searchframe,textvariable=self.billsearchvar).place(x=20,y=2.5,width=470,height=30)
        #search button
        search_btn=Button(searchframe,text="Search",font=("arial",12,"bold"),fg="white",bg="#3B3B98",border=2,command=self.search_bills).place(x=520,y=2.5,width=100,height=30)
        #clear button
        clear_btn=Button(searchframe,text="Clear",font=("arial",12,"bold"),fg="white",bg="#FEA47F",border=2,command=self.searchclear).place(x=650,y=2.5,width=100,height=30)


        ######################################################################
        name_label = Label(self.root, text="Name ", font=("goudy old style", 14), bg="#EEEEEE", fg="#2C3A47").place(x=130, y=150)
        name_text = Entry(self.root, textvariable=self.name, border=0, highlightbackground="#2C3A47", highlightthickness=1).place(x=250, y=155)

        contact_label = Label(self.root, text="Contact ", font=("goudy old style", 14), bg="#EEEEEE", fg="#2C3A47").place(x=130, y=200)
        contact_text = Entry(self.root, textvariable=self.contact, border=0, highlightbackground="#2C3A47", highlightthickness=1).place(x=250, y=205)

        invoice_label = Label(self.root, text="Invoice ", font=("goudy old style", 14), bg="#EEEEEE", fg="#2C3A47").place(x=130, y=250)
        invoice_text = Entry(self.root, textvariable=self.invoice, border=0, highlightbackground="#2C3A47", highlightthickness=1,state="readonly").place(x=250, y=255)

        amount_label = Label(self.root, text="Amount", font=("goudy old style", 14), bg="#EEEEEE", fg="#2C3A47").place(x=130, y=300)
        amount_text = Entry(self.root, textvariable=self.amount, border=0, highlightbackground="#2C3A47", highlightthickness=1,state="readonly").place(x=250, y=305)

        date_label = Label(self.root, text="Date", font=("goudy old style", 14), bg="#EEEEEE", fg="#2C3A47").place(x=130, y=350)
        date_text = Entry(self.root, textvariable=self.date, border=0, highlightbackground="#2C3A47", highlightthickness=1,state="readonly").place(x=250, y=355)

        clear_btn = Button(self.root, text="CLEAR", font=("arial", 14), fg="white", bg="#4834d4", border=1, command=self.clearbillfield,cursor="hand2").place(x=95, y=400, width=100, height=30)

        update_btn = Button(self.root, text="UPDATE", font=("arial", 14), fg="white", bg="#4834d4", border=1, command=self.update_bill,cursor="hand2").place(x=220, y=400, width=100, height=30)

        delete_btn = Button(self.root, text="DELETE", font=("arial", 14), fg="white", bg="#4834d4", border=1, command=self.delete_bill,cursor="hand2").place(x=345, y=400, width=100, height=30)
        #############----------------------button-------------------#############
    




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
        self.billtable.bind("<<TreeviewSelect>>", self.populate_fields)

        self.billtable.column("invoice", width=100)
        self.billtable.column("date", width=80)
        self.billtable.column("customer", width=150)
        self.billtable.column("contact", width=120)
        self.billtable.column("amount", width=100)

        ###################################################


    def clearbillfield(self):
        self.name.set("")
        self.contact.set("")
        self.invoice.set("")
        self.amount.set("")
        self.date.set("")

    def searchclear(self):
        self.billsearchvar.set("")
        self.billtable.delete(*self.billtable.get_children())

    def search_bills(self):
        self.billtable.delete(*self.billtable.get_children())
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT * FROM bill WHERE customer LIKE ? OR invoice LIKE ?", 
                            ('%' + self.billsearchvar.get() + '%', '%' + self.billsearchvar.get() + '%'))
        rows = self.cursor.fetchall()

        for row in rows:
            self.billtable.insert("", "end", values=row)


    def update_bill(self):
        # Update bill in the database based on invoice ID
        invoice_id = self.invoice.get()
        new_name = self.name.get()
        new_contact = self.contact.get()
        new_amount = self.amount.get()
        new_date = self.date.get()

        # Execute SQL UPDATE query
        self.conn = sqlite3.connect('data.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("UPDATE bill SET customer=?, contact=?, amount=?, date=? WHERE invoice=?", (new_name, new_contact, new_amount, new_date, invoice_id))
        self.conn.commit()

        messagebox.showinfo("Success", "Bill updated successfully")
        self.search_bills()


    def delete_bill(self):
        # Ask for confirmation before deleting
        if self.invoice.get() == "" or self.contact.get() == "" or self.contact.get() == "" or self.amount.get() == "" or self.date.get() == "" :
            messagebox.showinfo("Empty field","Please fill all fields")
        else:
            response = messagebox.askyesno("Delete", "Are you sure you want to delete this bill?")

            if response:
                # Delete bill from the database
                invoice_id = self.invoice.get()
                self.conn = sqlite3.connect('data.db')
                self.cursor = self.conn.cursor()
                self.cursor.execute("DELETE FROM bill WHERE invoice=?", (invoice_id,))
                self.conn.commit()
                messagebox.showinfo("Success", "Bill deleted successfully")
                self.clearbillfield()
                self.search_bills()

    def populate_fields(self, event):
    # Get the selected item
        selected_item = self.billtable.selection()[0]
        # Get the data of the selected item
        item_data = self.billtable.item(selected_item, 'values')
        # Populate the fields with the data
        self.invoice.set(item_data[0])
        self.date.set(item_data[1])
        self.name.set(item_data[2])
        self.contact.set(item_data[3])
        self.amount.set(item_data[4])

if __name__ == "__main__":
        root=Tk()
        obj=update_bill(root)
        root.mainloop() 