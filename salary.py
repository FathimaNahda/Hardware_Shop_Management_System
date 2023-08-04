from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry
import random
import os
import pyodbc
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.pagesizes import A4
from tkinter import filedialog
import smtplib
from email.message import EmailMessage
import ssl
from openpyxl import Workbook
import matplotlib.pyplot as plt
from db import Database

emp = Tk()
emp.geometry("1300x1000")
emp.title("Employee Salary Management")
emp.resizable(0,0)

# variables
var_id = StringVar()
var_name = StringVar()
var_designation = StringVar()
var_email = StringVar()
var_department = StringVar()
date_var = StringVar()
var_salary = IntVar()
var_day = StringVar()
var_absents = StringVar()
var_deduction = IntVar()
var_salCode = IntVar()
var_bonus = IntVar()
var_grosPay = IntVar()
var_netPay = IntVar()
var_idcombo = StringVar()
var_rate = IntVar()
var_receiptno = StringVar()


def exit():
    emp.destroy()


emp.protocol("WM_DELETE_WINDOW", exit)


def search_data():
    global cnxn
    if var_id.get() == '':
        messagebox.showerror("Error", "Enter valid Id to search")
    else:
        try:
            db = Database()
            cnxn = pyodbc.connect(db.cnxn_str)
            db.cursor = cnxn.cursor()
            db.cursor.execute("select Name,Department,Designation,Email,Salary from Employees where id LIKE '%" +var_id.get() + "%'")
            data = db.cursor.fetchall()
            if len(data) != 0:
                employee_table.delete(*employee_table.get_children())
                for i in data:
                    var_name.set(i[0])
                    var_department.set(i[1])
                    var_designation.set(i[2])
                    var_email.set(i[3])
                    var_salary.set(i[4])
                db.cnxn.commit()

            else:
                messagebox.showerror("Warning", "This Id is not in the record")
            db.cnxn.close()

        except Exception as es:
            messagebox.showerror("Error", f'Due to:{str(es)}', parent=emp)


# triggered when value of string varaible changes
def my_upd(*args):
    dt = cal.get_date()
    ssv = dt.strftime("%d-%B-%Y")  # changing the format
    l1.config(text=ssv)


def Search_salary():
    db = Database()
    cnxn = pyodbc.connect(db.cnxn_str)
    db.cursor = cnxn.cursor()
    # Check if search value is empty
    if not var_numbersearch.get():
        messagebox.showerror("Warning", "Please enter a search value")
        return
    if var_search.get() == "Ref No":
        db.cursor.execute("select * from salary where RefNo LIKE '%" + var_numbersearch.get() + "%'")
        data = db.cursor.fetchall()
        if len(data) != 0:
            employee_table.delete(*employee_table.get_children())
            for i in data:
                employee_table.insert("", END, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
                                                       i[10], i[11], i[12], i[13], i[14], i[15]))
            db.cnxn.commit()

    elif var_search.get() == "Id":
        db.cursor.execute("select * from salary where id LIKE '%" + var_numbersearch.get() + "%'")
        data = db.cursor.fetchall()
        if len(data) != 0:
            employee_table.delete(*employee_table.get_children())
            for i in data:
                employee_table.insert("", END, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
                                                       i[10], i[11], i[12], i[13], i[14], i[15]))
            db.cnxn.commit()
    elif var_search.get() == "Month":
        db.cursor.execute("select * from salary where MONTH(Date)  LIKE '%" + var_numbersearch.get() + "%'")
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


def fetch_data():
    db = Database()
    cnxn = pyodbc.connect(db.cnxn_str)
    db.cursor = cnxn.cursor()
    db.cursor.execute('select * from salary')

    data = db.cursor.fetchall()
    if len(data) != 0:
        # Sort data by date column
        data = sorted(data, key=lambda x: x[6], reverse=True)

        employee_table.delete(*employee_table.get_children())

        # Insert rows in reverse order
        for i in reversed(data):
            employee_table.insert("", 0, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10],
                                                 i[11], i[12], i[13], i[14], i[15]))

        db.cnxn.commit()
    db.cnxn.close()


def calsalary():

        groscal = IntVar()
        bs = var_salary.get()
        ot = var_deduction.get()
        rate = var_rate.get()
        ded = var_salCode.get()
        var_bonus.set((ot * rate))
        groscal = bs + var_bonus.get()
        var_grosPay.set(groscal)
        netcal = var_grosPay.get() - ded
        var_netPay.set(netcal)
        ref_pay = random.randint(20000, 709467)
        var_receiptno.set(str(ref_pay))


