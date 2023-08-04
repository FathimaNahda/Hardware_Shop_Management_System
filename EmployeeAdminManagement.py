
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import DateEntry
import os
from db import Database
import pyodbc
from openpyxl import Workbook
from collections import Counter
import matplotlib.pyplot as plt
import tkinter as tk
emp = Tk()
emp.geometry("1300x1000")
emp.title("Employee Admin login")
emp.resizable(0,0)

# variables
var_dep = StringVar()
var_name = StringVar()
var_designation = StringVar()
var_email = StringVar()
var_address = StringVar()
var_marital = StringVar()
var_dob = StringVar()
var_doj = StringVar()
var_idproofcombo = StringVar()
var_idproof = StringVar()
var_gender = StringVar()
var_phone = StringVar()
var_city = StringVar()
var_salary = StringVar()
var_dleft = StringVar()
date_var = StringVar()
var_logintype=StringVar()
var_passwords=StringVar()


def exit():
    emp.destroy()


emp.protocol("WM_DELETE_WINDOW", exit)


# functions
def add_data():
    if var_dep.get() == "" or var_name.get() == "" or var_designation.get() == "" or var_email.get() == "" or \
            var_address.get() == "" or var_marital.get() == "" or var_dob.get() == "" or var_doj.get() == "" or \
            var_idproofcombo.get() == "" or var_idproof.get() == "" or var_phone.get() == "" or var_city.get() == "" or\
            var_salary.get() == "":
        messagebox.showerror("Error", "All fields are required", parent=emp)

    elif len(str(var_name.get())) < 3:
        messagebox.showwarning("Error", "Enter valid Name(Ex:Samuwel)", parent=emp)
        return False
    elif len(str(var_phone.get())) != 10 or not str(var_phone.get()).isdigit():
        messagebox.showwarning("Error", "Enter valid 10 digits Contact number", parent=emp)
        return False
    elif len(str(var_address.get())) < 10:
        messagebox.showwarning("Error", "Enter valid address(Ex:20/A Cross Road)", parent=emp)
        return False
    elif len(str(var_city.get())) < 4:
        messagebox.showwarning("Error", "Enter valid city(Ex:Galle)", parent=emp)
        return False
    elif len(str(var_email.get())) < 7 or "@" not in var_email.get() or "." not in var_email.get():
        messagebox.showwarning("Error", "Enter valid email address(Ex:raviska@gmail.com)", parent=emp)
        return False
    elif var_logintype.get() == 'Type' and len(var_passwords.get()) != 8:
        messagebox.showwarning("Error", "Password should have exactly 8 characters and select a login type")
        return False
    elif var_logintype.get() == 'Type' and len(var_passwords.get()) == 8:
        messagebox.showwarning("Error", " Select a login type")
        return False
    elif var_logintype.get() in ('Employee', 'Sales', 'Inventory', 'Admin') and len(var_passwords.get()) != 8:
        messagebox.showwarning("Error", "Password should have exactly 8 characters")
        return False
    elif var_idproofcombo.get() == "NIC":
        if len(str(var_idproof.get())) != 10 and len(str(var_idproof.get())) != 12:
            messagebox.showwarning("Error", "Enter valid NIC", parent=emp)
            return False
        elif len(str(var_idproof.get())) == 10 and var_idproof.get()[-1] != 'V':
            messagebox.showwarning("Error", "Enter letter 'V' at the end of NIC", parent=emp)
            return False
        elif len(str(var_idproof.get())) == 12 and not var_idproof.get().isdigit():
            messagebox.showwarning("Error", "Enter only numbers in NIC", parent=emp)
            return False
    elif var_idproofcombo.get() == "License":
        if len(str(var_idproof.get())) != 8:
            messagebox.showwarning("Error", "Enter valid License Number(Ex:B3432111)", parent=emp)
            return False
        elif len(str(var_idproof.get())) == 8 and var_idproof.get()[0] != 'B':
            messagebox.showwarning("Error", "Enter letter 'B' at the beginning of License Number", parent=emp)
            return False

    try:
        db = Database()
        cnxn = pyodbc.connect(db.cnxn_str)
        db.cursor = cnxn.cursor()
        db.cursor.execute("INSERT INTO Employees VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       (var_dep.get(), var_name.get(), var_designation.get(), var_email.get(), var_address.get(),
                        var_marital.get(), var_dob.get(), var_doj.get(), var_idproofcombo.get(), var_idproof.get(),
                        var_gender.get(), var_phone.get(), var_city.get(), var_salary.get(), var_dleft.get(),
                        var_logintype.get(), var_passwords.get()))
        db.cnxn.commit()
        fetch_data()
        db.cnxn.close()
        messagebox.showinfo("Success", "Employee Successfully added", parent=emp)

    except Exception as es:
        messagebox.showerror("Error", f'Due to:{str(es)}', parent=emp)


