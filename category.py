
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
from db import Database
import pyodbc


class CategoryProduct:
    def __init__(self, categ):
        self.categ = categ
        self.categ.geometry("800x500")
        self.categ.title("Stock Management System")
        self.categ.resizable(0, 0)
        self.lbl_title = Label(self.categ, text="Manage Product Category", font=('times new roman', 20, 'bold'), fg='darkblue',
                          bg="lightblue")
        self.lbl_title.place(x=0, y=0, width=800, height=50)

        # variable
        var_categoryno = StringVar()
        var_category = StringVar()

        def back():
            self.categ.destroy()

        # load the image
        img = Image.open(r"F:\project\ShopManagement\images\back_conn.png")
        img = img.resize((40, 40))  # adjust the size of the image
        img = ImageTk.PhotoImage(img)

        # create the button with the image
        button_back = Button(self.categ, image=img, command=back, width=40, height=40, bd=0, cursor='hand2',
                                 bg="lightblue")
        button_back.image = img  # keep a reference to the image to prevent garbage collection
        button_back.place(x=4, y=4)
        # logo
        first_frame = LabelFrame(self.categ, bd=2, relief=RIDGE, bg="#d4d9cd", font=('times new roman', 10, 'bold'),
                                 fg='darkblue')
        first_frame.place(x=0, y=50, width=800, height=450)

        def add_category():
            if var_categoryno.get()=="" or var_category.get()=="":
                messagebox.showerror("Error", "All fields are required", parent=self.categ)
            elif len(str(var_category.get())) < 3:
                messagebox.showwarning("Error", "Enter valid Name(Ex:Kelivin)", parent=self.categ)
            else:
                try:
                    db = Database()
                    cnxn = pyodbc.connect(db.cnxn_str)
                    db.cursor = cnxn.cursor()
                    db.cursor.execute("INSERT INTO category VALUES(?,?)",
                                   (var_categoryno.get(), var_category.get()))
                    db.cnxn.commit()
                    fetch_data()
                    db.cnxn.close()
                    messagebox.showinfo("Success", "category Successfully added", parent=self.categ)

                except Exception as es:
                    messagebox.showerror("Error", f'Due to:{str(es)}', parent=self.categ)

        def remove_category():
            global cnxn, db
            if var_categoryno.get()=="" or var_category.get()=="":
                messagebox.showerror("Error", "All fields are required", parent=self.categ)
            elif len(str(var_category.get())) < 3:
                messagebox.showwarning("Error", "Enter valid Name(Ex:Kelivin)", parent=self.categ)
            else:
                try:
                    Delete = messagebox.askyesno('Delete', 'Are you sure delete this product category?', parent=self.categ)
                    if Delete > 0:
                        db = Database()
                        cnxn = pyodbc.connect(db.cnxn_str)
                        db.cursor = cnxn.cursor()
                        value = (var_categoryno.get(),)
                        db.cursor.execute("delete from category where CategoryNo=?", value)
                    else:
                        if not Delete:
                            return
                    db.cnxn.commit()
                    fetch_data()
                    db.cnxn.close()
                    messagebox.showinfo("Delete", "Product Category successfully Deleted")

                except Exception as es:
                    messagebox.showerror("Error", f'Due to:{str(es)}', parent=self.categ)

        def clr_category():
            var_categoryno.set("")
            var_category.set("")

        def fetch_data():
            db = Database()
            cnxn = pyodbc.connect(db.cnxn_str)
            db.cursor = cnxn.cursor()
            db.cursor.execute('select * from category')

            data = db.cursor.fetchall()
            if len(data) != 0:
                category_table.delete(*category_table.get_children())
                # Reverse the order of the rows in the data list
                data = data[::-1]

                for i in data:
                    category_table.insert("", END,
                                          values=(i[0], i[1]))

                db.cnxn.commit()
            db.cnxn.close()

        def get_cursor(event):
            cursor_row = category_table.focus()
            content = category_table.item(cursor_row)
            data = content['values']
            var_categoryno.set(data[0])
            var_category.set(data[1])

        def cat_update():
            global cnxn, db
            if var_categoryno.get()=="" or var_category.get()=="":
                messagebox.showerror("Error", "All fields are required", parent=self.categ)
            elif len(str(var_category.get())) < 3:
                messagebox.showwarning("Error", "Enter valid Name(Ex:Kelivin)", parent=self.categ)
            else:
                try:
                    upddate = messagebox.askyesno("Update", "Are you sure update this category")
                    if upddate > 0:

                        db = Database()
                        cnxn = pyodbc.connect(db.cnxn_str)
                        db.cursor = cnxn.cursor()
                        db.cursor.execute(
                            "update category set CategeoryName=? where CategoryNo=?",
                            ( var_category.get(),var_categoryno.get()))

                    else:
                        if not upddate:
                            return
                    db.cnxn.commit()
                    fetch_data()
                    db.cnxn.close()
                    messagebox.showinfo("Success", "Category updated successfully")

                except Exception as es:
                    messagebox.showerror("Error", f'Due to:{str(es)}', parent=self.categ)

        lbl_no = Label(first_frame, text="Product Category No:", font=('arial', 15, 'bold'), bg='#d4d9cd')
        lbl_no.grid(row=0, column=0, padx=20, pady=8, sticky=W)
        txt_no = ttk.Entry(first_frame, textvariable=var_categoryno, width=30, font=('arial', 11))
        txt_no.grid(row=1, column=0, padx=20, pady=8, sticky=W)

        lbl_no = Label(first_frame, text="Product Category Name:", font=('arial', 15, 'bold'), bg='#d4d9cd')
        lbl_no.grid(row=2, column=0, padx=20, pady=8, sticky=W)
        txt_no = ttk.Entry(first_frame, textvariable=var_category, width=30, font=('arial', 11))
        txt_no.grid(row=3, column=0, padx=20, pady=8, sticky=W)

        button_frame = Frame(first_frame, relief=RIDGE, bg="#d4d9cd", bd=0)
        button_frame.place(x=370, y=130, width=400, height=100)

        button_add = Button(button_frame, text='Add', command=add_category, font=('arial', 11, 'bold'), width=9,
                               bg='Green', fg='white', cursor="hand2")
        button_add.grid(row=0, column=0, padx=4, pady=8)

        button_update = Button(button_frame, text='Update', command=cat_update, font=('arial', 11, 'bold'), width=9,
                            bg='lightblue', fg='purple', cursor="hand2")
        button_update.grid(row=0, column=1, padx=4, pady=8)

        button_remove = Button(button_frame, text='Remove', command=remove_category, font=('arial', 11, 'bold'), width=9,
                               bg='Red', fg='white', cursor="hand2")
        button_remove.grid(row=0, column=2, padx=4, pady=8)

        button_clr = Button(button_frame, text='Clear', command=clr_category, font=('arial', 11, 'bold'), width=9, bg='brown',
                             fg='white', cursor="hand2")
        button_clr.grid(row=0, column=3, padx=4, pady=8)

        # category table
        table_frame = Frame(first_frame, bd=3, relief=RIDGE, bg="#d4d9cd")
        table_frame.place(x=370, y=15, width=400, height=100)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        category_table = ttk.Treeview(table_frame, columns=("CategoryNo", "CategoryName"),
                                      xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        s = ttk.Style(category_table)
        s.theme_use("clam")

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=category_table.xview)
        scroll_y.config(command=category_table.yview)

        category_table.heading("CategoryNo", text="CategoryNo")
        category_table.heading("CategoryName", text="CategoryName")

        category_table['show'] = "headings"
        category_table.column("CategoryNo", width=100)
        category_table.column("CategoryName", width=100)

        category_table.pack(fill=BOTH, expand=1)
        category_table.bind("<ButtonRelease-1>", get_cursor)
        fetch_data()

        # image 1
        self.image2 = Image.open("F:\project\ShopManagement\images\photoshop.jpg")
        self.image2 = self.image2.resize((350, 200))
        self.image2 = ImageTk.PhotoImage(self.image2)

        self.lbl_image2 = Label(first_frame, image=self.image2, bd=2, relief=RAISED)
        self.lbl_image2.place(x=20, y=200)
        # image 2
        self.imagenew = Image.open("F:\project\ShopManagement\images\stockphoto.jpg")
        self.imagenew = self.imagenew.resize((350, 200))
        self.imagenew = ImageTk.PhotoImage(self.imagenew)

        self.lbl_imagenew = Label(first_frame, image=self.imagenew, bd=2, relief=RAISED)
        self.lbl_imagenew.place(x=420, y=200)


if __name__=="__main__":
    categ = Tk()
    obj = CategoryProduct(categ)
    categ.mainloop()