def savesal():
    my_style = ParagraphStyle('Para style', fontName="Times-Roman",
                              fontSize=12,
                              alignment=0,
                              borderWidth=0,
                              leading=20)
    width, height = A4
    text = textReceipt.get('1.0', END)
    if not text.strip():  # Check if text is empty or only contains whitespace
        messagebox.showerror("Error", "Receipt text is empty!")
        return
    text = text.replace('\n', '<BR/>')
    p1 = Paragraph(text, my_style)
    file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save PDF", filetypes=(("PDF File", "*.pdf"),
                                                                                             ("All Files", "*.*")))
    c = canvas.Canvas(file, pagesize=A4)
    p1.wrapOn(c, 400, 400)
    p1.drawOn(c, width-500, height-500)
    c.save()
    textReceipt.delete('1.0', END)


def clearal():
    var_idcombo.set("")
    var_id.set("")
    var_name.set("")
    var_department.set("")
    var_designation.set("")
    var_email.set("")
    var_salary.set(int())
    date_var.set("")
    var_day.set("")
    var_absents.set("")
    var_deduction.set(int())
    var_salCode.set(int())
    var_bonus.set(int())
    var_grosPay.set(int())
    var_netPay.set(int())
    var_rate.set(int())
    var_receiptno.set("")
    var_numbersearch.set("")
    textReceipt.delete(1.0, END)
    textReceipt.delete(1.0, END)


def print():
    if var_id.get() == "" or var_name.get() == "" or var_department.get() == "" or \
            var_designation.get() == "" or var_email.get() == "" or var_salary.get() == "" or date_var.get() == "" or\
            var_day.get() == "" or var_absents.get() == "" or var_deduction.get() == "" or var_rate.get() == "" or\
            var_bonus.get() == "" or var_grosPay.get() == "" or var_salCode.get() == "" or var_netPay.get() == "" or \
            var_receiptno.get() == "":
        messagebox.showerror("Error", "All fields are required")

    # check if fields with digits do not contain strings
    elif (not str(var_salary.get()).isnumeric() or not str(var_absents.get()).isnumeric() or
          not str(var_deduction.get()).isnumeric() or not str(var_rate.get()).isnumeric() or
          not str(var_bonus.get()).isnumeric() or not str(var_grosPay.get()).isnumeric() or
          not str(var_netPay.get()).isnumeric() or not str(var_receiptno.get()).isnumeric()):
           messagebox.showerror("Error", "Fields with digits can only contain numbers")
    else:
        try:
            db = Database()
            cnxn = pyodbc.connect(db.cnxn_str)
            db.cursor = cnxn.cursor()
            db.cursor.execute("INSERT INTO salary VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (var_id.get(), var_name.get(), var_department.get(), var_designation.get(),
                            var_email.get(), var_salary.get(), date_var.get(), var_day.get(), var_absents.get(),
                            var_deduction.get(), var_rate.get(), var_bonus.get(), var_grosPay.get(),  var_salCode.get(),
                            var_netPay.get(), var_receiptno.get()))
            db.cnxn.commit()
            fetch_data()
            db.cnxn.close()
            messagebox.showinfo("Success", "Receipt printed successfully", parent=emp)
            textarea()

        except Exception as es:
            messagebox.showerror("Error", f'Due to:{str(es)}', parent=emp)


def delete():
    global cnxn, db
    if var_id.get() == "" or var_name.get() == "" or var_department.get() == "" or \
            var_designation.get() == "" or var_email.get() == "" or var_salary.get() == "" or date_var.get() == "" or \
            var_day.get() == "" or var_absents.get() == "" or var_deduction.get() == "" or var_rate.get() == "" or \
            var_bonus.get() == "" or var_grosPay.get() == "" or var_salCode.get() == "" or var_netPay.get() == "" or \
            var_receiptno.get() == "":
        messagebox.showerror("Error", "All fields are required")
    else:
        try:
            Delete = messagebox.askyesno('Delete', 'Are you sure delete this Salary Record?', parent=emp)
            if Delete > 0:
                db = Database()
                cnxn = pyodbc.connect(db.cnxn_str)
                db.cursor = cnxn.cursor()
                value = (var_id.get(),)
                db.cursor.execute("delete from salary where id=?", value)
            else:
                if not Delete:
                    return
            db.cnxn.commit()
            fetch_data()
            db.cnxn.close()
            messagebox.showinfo("Delete", "Record deleted successfully")

        except Exception as es:
            messagebox.showerror("Error", f'Due to:{str(es)}', parent=emp)


# calculator functions
operator = ''


def buttonClick(numbers):
    global operator
    operator = operator+numbers
    calculatorField.delete(0, END)
    calculatorField.insert(END, operator)


def clear():
    global operator
    operator = ''
    calculatorField.delete(0, END)


