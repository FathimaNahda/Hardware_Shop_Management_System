from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import os
import tkinter as tk
import pyodbc
from openpyxl import Workbook
import matplotlib.pyplot as plt
from db import Database

emp = Tk()
emp.geometry("1300x600")
emp.title("View Employee")
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
var_logintype = StringVar()


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


global data

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


def search_data():
    if var_search_id.get() == "":
        messagebox.showerror("Error", "Search data is required")
        return
    db = Database()
    cnxn = pyodbc.connect(db.cnxn_str)
    db.cursor = cnxn.cursor()
    if var_search.get() == "Id":
        db.cursor.execute("select Department,Name,Designation,Email,Address,Marital_Status,DOB,D_joined,id_type,id,Gender, "
                       "Phone,city,Salary,D_left,Login_Type from Employees where id LIKE '%" + var_search_id.get() + "%'")
        data = db.cursor.fetchall()
        if len(data) != 0:
            employee_table.delete(*employee_table.get_children())
            for i in data:
                employee_table.insert("", END, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
                                                       i[10], i[11], i[12], i[13], i[14], i[15]))
            db.cnxn.commit()

    elif var_search.get() == "Department":
        db.cursor.execute("select Department,Name,Designation,Email,Address,Marital_Status,DOB,D_joined,id_type,id,Gender, "
                       "Phone,city,Salary,D_left,Login_Type from Employees where Department LIKE '%" + var_search_id.get() + "%'")
        data = db.cursor.fetchall()
        if len(data) != 0:
            employee_table.delete(*employee_table.get_children())
            for i in data:
                employee_table.insert("", END, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
                                                       i[10], i[11], i[12], i[13], i[14], i[15]))
            db.cnxn.commit()
    elif var_search.get() == "Designation":
        db.cursor.execute("select Department,Name,Designation,Email,Address,Marital_Status,DOB,D_joined,id_type,id,Gender, "
                       "Phone,city,Salary,D_left,Login_Type from Employees where Designation  LIKE '%" + var_search_id.get() + "%'")
        data = db.cursor.fetchall()
        if len(data) != 0:
            employee_table.delete(*employee_table.get_children())
            for i in data:
                employee_table.insert("", END, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
                                                       i[10], i[11], i[12], i[13], i[14], i[15]))
            db.cnxn.commit()
    else:
        messagebox.showerror("Warning", "Invalid Search record")

    db.cnxn.close()


def save():
    if len(employee_table.get_children())< 1:
        messagebox.showinfo("Error", "No data available")
        return
    file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save Excel",
                                        filetypes=(("Excel File", "*.xlsx"),
                                                   ("All Files", "*.*")))
    wb = Workbook()
    ws = wb.active
    cols = ['Department', 'Name', 'Designation', 'Email', 'Address', 'Marital_Status', 'DOB', 'D_joined', 'id_type',
                    'id', 'Gender', 'Phone', 'city', 'Salary', 'D_left']
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


def clear():
    var_search_id.set("")
    var_search.set("Search by ")


lbl_title = Label(emp, text="View Employee Details", font=('times new roman', 30, 'bold'), fg='darkblue',
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
main_frame = Frame(emp, bd=3, relief=RIDGE, bg="#d4d9cd")
main_frame.place(x=0, y=135, width=1300, height=500)

# downFrame
down_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, bg="#d4d9cd", text="Employee Information Table",
                        font=('times new roman', 11, 'bold'), fg='darkblue')
down_frame.place(x=5, y=10, width=1290, height=460)

stayHome = Label(down_frame, text="Employee Information", font=('Times New Roman', 20, 'bold'), bg='#d4d9cd', fg='red')
stayHome.place(x=470, y=0, width=300, height=30)
# searchframe
search_frame = LabelFrame(down_frame, bd=4, relief=RIDGE, bg="#d4d9cd", text="Search Employee Information",
                          font=('times new roman', 11, 'bold'), fg='darkblue')
search_frame.place(x=0, y=30, width=1285, height=100)

search_by = Label(search_frame, text="Search by", font=('arial', 11, 'bold'), bg='#d4d9cd')
search_by.grid(row=0, column=0, padx=2, pady=2, sticky=W)
var_search = StringVar()
combo_code = ttk.Combobox(search_frame, textvariable=var_search, font=('times new roman', 10), width=15)
combo_code['value'] = ('Id', 'Department', 'Designation')
combo_code.grid(row=0, column=1, padx=2, pady=4, sticky=W)

var_search_id = StringVar()

# search

txt_NIC = ttk.Entry(search_frame, textvariable=var_search_id, width=22, font=('arial', 11))
txt_NIC.grid(row=0, column=2, padx=4, pady=2, sticky=W)


# search button
button_search = Button(search_frame, text='Search', command=search_data, font=('arial', 10, 'bold'), width=10, bg='brown'
                       , fg='white', cursor='hand2')
button_search.grid(row=0, column=3, padx=4, pady=3)

# display all button
button_showall = Button(search_frame, text='Show All', command=fetch_data,font=('arial', 10, 'bold'), width=10,
                        bg='light blue',  fg='black', cursor='hand2')
button_showall.grid(row=0, column=4, padx=4, pady=3)

# save button
button_report = Button(search_frame, text='Export', command=save,font=('arial', 10, 'bold'), width=10,
                       bg='brown', fg='white', cursor='hand2')
button_report.grid(row=0, column=5, padx=4, pady=3)

button_clear = Button(search_frame, command=clear, text='Clear', font=('arial', 10, 'bold'), width=10,bg='grey',
                      fg='black', cursor='hand2')
button_clear.grid(row=0, column=6, padx=4, pady=3)


def pie_chart():
    # Check if the table has data
    if not employee_table.get_children():
        messagebox.showerror("Error", "Table data is required.")
        return
    # Fetch data from the treeview table
    data = []
    for row in employee_table.get_children():
        values = employee_table.item(row)['values']
        department = values[0]
        data.append(department)

    # Generate a dictionary with department counts
    department_count = {}
    for department in data:
        if department not in department_count:
            department_count[department] = 1
        else:
            department_count[department] += 1

    # Generate the pie chart
    plt.figure(figsize=(5, 5))
    plt.pie(list(department_count.values()), labels=list(department_count.keys()), autopct='%1.1f%%')
    plt.title("Number of Employees by Department")
    plt.show()

 # Create the image button
search_photo = Image.open('F:\project\ShopManagement\images\employees.png')
search_photo = search_photo.resize((200, 60))
searchmask = ImageTk.PhotoImage(search_photo)
imagesearch = tk.Button(search_frame, image=searchmask, bg='#d4d9cd', command=pie_chart, cursor='hand2', bd=0)
imagesearch.place(x=880, y=0, width=300, height=40)
imagesearch.image = searchmask

# employee table-table frame
table_frame = Frame(down_frame, bd=3, relief=RIDGE, bg="#d4d9cd")
table_frame.place(x=0, y=100, width=1285, height=300)


scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

employee_table = ttk.Treeview(table_frame, columns=("Department", "Name", "Designation", "Email", "Address",
                                                    "Marital_Status", "DOB", "D_joined", "id_type", "id",
                                                    "Gender", "Phone", "city", "Salary", "D_left", "Login_Type"),
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
employee_table.column("Login_Type", width=150)

employee_table.pack(fill=BOTH,expand=1)
employee_table.bind("<ButtonRelease-1>", get_cursor)
fetch_data()

emp.mainloop()
