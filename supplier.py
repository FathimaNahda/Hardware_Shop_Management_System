import os
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import tkinter as tk
import pyodbc
from tkinter import filedialog
from openpyxl import Workbook
import webbrowser
import matplotlib.pyplot as plt
from datetime import datetime
from db import Database

from time import strftime
from datetime import date
from tkinter import scrolledtext as tkst
import dashboard


class SupplierDetails:
    def __init__(self, supnames):
        self.supnames = supnames
        self.supnames.geometry("1000x600")
        self.supnames.title("Stock Management System")
        self.supnames.resizable(0, 0)
        self.lbl_title = Label(self.supnames, text="Supplier Details", font=('times new roman', 20, 'bold'), fg='darkblue',
                          bg="lightblue")
        self.lbl_title.place(x=0, y=0, width=1000, height=50)

        def back():
            self.supnames.destroy()

        # load the image
        img = Image.open(r"F:\project\ShopManagement\images\back_conn.png")
        img = img.resize((40, 40))  # adjust the size of the image
        img = ImageTk.PhotoImage(img)

        # create the button with the image
        button_back = Button(self.supnames, image=img, command=back, width=40, height=40, bd=0, cursor='hand2',
                                 bg="lightblue")
        button_back.image = img  # keep a reference to the image to prevent garbage collection
        button_back.place(x=4, y=4)
        # logo
        first_frame = LabelFrame(self.supnames, bd=2, relief=RIDGE, bg="#d4d9cd", font=('times new roman', 10, 'bold'),
                                 fg='darkblue')
        first_frame.place(x=0, y=50, width=1000, height=545)


        var_printchar = StringVar()
        var_company = StringVar()
        var_product = StringVar()
        var_contacts = IntVar()
        var_email = StringVar()
        var_start = StringVar()
        varr_end = StringVar()
        var_search = StringVar()

        lbl_no = Label(first_frame, text="Supplier No:", font=('arial', 11, 'bold'), bg='#d4d9cd')
        lbl_no.grid(row=0, column=0, padx=1, pady=6, sticky=W)
        txt_no = ttk.Entry(first_frame, textvariable=var_printchar, width=36, font=('arial', 11))
        txt_no.grid(row=0, column=1, padx=1, pady=6, sticky=W)

        lbl_name = Label(first_frame, text="Company Name:", font=('arial', 11, 'bold'), bg='#d4d9cd')
        lbl_name.grid(row=1, column=0, padx=1, pady=6, sticky=W)
        txt_name = ttk.Entry(first_frame, textvariable=var_company, width=36, font=('arial', 11))
        txt_name.grid(row=1, column=1, padx=1, pady=6, sticky=W)

        lbl_products = Label(first_frame, text="Description:", font=('arial', 11, 'bold'), bg='#d4d9cd')
        lbl_products.grid(row=2, column=0, padx=1, pady=5, sticky=W)
        txt_products = Text(first_frame, font=('arial', 11), width=36, height=12, bd=2)
        txt_products.grid(row=2, column=1, sticky=W, padx=1, pady=9, rowspan=10)

        lbl_contacts = Label(first_frame, text="Contact No:", font=('arial', 11, 'bold'), bg='#d4d9cd')
        lbl_contacts.grid(row=0, column=2, padx=8, pady=6, sticky=W)
        txt_contacts = ttk.Entry(first_frame, textvariable=var_contacts, width=28, font=('arial', 11))
        txt_contacts.grid(row=0, column=3, padx=2, pady=6, sticky=W)

        lbl_email = Label(first_frame, text="Email:", font=('arial', 11, 'bold'), bg='#d4d9cd')
        lbl_email.grid(row=1, column=2, padx=8, pady=5, sticky=W)
        txt_email = ttk.Entry(first_frame, textvariable=var_email, width=28, font=('arial', 11))
        txt_email.grid(row=1, column=3, padx=2, pady=6, sticky=W)

        lbl_duration = Label(first_frame, text="Duration:", font=('arial', 11, 'bold'), bg='#d4d9cd')
        lbl_duration.grid(row=2, column=2, padx=8, pady=4, sticky=W)

        cal = DateEntry(first_frame, selectmode='day', textvariable=var_start, width=15)
        cal.grid(row=2, column=3, padx=2, pady=4, sticky=W)

        cal2 = DateEntry(first_frame, selectmode='day', textvariable=varr_end, width=15)
        cal2.grid(row=2, column=3, padx=120, pady=4, sticky=W)

        # load the image and resize it
        framephoto = Image.open('F:\project\ShopManagement\images\photoshop.jpg')
        framephoto = framephoto.resize((250, 110))
        # create a PhotoImage object from the resized image
        searchmask = ImageTk.PhotoImage(framephoto)
        # create a label with the image
        imagesearch = tk.Label(first_frame, image=searchmask, bg='#d4d9cd')
        imagesearch.place(x=470, y=130, width=250, height=110)
        # keep a reference to the PhotoImage object
        imagesearch.image = searchmask

        search_frame = LabelFrame(first_frame, bd=2, relief=RIDGE, bg="#d4d9cd", text="Search",
                                  font=('times new roman', 11, 'bold'), fg='darkblue')
        search_frame.place(x=1, y=224, width=995, height=312)
        search_by = Label(search_frame, text="Search by", font=('arial', 11, 'bold'), bg='#d4d9cd')
        search_by.grid(row=0, column=0, padx=2, pady=5, sticky=W)
        txt_model = ttk.Entry(search_frame, textvariable=var_search, width=22, font=('arial', 11))
        txt_model.grid(row=0, column=1, padx=4, pady=5, sticky=W)

        def search_data():
            global cnxn
            if var_search.get() == '':
                messagebox.showerror("Error", "Enter valid Id to search")
            else:
                try:
                    db = Database()
                    cnxn = pyodbc.connect(db.cnxn_str)
                    db.cursor = cnxn.cursor()
                    db.cursor.execute('select * from supplier where SupplierNo=?', (var_search.get()))
                    data = db.cursor.fetchall()
                    if len(data) != 0:
                        supplier_table.delete(*supplier_table.get_children())
                        for i in data:
                            supplier_table.insert("", END, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
                        db.cnxn.commit()

                    else:
                        messagebox.showerror("Warning", "This Id is not in the record")
                    db.cnxn.close()

                except Exception as es:
                    messagebox.showerror("Error", f'Due to:{str(es)}', parent=self.supnames)

        def fetch_data():
            db = Database()
            cnxn = pyodbc.connect(db.cnxn_str)
            db.cursor = cnxn.cursor()
            db.cursor.execute('select * from supplier')

            data = db.cursor.fetchall()
            if len(data) != 0:
                supplier_table.delete(*supplier_table.get_children())

                # Reverse the order of the rows in the data list
                data = data[::-1]

                for i in data:
                    # Check if contract has ended
                    if i[6] and datetime.now().date() > i[6]:
                        supplier_table.insert("", END, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6]),
                                              tags=('SupplierNo',))
                    else:
                        supplier_table.insert("", END, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))

                supplier_table.tag_configure('SupplierNo', background='red')

                db.cnxn.commit()
            db.cnxn.close()

        def get_cursor(event):
            cursor_row = supplier_table.focus()
            content = supplier_table.item(cursor_row)
            data = content['values']

            if content['tags'] and 'SupplierNo' in content['tags']:
                messagebox.showinfo("SupplierNo",
                                    f"Please contact {data[1]} ({data[4]}) as their contract has ended.")

            var_printchar.set(data[0])
            var_company.set(data[1])
            txt_products.delete(1.0,END)
            txt_products.insert(END,data[2])
            var_contacts.set(int(data[3]))
            var_email.set(data[4])
            var_start.set(data[5])
            varr_end.set(data[6])

        def save():
            if len(supplier_table.get_children()) < 1:
                messagebox.showinfo("Error", "No data available")
                return
            file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save Excel",
                                                filetypes=(("Excel File", "*.xlsx"),
                                                           ("All Files", "*.*")))
            wb = Workbook()
            ws = wb.active

            cols = ['SupplierNo', 'CompanyName', 'Description', 'ContactNo', 'Email', 'JoinDate', 'EndDate']
            ws.append(cols)
            for i in supplier_table.get_children():
                data = supplier_table.item(i)['values']
                ws.append(data)
            wb.save(file)
            messagebox.showinfo("Saved", "Record saved successfully")

        def pie_chart():
            db = Database()
            cnxn = pyodbc.connect(db.cnxn_str)
            db.cursor = cnxn.cursor()
            db.cursor.execute(
                'SELECT SupplierNo, CompanyName, Description, ContactNo, Email, JoinDate, EndDate FROM supplier')
            data = db.cursor.fetchall()

            if len(data) == 0:
                messagebox.showinfo("Error", "No records available")
                return

            labels = [f"{row[0]} - {row[1]}" for row in data]
            values = [row[3] for row in data]

            # Create a pie chart with percentage labels
            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct='%1.1f%%')
            ax.set_title('Suppliers by Supplier Number')

            plt.show()
            db.cnxn.close()

        button_search = Button(search_frame, text='Search', command=search_data, font=('arial', 10, 'bold'), width=10,
                               bg='brown', fg='white', cursor='hand2')
        button_search.grid(row=0, column=2, padx=4, pady=5)

        button_showall = Button(search_frame, text='Show All', command=fetch_data, font=('arial', 10, 'bold'), width=10,
                                bg='light blue', fg='black', cursor='hand2')
        button_showall.grid(row=0, column=3, padx=4, pady=5)
        stayHome = Label(search_frame, text=" View Suppliers", font=('times new roman', 18, 'bold'), bg='#d4d9cd', fg='darkblue')
        stayHome.place(x=596, y=5, width=200, height=30)

        button_report = Button(search_frame, text='Export', command=save, font=('arial', 10, 'bold'), width=10,
                               bg='#C14242', fg='white', cursor='hand2')
        button_report.grid(row=0, column=4, padx=4, pady=5)

        # Create the image button
        search_photo = Image.open('F:\project\ShopManagement\images\cskarrowdown.png')
        search_photo = search_photo.resize((50, 40))
        searchmask = ImageTk.PhotoImage(search_photo)
        imagesearch = tk.Button(search_frame, image=searchmask, bg='#d4d9cd', command=pie_chart, cursor='hand2', bd=0)
        imagesearch.place(x=790, y=1, width=50, height=40)
        imagesearch.image = searchmask
        # employee table-table frame
        table_frame = Frame(search_frame, bd=3, relief=RIDGE, bg="#d4d9cd")
        table_frame.place(x=0, y=60, width=995, height=230)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        supplier_table = ttk.Treeview(table_frame,
                                      columns=("SupplierNo", "CompanyName", "Description", "ContactNo", "Email",
                                               "JoinDate", "EndDate"), xscrollcommand=scroll_x.set,
                                      yscrollcommand=scroll_y.set)

        s = ttk.Style(supplier_table)
        s.theme_use("clam")

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=supplier_table.xview)
        scroll_y.config(command=supplier_table.yview)

        supplier_table.heading("SupplierNo", text="SupplierNo")
        supplier_table.heading("CompanyName", text="CompanyName")
        supplier_table.heading("Description", text="Description")
        supplier_table.heading("ContactNo", text="ContactNo")
        supplier_table.heading("Email", text="Email")
        supplier_table.heading("JoinDate", text="JoinDate")
        supplier_table.heading("EndDate", text="EndDate")

        supplier_table['show'] = "headings"
        supplier_table.column("SupplierNo", width=100)
        supplier_table.column("CompanyName", width=200)
        supplier_table.column("Description", width=150)
        supplier_table.column("ContactNo", width=200)
        supplier_table.column("Email", width=200)
        supplier_table.column("JoinDate", width=100)
        supplier_table.column("EndDate", width=150)

        supplier_table.pack(fill=BOTH, expand=1)
        supplier_table.bind("<ButtonRelease-1>", get_cursor)
        fetch_data()

        def add_data():
            if var_printchar.get() == "" or var_company.get() == "" or var_contacts.get() == "" or \
             var_email.get() == "" or var_start.get() == "" or varr_end.get() == "":
                messagebox.showerror("Error", "All fields are required")
                return False

            elif len(str(var_company.get())) < 3:
                messagebox.showwarning("Error", "Enter valid name(Ex:keviltom (pvt) Ltd)")
                return False
            elif len(str(var_email.get())) < 7:
                messagebox.showwarning("Error", " Enter valid email (Ex:ravishka@gmil.com)")
                return False
            elif len(str(var_contacts.get())) != 10 or not str(var_contacts.get()).isdigit():
                messagebox.showwarning("Error", "Enter valid 10 digits Contact number")
                return False
            else:
                try:
                    db = Database()
                    cnxn = pyodbc.connect(db.cnxn_str)
                    db.cursor = cnxn.cursor()
                    db.cursor.execute("INSERT INTO supplier VALUES(?,?,?,?,?,?,?)",
                                   (var_printchar.get(), var_company.get(), txt_products.get(1.0, END),
                                    var_contacts.get(), var_email.get(), var_start.get(), varr_end.get()))
                    db.cnxn.commit()
                    fetch_data()
                    db.cnxn.close()
                    messagebox.showinfo("Success", "Supplier added Successfully", parent=self.supnames)

                except Exception as es:
                    messagebox.showerror("Error", f'Due to:{str(es)}', parent=self.supnames)

        def update_data():
            global cnxn, db
            if var_printchar.get() == "" or var_company.get() == "" or var_contacts.get() == "" or \
                    var_email.get() == "" or var_start.get() == "" or varr_end.get() == "":
                messagebox.showerror("Error", "All fields are required")
            elif len(str(var_company.get())) < 3:
                messagebox.showwarning("Error", "Enter valid Name(Ex:keviltom (pvt) Ltd)")
                return False
            elif len(str(var_email.get())) < 7:
                messagebox.showwarning("Error", "Size is too small(Ex:ravishka@gmil.com)")
                return False
            elif len(str(var_contacts.get())) != 10 or not str(var_contacts.get()).isdigit():
                messagebox.showwarning("Error", "Enter valid 10 digits Contact number")
                return False
            else:
                try:
                    upddate = messagebox.askyesno("Update", "Are you sure update this supplier")
                    if upddate > 0:
                        db = Database()
                        cnxn = pyodbc.connect(db.cnxn_str)
                        db.cursor = cnxn.cursor()
                        db.cursor.execute("update supplier set CompanyName=?, Description=?, ContactNo=?,Email=?,"
                                       "JoinDate=?, EndDate=? where SupplierNo=?" ,(var_company.get(),
                                                                                    txt_products.get(1.0, END),
                                                                                    var_contacts.get(), var_email.get(),
                                                                                    var_start.get(), varr_end.get(),
                                                                                    var_printchar.get()))
                    else:
                        if not upddate:
                            return
                    db.cnxn.commit()
                    messagebox.showinfo("Success", "Employee updated successfully")
                    fetch_data()
                    db.cnxn.close()

                except Exception as es:
                    messagebox.showerror("Error", f'Due to:{str(es)}', parent=self.supnames)

        def delete_data():
            global cnxn, db
            if var_printchar.get() == "" or var_company.get() == "" or var_contacts.get() == "" or \
                    var_email.get() == "" or var_start.get() == "" or varr_end.get() == "":
                messagebox.showerror("Error", "All fields are required")
            else:
                try:
                    Delete = messagebox.askyesno('Delete', 'Are you sure delete this supplier?', parent=self.supnames)
                    if Delete > 0:
                        db = Database()
                        cnxn = pyodbc.connect(db.cnxn_str)
                        db.cursor = cnxn.cursor()
                        value = (var_printchar.get(),)
                        db.cursor.execute("delete from supplier where SupplierNo=?", value)
                    else:
                        if not Delete:
                            return
                    db.cnxn.commit()
                    fetch_data()
                    db.cnxn.close()
                    messagebox.showinfo("Delete", "Supplier Deleted Successfully")

                except Exception as es:
                    messagebox.showerror("Error", f'Due to:{str(es)}', parent=self.supnames)

        def clear_data():
            var_printchar.set("")
            var_company.set("")
            txt_products.delete(1.0, END)
            var_contacts.set(int())
            var_email.set("")
            var_start.set("")
            varr_end.set("")
            var_search.set("")

        def sendmail():
            recipient_email = var_email.get()
            if not recipient_email:
                messagebox.showinfo("Error", "Please enter recipient's email.")
                return
            subject = ""
            message = ""
            email_url = f"mailto:{recipient_email}?subject={subject}&body={message}"
            webbrowser.open_new_tab(email_url)

        # Button frame

        button_frame = Frame(first_frame, relief=RIDGE, bg="#d4d9cd", bd=0)
        button_frame.place(x=770, y=5, width=200, height=228)

        button_add=Button(button_frame, text='Add', command=add_data, font=('arial', 10, 'bold'), width=12,
                               bg='green', fg='white', cursor='hand2')
        button_add.grid(row=0, column=0, padx=6, pady=6)
        button_update = Button(button_frame, text='Update', command=update_data, font=('arial', 10, 'bold'), width=12,
                               bg='lightblue', fg='purple', cursor='hand2')
        button_update.grid(row=1, column=0, padx=6, pady=6)

        button_delete = Button(button_frame, text='Delete', command=delete_data, font=('arial', 10, 'bold'), width=12,
                               bg='red', fg='white', cursor='hand2')
        button_delete.grid(row=3, column=0, padx=6, pady=6)

        button_sendemail = Button(button_frame, text='Send Email', command=sendmail, font=('arial', 10, 'bold'), width=12,
                               bg='#DEB887', fg='black', cursor='hand2')
        button_sendemail.grid(row=4, column=0, padx=6, pady=6)

        button_clear = Button(button_frame, command=clear_data, text='Clear', font=('arial', 10, 'bold'), width=12,
                              bg='brown', fg='white', cursor='hand2')
        button_clear.grid(row=5, column=0, padx=6, pady=6)


if __name__=="__main__":
    supnames = Tk()
    obj = SupplierDetails(supnames)
    supnames.mainloop()