def answer():
    global operator
    result = str(eval(operator))
    calculatorField.delete(0, END)
    calculatorField.insert(0, result)
    operator = ''


def get_cursor(*args):
    cursor_row = employee_table.focus()
    content = employee_table.item(cursor_row)
    data = content['values']
    var_id.set(data[0])
    var_name.set(data[1])
    var_department.set(data[2])
    var_designation.set(data[3])
    var_email.set(data[4])
    var_salary.set(int(data[5]))
    date_var.set(data[6])
    var_day.set(data[7])
    var_absents.set(data[8])
    var_deduction.set(int(data[9]))
    var_rate.set(int(data[10]))
    var_bonus.set(int(data[11]))
    var_grosPay.set(int(data[12]))
    var_salCode.set(int(data[13]))
    var_netPay.set(int(data[14]))
    var_receiptno.set(data[15])
    textarea()


def textarea():
    textReceipt.insert(END, 'New Silver Line Traders (Pvt) Ltd\n')
    textReceipt.insert(END, '******************************************** \n')
    textReceipt.insert(END, 'Reference No:\t\t' + var_receiptno.get() + '\n')
    textReceipt.insert(END, 'Date:\t\t' + date_var.get() + '\n')
    textReceipt.insert(END, '*************************************\n')
    textReceipt.insert(END, 'Id:\t\t' + var_id.get() + '\n')
    textReceipt.insert(END, 'Name:\t\t' + var_name.get() + '\n')
    textReceipt.insert(END, 'Department:\t\t' + var_department.get() + '\n')
    textReceipt.insert(END, 'Designation:\t\t' + var_designation.get() + '\n')
    textReceipt.insert(END, 'Email:\t\t' + var_email.get() + '\n')
    textReceipt.insert(END, '************************************************************\n')
    textReceipt.insert(END, 'Basic Salary:\t\t' + 'Rs' + str(var_salary.get()) + '\n')
    textReceipt.insert(END, 'Work Days:\t\t' + var_day.get() + '\n')
    textReceipt.insert(END, 'Absent Days No:\t\t' + var_absents.get() + '\n')
    textReceipt.insert(END, 'Overtime Hours:\t\t' + str(var_deduction.get()) + '\n')
    textReceipt.insert(END, 'Overtime Rate:\t\t' + 'Rs' + str(var_rate.get()) + '\n')
    textReceipt.insert(END, 'OT:\t\t' + 'Rs' + str(var_bonus.get()) + '\n')
    textReceipt.insert(END, 'Gross Salary:\t\t' + 'Rs' + str(var_grosPay.get()) + '\n')
    textReceipt.insert(END, 'Deduction :\t\t' + 'Rs' + str(var_salCode.get()) + '\n')
    textReceipt.insert(END, 'Monthly Wage:\t\t' + 'Rs' + str(var_netPay.get()) + '\n')
    textReceipt.insert(END,  '\n')
    textReceipt.insert(END, "\n")
    textReceipt.insert(END, "We Value Your Service\n")
    textReceipt.insert(END, "Thank You!!\n")


def send():
    emp2 = Toplevel()
    emp2.title("Send Wage Receipt")
    emp2.config(bg="#d4d9cd")
    emp2.geometry('300x250+50+50')
    emp2.resizable(0, 0)

    # Logo image and icon
    logoimage = PhotoImage(file='F:\project\ShopManagement\images\send.png')
    emp2.iconphoto(False, logoimage)

    # Email recipient input field
    var_cont = StringVar()
    num_label = Label(emp2, text='Email:', font=('arial', 15, 'underline', 'bold'), bg='#d4d9cd')
    num_label.place(x=110, y=30)
    txt_no = ttk.Entry(emp2, textvariable=var_email, width=30, font=('arial', 12))
    txt_no.place(x=10, y=80)

    def nw_send():
        # Get the values of the receipt details
        reference_no = var_receiptno.get()
        date = date_var.get()
        id = var_id.get()
        name = var_name.get()
        department = var_department.get()
        designation = var_designation.get()
        email = var_email.get()
        salary = var_salary.get()
        work_days = var_day.get()
        absent_days = var_absents.get()
        overtime_hours = var_deduction.get()

        if var_email.get() == '':
            messagebox.showwarning("Error", "Email is required", parent=emp2)
            return False
        else:

            # Get the recipient email address
            recipient = var_email.get()
            # Create the email message body
            message_body = f'''New Silver Line Traders (Pvt) Ltd
******************************************
Reference No:\t{reference_no}
Date:\t\t\t{date}
******************************************
Id:\t\t\t\t{id}
Name:\t\t\t{name}
Department:\t\t{department}
Designation:\t\t{designation}
Email:\t\t\t{email}
******************************
Basic Salary:\t\tRs{salary}
Work Days:\t\t{work_days}
Absent Days No:\t\t{absent_days}
Overtime Hours:\t\t{overtime_hours}

We Value Your Service
Thank You!

*NOTE:This is a computer generated email and was sent for your information only.
'''

            # Create the email message object
            message = EmailMessage()
            message['From'] = 'n06131019@gmail.com'# Replace with your email address
            message['To'] = recipient
            message['Subject'] = 'Employee Wage Payment: New Silver Line Traders-Galle'
            message.set_content(message_body)

            # Send the email using SMTP
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as smtp:
                smtp.login('n06131019@gmail.com', 'kehqnqkbbjblfutu') # Replace with your email and app password
                smtp.send_message(message)

            messagebox.showinfo("Email", "Salary Receipt Sent Successfully")
            emp2.destroy()

    # Send button
    button_sendmail = Button(emp2, text='Send', command=nw_send, font=('arial', 10, 'bold'), width=10,
                             bg='light blue', fg='blue', relief=GROOVE)
    button_sendmail.place(x=100, y=130)

    emp2.mainloop()


