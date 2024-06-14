from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import sqlite3

class view_data:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1206x525+160+183")
        self.root.focus_force()
        self.root.config(bg="#EEEEEE")
        self.root.overrideredirect(True)
        
        self.searchvar = StringVar()
        self.billsearchvar = StringVar()

        view = Label(self.root, text="S E A R C H         M E N U", font=("ARIAL", 18), bg="#EEEEEE", fg="#130f40")
        view.place(x=20, y=10, width=1155, height=35)
        blank=Label(self.root,text="",bg="#30336b").place(x=20,y=42,width=1160,height=2)

        # Search frame for products
        searchframe = LabelFrame(self.root, bg="#CAD3C8", text="Search products", font=("calibri", 14))
        searchframe.place(x=5, y=60, width=600, height=60)
        text_search = Entry(searchframe, textvariable=self.searchvar).place(x=10, y=0, width=350, height=20)
        search_btn = Button(searchframe, text="Search", font=("arial", 12, "bold"), fg="white", bg="#304FFE", border=0, command=self.searchdata).place(x=380, y=0, width=85, height=20)
        clear_btn = Button(searchframe, text="Clear", font=("arial", 12, "bold"), fg="white", bg="#D50000", border=0, command=self.clear).place(x=490, y=0, width=85, height=20)

        disp = Frame(self.root, bd=2)
        disp.place(x=5, y=125, height=400, width=600)
        
        xscroll = Scrollbar(disp, orient=HORIZONTAL)
        xscroll.pack(side=BOTTOM, fill=X)
        yscroll = Scrollbar(disp, orient=VERTICAL)
        yscroll.pack(side=RIGHT, fill=Y)

        self.itemtable = ttk.Treeview(disp, columns=("sku", "name", "qty","mrp", "discount", "cp", "supplier", "godown"), xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
        xscroll.config(command=self.itemtable.xview)
        yscroll.config(command=self.itemtable.yview)

        self.itemtable.heading("sku", text="SKU")
        self.itemtable.heading("name", text="NAME")
        self.itemtable.heading("qty", text="QTY")
        self.itemtable.heading("cp", text="COST PRICE")
        self.itemtable.heading("discount", text="DISCOUNT(%)")
        self.itemtable.heading("mrp", text="MRP")
        self.itemtable.heading("supplier", text="SUPPLIER")
        self.itemtable.heading("godown", text="GODOWN")
        self.itemtable["show"] = "headings"
        self.itemtable.pack(fill=BOTH, expand=1)

        self.itemtable.column("sku", width=50)
        self.itemtable.column("name", width=180)
        self.itemtable.column("qty", width=50)
        self.itemtable.column("cp", width=100)
        self.itemtable.column("discount", width=100)
        self.itemtable.column("mrp", width=50)
        self.itemtable.column("supplier", width=150)
        self.itemtable.column("godown", width=100)


        billframe = LabelFrame(self.root, bg="#CAD3C8", text="Search Bills", font=("calibri", 14))
        billframe.place(x=620, y=60, width=580, height=60)
        text_search = Entry(billframe, textvariable=self.billsearchvar).place(x=10, y=0, width=350, height=20)
        search_btn = Button(billframe, text="Search", font=("arial", 12, "bold"), fg="white", bg="#304FFE", border=0, command=self.search_bills).place(x=380, y=0, width=85, height=20)
        clear_btn = Button(billframe, text="Clear", font=("arial", 12, "bold"), fg="white", bg="#D50000", border=0, command=self.clearbillframe).place(x=480, y=0, width=85, height=20)


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

        self.billtable.column("invoice", width=100)
        self.billtable.column("date", width=80)
        self.billtable.column("customer", width=150)
        self.billtable.column("contact", width=120)
        self.billtable.column("amount", width=100)


    def clear(self):
        self.searchvar.set("")
        self.itemtable.delete(*self.itemtable.get_children())

    def clearbillframe(self):
        self.billsearchvar.set("")
        self.billtable.delete(*self.billtable.get_children())

    def searchdata(self):
        con = sqlite3.connect(database="data.db")
        cur = con.cursor()
        try:
            search_string = self.searchvar.get()
            searchquery = "SELECT * FROM stock WHERE sku LIKE ? OR name LIKE ?"
            cur.execute(searchquery, ('%' + search_string + '%', '%' + search_string + '%'))
            rows = cur.fetchall()
            self.itemtable.delete(*self.itemtable.get_children())
            for row in rows:
                self.itemtable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search_bills(self):
        con = sqlite3.connect(database="data.db")
        cur = con.cursor()
        try:
            search_string = self.billsearchvar.get()
            searchquery ="SELECT * FROM bill WHERE invoice LIKE ? OR date LIKE ? OR amount LIKE ? OR customer LIKE ?"

            cur.execute(searchquery, ('%' + search_string + '%', '%' + search_string + '%', '%' + search_string + '%', '%' + search_string + '%'))
            rows = cur.fetchall()
            self.billtable.delete(*self.billtable.get_children())
            for row in rows:
                self.billtable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = view_data(root)
    root.mainloop()
