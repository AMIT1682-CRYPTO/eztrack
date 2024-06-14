from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
class add_data:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1206x525+160+183")
        self.root.focus_force()
        self.root.config(bg="#EEEEEE")
        self.root.overrideredirect(True)

        self.var_sku=StringVar()
        self.var_name=StringVar()
        self.var_mrp=StringVar()
        self.var_cp=StringVar()
        self.var_discount=StringVar()
        self.var_supplier=StringVar()
        self.var_godown=StringVar()
        self.var_qty = StringVar()

        blanktop=Label(self.root,text="",bg="#30336b").place(x=150,y=8,width=900,height=2)
        add=Label(self.root,text="A D D    I T E M S",font=("arial",18),bg="#EEEEEE",fg="#30336b")
        add.place(x=20,y=10,width=1155,height=35)
        blank=Label(self.root,text="",bg="#30336b").place(x=150,y=45,width=900,height=2)

        sku_label=Label(self.root,text="SKU ",font=("goudy old style",12),bg="#EEEEEE",fg="#2C3A47").place(x= 100,y=50)
        sku_text=Entry(self.root,textvariable=self.var_sku,border=0,highlightbackground="#2C3A47",highlightthickness=1).place(x=200,y=50)

        qty_label=Label(self.root,text="Quantity ",font=("goudy old style",12),bg="#EEEEEE",fg="#2C3A47").place(x= 100,y=150)
        qty_text=Entry(self.root,textvariable=self.var_qty,border=0,highlightbackground="#2C3A47",highlightthickness=1).place(x=200,y=150)

        name_label=Label(self.root,text="Name ",font=("goudy old style",12),bg="#EEEEEE",fg="#2C3A47").place(x= 100,y=100)
        name_text=Entry(self.root,textvariable=self.var_name,border=0,highlightbackground="#2C3A47",highlightthickness=1).place(x=200,y=100)

        cp_label=Label(self.root,text="Cost Price ",font=("goudy old style",12),bg="#EEEEEE",fg="#2C3A47").place(x= 100,y=300)
        cp_text=Entry(self.root,textvariable=self.var_cp,border=0,highlightbackground="#2C3A47",highlightthickness=1).place(x=200,y=200)

        disc_label=Label(self.root,text="Discount(%) ",font=("goudy old style",12),bg="#EEEEEE",fg="#2C3A47").place(x= 100,y=250)
        disc_text=Entry(self.root,textvariable=self.var_discount,border=0,highlightbackground="#2C3A47",highlightthickness=1).place(x=200,y=250)

        mrp_label=Label(self.root,text="MRP ",font=("goudy old style",12),bg="#EEEEEE",fg="#2C3A47").place(x= 100,y=200)
        mrp_text=Entry(self.root,textvariable=self.var_mrp,border=0,highlightbackground="#2C3A47",highlightthickness=1).place(x=200,y=300)

        supplier_label=Label(self.root,text="Supplier ",font=("goudy old style",12),bg="#EEEEEE",fg="#2C3A47").place(x= 100,y=350)
        supplier_text=Entry(self.root,textvariable=self.var_supplier,border=0,highlightbackground="#2C3A47",highlightthickness=1).place(x=200,y=350)
        
        godown_label=Label(self.root,text="Godown ",font=("goudy old style",12),bg="#EEEEEE",fg="#2C3A47").place(x= 100,y=400)
        godown_text=Entry(self.root,textvariable=self.var_godown,border=0,highlightbackground="#2C3A47",highlightthickness=1).place(x=200,y=400)

        #------button--------#
        #add
        self.addbtn = Image.open("savebtn.png")  
        self.addbtn = self.addbtn.resize((120, 50), Image.LANCZOS)  # Resize the image
        self.addbtn = ImageTk.PhotoImage(self.addbtn)
        add_button = Button(self.root, image=self.addbtn, border=0, cursor="hand2",command=self.add).place(x=215, y=450)
        
        #clear
        self.clearbtn = Image.open("clearfield.png")  
        self.clearbtn = self.clearbtn.resize((120, 50), Image.LANCZOS)  # Resize the image
        self.clearbtn = ImageTk.PhotoImage(self.clearbtn)
        clear_button = Button(self.root, image=self.clearbtn, border=0, cursor="hand2",command=self.clear_fields).place(x=85, y=450)

        #display area
        disp=Frame(self.root,bd=2)
        disp.place(x=400,y=80,width=780,height=420)

        #scrollbars for the frame
        xscroll=Scrollbar(disp,orient=HORIZONTAL)
        xscroll.pack(side=BOTTOM,fill=X)
        
        yscroll=Scrollbar(disp,orient=VERTICAL)
        yscroll.pack(side=RIGHT,fill=Y)
        #table view for entered data
        self.itemtable=ttk.Treeview(disp,columns=("sku","name","qty","mrp","discount","cp","supplier","godown"),xscrollcommand=xscroll.set,yscrollcommand=yscroll.set)
        xscroll.config(command=self.itemtable.xview)
        yscroll.config(command=self.itemtable.yview)

        self.itemtable.heading("sku",text="SKU")
        self.itemtable.heading("name",text="NAME")
        self.itemtable.heading("qty",text="QTY")
        self.itemtable.heading("cp",text="COST PRICE")
        self.itemtable.heading("discount",text="DISCOUNT(%)")
        self.itemtable.heading("mrp",text="MRP")
        self.itemtable.heading("supplier",text="SUPPLIER")
        self.itemtable.heading("godown",text="GODOWN")
        self.itemtable["show"]="headings"
        self.itemtable.pack(fill=BOTH,expand=1)
    

        self.itemtable.column("sku",width=30)
        self.itemtable.column("qty",width=20)
        self.itemtable.column("name",width=120)
        self.itemtable.column("cp",width=30)
        self.itemtable.column("discount",width=40)
        self.itemtable.column("mrp",width=30)
        self.itemtable.column("supplier",width=100)
        self.itemtable.column("godown",width=20)


    def clear_fields(self):
        # Clear the entry fields
        self.var_sku.set("")
        self.var_name.set("")
        self.var_mrp.set("")
        self.var_cp.set("")
        self.var_discount.set("")
        self.var_supplier.set("")
        self.var_godown.set("")
        self.var_qty.set("")
    

    def add(self):
        """Add a new item to the database."""
        con = sqlite3.connect(database="data.db")
        cur = con.cursor()
        try:
            if self.var_sku.get() == "" or self.var_name.get() == "":
                messagebox.showerror("Error", "SKU and Name cannot be empty", parent=self.root)
            else:
                cur.execute("SELECT * FROM stock WHERE sku=?", (self.var_sku.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showwarning("Already exist", "A product already exists with the same SKU, please try a different SKU", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO stock(sku,qty, name, mrp, discount, cp, supplier, godown) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            self.var_sku.get(),
                            self.var_qty.get(),
                            self.var_name.get(),
                            self.var_mrp.get(),
                            self.var_discount.get(),
                            self.var_cp.get(),
                            self.var_supplier.get(),
                            self.var_godown.get(),
                        )
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Data added successfully", parent=self.root)
                    self.showrecord(self.var_sku.get())
                    self.clear_fields()
                    
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()
            

    def showrecord(self, sku):
        """Show only the newly added record in the treeview."""
        con = sqlite3.connect(database="data.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM stock WHERE sku=?", (sku,))
            rows = cur.fetchall()
            self.itemtable.delete(*self.itemtable.get_children())
            for row in rows:
                self.itemtable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    

if __name__ == "__main__":
        root=Tk()
        obj=add_data(root)
        root.mainloop() 