from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
class update_data:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1206x525+160+183")
        self.root.focus_force()
        self.root.config(bg="#EEEEEE")
        self.root.overrideredirect(True)

        self.var_sku=StringVar()
        self.var_qty=StringVar()
        self.var_name=StringVar()
        self.var_mrp=StringVar()
        self.var_cp=StringVar()
        self.var_discount=StringVar()
        self.var_supplier=StringVar()
        self.var_godown=StringVar()

        self.var_searchstring=StringVar()


        finditem=Label(self.root,text="U P D A T E     W I N D O W",font=("arial",20),bg="#EEEEEE",fg="#30336b")
        finditem.place(x=50,y=10,width=1100,height=30)
        #searchframe
        searchframe=LabelFrame(self.root,bg="#9E9E9E")
        searchframe.place(x=210,y=60,width=800,height=40)
        text_search=Entry(searchframe,textvariable=self.var_searchstring).place(x=20,y=2.5,width=470,height=30)
        #search button
        search_btn=Button(searchframe,text="Search",font=("arial",12,"bold"),fg="white",bg="#3B3B98",border=2,command=self.searchdata).place(x=520,y=2.5,width=100,height=30)
        #clear button
        clear_btn=Button(searchframe,text="Clear",font=("arial",12,"bold"),fg="white",bg="#FEA47F",border=2,command=self.searchclear).place(x=650,y=2.5,width=100,height=30)

        sku_label=Label(self.root,text="SKU ",font=("goudy old style",12),bg="#EEEEEE",fg="#2C3A47").place(x= 100,y=100)
        sku_text=Entry(self.root,textvariable=self.var_sku,border=0,highlightbackground="#2C3A47",highlightthickness=1).place(x=200,y=100)

        qty_label=Label(self.root,text="Quantity ",font=("goudy old style",12),bg="#EEEEEE",fg="#2C3A47").place(x= 100,y=200)
        qty_text=Entry(self.root,textvariable=self.var_qty,border=0,highlightbackground="#2C3A47",highlightthickness=1).place(x=200,y=200)

        name_label=Label(self.root,text="Name ",font=("goudy old style",12),bg="#EEEEEE",fg="#2C3A47").place(x= 100,y=150)
        name_text=Entry(self.root,textvariable=self.var_name,border=0,highlightbackground="#2C3A47",highlightthickness=1).place(x=200,y=150)

        cp_label=Label(self.root,text="MRP ",font=("goudy old style",12),bg="#EEEEEE",fg="#2C3A47").place(x= 100,y=250)
        cp_text=Entry(self.root,textvariable=self.var_cp,border=0,highlightbackground="#2C3A47",highlightthickness=1).place(x=200,y=250)

        disc_label=Label(self.root,text="Discount(%) ",font=("goudy old style",12),bg="#EEEEEE",fg="#2C3A47").place(x= 100,y=300)
        disc_text=Entry(self.root,textvariable=self.var_discount,border=0,highlightbackground="#2C3A47",highlightthickness=1).place(x=200,y=300)

        mrp_label=Label(self.root,text="Cost price ",font=("goudy old style",12),bg="#EEEEEE",fg="#2C3A47").place(x= 100,y=350)
        mrp_text=Entry(self.root,textvariable=self.var_mrp,border=0,highlightbackground="#2C3A47",highlightthickness=1).place(x=200,y=350)

        supplier_label=Label(self.root,text="Supplier ",font=("goudy old style",12),bg="#EEEEEE",fg="#2C3A47").place(x= 100,y=400)
        supplier_text=Entry(self.root,textvariable=self.var_supplier,border=0,highlightbackground="#2C3A47",highlightthickness=1).place(x=200,y=400)
        
        godown_label=Label(self.root,text="Godown ",font=("goudy old style",12),bg="#EEEEEE",fg="#2C3A47").place(x= 100,y=450)
        godown_text=Entry(self.root,textvariable=self.var_godown,border=0,highlightbackground="#2C3A47",highlightthickness=1).place(x=200,y=450)

        #update
        self.updatebtn = Image.open("updatebtn.png")  
        self.updatebtn = self.updatebtn.resize((100, 40), Image.LANCZOS)  # Resize the image
        self.updatebtn = ImageTk.PhotoImage(self.updatebtn)
        update_button = Button(self.root, image=self.updatebtn, border=0, cursor="hand2",command=self.update).place(x=350, y=200)

        #delete
        self.deletebtn = Image.open("deletebtn.png")  
        self.deletebtn = self.deletebtn.resize((100, 40), Image.LANCZOS)  # Resize the image
        self.deletebtn = ImageTk.PhotoImage(self.deletebtn)
        delete_button = Button(self.root, image=self.deletebtn, border=0, cursor="hand2",command=self.delete).place(x=350, y=260)
        
        #clear
        self.clearbtn = Image.open("clearfield.png")  
        self.clearbtn = self.clearbtn.resize((100, 40), Image.LANCZOS)  # Resize the image
        self.clearbtn = ImageTk.PhotoImage(self.clearbtn)
        clear_button = Button(self.root, image=self.clearbtn, border=0, cursor="hand2",command=self.clear_fields).place(x=350, y=320)

        #display area
        disp=Frame(self.root,bd=2)
        disp.place(x=480,y=120,width=720,height=400)

        #scrollbars for the frame
        xscroll=Scrollbar(disp,orient=HORIZONTAL)
        xscroll.pack(side=BOTTOM,fill=X)
        
        yscroll=Scrollbar(disp,orient=VERTICAL)
        yscroll.pack(side=RIGHT,fill=Y)
        #table view for entered data
        self.itemtable=ttk.Treeview(disp,columns=("sku","name","qty","cp","discount","mrp","supplier","godown"),xscrollcommand=xscroll.set,yscrollcommand=yscroll.set)
        xscroll.config(command=self.itemtable.xview)
        yscroll.config(command=self.itemtable.yview)

        self.itemtable.heading("sku",text="SKU")
        self.itemtable.heading("name",text="NAME")
        self.itemtable.heading("qty",text="QUANTITY")
        self.itemtable.heading("cp",text="MRP")
        self.itemtable.heading("discount",text="DISCOUNT(%)")
        self.itemtable.heading("mrp",text="COST PRICE")
        self.itemtable.heading("supplier",text="SUPPLIER")
        self.itemtable.heading("godown",text="GODOWN")
        self.itemtable["show"]="headings"
        self.itemtable.pack(fill=BOTH,expand=1)
        self.itemtable.bind("<ButtonRelease-1>",self.get_data)

        self.itemtable.column("sku",width=30)
        self.itemtable.column("name",width=120)
        self.itemtable.column("qty",width=30)
        self.itemtable.column("cp",width=30)
        self.itemtable.column("discount",width=40)
        self.itemtable.column("mrp",width=30)
        self.itemtable.column("supplier",width=100)
        self.itemtable.column("godown",width=20)

    def clear_fields(self):
        self.var_sku.set("")
        self.var_qty.set("")
        self.var_name.set("")
        self.var_mrp.set("")
        self.var_cp.set("")
        self.var_discount.set("")
        self.var_supplier.set("")
        self.var_godown.set("")


    def searchclear(self):
        self.var_searchstring.set("")


    def searchdata(self):
        con=sqlite3.connect(database="data.db")
        cur=con.cursor()
        search_string = self.var_searchstring.get()
        searchquery = "SELECT * FROM stock WHERE sku LIKE ? OR name LIKE ?"  
        cur.execute(searchquery, ('%' + search_string + '%', '%' + search_string + '%'))
        rows = cur.fetchall()
        self.itemtable.delete(*self.itemtable.get_children())
        for row in rows:
            self.itemtable.insert('', END, values=row)
    

    def get_data(self,ev):
        select=self.itemtable.focus()
        content=(self.itemtable.item(select))
        row=content['values']
        self.var_sku.set(row[0]),
        self.var_qty.set(row[2]),
        self.var_name.set(row[1]),
        self.var_mrp.set(row[5]),
        self.var_cp.set(row[3]),
        self.var_discount.set(row[4]),
        self.var_supplier.set(row[6]),
        self.var_godown.set(row[7])


    def update(self):
        con = sqlite3.connect(database="data.db")
        cur = con.cursor()
        try:
            if self.var_sku.get() == "" or self.var_name.get() == "":
                messagebox.showerror("Error", "Please insert SKU and Name", parent=self.root)
            else:
                cur.execute("SELECT * FROM stock WHERE sku=?", (self.var_sku.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showwarning("Invalid Data", "Please enter valid SKU and name", parent=self.root)
                else:
                    cur.execute("UPDATE stock SET name=?, qty=?, mrp=?, discount=?, cp=?, supplier=?, godown=? WHERE sku=?",
                        (self.var_name.get(),self.var_qty.get(), self.var_mrp.get(), self.var_discount.get(),
                         self.var_cp.get(), self.var_supplier.get(), self.var_godown.get(), self.var_sku.get()))

                    con.commit()
                    messagebox.showinfo("Success", "Data updated successfully", parent=self.root)
                    self.showupdated()  # Call showupdated method to display the updated record
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {str(ex)}", parent=self.root)


    def showupdated(self):
        con = sqlite3.connect(database="data.db")
        cur = con.cursor()
        try:
            sku = self.var_sku.get()
            cur.execute("SELECT * FROM stock WHERE sku=?", (sku,))
            rows = cur.fetchall()
            if rows:
                self.itemtable.delete(*self.itemtable.get_children())
                for row in rows:
                    self.itemtable.insert('', END, values=row)
            else:
                messagebox.showinfo("No Data", "No records found for the given SKU", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def delete(self):
        con = sqlite3.connect(database="data.db")
        cur = con.cursor()
        try:
            if self.var_sku.get() == "" or self.var_name.get() == "":
                messagebox.showerror("Error", "Please insert SKU and Name", parent=self.root)
            else:
                cur.execute("SELECT * FROM stock WHERE sku=?", (self.var_sku.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showwarning("Invalid Data", "Please enter valid SKU and name", parent=self.root)
                else:
                    cur.execute("delete from stock where sku=?",(self.var_sku.get(),))
                    con.commit()
                    messagebox.showinfo("success","data deleted successfully",parent=self.root)
                    self.clear_fields()
                    self.showrecord()
                    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def showrecord(self):
        con=sqlite3.connect(database="data.db")
        cur=con.cursor()
        try:
            cur.execute("select * from stock")
            rows=cur.fetchall()
            self.itemtable.delete(*self.itemtable.get_children())
            for row in rows:
                self.itemtable.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("error",f"error due to :{str(ex)}",parent=self.root)


if __name__ == "__main__":
        root=Tk()
        obj=update_data(root)
        root.mainloop() 