def fetch_data():
    db = Database()
    cnxn = pyodbc.connect(db.cnxn_str)
    db.cursor = cnxn.cursor()
    db.cursor.execute('select * from Employees')

    data = db.cursor.fetchall()
    if len(data) != 0:
        employee_table.delete(*employee_table.get_children())

        # Sort data by date column
        data = sorted(data, key=lambda x: x[7], reverse=True)

        # Insert rows in reverse order
        for i in reversed(data):
            employee_table.insert("", 0, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10],
                                                 i[11], i[12], i[13], i[14], i[15], i[16]))

        db.cnxn.commit()
    db.cnxn.close()


# getCursor
def get_cursor(event):
        cursor_row = employee_table.focus()
        content = employee_table.item(cursor_row)
        data = content['values']

        var_dep.set(data[0])
        var_name.set(data[1])
        var_designation.set(data[2])
        var_email.set(data[3])
        var_address.set(data[4])
        var_marital.set(data[5])
        var_dob.set(data[6])
        var_doj.set(data[7])
        var_idproofcombo.set(data[8])
        var_idproof.set(data[9])
        var_gender.set(data[10])
        var_phone.set(data[11])
        var_city.set(data[12])
        var_salary.set(data[13])
        var_dleft.set(data[14])
        var_logintype.set(data[15])
        var_passwords.set(data[16])


def update_data():
    global cnxn, db
    if var_dep.get() == "" or var_name.get() == "" or var_designation.get() == "" or var_email.get() == "" or \
            var_address.get() == "" or var_marital.get() == "" or var_dob.get() == "" or var_doj.get() == "" or \
            var_idproofcombo.get() == "" or var_idproof.get() == "" or var_phone.get() == "" or var_city.get() == "" or\
            var_salary.get() == "":
        messagebox.showerror("Error", "All fields are required", parent=emp)

    elif len(str(var_name.get())) < 3:
        messagebox.showwarning("Error", "Enter valid Name(Ex:Samuwel)", parent=emp)
        return False
    elif len(str(var_phone.get())) != 10 or not str(var_phone.get()).isdigit():
        messagebox.showwarning("Error", "Enter valid 10 digits Contact number", parent=emp)
        return False
    elif len(str(var_address.get())) < 10:
        messagebox.showwarning("Error", "Enter valid address(Ex:20/A Cross Road)", parent=emp)
        return False
    elif len(str(var_city.get())) < 4:
        messagebox.showwarning("Error", "Enter valid city(Ex:Galle)", parent=emp)
        return False
    elif len(str(var_email.get())) < 7 or "@" not in var_email.get() or "." not in var_email.get():
        messagebox.showwarning("Error", "Enter valid email address(Ex:raviska@gmail.com)", parent=emp)
        return False
    elif var_logintype.get() == 'Type' and len(var_passwords.get()) != 8:
        messagebox.showwarning("Error", "Password should have exactly 8 characters and select a login type")
        return False
    elif var_logintype.get() == 'Type' and len(var_passwords.get()) == 8:
        messagebox.showwarning("Error", " Select a login type")
        return False
    elif var_logintype.get() in ('Employee', 'Sales', 'Inventory', 'Admin') and len(var_passwords.get()) != 8:
        messagebox.showwarning("Error", "Password should have exactly 8 characters")
        return False
    elif var_idproofcombo.get() == "NIC":
        if len(str(var_idproof.get())) != 10 and len(str(var_idproof.get())) != 12:
            messagebox.showwarning("Error", "Enter valid NIC", parent=emp)
            return False
        elif len(str(var_idproof.get())) == 10 and var_idproof.get()[-1] != 'V':
            messagebox.showwarning("Error", "Enter letter 'V' at the end of NIC", parent=emp)
            return False
        elif len(str(var_idproof.get())) == 12 and not var_idproof.get().isdigit():
            messagebox.showwarning("Error", "Enter only numbers in NIC", parent=emp)
            return False
    elif var_idproofcombo.get() == "License":
        if len(str(var_idproof.get())) != 8:
            messagebox.showwarning("Error", "Enter valid License Number(Ex:B3432111)", parent=emp)
            return False
        elif len(str(var_idproof.get())) == 8 and var_idproof.get()[0] != 'B':
            messagebox.showwarning("Error", "Enter letter 'B' at the beginning of License Number", parent=emp)
            return False

    cursor_row = employee_table.focus()
    content = employee_table.item(cursor_row)
    row = content['values']

    dep = var_dep.get()
    name = var_name.get()
    designation = var_designation.get()
    email = var_email.get()
    address = var_address.get()
    marital = var_marital.get()
    dob = var_dob.get()
    doj = var_doj.get()
    idproofcomb = var_idproofcombo.get()
    gender = var_gender.get()
    phone = var_phone.get()
    city = var_city.get()
    salary = var_salary.get()
    left = var_dleft.get()
    logintype = var_logintype.get()
    password = var_passwords.get()
    idproof = var_idproof.get()

    try:
        update = messagebox.askyesno("Update","Are you sure update this employee")
        if update > 0:
            db = Database()
            cnxn = pyodbc.connect(db.cnxn_str)
            db.cursor = cnxn.cursor()
            query = "UPDATE Employees SET Department=?, Name=?, Designation=?, Email=?, Address=?, Marital_Status=?," \
                         "DOB=?, D_joined=?, id_type=?, id=?, Gender=?, Phone=?, city=?, Salary=?, D_left=?, Login_Type=?," \
                         "Password=? WHERE id=?"

            db.cursor.execute(query, (dep, name, designation, email, address, marital, dob, doj, idproofcomb, idproof,
                                        gender, phone, city, salary, left, logintype, password, row[9]))
            db.cnxn.commit()
            messagebox.showinfo("Success", "Employee updated successfully")
        fetch_data()
        db.cnxn.close()

    except Exception as es:
            messagebox.showerror("Error", f'Due to:{str(es)}', parent=emp)