def logout():
    sure = messagebox.askyesno("Exit", "Are you sure you want to Logout?", parent=emp)
    if sure == True:
        emp.destroy()
        os.system("employee.py")

db = Database()
cnxn = pyodbc.connect(db.cnxn_str)
db.cursor = cnxn.cursor()
global my_values
my_values = db.cursor.execute('select distinct id_type from Employees')
list_dep = [r for r, in my_values]
list2 = []


def my_list(*args):
    global list2
    query = "select id from Employees where id_type='" + var_idcombo.get() + "'"
    my_data = db.cursor.execute(query)
    list2 = [r for r, in my_data]
    sr_id['values'] = list2


def savelist():
    if len(employee_table.get_children()) < 1:
        messagebox.showinfo("Error", "No data available")
        return
    file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save Excel",
                                        filetypes=(("Excel File", "*.xlsx"),
                                                   ("All Files", "*.*")))
    wb = Workbook()
    ws = wb.active
    cols = ['Employee Id', 'Name', 'Department', 'Designation', 'Email', 'Salary', 'Date', 'WorkDays',
                'Absents', 'OT Hours', 'Rate', 'Bonus', 'Gross Pay', 'Deduction', 'Net Pay', 'Ref No']
    ws.append(cols)
    for i in employee_table.get_children():
        data = employee_table.item(i)['values']
        ws.append(data)
    wb.save(file)
    messagebox.showinfo("Saved", "Record saved successfully")


lbl_title = Label(emp, text="Employee Salary Management", font=('times new roman', 30, 'bold'), fg='darkblue',
                  bg="lightblue")
lbl_title.place(x=0, y=0, width=1300, height=50)
button_logout = Button(emp, text='Logout', command=logout, font=('arial', 10, 'bold'), width=10, bg='brown', fg='white',
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
upper_frame.place(x=2, y=10, width=680, height=200)

lbl_dep = Label(upper_frame, text="Employee Id", font=('arial', 11, 'bold'), bg='#d4d9cd')
lbl_dep.grid(row=0, column=0, padx=2, sticky=W)
combo_id = ttk.Combobox(upper_frame, textvariable=var_idcombo, font=('times new roman', 12), width=12, state='readonly',
                        values=list_dep)
combo_id.current(0)
combo_id.grid(row=0, column=0, padx=2, pady=2, sticky=W)

sr_id = ttk.Combobox(upper_frame, textvariable=var_id, font=('times new roman', 12), width=20, values=list2)
sr_id.grid(row=0, column=1, padx=1, pady=2, sticky=W)
var_idcombo.trace('w', my_list)

button_search = Button(upper_frame, text='Search', command=search_data, font=('arial', 10, 'bold'), width=10, bg='brown'
                       , fg='white', cursor='hand2')
button_search.grid(row=0, column=2, padx=6, pady=2)
# name
lbl_name = Label(upper_frame, text="Name", font=('arial', 11, 'bold'), bg='#d4d9cd')
lbl_name.grid(row=1, column=0, padx=2, pady=7, sticky=W)
txt_name = ttk.Entry(upper_frame, textvariable=var_name, width=22, font=('arial', 11))
txt_name.grid(row=1, column=1, padx=1, pady=10)
# department
lbl_name = Label(upper_frame, text="Department", font=('arial', 11, 'bold'), bg='#d4d9cd')
lbl_name.grid(row=1, column=2, padx=6, pady=7, sticky=W)
txt_name = ttk.Entry(upper_frame, textvariable=var_department, width=25, font=('arial', 11))
txt_name.grid(row=1, column=3, padx=1, pady=10)
# designation
lbl_designation = Label(upper_frame, text="Designation", font=('arial', 11, 'bold'), bg='#d4d9cd')
lbl_designation.grid(row=2, column=0, padx=2, pady=7, sticky=W)
txt_designation = ttk.Entry(upper_frame, textvariable=var_designation, width=22, font=('arial', 11))
txt_designation.grid(row=2, column=1, padx=1, pady=10)
# email
lbl_email = Label(upper_frame, text="Email", font=('arial', 11, 'bold'), bg='#d4d9cd')
lbl_email.grid(row=2, column=2, padx=6, pady=7, sticky=W)
txt_email = ttk.Entry(upper_frame, textvariable=var_email, width=25, font=('arial', 11))
txt_email.grid(row=2, column=3, padx=1, pady=10)
# Salary
lbl_BasicSalary = Label(upper_frame, text="Salary(B)", font=('arial', 11, 'bold'), bg='#d4d9cd')
lbl_BasicSalary.grid(row=3, column=0, padx=2, pady=7, sticky=W)
txt_BasicSalary = ttk.Entry(upper_frame, textvariable=var_salary, width=22, font=('arial', 11))
txt_BasicSalary.grid(row=3, column=1, padx=1, pady=10)

# sideFrame
side_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, bg="#d4d9cd", font=('times new roman', 11, 'bold'),
                        fg='darkblue')
