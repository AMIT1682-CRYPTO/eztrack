from tkinter import *
from tkinter import ttk, messagebox, filedialog
import sqlite3
from fpdf import FPDF
import os
import subprocess
from datetime import datetime

class bill:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1206x525+160+183")
        self.root.focus_force()
        self.root.config(bg="#EEEEEE")
        self.root.overrideredirect(True)

        self.var_customer_name=StringVar()
        self.var_customer_contact=StringVar()
        self.var_customer_address=StringVar()
        self.var_invoice = StringVar()
        self.var_date = StringVar()
        self.var_sku = StringVar()
        self.var_name = StringVar()
        self.var_mrp = StringVar()
        self.var_rate = StringVar()
        self.var_quantity = StringVar()
        self.var_amount = StringVar()
        self.var_searchstring = StringVar()

        # Tracing changes to calculate amount
        self.var_rate.trace("w", self.calculate_amount)
        self.var_quantity.trace("w", self.calculate_amount)

        billing = Label(self.root, text="B I L L I N G     W I N D O W", font=("arial", 20), bg="#EEEEEE", fg="#130f40")
        billing.place(x=50, y=5, width=1100, height=30)
        
        # Search frame
        searchframe = LabelFrame(self.root, bg="#CAD3C8",text="Search for products here",fg="#30336b")
        searchframe.place(x=210, y=40, width=800, height=60)
        text_search = Entry(searchframe, textvariable=self.var_searchstring).place(x=20, y=2.5, width=470, height=30)
        
        # Search button
        search_btn = Button(searchframe, text="Search", font=("arial", 12, "bold"), fg="white", bg="#3B3B98", border=2, command=self.searchdata).place(x=520, y=2.5, width=100, height=30)
        
        # Clear button
        clear_btn = Button(searchframe, text="Clear", font=("arial", 12, "bold"), fg="white", bg="#FEA47F", border=2, command=self.searchclear).place(x=650, y=2.5, width=100, height=30)

        # Stock frame
        disp = Frame(self.root, bd=2)
        disp.place(x=50, y=120, width=400, height=400)
        
        # Scrollbars for the frame
        xscroll = Scrollbar(disp, orient=HORIZONTAL)
        xscroll.pack(side=BOTTOM, fill=X)
        
        yscroll = Scrollbar(disp, orient=VERTICAL)
        yscroll.pack(side=RIGHT, fill=Y)
        
        # Table view for entered data
        self.itemtable = ttk.Treeview(disp, columns=("sku", "name","qty", "mrp"), xscrollcommand=xscroll.set, yscrollcommand=yscroll.set)
        xscroll.config(command=self.itemtable.xview)
        yscroll.config(command=self.itemtable.yview)
        
        self.itemtable.heading("sku", text="SKU")
        self.itemtable.heading("name", text="NAME")
        self.itemtable.heading("qty", text="QTY")
        self.itemtable.heading("mrp", text="MRP")
        self.itemtable["show"] = "headings"
        self.itemtable.pack(fill=BOTH, expand=1)
        self.itemtable.bind("<ButtonRelease-1>", self.get_data)

        self.itemtable.column("sku", width=10)
        self.itemtable.column("name", width=100)
        self.itemtable.column("qty", width=50)
        self.itemtable.column("mrp", width=10)

        # Fields
        customer_name_label = Label(self.root, text="Customer  ", font=("goudy old style", 12), bg="#EEEEEE", fg="#2C3A47").place(x=450, y=110)
        customer_name_text = Entry(self.root, textvariable=self.var_customer_name, border=0, highlightbackground="#2C3A47", highlightthickness=1).place(x=550, y=110)

        customer_contact_label = Label(self.root, text="contact ", font=("goudy old style", 12), bg="#EEEEEE", fg="#2C3A47").place(x=450, y=133)
        customer_contact_text = Entry(self.root, textvariable=self.var_customer_contact, border=0, highlightbackground="#2C3A47", highlightthickness=1).place(x=550, y=133)

        address_label = Label(self.root, text="Address", font=("goudy old style", 12), bg="#EEEEEE", fg="#2C3A47").place(x=450, y=158)
        address_text = Entry(self.root, textvariable=self.var_customer_address, border=0, highlightbackground="#2C3A47", highlightthickness=1).place(x=550, y=158)

        Invoice_label = Label(self.root, text="Invoice ID ", font=("goudy old style", 12), bg="#EEEEEE", fg="#2C3A47").place(x=450, y=190)
        Invoice_text = Entry(self.root, textvariable=self.var_invoice, border=0, highlightbackground="#2C3A47", highlightthickness=1,state="readonly").place(x=550, y=190)

        date_label = Label(self.root, text="Date ", font=("goudy old style", 12), bg="#EEEEEE", fg="#2C3A47").place(x=450, y=213)
        date_text = Entry(self.root, textvariable=self.var_date, border=0, highlightbackground="#2C3A47", highlightthickness=1,state="readonly").place(x=550, y=213)
        
        sku_label = Label(self.root, text="SKU ", font=("goudy old style", 12), bg="#EEEEEE", fg="#2C3A47").place(x=450, y=250)
        sku_text = Entry(self.root, textvariable=self.var_sku, border=0, highlightbackground="#2C3A47", highlightthickness=1,state="readonly").place(x=550, y=250)
        

        name_label = Label(self.root, text="Name ", font=("goudy old style", 12), bg="#EEEEEE", fg="#2C3A47").place(x=450, y=275)
        name_text = Entry(self.root, textvariable=self.var_name, border=0, highlightbackground="#2C3A47", highlightthickness=1,state="readonly").place(x=550, y=275)

        rate_label = Label(self.root, text="Rate ", font=("goudy old style", 12), bg="#EEEEEE", fg="#2C3A47").place(x=450, y=300)
        rate_text = Entry(self.root, textvariable=self.var_rate, border=0, highlightbackground="#2C3A47", highlightthickness=1).place(x=550, y=300)

        quantity_label = Label(self.root, text="Quantity ", font=("goudy old style", 12), bg="#EEEEEE", fg="#2C3A47").place(x=450, y=325)
        quantity_text = Entry(self.root, textvariable=self.var_quantity, border=0, highlightbackground="#2C3A47", highlightthickness=1).place(x=550, y=325)

        amount_label = Label(self.root, text="Amount ", font=("goudy old style", 12), bg="#EEEEEE", fg="#2C3A47").place(x=450, y=350)
        amount_text = Entry(self.root, textvariable=self.var_amount, border=0, highlightbackground="#2C3A47", highlightthickness=1, state='readonly').place(x=550, y=350)

        # Cart frame
        disp1 = Frame(self.root, bd=2)
        disp1.place(x=700, y=120, width=500, height=400)
        
        # Scrollbars for the frame
        x1scroll = Scrollbar(disp1, orient=HORIZONTAL)
        x1scroll.pack(side=BOTTOM, fill=X)
        
        y1scroll = Scrollbar(disp1, orient=VERTICAL)
        y1scroll.pack(side=RIGHT, fill=Y)
        
        # Table view for entered data
        self.cart = ttk.Treeview(disp1, columns=("sku", "name", "rate", "quantity", "amount"), xscrollcommand=x1scroll.set, yscrollcommand=y1scroll.set)
        x1scroll.config(command=self.cart.xview)
        y1scroll.config(command=self.cart.yview)
        
        self.cart.heading("sku", text="SKU")
        self.cart.heading("name", text="NAME")
        self.cart.heading("rate", text="RATE")
        self.cart.heading("quantity", text="QTY")
        self.cart.heading("amount", text="AMOUNT")
        self.cart["show"] = "headings"
        self.cart.pack(fill=BOTH, expand=1)
        
        self.cart.column("sku", width=10)
        self.cart.column("name", width=100)
        self.cart.column("rate", width=10)
        self.cart.column("quantity", width=10)
        self.cart.column("amount", width=20)

        # Buttons
        clear_btn = Button(self.root, text="Clear", font=("arial", 12, "bold"), fg="white", bg="#686de0", border=2, command=self.clear_fields).place(x=450, y=400, width=100, height=30)

        add_Cart_btn = Button(self.root, text="Add to cart", font=("arial", 12, "bold"), fg="white", bg="#686de0", border=2, command=self.add_to_cart).place(x=570, y=400, width=100, height=30)

        clearcart_btn = Button(self.root, text="Clear Cart", font=("arial", 12, "bold"), fg="white", bg="#686de0", border=2, command=self.clear_cart).place(x=450, y=450, width=100, height=30)

        print_btn = Button(self.root, text="Print Bill", font=("arial", 12, "bold"), fg="white", bg="#686de0", border=2, command=self.print_bill)
        print_btn.place(x=570, y=450, width=100, height=30)

        self.generate_invoice_id()
        self.displaydata()
        self.var_date.set(datetime.now().strftime("%d-%m-%Y"))

    # Function to clear input fields
    def clear_fields(self):
        self.var_sku.set("")
        self.var_name.set("")
        self.var_rate.set("")
        self.var_quantity.set("")
        self.var_amount.set("")


    # Function to clear the search input field
    def searchclear(self):
        self.var_searchstring.set("")

    # Function to search data in the database
    def searchdata(self):
        con = sqlite3.connect(database="data.db")
        cur = con.cursor()
        search_string = self.var_searchstring.get()
        searchquery = "SELECT * FROM stock WHERE sku LIKE ? OR name LIKE ?"  
        cur.execute(searchquery, ('%' + search_string + '%', '%' + search_string + '%'))
        rows = cur.fetchall()
        self.itemtable.delete(*self.itemtable.get_children())
        for row in rows:
            self.itemtable.insert('', END, values=row)
        con.close()

    # Function to get data from the selected row
    def get_data(self, ev):
        select = self.itemtable.focus()
        content = (self.itemtable.item(select))
        row = content['values']
        self.var_sku.set(row[0])
        self.var_name.set(row[1])
        

    # Function to calculate the amount
    def calculate_amount(self, *args):
        
        try:
            
            rate = float(self.var_rate.get())
            quantity = int(self.var_quantity.get())
            amount = rate * quantity
            self.var_amount.set(str(amount))
        except ValueError:
            self.var_amount.set("")

    # Function to add item to the cart
    def add_to_cart(self):
        sku = self.var_sku.get()
        name = self.var_name.get()
        rate = self.var_rate.get()
        quantity = self.var_quantity.get()
        amount = self.var_amount.get()

        if sku and name and rate and quantity and amount:
            self.cart.insert('', END, values=(sku, name, rate, quantity, amount))
            self.clear_fields()
        else:
            messagebox.showerror("Error", "Please fill all fields")

    # Function to clear the cart
    def clear_cart(self):
    # Get items from the cart and update stock to restore original quantity
        cart_items = self.cart.get_children()
        for item in cart_items:
            data = self.cart.item(item)['values']
            sku = data[0]
            quantity = int(data[3])
            
            # Update stock table with restored quantity
            con = sqlite3.connect(database="data.db")
            cur = con.cursor()
            cur.execute("SELECT qty FROM stock WHERE sku=?", (sku,))
            stock_quantity = cur.fetchone()[0]
            new_quantity = stock_quantity + quantity
            cur.execute("UPDATE stock SET qty=? WHERE sku=?", (new_quantity, sku))
            con.commit()  # Commit the transaction
            con.close()  # Close the connection

        # Clear the cart
        self.clear_cart_gui()
        self.searchdata()

        
    def clear_cart_gui(self):
    # Clear the cart in the GUI
        self.cart.delete(*self.cart.get_children())


    def generate_invoice_id(self):
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()

        # Get the current financial year
        now = datetime.now()
        current_year = now.year if now.month > 3 else now.year - 1
        next_year = current_year + 1
        financial_year = f"{current_year}-{str(next_year)[-2:]}"

        cursor.execute("SELECT MAX(invoice) FROM bill")
        result = cursor.fetchone()
        conn.close()

        if result[0]:
            max_id = result[0].split('/')[-1]
            new_id = int(max_id) + 1
        else:
            new_id = 1

        self.var_invoice.set(f"BHE/{financial_year}/{new_id}")

    def displaydata(self):
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM stock")
            rows = cursor.fetchall()
            self.itemtable.delete(*self.itemtable.get_children())
            for row in rows:
                self.itemtable.insert('', END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def print_bill(self):
        invoice_id = self.var_invoice.get()
        customer_name = self.var_customer_name.get()
        customer_contact = self.var_customer_contact.get()
        customer_address = self.var_customer_address.get()
        date = self.var_date.get()
        cart_items = self.cart.get_children()
        if not cart_items:
            messagebox.showerror("Error", "No items in the cart to print.")
            return

        total_amount = 0
        bill_data = []
        for item in cart_items:
            data = self.cart.item(item)['values']
            bill_data.append(data)
            total_amount += float(data[4])

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.rect(8, 8, 195, 280) 
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 5, txt="TAX INVOICE", ln=1, align="C")
        pdf.cell(100, 10, txt="", ln=1)
        pdf.cell(190, 5, txt="BALAJI HARDWARE AND ELECTRICALS", ln=1, align="R")
        pdf.set_font("Arial", size=6)
        pdf.cell(190, 5, txt="One stop for complete hardware and electrical goods.", ln=1, align="R")
        pdf.cell(180, 5, txt="Thana Road, Jorhat, Assam", ln=1, align="R")
        logo_path = "bill_logo.png"  
        pdf.image(logo_path,x=15,y=15,w=30,h=30)
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt="", ln=1, align="C")

        pdf.cell(200, 5, txt="BILLING DETAILS", ln=1, align="L")
        pdf.cell(200, 4, txt="", ln=1, align="C")
        pdf.set_font("Arial", size=8)
        pdf.cell(150, 5, txt=f"Customer Name: {customer_name}", ln=0)
        pdf.set_font("Arial", size=10)
        pdf.cell(150, 5, txt=f"Invoice Id: {invoice_id}", ln=1, align="L")
        pdf.set_font("Arial", size=8)
        pdf.cell(150, 5, txt=f"Contact: {customer_contact}", ln=0)
        pdf.set_font("Arial", size=10)
        pdf.cell(150, 5, txt=f"Date: {date}", ln=1, align="L")
        pdf.set_font("Arial", size=8)
        pdf.cell(200, 5, txt=f"Address: {customer_address}", ln=1)

        pdf.cell(200, 10, txt="", ln=1)
        
        pdf.cell(20, 10, "SKU", 1, 0, "C")
        pdf.cell(90, 10, "Name", 1, 0, "C")
        pdf.cell(30, 10, "Rate", 1, 0, "C")
        pdf.cell(20, 10, "Quantity", 1, 0, "C")
        pdf.cell(30, 10, "Amount", 1, 1, "C") 
        
        # rows
        for data in bill_data:
            sku, name, rate, quantity, amount = data
            pdf.cell(20, 10, str(sku), 1, 0, "C")
            pdf.cell(90, 10, str(name), 1, 0, "C")
            pdf.cell(30, 10, str(rate), 1, 0, "C")
            pdf.cell(20, 10, str(quantity), 1, 0, "C")
            pdf.cell(30, 10, str(amount), 1, 1, "C")  # Move to next line after the last cell
        
        # Add total amount row
        pdf.cell(160, 10, "Total", 1, 0, "R")
        pdf.cell(30, 10, str(total_amount), 1, 1, "C")  # Move to next line after the last cell

        self.add_footer(pdf)
        
        # Ask user where to save the PDF
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return  # User cancelled the save dialog
        
        pdf.output(file_path)
        
        # Open the PDF file for printing
        if os.name == 'nt':  # For Windows
            try:
                subprocess.run(['start', '', '/WAIT', file_path], shell=True, check=True)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to print the PDF: {e}")

        ###############store into database###################
        con=sqlite3.connect(database="data.db")
        cur=con.cursor()
        cur.execute("insert into bill(invoice,date,customer,contact,amount) values(?,?,?,?,?)",
                    (invoice_id,
                    date,
                    customer_name,
                    customer_contact,
                    total_amount
                    ))
        con.commit()
        con.close()
        #####################################################

    def add_footer(self, pdf):
        pdf.set_y(-20)  # Set position 15mm from bottom
        pdf.set_font("Arial", "I", 6)
        pdf.cell(200, 5, "-------------------This is a computer generated bill and does not require any signature-------------------", 0, 0, "C")
    # Function to add item to the cart
    def add_to_cart(self):
        sku = self.var_sku.get()
        name = self.var_name.get()
        rate = self.var_rate.get()
        quantity = self.var_quantity.get()
        amount = self.var_amount.get()

        if sku and name and rate and quantity and amount:
            # Check if the quantity entered is more than available in stock
            con = sqlite3.connect(database="data.db")
            cur = con.cursor()
            cur.execute("SELECT qty FROM stock WHERE sku=?", (sku,))
            stock_quantity = cur.fetchone()[0]
            con.close()

            if int(quantity) > stock_quantity:
                messagebox.showerror("Error", "Insufficient stock")
                return

            # If quantity is sufficient, proceed to add item to the cart and update stock
            self.cart.insert('', END, values=(sku, name, rate, quantity, amount))

            # Update stock table with reduced quantity
            new_quantity = stock_quantity - int(quantity)
            con = sqlite3.connect(database="data.db")
            cur = con.cursor()
            cur.execute("UPDATE stock SET qty=? WHERE sku=?", (new_quantity, sku))
            con.commit()  # Commit the transaction
            con.close()  # Close the connection

            # Clear search string to refresh product window
            self.var_searchstring.set("")
            self.searchdata()  # Refresh product window

            self.clear_fields()
        else:
            messagebox.showerror("Error", "Please fill all fields")



    # Function to update the stock table with the updated quantity
    def update_stock(self, cart_items):
        con = sqlite3.connect(database="data.db")
        cur = con.cursor()
        for item in cart_items:
            sku = item[0]
            quantity = item[3]
            cur.execute("UPDATE stock SET qty = qty - ? WHERE sku = ?", (quantity, sku))
        con.commit()
        con.close()


if __name__ == "__main__":
    root = Tk()
    obj = bill(root)
    root.mainloop()