def delete_data():
    global cnxn, db
    if var_dep.get() == "" or var_name.get() == "" or var_designation.get() == "" or var_email.get() == "" or \
            var_address.get() == "" or var_marital.get() == "" or var_dob.get() == "" or var_doj.get() == "" or \
            var_idproofcombo.get() == "" or var_idproof.get() == "" or var_phone.get() == "" or var_city.get() == "" \
            or var_salary.get() == "":
        messagebox.showerror("Error", "All fields are required")
    else:
        try:
            Delete = messagebox.askyesno('Delete', 'Are you sure delete this employee?', parent=emp)
            if Delete > 0:
                db = Database()
                cnxn = pyodbc.connect(db.cnxn_str)
                db.cursor = cnxn.cursor()
                value = (var_idproof.get(),)
                db.cursor.execute("delete from Employees where id=?", value)
            else:
                if not Delete:
                    return
            db.cnxn.commit()
            fetch_data()
            db.cnxn.close()
            messagebox.showinfo("Delete", "Employee successfully Deleted")

        except Exception as es:
            messagebox.showerror("Error", f'Due to:{str(es)}', parent=emp)


def clear_data():
    var_dep.set("Select Department")
    var_name.set("")
    var_designation.set("")
    var_email.set("")
    var_address.set("")
    var_marital.set("Married")
    var_dob.set("")
    var_doj.set("")
    var_idproofcombo.set("Id Proof")
    var_idproof.set("")
    var_gender.set("")
    var_phone.set("")
    var_city.set("")
    var_salary.set("")
    var_dleft.set("")
    var_search_id.set("")
    var_logintype.set("Login Type")
    var_passwords.set("")


def search_data():
    global cnxn
    if var_search_id.get() == '':
        messagebox.showerror("Error", "Enter valid Id to search")
    else:
        try:
            db = Database()
            cnxn = pyodbc.connect(db.cnxn_str)
            db.cursor = cnxn.cursor()
            db.cursor.execute("select * from Employees where id LIKE '%" + var_search_id.get() + "%'")
            data = db.cursor.fetchall()
            if len(data) != 0:
                employee_table.delete(*employee_table.get_children())
                for i in data:
                    employee_table.insert("", END, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
                                                           i[10], i[11], i[12], i[13], i[14],i[15],i[16]))
                db.cnxn.commit()
            else:
                messagebox.showerror("Warning", "This Id is not in the record")

            db.cnxn.close()

        except Exception as es:
            messagebox.showerror("Error", f'Due to:{str(es)}', parent=emp)


def save():
    if len(employee_table.get_children()) < 1:
        messagebox.showinfo("Error", "No data available")
        return
    file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save Excel",
                                        filetypes=(("Excel File", "*.xlsx"),
                                                   ("All Files", "*.*")))
    wb = Workbook()
    ws = wb.active
    cols = ['Department', 'Name', 'Designation', 'Email', 'Address', 'Marital_Status', 'DOB', 'D_joined',
                    'id_type',
                    'id', 'Gender', 'Phone', 'city', 'Salary', 'D_left','Login_Type', 'Password']
    ws.append(cols)
    for i in employee_table.get_children():
        data = employee_table.item(i)['values']
        ws.append(data)
    wb.save(file)
    messagebox.showinfo("Saved", "Record saved successfully")


def logout():
    sure = messagebox.askyesno("Exit", "Are you sure you want to Logout?", parent=emp)
    if sure == True:
        emp.destroy()
        os.system("employee.py")


lbl_title = Label(emp, text="Employee Management Admin Page", font=('times new roman', 30, 'bold'), fg='darkblue',
                  bg="lightblue")