side_frame.place(x=690, y=16, width=600, height=540)

# receipt frame
Receipt_frame = LabelFrame(side_frame, bd=2, relief=RIDGE, bg="#d4d9cd", font=('times new roman', 11, 'bold'),
                           fg='darkblue')
Receipt_frame.place(x=260, y=2, width=330, height=530)

lbl_Receipt = Label(Receipt_frame, text="Salary Details", font=('arial', 15, 'bold'), fg='#db8756', bg="#d4d9cd")
lbl_Receipt.grid(row=0, column=0, padx=90, sticky=W)

textReceipt = Text(Receipt_frame, font=('arial', 10, 'bold'), bd=3, width=330, height=355)
textReceipt.grid(row=1, column=0)

buttonFrame = LabelFrame(side_frame, relief=RIDGE, bg="#d4d9cd")
buttonFrame.place(x=2, y=200, width=250, height=120)

# buttons
button_save = Button(buttonFrame, text='Invoice Pdf', command=savesal, font=('arial', 10, 'bold'), width=12, bg='#73A16C',
                     cursor='hand2')
button_save.grid(row=1, column=0, padx=4, pady=15)

button_delete = Button(buttonFrame, text='Delete Record', command=delete, font=('arial', 10, 'bold'), width=12, bg='red',
                       fg='white', cursor='hand2')
button_delete.grid(row=0, column=1, padx=8, pady=17)

button_print = Button(buttonFrame, text=' Print Invoice', command=print, font=('arial', 10, 'bold'), width=12, bg='#F9E29C', cursor='hand2')
button_print.grid(row=0, column=0, padx=4, pady=17)

button_send = Button(buttonFrame, text='Send Email', command=send, font=('arial', 10, 'bold'), width=12,
                     bg='light blue', fg='purple', cursor='hand2')
button_send.grid(row=1, column=1, padx=8, pady=15)

# search receipt
search_frame = LabelFrame(side_frame, bd=2, relief=RIDGE, bg="#d4d9cd")
search_frame.place(x=2, y=340, width=251, height=190)

search_by = Label(search_frame, text="Search by:", font=('arial', 10, 'bold'), bg='#d4d9cd')
search_by.grid(row=0, column=0, padx=2, pady=6, sticky=W)

var_search = StringVar()
combo_code = ttk.Combobox(search_frame, textvariable=var_search, font=('times new roman', 10), width=15)
combo_code['value'] = ('Ref No', 'Id', 'Month')
combo_code.grid(row=1, column=0, padx=2, pady=8, sticky=W)

var_numbersearch = StringVar()
txt_adsearch = ttk.Entry(search_frame, textvariable=var_numbersearch, width=13, font=('arial', 11))
txt_adsearch.grid(row=1, column=1, padx=8, pady=8, sticky=W)

button_search = Button(search_frame, text='Search', command=Search_salary, font=('arial', 10, 'bold'),
                       width=12, bg='brown', fg='white', cursor='hand2')
button_search.grid(row=2, column=0, padx=2, pady=8, sticky=W)

button_showall = Button(search_frame, text='View All', command=fetch_data, font=('arial', 10, 'bold'), width=12,
                        bg='light blue',  fg='black', cursor='hand2')
