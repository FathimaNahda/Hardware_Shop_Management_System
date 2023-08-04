
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import os
from db import Database
import pyodbc
from openpyxl import Workbook
import matplotlib.pyplot as plt


class ProductDetails:
    def __init__(self, pdetail):
        self.pdetail = pdetail
        self.pdetail.geometry("1000x600")
        self.pdetail.title("Stock Management System")
        self.pdetail.resizable(0, 0)
        self.lbl_title = Label(self.pdetail, text="Product Details", font=('times new roman', 20, 'bold'), fg='darkblue',
                          bg="lightblue")
        self.lbl_title.place(x=0, y=0, width=1000, height=50)

        def back():
            self.pdetail.destroy()

        # load the image
        img = Image.open(r"F:\project\ShopManagement\images\back_conn.png")
        img = img.resize((40, 40))  # adjust the size of the image
        img = ImageTk.PhotoImage(img)

        # create the button with the image
        button_back = Button(self.pdetail, image=img, command=back, width=40, height=40, bd=0, cursor='hand2',
                                 bg="lightblue")
        button_back.image = img  # keep a reference to the image to prevent garbage collection
        button_back.place(x=4, y=4)

        var_category = StringVar()
        var_sup_cat = StringVar()
        var_supplier = StringVar()
        var_pro_no = StringVar()
        var_product_name = StringVar()
        var_price = IntVar()
        var_quantity = IntVar()
        var_status = StringVar()

        # logo
        first_frame = LabelFrame(self.pdetail, bd=2, relief=RIDGE, bg="#d4d9cd", font=('times new roman', 10, 'bold'),
                                 fg='darkblue')
        first_frame.place(x=0, y=50, width=440, height=545)

        title = Label(first_frame, text="Manage Products", font=('times new roman', 16, 'bold'), fg='white', bg="#0f4d7d")
        title.pack(side=TOP, fill=X)

        lbl_cat = Label(first_frame, text="Category", font=('arial', 11, 'bold'), bg='#d4d9cd')
        lbl_cat.place(x=30, y=60)

        db = Database()
        cnxn = pyodbc.connect(db.cnxn_str)
        db.cursor = cnxn.cursor()
        global my_values
        my_values = db.cursor.execute('select distinct  CategeoryName from category')
        list_dep = [r for r, in my_values]
        list2 = []

        def my_list(*args):
            global list2
            query = "select SubCategory from product where CategeoryName='" + var_category.get() + "'"
            my_data = db.cursor.execute(query)
            list2 = [r for r, in my_data]
            combo_sub_cat['values'] = list2

        def dep_role():
            global list2
            global list_dep
            global my_values
            combo_sub_cat['values'] = (var_sup_cat.get(),)
            my_values = db.cursor.execute(
                "insert into product (SubCategory)values(')" + var_sup_cat.get() + "'")
            list2 = [r for r, in my_values]
            combo_sub_cat['values'] = list2

        global combo_category
        combo_category = ttk.Combobox(first_frame, textvariable=var_category, font=('times new roman', 11), width=22,
                                      values=list_dep, state="readonly", justify=CENTER)
        combo_category.place(x=195, y=60)
        combo_category.current(0)

        lbl_sub_cat = Label(first_frame, text="Sub-Category", font=('arial', 11, 'bold'), bg='#d4d9cd')
        lbl_sub_cat.place(x=30, y=110)
        global combo_sub_cat
        combo_sub_cat = ttk.Combobox(first_frame, textvariable=var_sup_cat, font=('times new roman', 12), width=20,
                                     values=list2)
        combo_sub_cat.place(x=195, y=110)
        var_category.trace('w', my_list)

        button_changes = Button(first_frame, text='Edit', command=dep_role, font=('arial', 8, 'bold'), width=7,
                                bg='light blue', fg='blue', cursor='hand2')
        button_changes.place(x=376, y=110)

        cnxn = pyodbc.connect(db.cnxn_str)
        db.cursor = db.cnxn.cursor()
        global my_values_new
        my_values_new = db.cursor.execute('select distinct  CompanyName from supplier')
        list_supplier = [r for r, in my_values_new]

        lbl_supplier_name = Label(first_frame, text="Supplier", font=('arial', 11, 'bold'), bg='#d4d9cd')
        lbl_supplier_name.place(x=30, y=160)
        combo_supplier = ttk.Combobox(first_frame, textvariable=var_supplier, font=('times new roman', 11), width=23,
                                      values=list_supplier, state="readonly", justify=CENTER)
        combo_supplier.place(x=195, y=160)
        combo_supplier.current(0)

        lbl_code_no = Label(first_frame, text="Product Code", font=('arial', 11, 'bold'), bg='#d4d9cd')
        lbl_code_no.place(x=30, y=210)
        txt_code = ttk.Entry(first_frame, textvariable=var_pro_no, width=22, font=('arial', 11))
        txt_code.place(x=195, y=210)

        lbl_product_name = Label(first_frame, text="Product Name", font=('arial', 11, 'bold'), bg='#d4d9cd')
        lbl_product_name.place(x=30, y=260)
        txt_product_name = ttk.Entry(first_frame, textvariable=var_product_name, width=22, font=('arial', 11))
        txt_product_name.place(x=195, y=260)

        lbl_prdct_price = Label(first_frame, text="Price", font=('arial', 11, 'bold'), bg='#d4d9cd')
        lbl_prdct_price.place(x=30, y=310)
        txt_prdct_price = ttk.Entry(first_frame, textvariable=var_price, width=22, font=('arial', 11))
        txt_prdct_price.place(x=195, y=310)

        lbl_quantity = Label(first_frame, text="Quantity", font=('arial', 11, 'bold'), bg='#d4d9cd')
        lbl_quantity.place(x=30, y=360)
        txt_quantity = ttk.Entry(first_frame, textvariable=var_quantity, width=22, font=('arial', 11))
        txt_quantity.place(x=195, y=360)

        lbl_status = Label(first_frame, text="Status", font=('arial', 11, 'bold'), bg='#d4d9cd')
        lbl_status.place(x=30, y=410)
        combo_status = ttk.Combobox(first_frame, textvariable=var_status, font=('times new roman', 11), width=22,
                                    values=('Active', 'Inactive'), state="readonly", justify=CENTER)
        combo_status.place(x=195, y=410)
        combo_status.current(0)

        def add_product():
            if var_category.get()=="" or var_supplier.get()=="" or var_product_name.get()=="" or var_price.get()=="":
                messagebox.showerror("Error", "All fields are required", parent=self.pdetail)
            elif len(str(var_product_name.get())) < 3:
                messagebox.showwarning("Error", "Enter valid Name(Ex:kevilton)", parent=self.pdetail)
                return False

            else:
                try:
                    db = Database()
                    cnxn = pyodbc.connect(db.cnxn_str)
                    db.cursor = cnxn.cursor()
                    db.cursor.execute("INSERT INTO product VALUES(?,?,?,?,?,?,?,?)",
                                   (var_category.get(), var_sup_cat.get(), var_supplier.get(), var_pro_no.get(),
                                    var_product_name.get(), var_price.get(), var_quantity.get(), var_status.get()))
                    db.cnxn.commit()
                    fetch_data()
                    db.cnxn.close()
                    messagebox.showinfo("Success", "product Successfully added", parent=self.pdetail)

                except Exception as es:
                    messagebox.showerror("Error", f'Due to:{str(es)}', parent=self.pdetail)

        def update_prod():
            global cnxn, db
            cursor_row = product_table.focus()
            content = product_table.item(cursor_row)
            row = content['values']

            category_name = var_category.get()
            sub_category = var_sup_cat.get()
            supplier = var_supplier.get()
            product_no = var_pro_no.get()
            product_name = var_product_name.get()
            price = var_price.get()
            quantity = var_quantity.get()
            status = var_status.get()
            if var_category.get() == "" or var_supplier.get()=="" or var_product_name.get() == "" or var_price.get()=="":
                messagebox.showerror("Error", "All fields are required", parent=self.pdetail)
            elif len(str(var_product_name.get())) < 3:
                messagebox.showwarning("Error", "Enter valid Name(Ex:kevilton)", parent=self.pdetail)
                return False
            else:
                try:
                    upddate = messagebox.askyesno("Update", "Are you sure update this product")
                    if upddate > 0:
                        db = Database()
                        cnxn = pyodbc.connect(db.cnxn_str)
                        db.cursor = cnxn.cursor()
                        query = "UPDATE product SET CategeoryName=?, SubCategory=?, Supplier=?," \
                                " ProductName=?, Price=?, Quantity=?, Status=? WHERE ProductNo=?"
                        db.cursor.execute(query, (
                        category_name, sub_category, supplier, product_name, price, quantity, status,
                        row[3]))
                        db.cnxn.commit()
                        messagebox.showinfo("Success", "Record updated successfully")
                    fetch_data()
                    db.cnxn.close()
                except Exception as es:
                    messagebox.showerror("Error", f'Due to:{str(es)}', parent=self.pdetail)

        def del_prod():
            global cnxn, db
            if var_category.get() == "" or var_supplier.get() == "" or var_product_name.get() == "" or var_price.get() \
                    == "":
                messagebox.showerror("Error", "All fields are required", parent=self.pdetail)
            elif len(str(var_product_name.get())) < 3:
                messagebox.showwarning("Error", "Enter valid Name(Ex:kevilton)", parent=self.pdetail)
                return False
            else:
                try:
                    Delete = messagebox.askyesno('Delete', 'Are you sure delete this product?', parent=self.pdetail)
                    if Delete > 0:
                        db = Database()
                        cnxn = pyodbc.connect(db.cnxn_str)
                        db.cursor = cnxn.cursor()
                        value = (var_pro_no.get(),)
                        db.cursor.execute("delete from product where ProductNo=?", value)
                    else:
                        if not Delete:
                            return
                    db.cnxn.commit()
                    fetch_data()
                    db.cnxn.close()
                    messagebox.showinfo("Delete", "Product successfully Deleted")

                except Exception as es:
                    messagebox.showerror("Error", f'Due to:{str(es)}', parent=self.pdetail)

        def clr_prod():
            var_category.set("Select Category")
            var_sup_cat.set("")
            var_supplier.set("")
            var_pro_no.set("")
            var_product_name.set("")
            var_price.set(int())
            var_quantity.set(int())
            var_status.set("Select Status")
            var_search_id.set("")
            var_search.set("Search by")

        def search_data():
            if not var_search.get():
                messagebox.showerror("Error", "Please enter data to search", parent=pdetail)
                return
            db = Database()
            cnxn = pyodbc.connect(db.cnxn_str)
            db.cursor = cnxn.cursor()
            if var_search.get() == "ProductNo":
                db.cursor.execute("select * from product where ProductNo LIKE '%" + var_search_id.get() + "%'")
                data = db.cursor.fetchall()
                if len(data) != 0:
                    product_table.delete(*product_table.get_children())
                    for i in data:
                        product_table.insert("", END, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
                    db.cnxn.commit()

            elif var_search.get() == "Category":
                db.cursor.execute("select * from product where CategeoryName LIKE '%" + var_search_id.get() + "%'")
                data = db.cursor.fetchall()
                if len(data) != 0:
                    product_table.delete(*product_table.get_children())
                    for i in data:
                        product_table.insert("", END, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
                    db.cnxn.commit()

            elif var_search.get() == "SubCategory":
                db.cursor.execute("select * from product where SubCategory LIKE '%" + var_search_id.get() + "%'")
                data = db.cursor.fetchall()
                if len(data) != 0:
                    product_table.delete(*product_table.get_children())
                    for i in data:
                        product_table.insert("", END, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))
                    db.cnxn.commit()

            else:
                messagebox.showerror("Warning", "Invalid Search record")

            db.cnxn.close()

        def is_inactive(Status):
            return Status.lower() == 'Inactive'

        def fetch_data():
            db = Database()
            cnxn = pyodbc.connect(db.cnxn_str)
            db.cursor = cnxn.cursor()
            db.cursor.execute('SELECT * FROM product')

            data = db.cursor.fetchall()
            if len(data) != 0:
                product_table.delete(*product_table.get_children())
                for i in data:
                    if is_inactive(i[7]):
                        product_table.insert("", 0, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]),
                                             tags=('Inactive',))
                    else:
                        product_table.insert("", 0, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))

                # Define a new style for the inactive rows
                product_table.tag_configure('Inactive', background='red')

                db.cnxn.commit()
            db.cnxn.close()

        def save_data():
            if len(product_table.get_children()) < 1:
                messagebox.showinfo("Error", "No data available")
                return
            file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save Excel",
                                                filetypes=(("Excel File", "*.xlsx"),
                                                           ("All Files", "*.*")))
            wb = Workbook()
            ws = wb.active
            cols = ['CategeoryName', 'SubCategory', 'Supplier', 'ProductNo', 'ProductName', 'Price', 'Quantity',
                            'Status']
            ws.append(cols)
            for i in product_table.get_children():
                data = product_table.item(i)['values']
                ws.append(data)
            wb.save(file)
            messagebox.showinfo("Saved", "Record saved successfully")

        def get_cursor(event):
            cursor_row = product_table.focus()
            content = product_table.item(cursor_row)
            data = content['values']

            var_category.set(data[0])
            var_sup_cat.set(data[1])
            var_supplier.set(data[2])
            var_pro_no.set(data[3])
            var_product_name.set(data[4])
            var_price.set(int(data[5]))
            var_quantity.set(int(data[6]))
            var_status.set(data[7])

            if var_status.get() == 'Inactive':
                company_name = var_supplier.get()
                messagebox.showwarning("Product Inactive",
                                       f"The product is inactive. Please contact {company_name} and get supplied the"
                                       f" product.")
                product_table.item(cursor_row, tags=('Inactive',))
            else:
                product_table.item(cursor_row, tags=())

            # Select the first item in the table and ensure that it is visible
            first_item = product_table.get_children()[0]
            product_table.selection_set(first_item)
            product_table.focus(first_item)

        def report():
            # Check if there are any records in the table
            if len(product_table.get_children()) == 0:
                messagebox.showerror("Error", "No records available")
                return
            x = []
            y1 = []
            y2 = []

            # Fetch data from the treeview table
            for child in product_table.get_children():
                values = product_table.item(child)['values']
                x.append(values[4])  # Product name
                y1.append(values[5])  # Price
                y2.append(values[6])  # Quantity

            # Create a line chart
            fig, ax = plt.subplots()
            ax.plot(x, y1, label='Price')
            ax.plot(x, y2, label='Quantity')

            # Highlight specific data points
            for i in range(len(x)):
                ax.scatter(x[i], y1[i], c='red', marker='o')  # Highlight data point for price
                ax.scatter(x[i], y2[i], c='red', marker='o')  # Highlight data point for quantity

            ax.set_xlabel('Product Name')
            ax.set_ylabel('Price/Quantity')
            ax.set_title('Product Price and Quantity Chart')
            ax.legend()

            # Display the chart
            plt.show()

        # Button frame
        button_frame = Frame(first_frame, relief=RIDGE, bg="#d4d9cd")
        button_frame.place(x=4, y=470, width=425, height=40)

        button_add = Button(button_frame, text='Add', command=add_product, font=('arial', 10, 'bold'), width=9,
                            bg='green', fg='white', cursor='hand2')
        button_add.grid(row=0, column=0, padx=0, pady=5)

        button_update = Button(button_frame, text='Update', command=update_prod, font=('arial', 10, 'bold'), width=9,
                               bg='lightblue', fg='purple', cursor='hand2')
        button_update.grid(row=0, column=1, padx=1, pady=5)

        button_delete = Button(button_frame, text='Delete', command=del_prod, font=('arial', 10, 'bold'), width=9,
                               bg='red', fg='white', cursor='hand2')
        button_delete.grid(row=0, column=2, padx=1, pady=5)

        button_clear = Button(button_frame, command=clr_prod, text='Clear', font=('arial', 10, 'bold'), width=9,
                              bg='brown', fg='white', cursor='hand2')
        button_clear.grid(row=0, column=3, padx=1, pady=5)

        button_report = Button(button_frame, text='Stat View', command=report, font=('arial', 10, 'bold'), width=12,
                               bg='#DEB887', fg='black', cursor='hand2')
        button_report.grid(row=0, column=4, padx=1, pady=5)

        # second frame
        down_frame = LabelFrame(self.pdetail, bd=2, relief=RIDGE, bg="#d4d9cd",  font=('times new roman', 11, 'bold'),
                                fg='darkblue')
        down_frame.place(x=443, y=50, width=554, height=545)
        # search frame
        search_frame = LabelFrame(down_frame, bd=2, relief=RIDGE, bg="#d4d9cd", text="Search Product Information",
                                  font=('times new roman', 11, 'bold'), fg='darkblue')
        search_frame.place(x=0, y=1, width=546, height=60)

        var_search = StringVar()
        combo_code = ttk.Combobox(search_frame, textvariable=var_search, font=('arial', 11), width=14)
        combo_code['value'] = ('ProductNo', 'Category', 'SubCategory')
        combo_code.grid(row=0, column=0, padx=1, pady=2, sticky=W)

        var_search_id = StringVar()

        # search

        txt_search = ttk.Entry(search_frame, textvariable=var_search_id, width=18, font=('arial', 11))
        txt_search.grid(row=0, column=1, padx=1, pady=2, sticky=W)

        button_search = Button(search_frame, text='Search', command=search_data, font=('arial', 10, 'bold'), width=9,
                               bg='brown', fg='white', cursor='hand2')
        button_search.grid(row=0, column=2, padx=2, pady=3)

        button_showall = Button(search_frame, text='Show All', command=fetch_data, font=('arial', 10, 'bold'), width=9,
                                bg='light blue', fg='black', cursor='hand2')
        button_showall.grid(row=0, column=3, padx=1, pady=3)
        # save button
        button_report = Button(search_frame, text='Export', command=save_data, font=('arial', 10, 'bold'), width=9,
                               bg='#8f5d36', fg='white',cursor='hand2')
        button_report.grid(row=0, column=4, padx=1, pady=3)

        # employee table-table frame
        table_frame = Frame(down_frame, bd=3, relief=RIDGE, bg="#d4d9cd")
        table_frame.place(x=0, y=70, width=543, height=200)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        product_table = ttk.Treeview(table_frame, columns=("CategeoryName", "SubCategory","Supplier", "ProductNo"
                                                            , "ProductName", "Price", "Quantity", "Status"),
                                      xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        s = ttk.Style(product_table)
        s.theme_use("clam")

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=product_table.xview)
        scroll_y.config(command=product_table.yview)

        product_table.heading("CategeoryName", text="CategeoryName")
        product_table.heading("SubCategory", text="SubCategory")
        product_table.heading("Supplier", text="Supplier")
        product_table.heading("ProductNo", text="ProductNo")
        product_table.heading("ProductName", text="ProductName")
        product_table.heading("Price", text="Price")
        product_table.heading("Quantity", text="Quantity")
        product_table.heading("Status", text="Status")

        product_table['show'] = "headings"
        product_table.column("CategeoryName", width=200)
        product_table.column("SubCategory", width=150)
        product_table.column("Supplier", width=200)
        product_table.column("ProductNo", width=200)
        product_table.column("ProductName", width=200)
        product_table.column("Price", width=100)
        product_table.column("Quantity", width=150)
        product_table.column("Status", width=200)

        product_table.pack(fill=BOTH, expand=1)
        product_table.bind("<ButtonRelease-1>", get_cursor)
        fetch_data()

        # image 1
        self.image2 = Image.open("F:\project\ShopManagement\images\stockphoto.jpg")
        self.image2 = self.image2.resize((535, 255))
        self.image2 = ImageTk.PhotoImage(self.image2)
        self.lbl_image2 = Label(down_frame, image=self.image2, bd=2, relief=RAISED)
        self.lbl_image2.place(x=0, y=280)


if __name__=="__main__":
    pdetail = Tk()
    obj = ProductDetails(pdetail)
    pdetail.mainloop()