lbl_title.place(x=0, y=0, width=1300, height=50)
button_logout = Button(emp, text='Logout', command=logout,font=('arial', 10, 'bold'), width=10, bg='brown', fg='white',
                       cursor='hand2')
button_logout.place(x=2, y=4)
# logo
logoimage = Image.open(
            'F:\project\electrochip-html\electrochip-html\images\Screenshot_2022-07-13_081400-removebg-preview.png')
logoimage = logoimage.resize((50, 50))
photo = ImageTk.PhotoImage(logoimage)

logo = Label(emp, image=photo, bg="lightblue")
logo.place(x=270, y=50, width=50, height=50)

img_frame = Frame(emp, bd=2, relief=RIDGE, bg="#d4d9cd")
img_frame.place(x=0, y=50, width=1300, height=85)

# 1st image
img1 = Image.open('F:\project\ShopManagement\images\psettinground.jpg')
img1 = img1.resize((200, 100))
photo1in = ImageTk.PhotoImage(img1)

img_photo = Label(img_frame, image=photo1in, bg="#d4d9cd")
img_photo.place(x=0, y=0, width=200, height=84)

# 2nd image
img2 = Image.open('F:\project\ShopManagement\images\imageside.png')
img2 = img2.resize((230, 100))
photo2nd = ImageTk.PhotoImage(img2)

img2photo = Label(img_frame, image=photo2nd, bg="#d4d9cd")
img2photo.place(x=200, y=0, width=230, height=85)

# 3rd image
img3 = Image.open('F:\project\ShopManagement\images\photoshop.jpg')
img3 = img3.resize((250, 100))
photo3rd = ImageTk.PhotoImage(img3)

img3rdphoto = Label(img_frame, image=photo3rd, bg="white")
img3rdphoto.place(x=431, y=0, width=250, height=85)

# 4rd image
img4 = Image.open('F:\project\ShopManagement\images\phtoset.jpg')
img4 = img4.resize((250, 100))
photo4rd = ImageTk.PhotoImage(img4)

img4rdphoto = Label(img_frame, image=photo4rd, bg="white")
img4rdphoto.place(x=682, y=0, width=250, height=85)

# 5th image
img5 = Image.open('F:\project\ShopManagement\images\hardware.png')
img5 = img5.resize((280, 100))
photo5th = ImageTk.PhotoImage(img5)

img5thphoto = Label(img_frame, image=photo5th, bg="white")
img5thphoto.place(x=933, y=0, width=280, height=85)

# 6th image
img6 = Image.open('F:\project\ShopManagement\images\screwphto.jpg')
img6 = img6.resize((100, 100))
photo6th = ImageTk.PhotoImage(img6)

img6thphoto = Label(img_frame, image=photo6th, bg="white")
img6thphoto.place(x=1200, y=0, width=100, height=85)

# main frame
main_frame = Frame(emp, bd=2, relief=RIDGE, bg="#d4d9cd")
main_frame.place(x=0, y=135, width=1300, height=600)

# upperFrame
upper_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, bg="#d4d9cd", text="Employee Information",
                         font=('times new roman', 11, 'bold'), fg='darkblue')
upper_frame.place(x=5, y=10, width=1290, height=280)

global cal


# triggered when value of string variable changes
def my_upd(*args):
    dt = cal.get_date()
    ssv = dt.strftime("%d-%B-%Y")  # changing the format


db = Database()
cnxn = pyodbc.connect(db.cnxn_str)
db.cursor = cnxn.cursor()
global my_values
my_values = db.cursor.execute('select distinct  Departments from DepartmentRole')
list_dep = [r for r, in my_values]
list2 = []


def my_list(*args):
    global list2
    query = "select Designation from DepartmentRole where Departments='" + var_dep.get() + "'"
    my_data = db.cursor.execute(query)
    list2 = [r for r, in my_data]
    combo_designation['values'] = list2


global combo_designation
global combo_dep


def edit_deps():

    global list_dep
    global list2
    global my_values
    if var_dep.get() not in combo_dep['values']:
        combo_dep['values'] += (var_dep.get(),)
        my_values = db.cursor.execute("insert into DepartmentRole (Departments)values(')" + var_dep.get() + "'")
        list_dep = [r for r, in my_values]
        list2 = []


def dep_role():

    global list2
    global list_dep
    global my_values
    combo_designation['values'] = (var_designation.get(),)
    my_values = db.cursor.execute("insert into DepartmentRole (Designation)values(')" + var_designation.get() + "'")
    list2 = [r for r, in my_values]
    combo_designation['values'] = list2