button_showall.grid(row=2, column=1, padx=8, pady=10, sticky=W)

button_savetreeview = Button(search_frame, text='Export List', command=savelist, font=('arial', 10, 'bold'), width=12,
                             bg='#BDB76B',  fg='black', cursor='hand2')
button_savetreeview.grid(row=3, column=0, padx=2, pady=10, sticky=W)


def report():
    if not employee_table.get_children():
        messagebox.showerror("Error", "Table data is required")
    else:
        data = {}  # dictionary to store salary data for each employee id

        # Fetch data from the treeview table
        for child in employee_table.get_children():
            values = employee_table.item(child)['values']
            emp_id = values[0]
            salary = values[14]

            if emp_id not in data:
                data[emp_id] = {'x': [], 'y': []}
            data[emp_id]['x'].append(len(data[emp_id]['x']) + 1)  # assign a unique x-value for each record
            data[emp_id]['y'].append(salary)

        # Create a line chart for each employee
        fig, ax = plt.subplots()

        for emp_id, values in data.items():
            ax.plot(values['x'], values['y'], label=f'Employee {emp_id}')

            # Highlight specific data points
            for i in range(len(values['x'])):
                ax.scatter(values['x'][i], values['y'][i], c='red', marker='o')

        ax.set_xlabel('Record Number')
        ax.set_ylabel('Net Salary LKR')
        ax.set_title('Employee Salary Static View')
        ax.legend()

        # Display the chart
        plt.show()


button_report = Button(search_frame, text='Stat View', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=12,
                   command=report, cursor='hand2')
button_report.grid(row=3, column=1, padx=8, pady=10, sticky=W)


# calculator frame
cal_frame = LabelFrame(side_frame, bd=2, relief=RIDGE, bg="#d4d9cd", font=('times new roman', 11, 'bold'), fg='darkblue'
                       )
cal_frame.place(x=2, y=2, width=250, height=180)

calculatorField = Entry(cal_frame, font=('arial', 10, 'bold'), width=31, justify=RIGHT,bg="#d4d9cd", bd=0)
calculatorField.grid(row=0, column=0, columnspan=4)  # columnspan can add 4 button iside 1 column

# buttons calculator
buttonBracket = Button(cal_frame, text='()', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=6, padx=2,
                       command=lambda: buttonClick('()'), cursor='hand2')
buttonBracket.grid(row=1, column=0)

buttonper = Button(cal_frame, text='%', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=6, padx=2,
                   command=lambda: buttonClick('%'), cursor='hand2')
buttonper.grid(row=1, column=1)

buttondiv = Button(cal_frame, text='/', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=6, padx=2,
                   command=lambda: buttonClick('/'), cursor='hand2')
buttondiv.grid(row=1, column=2)

buttonback = Button(cal_frame, text='', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=6, padx=2,
                    command=lambda: buttonClick('x'), cursor='hand2')
buttonback.grid(row=1, column=3)

button7 = Button(cal_frame, text='7', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=6, padx=2,
                 command=lambda: buttonClick('7'), cursor='hand2')   # when click 7 pass the value-lamda keywrd
button7.grid(row=2, column=0)

button8 = Button(cal_frame, text='8', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=6, padx=2,
                 command=lambda: buttonClick('8'), cursor='hand2')
button8.grid(row=2, column=1)

button9 = Button(cal_frame, text='9', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=6, padx=2,
                 command=lambda: buttonClick('9'), cursor='hand2')
button9.grid(row=2, column=2)

buttonPlus = Button(cal_frame, text='+', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=6, padx=2,
                    command=lambda: buttonClick('+'), cursor='hand2')
buttonPlus.grid(row=2, column=3)

button4 = Button(cal_frame, text='4', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=6, padx=2,
                 command=lambda: buttonClick('4'), cursor='hand2')
button4.grid(row=3, column=0)

button5 = Button(cal_frame, text='5', font=('arial', 10, 'bold'), bg='Grey', bd=3, width=6, padx=2,
                 command=lambda: buttonClick('5'), cursor='hand2')
button5.grid(row=3, column=1)

button6 = Button(cal_frame, text='6', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=6, padx=2,
                 command=lambda: buttonClick('6'), cursor='hand2')
button6.grid(row=3, column=2)

buttonMinus = Button(cal_frame, text='-', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=6, padx=2,
                     command=lambda: buttonClick('-'), cursor='hand2')
buttonMinus.grid(row=3, column=3)

button1 = Button(cal_frame, text='1', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=6, padx=2,
                 command=lambda: buttonClick('1'), cursor='hand2')
button1.grid(row=4, column=0)