def profession():
    # Professional frame
    prof_frame = LabelFrame(upper_frame, bd=2, relief=RIDGE, bg="#d4d9cd", text="Professional Details",
                            font=('times new roman', 10, 'bold'), fg='darkblue')
    prof_frame.place(x=2, y=2, width=290, height=255)

    # Department
    lbl_dep = Label(prof_frame, text="Department", font=('arial', 11, 'bold'), bg='#d4d9cd')
    lbl_dep.grid(row=0, column=0, padx=1, sticky=W)

    global combo_dep
    combo_dep = ttk.Combobox(prof_frame, textvariable=var_dep, font=('times new roman', 12), width=15, values=list_dep)
    combo_dep.grid(row=0, column=1, padx=1, pady=2, sticky=W)

    button_changes = Button(prof_frame, text='Edit', command=edit_deps, font=('arial', 8, 'bold'), width=5, bg='light blue',
                            fg='blue', cursor='hand2')
    button_changes.place(x=234, y=2)
    # designation
    lbl_designation = Label(prof_frame, text="Designation", font=('arial', 11, 'bold'), bg='#d4d9cd')
    lbl_designation.grid(row=1, column=0, padx=1, pady=7, sticky=W)
    global combo_designation
    combo_designation = ttk.Combobox(prof_frame, textvariable=var_designation, font=('times new roman', 12), width=15,
                                     values=list2)
    combo_designation.grid(row=1, column=1, padx=1, pady=7, sticky=W)
    var_dep.trace('w', my_list)
    button_changes = Button(prof_frame, text='Edit', command=dep_role, font=('arial', 8, 'bold'), width=5, bg='light blue',
                            fg='blue',cursor='hand2')
    button_changes.place(x=234, y=35)
    # Salary
    lbl_BasicSalary = Label(prof_frame, text="Salary(B)", font=('arial', 11, 'bold'), bg='#d4d9cd')
    lbl_BasicSalary.grid(row=2, column=0, padx=1, pady=7, sticky=W)
    txt_BasicSalary = ttk.Entry(prof_frame, textvariable=var_salary, width=22, font=('arial', 11))
    txt_BasicSalary.grid(row=2, column=1, padx=1, pady=7)
    # Dofjoin
    lbl_joinedDate = Label(prof_frame, text="D_Joined", font=('arial', 11, 'bold'), bg='#d4d9cd')
    lbl_joinedDate.grid(row=3, column=0, padx=1, pady=7, sticky=W)
    cal=DateEntry(prof_frame, selectmode='day', textvariable=var_doj,width=27)
    cal.grid(row=3, column=1, padx=1, pady=7, sticky=W)

    #type employee
    lbl_log = Label(prof_frame, text="Login Type", font=('arial', 11, 'bold'), bg='#d4d9cd')
    lbl_log.grid(row=4, column=0, padx=1, pady=7, sticky=W)
    combo_dep = ttk.Combobox(prof_frame, textvariable=var_logintype, font=('arial', 11,), width=20,
                             state='readonly')
    combo_dep['value'] = ('Type', 'Employee', 'Sales', 'Inventory', 'Admin')
    combo_dep.grid(row=4, column=1, padx=1, pady=7, sticky=W)

    def backs():
        prof_frame.destroy()


    # load the image
    img = Image.open(r"F:\project\ShopManagement\images\back_conn.png")
    img = img.resize((30, 30))  # adjust the size of the image
    img = ImageTk.PhotoImage(img)

    # create the button with the image
    button_back = Button(prof_frame, image=img, command=backs, width=30, height=30, bd=0, cursor='hand2',
                         bg="#d4d9cd")
    button_back.image = img  # keep a reference to the image to prevent garbage collection
    button_back.grid(row=5, column=1, padx=1, pady=7, sticky=W)


button_professional = Button(upper_frame, text='Job Info', command=profession, font=('arial', 12, 'bold'), width=10,
                             bg='#dbb156',cursor='hand2')
button_professional.place(x=4, y=2)

color_frame = LabelFrame(upper_frame, bd=2, relief=RIDGE, bg="#FAFAD2")
color_frame.place(x=1, y=35, width=880, height=220)


def personal():
    # Personal Info
    personal_frame = LabelFrame(upper_frame, bd=2, relief=RIDGE, bg="#d4d9cd", text="Personal Details",
                                font=('times new roman', 10, 'bold'), fg='darkblue')
    personal_frame.place(x=300, y=2, width=310, height=255)
    # name
    lbl_name = Label(personal_frame, text="Name", font=('arial', 11, 'bold'), bg='#d4d9cd')
    lbl_name.grid(row=0, column=0, padx=1, pady=2, sticky=W)
    txt_name = ttk.Entry(personal_frame, textvariable=var_name, width=22, font=('arial', 11))
    txt_name.grid(row=0, column=1, padx=1, pady=2)
    # NIC
    combo_NIC = ttk.Combobox(personal_frame, textvariable=var_idproofcombo, font=('arial', 11, 'bold'), width=10,
                             state='readonly')
    combo_NIC['value'] = ('Id Type', 'NIC', 'License')
    combo_NIC.current(0)
    combo_NIC.grid(row=1, column=0, padx=1, pady=7, sticky=W)

    txt_NIC = ttk.Entry(personal_frame, textvariable=var_idproof, width=22, font=('arial', 11))
    txt_NIC.grid(row=1, column=1, padx=1, pady=7)

    # DOB
    lbl_dob = Label(personal_frame, text="DOB", font=('arial', 11, 'bold'), bg='#d4d9cd')
    lbl_dob.grid(row=2, column=0, padx=1, pady=7, sticky=W)
    cal=DateEntry(personal_frame,selectmode='day', textvariable=var_dob, width=27)
    cal.grid(row=2, column=1, padx=1, pady=7, sticky=W)
    # Gender
    lbl_Gender = Label(personal_frame, text="Gender", font=('arial', 11, 'bold'), bg='#d4d9cd')
    lbl_Gender.grid(row=3, column=0, padx=1, pady=7, sticky=W)

    combo_Gender = ttk.Combobox(personal_frame, textvariable=var_gender, font=('times new roman', 12), width=20,
                                state='readonly')
    combo_Gender['value'] = ('Male', 'Female', 'Other')
    combo_Gender.current(0)
    combo_Gender.grid(row=3, column=1, padx=1, pady=7, sticky=W)
    # maritalStatus
    lbl_marital = Label(personal_frame, text="Marital Status", font=('arial', 11, 'bold'), bg='#d4d9cd')
    lbl_marital.grid(row=4, column=0, padx=1,pady=7, sticky=W)

    combo_marital = ttk.Combobox(personal_frame, textvariable=var_marital, font=('times new roman', 12), width=20,
                                 state='readonly')
    combo_marital['value'] = ('Married', 'UnMarried')
    combo_marital.current(0)
    combo_marital.grid(row=4, column=1, padx=1, pady=7, sticky=W)

    def backs():
        personal_frame.destroy()

    # load the image
    img = Image.open(r"F:\project\ShopManagement\images\back_conn.png")
    img = img.resize((30, 30))  # adjust the size of the image
    img = ImageTk.PhotoImage(img)

    # create the button with the image
    button_back = Button(personal_frame, image=img, command=backs, width=30, height=30, bd=0, cursor='hand2',
                         bg="#d4d9cd")
    button_back.image = img  # keep a reference to the image to prevent garbage collection
    button_back.grid(row=5, column=1, padx=1, pady=7, sticky=W)


button_personal = Button(upper_frame, text='Personal Info', command=personal, font=('arial', 12, 'bold'), width=12,
                         bg='#dbb156', cursor='hand2')
button_personal.place(x=300, y=2)


def contact():
    # Contact Info
    contact_frame = LabelFrame(upper_frame, bd=2, relief=RIDGE, bg="#d4d9cd", text="Contact Details", font=('times new roman', 10, 'bold'),
                               fg='darkblue')
    contact_frame.place(x=620, y=2, width=268, height=255)
    # Phone
    lbl_phone = Label(contact_frame, text="Phone No", font=('arial', 11, 'bold'), bg='#d4d9cd')
    lbl_phone.grid(row=0, column=0, padx=1, pady=2, sticky=W)
    txt_phone = ttk.Entry(contact_frame, textvariable=var_phone, width=22, font=('arial', 11))
    txt_phone.grid(row=0, column=1, padx=1, pady=2)

    # email
    lbl_email = Label(contact_frame, text="Email", font=('arial', 11, 'bold'), bg='#d4d9cd')
    lbl_email.grid(row=1, column=0, padx=1, pady=7, sticky=W)
    txt_email = ttk.Entry(contact_frame, textvariable=var_email, width=22, font=('arial', 11))
    txt_email.grid(row=1, column=1, padx=1, pady=7)
    # address
    lbl_address = Label(contact_frame, text="Address", font=('arial', 11, 'bold'), bg='#d4d9cd')
    lbl_address.grid(row=2, column=0, padx=1, pady=7, sticky=W)
    txt_address = ttk.Entry(contact_frame, textvariable=var_address, width=22, font=('arial', 11))
    txt_address.grid(row=2, column=1, padx=1, pady=7)
    # City
    lbl_City = Label(contact_frame, text="City", font=('arial', 11, 'bold'), bg='#d4d9cd')
    lbl_City.grid(row=3, column=0, padx=1, pady=7, sticky=W)
    txt_City = ttk.Entry(contact_frame, textvariable=var_city, width=22, font=('arial', 11))
    txt_City.grid(row=3, column=1, padx=1, pady=7)
    #password
    lbl_pw = Label(contact_frame, text="Password", font=('arial', 11, 'bold'), bg='#d4d9cd')
    lbl_pw.grid(row=4, column=0, padx=1, pady=7, sticky=W)
    txt_pw = ttk.Entry(contact_frame, textvariable=var_passwords, width=22, font=('arial', 11))
    txt_pw.grid(row=4, column=1, padx=1, pady=7)

    def backs():
        contact_frame.destroy()

    # load the image
    img = Image.open(r"F:\project\ShopManagement\images\back_conn.png")
    img = img.resize((30, 30))  # adjust the size of the image
    img = ImageTk.PhotoImage(img)

    # create the button with the image
    button_back = Button(contact_frame, image=img, command=backs, width=30, height=30, bd=0, cursor='hand2',
                         bg="#d4d9cd")
    button_back.image = img  # keep a reference to the image to prevent garbage collection
    button_back.grid(row=5, column=1, padx=1, pady=7, sticky=W)