button2 = Button(cal_frame, text='2', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=6, padx=2,
                 command=lambda: buttonClick('2'), cursor='hand2')
button2.grid(row=4, column=1)

button3 = Button(cal_frame, text='3', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=6, padx=2,
                 command=lambda: buttonClick('3'), cursor='hand2')
button3.grid(row=4, column=2)

buttonmulti = Button(cal_frame, text='*', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=6, padx=2,
                     command=lambda: buttonClick('*'), cursor='hand2')
buttonmulti.grid(row=4, column=3)

buttonanswer = Button(cal_frame, text='Ans', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=6, padx=2,
                      command=answer, cursor='hand2')
buttonanswer.grid(row=5, column=0)

buttonpoint = Button(cal_frame, text='.', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=6, padx=2,
                     command=lambda: buttonClick('.'), cursor='hand2')
buttonpoint.grid(row=5, column=1)


button0 = Button(cal_frame, text='0', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=6, padx=2,
                 command=lambda: buttonClick('0'), cursor='hand2')
button0.grid(row=5, column=2)

buttonclr = Button(cal_frame, text='Clear', font=('arial', 10, 'bold'), bg='Grey', bd=2, width=6, padx=2,
                   command=clear, cursor='hand2')
buttonclr.grid(row=5, column=3)


# downFrame
down_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, bg="#d4d9cd", text="Salary Calculation",
                        font=('times new roman', 11, 'bold'), fg='darkblue')
down_frame.place(x=2, y=210, width=680, height=180)
# Date
lbl_name = Label(down_frame, text="Date:", font=('arial', 11, 'bold'), bg='#d4d9cd')
lbl_name.grid(row=0, column=0, padx=1, pady=4, sticky=W)

cal = DateEntry(down_frame, selectmode='day', textvariable=date_var)
cal.grid(row=0, column=1, padx=2, sticky=W)

l1 = Label(down_frame,bg='yellow')  # Label to display date
l1.grid(row=0, column=2, padx=2, pady=4, sticky=W)
date_var.trace('w', my_upd)  # on change of string variable

buttndate = Button(down_frame, text='Read', command=my_upd)
buttndate.grid(row=0, column=3)

buttnalt = Button(down_frame, text='Clear', command=lambda: cal.delete(0, 'end'))
buttnalt.grid(row=0, column=4)
# total workingdays
lbl_workingday = Label(down_frame, text="Total Days:", font=('arial', 11, 'bold'), bg='#d4d9cd')
lbl_workingday.grid(row=1, column=0, padx=2, pady=7, sticky=W)

combo_dep = ttk.Combobox(down_frame, textvariable=var_day, font=('times new roman', 10), width=12)
combo_dep['value'] = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                      '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31')
combo_dep.grid(row=1, column=1, padx=1, pady=2, sticky=W)

# absents
lbl_absents = Label(down_frame, text="Absents:", font=('arial', 11, 'bold'), bg='#d4d9cd')
lbl_absents.grid(row=1, column=2, padx=3, pady=7, sticky=W)
combo_dep = ttk.Combobox(down_frame, textvariable=var_absents, font=('times new roman', 10), width=12)
combo_dep['value'] = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18',
                      '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31')
combo_dep.grid(row=1, column=3, padx=3, pady=2, sticky=W)

# OT
lbl_salcode = Label(down_frame, text="OT Hours:", font=('arial', 11, 'bold'), bg='#d4d9cd')
lbl_salcode.grid(row=1, column=4, padx=4, pady=7, sticky=W)
txt_salcode = ttk.Entry(down_frame, textvariable=var_deduction, width=11, font=('arial', 11))
txt_salcode.grid(row=1, column=5, padx=4, pady=3)
# calculate bill
button_calculate = Button(down_frame, text='Calculate Sal', command=calsalary, font=('arial', 10, 'bold'), width=11,
                          bg='blue', fg='white', cursor='hand2')
button_calculate.grid(row=1, column=6, padx=4, pady=3)
#clear field
button_clear = Button(down_frame, text='Clear', command=clearal, font=('arial', 10, 'bold'), width=11, bg='#db8756',
                      cursor='hand2')
button_clear.grid(row=2, column=6, padx=4, pady=3)

# OT rate
lbl_salarydeductuion = Label(down_frame, text="OT rate:", font=('arial', 11, 'bold'), bg='#d4d9cd')
lbl_salarydeductuion.grid(row=2, column=0, padx=2, pady=6, sticky=W)
txt_salarydeductuion = ttk.Entry(down_frame, textvariable=var_rate, width=11, font=('arial', 11))
txt_salarydeductuion.grid(row=2, column=1, padx=1, pady=6)