button_personal = Button(upper_frame, text='Contact Info', command=contact, font=('arial', 12, 'bold'), width=12,
                         bg='#dbb156', cursor='hand2')
button_personal.place(x=620, y=2)


# employee image
employee_photo = Image.open('F:\project\electrochip-html\electrochip-html\images\employeephoto.jpg')
employee_photo = employee_photo.resize((130, 200))
photoMask = ImageTk.PhotoImage(employee_photo)

photo_mask = Label(upper_frame, image=photoMask, bg='#d4d9cd')
photo_mask.place(x=880, y=0, width=180, height=220)

# Button frame
button_frame = Frame(main_frame, relief=RIDGE, bg="#d4d9cd")
button_frame.place(x=1050, y=30, width=180, height=240)

button_add = Button(button_frame, text='Add', command=add_data, font=('arial', 15, 'bold'), width=12, bg='green',
                    fg='white', cursor='hand2')
button_add.grid(row=0, column=0, padx=1, pady=5)

button_update = Button(button_frame, text='Update', command=update_data, font=('arial', 15, 'bold'), width=12,
                       bg='lightblue', fg='purple', cursor='hand2')
button_update.grid(row=1, column=0, padx=1, pady=5)

button_delete = Button(button_frame, text='Delete', command=delete_data, font=('arial', 15, 'bold'), width=12, bg='red',
                       fg='white', cursor='hand2')
button_delete.grid(row=2, column=0, padx=1, pady=5)

button_clear = Button(button_frame, command=clear_data, text='Clear', font=('arial', 15, 'bold'), width=12,bg='brown',
                      fg='white', cursor='hand2')
button_clear.grid(row=3, column=0, padx=1, pady=5)

# downFrame
down_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, bg="#d4d9cd", text="Employee Information Table",
                        font=('times new roman', 11, 'bold'), fg='darkblue')
down_frame.place(x=5, y=290, width=1290, height=250)
# search frame
search_frame = LabelFrame(down_frame, bd=2, relief=RIDGE, bg="#d4d9cd", text="Search Employee Information",
                          font=('times new roman', 11, 'bold'), fg='darkblue')
search_frame.place(x=0, y=0, width=1285, height=60)

search_by = Label(search_frame, text="Search by", font=('arial', 11, 'bold'), bg='#d4d9cd')
search_by.grid(row=0, column=0, padx=2, pady=2, sticky=W)

var_search_id = StringVar()


# search

txt_NIC = ttk.Entry(search_frame, textvariable=var_search_id, width=22, font=('arial', 11))
txt_NIC.grid(row=0, column=2, padx=4, pady=2, sticky=W)


button_search = Button(search_frame, text='Search', command=search_data,font=('arial', 10, 'bold'), width=10, bg='brown'
                       , fg='white', cursor='hand2')
button_search.grid(row=0, column=3, padx=4, pady=3)

button_showall = Button(search_frame, text='Show All', command=fetch_data,font=('arial', 10, 'bold'), width=10,
                        bg='light blue',  fg='black', cursor='hand2')
button_showall.grid(row=0, column=4, padx=4, pady=3)
# save button
button_report = Button(search_frame, text='Export', command=save, font=('arial', 10, 'bold'), width=10,
                       bg='#8f5d36', fg='black', cursor='hand2')
button_report.grid(row=0, column=5, padx=4, pady=3)

stayHome = Label(search_frame, text=" View Employee", font=('Times New Roman', 20, 'bold'), bg='#d4d9cd', fg='red')
stayHome.place(x=600, y=0, width=250, height=30)