# salary offer
lbl_bonus = Label(down_frame, text="Bonus:", font=('arial', 11, 'bold'), bg='#d4d9cd')
lbl_bonus.grid(row=2, column=2, padx=2, pady=6, sticky=W)
txt_bonus = ttk.Entry(down_frame, textvariable=var_bonus, width=11, font=('arial', 11))
txt_bonus.grid(row=2, column=3, padx=1, pady=6)

# Gross salary
lbl_gross = Label(down_frame, text="Gross Pay:", font=('arial', 11, 'bold'), bg='#d4d9cd')
lbl_gross.grid(row=2, column=4, padx=4, pady=7, sticky=W)
txt_gross = ttk.Entry(down_frame, textvariable=var_grosPay, width=11, font=('arial', 11))
txt_gross.grid(row=2, column=5, padx=4, pady=3)
# Salary deduction
lbl_ded = Label(down_frame, text="Deduction:", font=('arial', 11, 'bold'), bg='#d4d9cd')
lbl_ded.grid(row=3, column=0, padx=2, pady=6, sticky=W)
txt_ded = ttk.Entry(down_frame, textvariable=var_salCode, width=11, font=('arial', 11))
txt_ded.grid(row=3, column=1, padx=1, pady=6)

# Net salary
lbl_net = Label(down_frame, text="Net Salary:", font=('arial', 11, 'bold'), bg='#d4d9cd')
lbl_net.grid(row=3, column=2, padx=2, pady=6, sticky=W)
txt_net = ttk.Entry(down_frame, textvariable=var_netPay, width=11, font=('arial', 11))
txt_net.grid(row=3, column=3, padx=1, pady=6)

# receipt no
lbl_recno = Label(down_frame, text="Ref No:", font=('arial', 11, 'bold'), bg='#d4d9cd')
lbl_recno.grid(row=3, column=4, padx=2, pady=6, sticky=W)
txt_recno = ttk.Entry(down_frame, textvariable=var_receiptno, width=11, font=('arial', 11))
txt_recno.grid(row=3, column=5, padx=1, pady=6)
# search receipt
search_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, bg="#d4d9cd")
search_frame.place(x=1, y=400, width=680, height=150)

# employee table-table frame
table_frame = Frame(search_frame, bd=2, relief=RIDGE, bg="#d4d9cd")
table_frame.place(x=0, y=0, width=680, height=150)


scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

employee_table = ttk.Treeview(table_frame, columns=("Id", "Name", "Department", "Designation", "Email",
                                                    "Salary", "Date", "WorkDays", "Absents", "OTHours",
                                                    "Rate", "Bonus", "GrossPay", "Deduction", "NetPay",
                                                    "RefNo"),
                              xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

s = ttk.Style(employee_table)
s.theme_use("clam")

scroll_x.pack(side=BOTTOM, fill=X)
scroll_y.pack(side=RIGHT, fill=Y)

scroll_x.config(command=employee_table.xview)
scroll_y.config(command=employee_table.yview)

employee_table.heading("Id", text="Employee Id")
employee_table.heading("Name", text="Name")
employee_table.heading("Department", text="Department")
employee_table.heading("Designation", text="Designation")
employee_table.heading("Email", text="Email")
employee_table.heading("Salary", text="Salary(B)")
employee_table.heading("Date", text="Date")
employee_table.heading("WorkDays", text="Total Days")
employee_table.heading("Absents", text="Absents")
employee_table.heading("OTHours", text="OT Hours")
employee_table.heading("Rate", text="OT rate")
employee_table.heading("Bonus", text="Bonus")
employee_table.heading("GrossPay", text="Gross Pay")
employee_table.heading("Deduction", text="Deduction")
employee_table.heading("NetPay", text="Net Salary")
employee_table.heading("RefNo", text="Ref No")

employee_table['show'] = "headings"

employee_table.column("Id", width=100)
employee_table.column("Name", width=200)
employee_table.column("Department", width=100)
employee_table.column("Designation", width=100)
employee_table.column("Email", width=200)
employee_table.column("Salary", width=100)
employee_table.column("Date", width=100)
employee_table.column("WorkDays", width=100)
employee_table.column("Absents", width=100)
employee_table.column("OTHours", width=100)
employee_table.column("Rate", width=100)
employee_table.column("Bonus", width=100)
employee_table.column("GrossPay", width=100)
employee_table.column("Deduction", width=100)
employee_table.column("NetPay", width=100)
employee_table.column("RefNo", width=100)
employee_table.pack(fill=BOTH, expand=1)
employee_table.bind("<ButtonRelease-1>", get_cursor)
fetch_data()


emp.mainloop()