def pie_chart():
    # Get all the values in the "Department", "Designation", and "Basic Salary" columns
    values = [(employee_table.item(child)["values"][0], employee_table.item(child)["values"][2],
               float(employee_table.item(child)["values"][13])) for child in employee_table.get_children()]
    # Count the frequency of each department
    counts_department = Counter([value[0] for value in values])
    # Count the frequency of each designation and get the sum of basic salaries for each designation
    counts_designation = {}
    for value in values:
        if value[1] not in counts_designation:
            counts_designation[value[1]] = {"count": 1, "basic_salary_sum": value[2]}
        else:
            counts_designation[value[1]]["count"] += 1
            counts_designation[value[1]]["basic_salary_sum"] += value[2]
    # Create a list of department labels and corresponding counts
    department_labels = list(counts_department.keys())
    department_sizes = list(counts_department.values())
    # Create a list of designation labels and corresponding counts
    designation_labels = list(counts_designation.keys())
    designation_sizes = [counts_designation[designation]["count"] for designation in designation_labels]
    # Create a list of basic salary sums for each designation
    designation_basic_salary_sums = [counts_designation[designation]["basic_salary_sum"] for designation in
                                     designation_labels]
    # Create the pie chart for departments, designations, and basic salary by designation
    fig, (ax1, ax2, ax3) = plt.subplots(ncols=1, nrows=3, figsize=(50, 40), gridspec_kw={"height_ratios": [3, 3, 3]})
    plt.subplots_adjust(hspace=0.5)
    ax1.pie(department_sizes, labels=department_labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    ax1.set_title('Employees by Departments')
    ax2.pie(designation_sizes, labels=designation_labels, autopct='%1.1f%%', startangle=90)
    ax2.axis('equal')
    ax2.set_title('Employees by Designations')
    ax3.bar(designation_labels, designation_basic_salary_sums)
    ax3.set_xlabel('Designation')
    ax3.set_ylabel('Basic Salary Sum - LKR')
    ax3.set_title('Basic Salary by Designation')
    plt.show()

 # Create the image button
search_photo = Image.open('F:\project\ShopManagement\images\cskarrowdown.png')
search_photo = search_photo.resize((50, 30))
searchmask = ImageTk.PhotoImage(search_photo)
imagesearch = tk.Button(search_frame, image=searchmask, bg='#d4d9cd', command=pie_chart, cursor='hand2', bd=0)
imagesearch.place(x=860, y=1, width=50, height=38)
imagesearch.image = searchmask
# employee table-table frame
table_frame = Frame(search_frame, bd=3, relief=RIDGE, bg="#d4d9cd")
table_frame.place(x=0, y=60, width=995, height=230)


# employee table-table frame
table_frame = Frame(down_frame, bd=3, relief=RIDGE, bg="#d4d9cd")
table_frame.place(x=0, y=60, width=1285, height=150)


scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

employee_table = ttk.Treeview(table_frame, columns=("Department", "Name", "Designation", "Email", "Address"
                                                                 , "Marital_Status", "DOB", "D_joined", "id_type", "id",
                                                    "Gender", "Phone", "city", "Salary", "D_left", "Login_Type","Password"),
                              xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

s = ttk.Style(employee_table)
s.theme_use("clam")

scroll_x.pack(side=BOTTOM, fill=X)
scroll_y.pack(side=RIGHT, fill=Y)

scroll_x.config(command=employee_table.xview)
scroll_y.config(command=employee_table.yview)

employee_table.heading("Department", text="Department")
employee_table.heading("Name", text="Name")
employee_table.heading("Designation", text="Designation")
employee_table.heading("Email", text="Email")
employee_table.heading("Address", text="Address")
employee_table.heading("Marital_Status", text="Marital Status")
employee_table.heading("DOB", text="DOB")
employee_table.heading("D_joined", text="D_Joined")
employee_table.heading("id_type", text="ID Type")
employee_table.heading("id", text="ID")
employee_table.heading("Gender", text="Gender")
employee_table.heading("Phone", text="Phone No")
employee_table.heading("city", text="City")
employee_table.heading("Salary", text="Salary")
employee_table.heading("D_left", text="D_left")
employee_table.heading("Login_Type", text="Login_Type")
employee_table.heading("Password", text="Password")

employee_table['show'] = "headings"
employee_table.column("Department", width=100)
employee_table.column("Name", width=200)
employee_table.column("Designation", width=150)
employee_table.column("Email", width=200)
employee_table.column("Address", width=200)
employee_table.column("Marital_Status", width=100)
employee_table.column("DOB", width=150)
employee_table.column("D_joined", width=150)
employee_table.column("id_type", width=100)
employee_table.column("id", width=100)
employee_table.column("Gender", width=80)
employee_table.column("Phone", width=150)
employee_table.column("city", width=150)
employee_table.column("Salary", width=100)
employee_table.column("D_left", width=150)
employee_table.column("Login_Type", width=100)
employee_table.column("Password", width=100)


employee_table.pack(fill=BOTH,expand=1)
employee_table.bind("<ButtonRelease-1>", get_cursor)
fetch_data()


emp.mainloop()



