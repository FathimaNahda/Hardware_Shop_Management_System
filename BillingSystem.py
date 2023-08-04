import os
from tkinter import *
from PIL import Image, ImageTk
from db import Database
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from time import strftime
import pyodbc
import random
import tempfile
import sys
import tkinter as tk
from openpyxl import Workbook

username = sys.argv[1]
Bill = Tk()  # instance for tkinter
Bill.geometry("1300x1000")
Bill.title("Billing System")
Bill.resizable(0, 0)
cart_list = []
chk_print = 0


def exit():
    Bill.destroy()


Bill.protocol("WM_DELETE_WINDOW", exit)


def logout():
    sure = messagebox.askyesno("Exit", "Are you sure you want to Logout?", parent=Bill)
    if sure == True:
        Bill.destroy()
        os.system("employee.py")



def total():
    # check if discount and subtotal fields are not empty
    if var_discount.get() == "" or var_subtotal.get() == "":
        messagebox.showwarning("Error", "Discount and Subtotal fields are required")
        return

    dis_percent = float(var_discount.get() / 100)
    var_netTotal.set(float(var_subtotal.get() * dis_percent))
    var_totalbill.set(float(var_subtotal.get() - var_netTotal.get()))

    ref_pay = random.randint(20000, 709467)
    var_billNo.set(int(ref_pay))


def change():
    if not str(var_totalbill.get()):
        messagebox.showwarning("Error", "Total amount is required")
    else:
        var_change.set(var_cash.get() - var_totalbill.get())


def addcart():
    if var_count.get() == '':
        messagebox.showerror('Error', "Quantity is required", parent=Bill)
    elif int(var_count.get()) > int(var_stock.get()):
        messagebox.showerror('Error', "Invalid QTY", parent=Bill)
    else:
        price_cal = float(int(var_count.get()) * float(var_price.get()))
        price_cal = float(price_cal)
        cart_data = [var_pName.get(), var_price.get(), var_count.get(), price_cal, var_stock.get()]
        # update car
        present = 'no'
        index_ = 0
        for row in cart_list:
            if var_pName.get() == row[0]:
                present = 'yes'
                break
            index_ += 1
        if present == 'yes':
            op = messagebox.askyesno("Confirm", "Product already present \n Do you want to Update|Remove from the cart"
                                                " list", parent=Bill)
            if op == True:
                if var_count.get() == 0:
                    cart_list.pop(index_)
                else:
                    cart_list[index_][1] = var_price.get()
                    cart_list[index_][2] = var_count.get()
                    cart_list[index_][3] = price_cal
        else:
            cart_list.append(cart_data)
        show_cart()
        bill_updates()


def bill_updates():
    bill_amount = 0
    net_pay = 0

    for row in cart_list:
        bill_amount = bill_amount+float(row[3])
        net_pay = net_pay+(row[2])

        cartTitle.config(text=f'Total Products: \t [{str(len(cart_list))}]\nTotal Items Count:\t[{str(net_pay)}]')

    var_subtotal.set(bill_amount)


def show_cart():
    try:
       prod_table.delete(*prod_table.get_children())
       for row in cart_list:
           prod_table.insert('', END, values=row)

    except EXCEPTION as ex:
        messagebox.showerror("Error", f"error due to: {str(ex)}", parent=Bill)


def billing():
    if var_phone.get() == '':
        messagebox.showerror("Error", f"Customer contact no is required", parent=Bill)
    elif len(cart_list) == 0:
        messagebox.showerror("Error", f"Please add product to the cart!!!", parent=Bill)
    else:
        bill_top()
        bill_middle()
        bill_bottom()
        global chk_print
        chk_print = 1
        sales_db()


def sales_db():
    if var_phone.get() == "" or  len(str(var_phone.get())) != 10 or not str(var_phone.get()).isdigit() or var_category.get() == "" or var_sub.get() == "" or var_subtotal.get() == "" or \
            var_totalbill.get() == "" or var_cash.get() == "":
        messagebox.showwarning("Error", "All fields are required")
        return
    try:
        db = Database()
        cnxn = pyodbc.connect(db.cnxn_str)
        db.cursor = cnxn.cursor()

        # Get the text value of lbl_dateadd
        current_time = lbl_dateadd.cget("text")

        # Insert sales header
        db.cursor.execute("INSERT INTO sales (Bill_No, Username, Date, Name, PhoneNo, Email, CategeoryName, SubCategory, "
                       "SubTotal,NetTotal, Discount, Total, Paid, Change) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (var_billNo.get(), username, current_time, var_name.get(), var_phone.get(), var_email.get(),
             var_category.get(), var_sub.get(), var_subtotal.get(),var_netTotal.get(), var_discount.get(),
             var_totalbill.get(), var_cash.get(), var_change.get()))

        # Insert sales details
        for product in cart_list:
            product_name, price, count, subtotal = product[0], product[1], product[2], product[3]
            db.cursor.execute("INSERT INTO salesDetails (Bill_No, P_Name, Price, Count, SubTotal) VALUES(?,?,?,?,?)",
                (var_billNo.get(), product_name, price, count, subtotal))
        db.cnxn.commit()
        db.cnxn.close()
        messagebox.showinfo("Success", "Receipt printed successfully", parent=Bill)

    except Exception as es:
        messagebox.showerror("Error", f'Due to:{str(es)}', parent=Bill)


def bill_top():

    bill_top_temp = f''' 
    \t \t New Silver Line Traders (Pvt) Ltd
    \t \t   Hirimbura Cross Road Galle
    Salesman: {username}
    Date: {lbl_dateadd.cget("text")}
    Bill No: { (var_billNo.get())}   
    {str("="*50)}
    Customer Name: {var_name.get()}     
    Contact No: {var_phone.get()}
    {str("="*50)}
    Product Name \t\t\t Price \t QTY \tAmount
    {str("="*50)}                                                                                                                                                                                 
    '''
    textarea.delete('1.0', END)
    textarea.insert('1.0', bill_top_temp)


def bill_bottom():
    bill_bottom_temp = f'''
    {str("="*50)}
    Bill Amount\t\t\t\tRs:{var_subtotal.get()}
    Discount\t\t\t\tRs:{var_netTotal.get()}
    Total Bill\t\t\t\tRs:{var_totalbill.get()} 
    {str("="*50)}\n 
    Total Payment\t\t\t\tRs:{var_cash.get()}
    Balance\t\t\t\tRs:{var_change.get()}
    {str("="*50)}\n 
    '''
    textarea.insert(END, bill_bottom_temp)


def bill_middle():
    db = Database()
    cnxn = pyodbc.connect(db.cnxn_str)
    db.cursor = cnxn.cursor()
    try:
        for row in cart_list:
                name = row[0]
                price = row[1]
                Status = row[4]
                qty = int(row[4])-int(row[2])
                if int(row[2]) == int(row[4]):
                    Status='Inactive'
                if int(row[2]) != int(row[4]):
                    Status='Active'

                amounts = float(row[1]) * float(row[2])
                name = str(name)
                price = str(price)
                qty = str(qty)
                amounts = str(amounts)
                textarea.insert(END, name+"\t\t\tRs"+price+"\t"+str(row[2])+"\tRs"+amounts+"\n")
                db.cursor.execute('update product set Quantity=?, Status=? where ProductName=?', (qty, Status, name))

                db.cnxn.commit()
        db.cnxn.close()
        fetch_data()
    except EXCEPTION as ex:
        messagebox.showerror("Error", f"error due to: {str(ex)}", parent=Bill)


def print():
    if chk_print == 1:
        messagebox.showinfo("Print", "Please wait while printing", parent=Bill)
        new_file = tempfile.mktemp('.txt')
        open(new_file, 'w').write(textarea.get('1.0', END))
        os.startfile(new_file,'print')
    else:
        messagebox.showerror("Print", "Please generate bill, to print the receipt", parent=Bill)


def clear():
    var_prodno.set('')
    Var_billno.set(int())
    Var_Date.set('')
    var_name.set('')
    var_phone.set(int())
    var_email.set('')
    var_category.set('')
    var_sub.set('')
    var_price.set(int())
    var_count.set(int())
    var_pName.set('')
    var_subtotal.set(int())
    var_discount.set(int())
    var_totalbill.set(int())
    var_cash.set(int())
    var_change.set(int())
    var_netTotal.set(int())
    var_billNo.set(int())
    textarea.delete('1.0', END)
    del cart_list[:]
    clr_cart()
    show_cart()
    cartTitle.config(text=f"Cart \t Total Product: [0]")


def sel_pro(Bill):
    cursor_row_nw = sales_prod_table.focus()
    content = sales_prod_table.item(cursor_row_nw)
    rows = content['values']
    var_prodno.set(rows[0])
    var_category.set(rows[1])
    var_sub.set(rows[2])
    var_pName.set(rows[3])
    var_price.set(int(rows[4]))
    var_count.set(1)
    cartTitle.config(text=f'Total Product[{str(rows[6])}]')
    var_stock.set(int(rows[6]))


def clr_cart():
    prod_table.delete(*prod_table.get_children())
    for row in cart_list:
        prod_table.delete('', END)


def cart_get_data(Bill):
    cursor_row_nw = prod_table.focus()
    content = prod_table.item(cursor_row_nw)
    rows = content['values']
    var_pName.set(rows[0])
    var_price.set(int(rows[1]))
    var_count.set(int(rows[2]))


operator = ''


def cal():
    # calculator functions

    def buttonClick(numbers):
        global operator
        operator = operator + numbers
        calculatorField.delete(0, END)
        calculatorField.insert(END, operator)

    def clr():
        global operator
        operator = ''
        calculatorField.delete(0, END)

    def answer():
        global operator
        result = str(eval(operator))
        calculatorField.delete(0, END)
        calculatorField.insert(0, result)
        operator = ''

    def remove_cal():
        cal_frame.destroy()

    # calculator frame
    cal_frame = LabelFrame(Bill, bd=2, relief=RIDGE, bg="#d4d9cd", font=('times new roman', 11, 'bold'), fg='darkblue')
    cal_frame.place(x=580, y=460, width=230, height=150)

    calculatorField = Entry(cal_frame, bd=0, font=('arial', 10, 'bold'), width=31, justify=RIGHT,bg="#d4d9cd")
    calculatorField.grid(row=0, column=0, columnspan=4,padx=0)  # columnspan can add 4 button iside 1 column

    # buttons calculator
    buttonBracket = Button(cal_frame, text='()', font=('arial', 8, 'bold'), bg='Grey', bd=2, width=7,
                           command=lambda: buttonClick('()'), cursor='hand2')
    buttonBracket.grid(row=1, column=0)

    buttonper = Button(cal_frame, text='%', font=('arial', 8, 'bold'), bg='Grey', bd=2, width=7,
                       command=lambda: buttonClick('%'), cursor='hand2')
    buttonper.grid(row=1, column=1)

    buttondiv = Button(cal_frame, text='/', font=('arial', 8, 'bold'), bg='Grey', bd=2, width=7,
                       command=lambda: buttonClick('/'), cursor='hand2')
    buttondiv.grid(row=1, column=2)

    buttonback = Button(cal_frame, text='Back', font=('arial', 8, 'bold'), bg='#d4d9cd', bd=2, width=7,
                        command=lambda: remove_cal(), cursor='hand2')
    buttonback.grid(row=1, column=3)

    button7 = Button(cal_frame, text='7', font=('arial', 8, 'bold'), bg='Grey', bd=2, width=7,
                     command=lambda: buttonClick('7'), cursor='hand2')
    button7.grid(row=2, column=0)

    button8 = Button(cal_frame, text='8', font=('arial', 8, 'bold'), bg='Grey', bd=2, width=7,
                     command=lambda: buttonClick('8'), cursor='hand2')
    button8.grid(row=2, column=1)

    button9 = Button(cal_frame, text='9', font=('arial', 8, 'bold'), bg='Grey', bd=2, width=7,
                     command=lambda: buttonClick('9'), cursor='hand2')
    button9.grid(row=2, column=2)

    buttonPlus = Button(cal_frame, text='+', font=('arial', 8, 'bold'), bg='Grey', bd=2, width=7,
                        command=lambda: buttonClick('+'), cursor='hand2')
    buttonPlus.grid(row=2, column=3)

    button4 = Button(cal_frame, text='4', font=('arial', 8, 'bold'), bg='Grey', bd=2, width=7,
                     command=lambda: buttonClick('4'), cursor='hand2')
    button4.grid(row=3, column=0)

    button5 = Button(cal_frame, text='5', font=('arial', 8, 'bold'), bg='Grey', bd=3, width=7,
                     command=lambda: buttonClick('5'), cursor='hand2')
    button5.grid(row=3, column=1)

    button6 = Button(cal_frame, text='6', font=('arial', 8, 'bold'), bg='Grey', bd=2, width=7,
                     command=lambda: buttonClick('6'), cursor='hand2')
    button6.grid(row=3, column=2)

    buttonMinus = Button(cal_frame, text='-', font=('arial', 8, 'bold'), bg='Grey', bd=2, width=7,
                         command=lambda: buttonClick('-'), cursor='hand2')
    buttonMinus.grid(row=3, column=3)

    button1 = Button(cal_frame, text='1', font=('arial', 8, 'bold'), bg='Grey', bd=2, width=7,
                     command=lambda: buttonClick('1'), cursor='hand2')
    button1.grid(row=4, column=0)

    button2 = Button(cal_frame, text='2', font=('arial', 8, 'bold'), bg='Grey', bd=2, width=7,
                     command=lambda: buttonClick('2'), cursor='hand2')
    button2.grid(row=4, column=1)

    button3 = Button(cal_frame, text='3', font=('arial', 8, 'bold'), bg='Grey', bd=2, width=7,
                     command=lambda: buttonClick('3'), cursor='hand2')
    button3.grid(row=4, column=2)

    buttonmulti = Button(cal_frame, text='*', font=('arial', 8, 'bold'), bg='Grey', bd=2, width=7,
                         command=lambda: buttonClick('*'), cursor='hand2')
    buttonmulti.grid(row=4, column=3)

    buttonanswer = Button(cal_frame, text='Ans', font=('arial', 8, 'bold'), bg='Light blue', bd=2, width=7,
                          command=answer, cursor='hand2')
    buttonanswer.grid(row=5, column=0)

    buttonpoint = Button(cal_frame, text='.', font=('arial', 8, 'bold'), bg='Grey', bd=2, width=7,
                         command=lambda: buttonClick('.'), cursor='hand2')
    buttonpoint.grid(row=5, column=1)

    button0 = Button(cal_frame, text='0', font=('arial', 8, 'bold'), bg='Grey', bd=2, width=7,
                     command=lambda: buttonClick('0'), cursor='hand2')
    button0.grid(row=5, column=2)

    buttonclr = Button(cal_frame, text='Clear', font=('arial', 8, 'bold'), bg='#db8756', bd=2, width=7, command=clr,
                       cursor='hand2')
    buttonclr.grid(row=5, column=3)


def view_bill():
    global product_frame
    product_frame = LabelFrame(Bill, bd=0, relief=RIDGE, text='Search Products', font=('Times New Roman', 11, 'bold'),
                               fg='darkblue')
    product_frame.place(x=2, y=450, width=603, height=60)

    def search_data():
        if not var_search.get():
            messagebox.showerror("Error", "Please enter a search term", parent=Bill)
            return
        db = Database()
        cnxn = pyodbc.connect(db.cnxn_str)
        db.cursor = cnxn.cursor()
        try:
            if var_com_search.get() == "Bill_No":
                db.cursor.execute(
                    "SELECT sales.*, items.items FROM sales LEFT JOIN (SELECT Bill_No, STRING_AGG(CONCAT(P_Name, ', "
                    "Price: ', CAST(Price AS VARCHAR(10)), ', Count: ', CAST(Count AS VARCHAR(10)), ', SubTotal: ',"
                    " CAST(SubTotal AS VARCHAR(10))), ', ') AS items FROM salesDetails GROUP BY Bill_No) AS items ON "
                    "sales.Bill_No = items.Bill_No WHERE sales.Bill_No LIKE '%" + var_search.get() + "%'")
                data = db.cursor.fetchall()
                if len(data) != 0:
                    sales_table.delete(*sales_table.get_children())
                    for i in data:
                        sales_table.insert("", END, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
                                                            i[10], i[11], i[12], i[13], i[14]))

                    db.cnxn.commit()

            elif var_com_search.get() == "Date":
                db.cursor.execute(
                    "SELECT sales.*, items.items FROM sales LEFT JOIN (SELECT Bill_No, STRING_AGG(CONCAT(P_Name, ',"
                    " Price: ', CAST(Price AS VARCHAR(10)), ', Count: ', CAST(Count AS VARCHAR(10)), ', SubTotal: ', "
                    "CAST(SubTotal AS VARCHAR(10))), ', ') AS items FROM salesDetails GROUP BY Bill_No) AS items ON"
                    " sales.Bill_No = items.Bill_No WHERE sales.Date LIKE '%" + var_search.get() + "%'")
                data = db.cursor.fetchall()
                if len(data) != 0:
                    sales_table.delete(*sales_table.get_children())
                    for i in data:
                        sales_table.insert("", END, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
                                                            i[10], i[11], i[12], i[13], i[14]))

                    db.cnxn.commit()
            elif var_com_search.get() == "PhoneNo":
                db.cursor.execute(
                    "SELECT sales.*, items.items FROM sales LEFT JOIN (SELECT Bill_No, STRING_AGG(CONCAT(P_Name, ',"
                    " Price: ', CAST(Price AS VARCHAR(10)), ', Count: ', CAST(Count AS VARCHAR(10)), ', SubTotal: ', "
                    "CAST(SubTotal AS VARCHAR(10))), ', ') AS items FROM salesDetails GROUP BY Bill_No) AS items ON"
                    " sales.Bill_No = items.Bill_No WHERE sales.PhoneNo LIKE '%" + var_search.get() + "%'")
                data = db.cursor.fetchall()
                if len(data) != 0:
                    sales_table.delete(*sales_table.get_children())
                    for i in data:
                        sales_table.insert("", END, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
                                                            i[10], i[11], i[12], i[13], i[14]))

                    db.cnxn.commit()
            else:
                messagebox.showerror("Warning", "Invalid Search record", parent=Bill)

            db.cnxn.close()
        except Exception as es:
            messagebox.showerror("Error", f'Due to:{str(es)}', parent=Bill)

    def clr():
        bill_frame.destroy()
        table_frame.destroy()
        var_search.set('')
        product_frame.destroy()

    def save():
        if len(sales_table.get_children()) < 1:
            messagebox.showinfo("Error", "No data available")
            return
        file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save Excel",
                                            filetypes=(("Excel File", "*.xlsx"),
                                                       ("All Files", "*.*")))
        wb = Workbook()
        ws = wb.active
        cols = ['Bill_No', 'Username', 'Date', 'Name', 'PhoneNo', 'Email', 'CategeoryName', 'SubCategory', 'NetTotal',
                'Discount', 'Total', 'Paid', 'Change', 'Before Discount', 'Purchased Items']
        ws.append(cols)
        for i in sales_table.get_children():
            data = sales_table.item(i)['values']
            ws.append(data)
        wb.save(file)
        messagebox.showinfo("Saved", "Record saved successfully")

    # button save
    button_cart = Button(frame_buttons, text='Save', command=save, font=('arial', 10, 'bold'), width=10,
                         bg='#40a165', cursor='hand2')
    button_cart.grid(row=0, column=1, padx=5, pady=2, sticky=W)

    # search frame
    bill_frame = LabelFrame(Bill, bd=2, relief=RIDGE)
    bill_frame.place(x=2, y=450, width=478, height=40)

    search_by = Label(bill_frame, text="Search by", font=('arial', 11, 'bold'))
    search_by.grid(row=0, column=0, padx=2, pady=2, sticky=W)
    # search details
    var_com_search = StringVar()
    combo_search = ttk.Combobox(bill_frame, textvariable=var_com_search, font=('times new roman', 11), width=10,
                                state='readonly')
    combo_search['value'] = ('Bill_No', 'Date', 'PhoneNo')
    combo_search.current(0)
    combo_search.grid(row=0, column=1, padx=1, pady=2, sticky=W)

    var_search = StringVar()
    txt_search = ttk.Entry(bill_frame, textvariable=var_search, width=15, font=('arial', 11))
    txt_search.grid(row=0, column=2, padx=1, pady=2)

    button_search = Button(bill_frame, text='Search', command=search_data, font=('arial', 10, 'bold'), width=10,
                           bg='#ebdb34'
                           , cursor='hand2')
    button_search.grid(row=0, column=3, padx=1, pady=2)
    # button clr
    button_clear_page = Button(bill_frame, text='Clear', command=clr, font=('arial', 10, 'bold'), width=8,
                               bg='lightblue', cursor='hand2')
    button_clear_page.grid(row=0, column=4, padx=1, pady=2, sticky=W)

    def get_cursor(*args):
        cursor_row = sales_table.focus()
        if cursor_row:
            content = sales_table.item(cursor_row)
            data = content['values']
            Var_billno.set(int(data[0]))
            username_entry.set(data[1])
            Var_Date.set(data[2])
            var_name.set(data[3])
            var_phone.set(int(data[4]))
            var_email.set(data[5])
            var_category.set(data[6])
            var_sub.set(data[7])
            var_netTotal.set(int(data[8]))
            var_discount.set(int(data[9]))
            var_totalbill.set(int(data[10]))
            var_cash.set(int(data[11]))
            var_change.set(int(data[12]))
            var_subtotal.set(int(data[13]))
            var_pName.set(data[14])
            addcart()
            show_cart()
            bill_updates()
            bill_top()
            bill_middle()
            bill_bottom()

    # Bill frame
    table_frame = Frame(Bill, bd=2, relief=RIDGE, bg="#d4d9cd")
    table_frame.place(x=2, y=500, width=800, height=150)

    scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
    scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

    sales_table = ttk.Treeview(table_frame, columns=("Bill_No", "Username", "Date", "Name", "PhoneNo",
                                                     "Email", "CategeoryName", "SubCategory", "NetTotal", "Discount",
                                                     "Total", "Paid", "Change", "SubTotal", "P_Name"),
                               xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

    s = ttk.Style(sales_table)
    s.theme_use("clam")

    scroll_x.pack(side=BOTTOM, fill=X)
    scroll_y.pack(side=RIGHT, fill=Y)

    scroll_x.config(command=sales_table.xview)
    scroll_y.config(command=sales_table.yview)

    sales_table.heading("Bill_No", text="Bill_No")
    sales_table.heading("Username", text="Username")
    sales_table.heading("Date", text="Date")
    sales_table.heading("Name", text="Name")
    sales_table.heading("PhoneNo", text="PhoneNo")
    sales_table.heading("Email", text="Email")
    sales_table.heading("CategeoryName", text="CategeoryName")
    sales_table.heading("SubCategory", text="SubCategory")
    sales_table.heading("NetTotal", text="NetTotal")
    sales_table.heading("Discount", text="Discount")
    sales_table.heading("Total", text="Total")
    sales_table.heading("Paid", text="Paid")
    sales_table.heading("Change", text="Change")
    sales_table.heading("SubTotal", text="Before Discount")
    sales_table.heading("P_Name", text="Purchased Items")

    sales_table['show'] = "headings"

    sales_table.column("Bill_No", width=100)
    sales_table.column("Username", width=150)
    sales_table.column("Date", width=200)
    sales_table.column("Name", width=100)
    sales_table.column("PhoneNo", width=150)
    sales_table.column("Email", width=100)
    sales_table.column("CategeoryName", width=150)
    sales_table.column("SubCategory", width=150)
    sales_table.column("SubTotal", width=100)
    sales_table.column("Discount", width=100)
    sales_table.column("Total", width=100)
    sales_table.column("Paid", width=100)
    sales_table.column("Change", width=100)
    sales_table.column("NetTotal", width=100)
    sales_table.column("P_Name", width=1000)

    sales_table.pack(fill=BOTH, expand=1)
    sales_table.bind("<ButtonRelease-1>", get_cursor)


lbl_title = Label(Bill, text="Billing System", font=('times new roman', 30, 'bold'), fg='darkblue', bg="lightblue")
lbl_title.place(x=0, y=0, width=1300, height=50)
button_logout = Button(Bill, text='Logout', command=logout, font=('arial', 10, 'bold'), width=10, bg='brown'
                       , fg='white', cursor='hand2')
button_logout.place(x=2, y=4)


# Create a label and an entry widget to display the username
username_label = tk.Label(Bill, text="Username:", font=('times new roman', 13, 'bold'), fg='black', bg="lightblue")
username_label.place(x=100, y=9)
username_entry = tk.Entry(Bill,  width=20, font=('times new roman', 13, 'bold'),bg="lightblue", bd=0)
username_entry.insert(0, username)  # Insert the username into the entry widget
username_entry.place(x=200, y=11)


def my_time():
    time_string = strftime('%H:%M:%S%p  - %A  - %x')
    lbl_dateadd.config(text=time_string)
    lbl_dateadd.after(1000, my_time)


lbl_dateadd= Label(Bill, font=('times new roman', 13, 'bold'), fg='black', bg="lightblue")
lbl_dateadd.place(x=950, y=9)
my_time()


# logo
logoimage = Image.open(
            'F:\project\electrochip-html\electrochip-html\images\Screenshot_2022-07-13_081400-removebg-preview.png')
logoimage = logoimage.resize((50, 50))
photo = ImageTk.PhotoImage(logoimage)

logo = Label(Bill, image=photo, bg="lightblue")
logo.place(x=270, y=50, width=50, height=50)

img_frame = Frame(Bill, bd=2, relief=RIDGE, bg="#d4d9cd")
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


# variables
var_prodno=StringVar()
Var_billno=IntVar()
username_entry = StringVar()
Var_Date = StringVar()
var_name = StringVar()
var_phone = IntVar()
var_email = StringVar()
var_category = StringVar()
var_sub = StringVar()
var_price = IntVar()
var_count = IntVar()
var_pName = StringVar()
var_subtotal = IntVar()
var_discount = DoubleVar()
var_totalbill = DoubleVar()
var_cash = DoubleVar()
var_change = DoubleVar()
var_netTotal = DoubleVar()
var_billNo = IntVar()
var_stock = IntVar()

# main frame
main_frame = Frame(Bill, bd=2, relief=RIDGE)
main_frame.place(x=0, y=134, width=800, height=150)

# upperFrame
customer_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Customer", font=('times new roman', 11, 'bold'),
                            fg='darkblue')
customer_frame.place(x=1, y=2, width=250, height=140)
# name
lbl_name = Label(customer_frame, text="Name", font=('arial', 11, 'bold'))
lbl_name.grid(row=0, column=0, padx=2, pady=2, sticky=W)
txt_name = ttk.Entry(customer_frame, textvariable=var_name, width=18, font=('arial', 11))
txt_name.grid(row=0, column=1, padx=1, pady=2)
# Phone
lbl_phone = Label(customer_frame, text="Phone No", font=('arial', 11, 'bold'))
lbl_phone.grid(row=1, column=0, padx=2, pady=6, sticky=W)
txt_phone = ttk.Entry(customer_frame, textvariable=var_phone, width=18, font=('arial', 11))
txt_phone.grid(row=1, column=1, padx=1, pady=6)
# email
lbl_email = Label(customer_frame, text="Email", font=('arial', 11, 'bold'))
lbl_email.grid(row=2, column=0, padx=2, pady=7, sticky=W)
txt_email = ttk.Entry(customer_frame, textvariable=var_email, width=18, font=('arial', 11))
txt_email.grid(row=2, column=1, padx=1, pady=7)

# 2ndframe
product_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Products", font= ('times new roman', 11, 'bold'),
                            fg='darkblue')
product_frame.place(x=255, y=2, width=540, height=140)

# product category
lbl_productCategory = Label(product_frame, text="Product Category", font=('arial', 11, 'bold'))
lbl_productCategory.grid(row=0, column=0, padx=2, pady=2, sticky=W)

txt_category = ttk.Entry(product_frame, textvariable=var_category, width=20, font=('arial', 11))
txt_category.grid(row=0, column=1, padx=1, pady=2, sticky=W)
# sub category
lbl_subCategory = Label(product_frame, text="Sub Category", font=('arial', 11, 'bold'))
lbl_subCategory.grid(row=1, column=0, padx=2, pady=4, sticky=W)

txt_sub = ttk.Entry(product_frame, textvariable=var_sub, width=20, font=('arial', 11))
txt_sub.grid(row=1, column=1, padx=1, pady=4, sticky=W)

# product Name
lbl_productName = Label(product_frame, text="Product Name", font=('arial', 11, 'bold'))
lbl_productName.grid(row=2, column=0, padx=2, pady=6, sticky=W)

txt_product = ttk.Entry(product_frame, textvariable=var_pName, width=20, font=('arial', 11))
txt_product.grid(row=2, column=1, padx=1, pady=6, sticky=W)

# price
lbl_price = Label(product_frame, text="Price", font=('arial', 11, 'bold'))
lbl_price.grid(row=0, column=2, padx=4, pady=2, sticky=W)
txt_price = ttk.Entry(product_frame, textvariable=var_price, width=18, font=('arial', 11))
txt_price.grid(row=0, column=3, padx=4, pady=2, sticky=W)


# count
lbl_count = Label(product_frame, text="Count", font=('arial', 11, 'bold'))
lbl_count.grid(row=1, column=2, padx=6, pady=2, sticky=W)
txt_count = ttk.Entry(product_frame, textvariable=var_count, width=18, font=('arial', 11))
txt_count.grid(row=1, column=3, padx=6, pady=1, sticky=W)
# Add to cart
button_addtocart = Button(product_frame, text='Add Update Cart', command=addcart, font=('arial', 10, 'bold'), width=14,
                         bg='#db8756', cursor='hand2')
button_addtocart.grid(row=2, column=3, padx=6, pady=1, sticky=W)
# clear cart
button_clear = Button(product_frame, text='Clear Cart', command=clr_cart, font=('arial', 8, 'bold'), width=8, bg='grey'
                      , cursor='hand2')
button_clear.grid(row=2, column=2, padx=4, pady=2, sticky=W)

# down frame
down_frame = LabelFrame(Bill, bd=2, relief=RIDGE, text="Billing", font=('times new roman', 11, 'bold'),
                        fg='darkblue')
down_frame.place(x=1, y=290, width=480, height=150)
# subTotal
lbl_subtotal = Label(down_frame, text="Sub Total", font=('arial', 11, 'bold'))
lbl_subtotal.grid(row=0, column=0, padx=1, pady=2, sticky=W)
txt_subtotal = ttk.Entry(down_frame, textvariable=var_subtotal, width=15, font=('arial', 11))
txt_subtotal.grid(row=0, column=1, padx=4, pady=2, sticky=W)
# Discount
lbl_discount = Label(down_frame, text="Discount %", font=('arial', 11, 'bold'))
lbl_discount.grid(row=1, column=0, padx=1, pady=4, sticky=W)
txt_discount = ttk.Entry(down_frame, textvariable=var_discount, width=15, font=('arial', 11))
txt_discount.grid(row=1, column=1, padx=4, pady=4, sticky=W)
# net
lbl_nettotal = Label(down_frame, text="Discount Price", font=('arial', 11, 'bold'))
lbl_nettotal.grid(row=2, column=0, padx=1, pady=2, sticky=W)
txt_nettotal = ttk.Entry(down_frame, textvariable=var_netTotal, width=15, font=('arial', 11))
txt_nettotal.grid(row=2, column=1, padx=4, pady=2, sticky=W)
# Total
lbl_totalbill = Label(down_frame, text="Total", font=('arial', 11, 'bold'))
lbl_totalbill.grid(row=3, column=0, padx=1, pady=4, sticky=W)
txt_totalbill = ttk.Entry(down_frame, textvariable=var_totalbill, width=15, font=('arial', 11))
txt_totalbill.grid(row=3, column=1, padx=4, pady=4, sticky=W)
# Cash
lbl_cash = Label(down_frame, text="Paid", font=('arial', 11, 'bold'))
lbl_cash.grid(row=0, column=2, padx=1, pady=4, sticky=W)
txt_cash = ttk.Entry(down_frame, textvariable=var_cash, width=18, font=('arial', 11))
txt_cash.grid(row=0, column=3, padx=4, pady=4, sticky=W)
# change
lbl_change = Label(down_frame, text="Change", font=('arial', 11, 'bold'))
lbl_change.grid(row=1, column=2, padx=1, pady=4, sticky=W)
txt_change = ttk.Entry(down_frame, textvariable=var_change, width=18, font=('arial', 11))
txt_change.grid(row=1, column=3, padx=4, pady=4, sticky=W)
# Bill No
lbl_Bill_No = Label(down_frame, text="Bill No", font=('arial', 11, 'bold'))
lbl_Bill_No.grid(row=2, column=2, padx=1, pady=4, sticky=W)
txt_Bill_No = ttk.Entry(down_frame, textvariable=var_billNo, width=18, font=('arial', 11))
txt_Bill_No.grid(row=2, column=3, padx=4, pady=4, sticky=W)
# button change
button_save = Button(down_frame, text='Change', command=change, font=('arial', 8, 'bold'), width=8, bg='#db8756',
                     cursor='hand2')
button_save.grid(row=3, column=3, padx=4, pady=2, sticky=W)
# button total
button_caltotal = Button(down_frame, text='Total', command=total, font=('arial', 8, 'bold'), width=8, bg='blue',
                         fg='white', cursor='hand2')
button_caltotal.grid(row=3, column=3, padx=80, pady=2, sticky=W)

# button frame
frame_buttons = LabelFrame(Bill, relief=RIDGE,bd=0)
frame_buttons.place(x=1, y=660, width=720, height=33)
# button bill
button_bill = Button(frame_buttons, text='Bill', command=billing, font=('arial', 10, 'bold'), width=10, bg='#739e96'
                     , cursor='hand2')
button_bill.grid(row=0, column=2, padx=6, pady=2, sticky=W)
# button print
button_print = Button(frame_buttons, text='Print', command=print, font=('arial', 10, 'bold'), width=10, bg='#db8756'
                      , cursor='hand2')
button_print.grid(row=0, column=3, padx=7, pady=2, sticky=W)
# button clear
button_clear = Button(frame_buttons, text='Clear All', command=clear, font=('arial', 10, 'bold'), width=10, bg='Grey'
                      , cursor='hand2')
button_clear.grid(row=0, column=4, padx=7, pady=2, sticky=W)
# button view
button_save = Button(frame_buttons, text='View Bill', command=view_bill, font=('arial', 10, 'bold'), width=10,
                     bg='#a3bfaa', cursor='hand2')
button_save.grid(row=0, column=5, padx=6, pady=2, sticky=W)
# button caal
button_cal = Button(frame_buttons, text='Calculator', command=cal, font=('arial', 10, 'bold'), width=10, bg='#db8756'
                    , cursor='hand2')
button_cal.grid(row=0, column=6, padx=5, pady=2, sticky=W)

lbl_employee = Label(frame_buttons, font=('times new roman', 13, 'bold'), fg='black')
lbl_employee.grid(row=0, column=7, padx=5, pady=2, sticky=W)


# side
side_frame = LabelFrame(Bill, bd=3, relief=RIDGE)
side_frame.place(x=800, y=134, width=497, height=550)
# Bill frame
search_frame = LabelFrame(side_frame, bd=2, relief=RIDGE, fg='darkblue')
search_frame.place(x=0, y=0, width=487, height=32)

# label heading
area = Label(side_frame, text="Bill Area", font=('Times New Roman', 14, 'bold'), bg="#739e96")
area.pack(padx=3, fill=X, pady=2)
# text area
text_frame = LabelFrame(side_frame, bd=3, relief=RIDGE)
text_frame.place(x=0, y=44, width=490, height=500)

scroll_x = ttk.Scrollbar(text_frame, orient=HORIZONTAL)
scroll_y = ttk.Scrollbar(text_frame, orient=VERTICAL)

textarea = Text(text_frame, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set, bg='white', fg='blue',
                font=('times new roman', 11))
scroll_x.pack(side=BOTTOM, fill=X)
scroll_y.pack(side=RIGHT, fill=Y)
scroll_x.config(command=textarea.xview)
scroll_y.config(command=textarea.yview)
textarea.pack(fill=BOTH, expand=1)


# carts frame
carts_frame = LabelFrame(Bill, bd=2, relief=RIDGE, text="Cart", font=('times new roman', 11, 'bold'),
                        fg='darkblue')
carts_frame.place(x=490, y=290, width=315, height=150)

cartTitle = Label(carts_frame, text="Cart \t Total Product:", font=('times new roman', 11, 'bold'), bg='grey')
cartTitle.pack(side=TOP, fill=X)

scrollss_x = ttk.Scrollbar(carts_frame, orient=HORIZONTAL)
scrollss_y = ttk.Scrollbar(carts_frame, orient=VERTICAL)
prod_table = ttk.Treeview(carts_frame, columns=("ProductName", "Price", "Quantity", "Total Price", "Stock"), xscrollcommand=scrollss_x.set,
                          yscrollcommand=scrollss_y.set)

cart = ttk.Style(prod_table)
cart.theme_use("clam")

scrollss_x.pack(side=BOTTOM, fill=X)
scrollss_y.pack(side=RIGHT, fill=Y)

scrollss_x.config(command=prod_table.xview)
scrollss_y.config(command=prod_table.yview)

prod_table.heading("ProductName", text="ProductName")
prod_table.heading("Price", text="Price")
prod_table.heading("Quantity", text="Quantity")
prod_table.heading("Total Price", text="Total Price")
prod_table.heading("Stock", text="Stock")


prod_table['show'] = "headings"

prod_table.column("ProductName", width=150)
prod_table.column("Price", width=100)
prod_table.column("Quantity", width=100)
prod_table.column("Total Price", width=100)
prod_table.column("Stock", width=100)


prod_table.pack(fill=BOTH, expand=1)
prod_table.bind("<ButtonRelease-1>", cart_get_data)


def search_product():
    if products_search.get() == '':
        messagebox.showerror("Error", "Enter valid name to search", parent=Bill)
    else:
        try:
            db = Database()
            cnxn = pyodbc.connect(db.cnxn_str)
            db.cursor = cnxn.cursor()
            db.cursor.execute("select ProductNo,CategeoryName, SubCategory,ProductName,Price, Status, Quantity from product"
                           " where ProductName LIKE '%" +products_search.get() + "%' and Status='Active'")
            data = db.cursor.fetchall()
            if len(data) != 0:
                sales_prod_table.delete(*sales_prod_table.get_children())
                for i in data:
                    sales_prod_table.insert("", END, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
                db.cnxn.commit()
            else:
                messagebox.showerror("Warning", "This Product is not in the record")

            db.cnxn.close()

        except Exception as es:
            messagebox.showerror("Error", f'Due to:{str(es)}', parent=Bill)


def fetch_data():
    db = Database()
    cnxn = pyodbc.connect(db.cnxn_str)
    db.cursor = cnxn.cursor()
    db.cursor.execute("select ProductNo,CategeoryName, SubCategory, ProductName, Price, Status, Quantity from product "
                   "where Status= 'Active' ")
    data = db.cursor.fetchall()
    if len(data) != 0:
        sales_prod_table.delete(*sales_prod_table.get_children())

        for i in data:
            sales_prod_table.insert("", END, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6]))

        db.cnxn.commit()
    db.cnxn.close()


def clr_search():
    products_search.set("")


# product frame
product_frame = LabelFrame(Bill, bd=0, relief=RIDGE, text='Search Products',font=('Times New Roman', 11, 'bold'), fg='darkblue')
product_frame.place(x=2, y=450, width=603, height=60)

search_by = Label(product_frame, text="Product Name", font=('arial', 11, 'bold'))
search_by.grid(row=0, column=0, padx=2, pady=2, sticky=W)
# search details
products_search = StringVar()
txt_searchP = ttk.Entry(product_frame, textvariable=products_search, width=24, font=('arial', 11))
txt_searchP.grid(row=0, column=1, padx=2, pady=2)

button_search = Button(product_frame, text='Search', command=search_product, font=('arial', 10, 'bold'), width=10,
                           bg='#ebdb34', cursor='hand2')
button_search.grid(row=0, column=2, padx=3, pady=2)
# button show all
button_show = Button(product_frame, text='Show All', command=fetch_data, font=('arial', 10, 'bold'), width=10,
                               bg='brown',  fg='white', cursor='hand2')
button_show.grid(row=0, column=3, padx=3, pady=2, sticky=W)
# button clear
button_clear = Button(product_frame, text='Clear Search', command=clr_search, font=('arial', 10, 'bold'), width=10,
                               bg='lightblue', cursor='hand2')
button_clear.grid(row=0, column=4, padx=3, pady=2, sticky=W)


# pr frame
tablep_frame = Frame(Bill, bd=2, relief=RIDGE, bg="#d4d9cd")
tablep_frame.place(x=2, y=510, width=603, height=150)

scrollssprod_x = ttk.Scrollbar(tablep_frame, orient=HORIZONTAL)
scrollssprod_y = ttk.Scrollbar(tablep_frame, orient=VERTICAL)
sales_prod_table = ttk.Treeview(tablep_frame, columns=("ProductNo", "CategeoryName", "SubCategory", "ProductName",
                                                      "Price","Status", "Quantity"), xscrollcommand=scrollssprod_x.set,
                                yscrollcommand=scrollssprod_y.set)

cart = ttk.Style(sales_prod_table)
cart.theme_use("clam")

scrollssprod_x.pack(side=BOTTOM, fill=X)
scrollssprod_y.pack(side=RIGHT, fill=Y)

scrollssprod_x.config(command=sales_prod_table.xview)
scrollssprod_y.config(command=sales_prod_table.yview)

sales_prod_table.heading("ProductNo", text="ProductNo")
sales_prod_table.heading("CategeoryName", text="CategeoryName")
sales_prod_table.heading("SubCategory", text="SubCategory")
sales_prod_table.heading("ProductName", text="ProductName")
sales_prod_table.heading("Price", text="Price")
sales_prod_table.heading("Status", text="Status")
sales_prod_table.heading("Quantity", text="Quantity")
sales_prod_table['show'] = "headings"

sales_prod_table.column("ProductNo", width=120)
sales_prod_table.column("CategeoryName", width=150)
sales_prod_table.column("SubCategory", width=150)
sales_prod_table.column("ProductName", width=180)
sales_prod_table.column("Price", width=100)
sales_prod_table.column("Status", width=100)
sales_prod_table.column("Quantity", width=100)

sales_prod_table.pack(fill=BOTH, expand=1)
sales_prod_table.bind("<ButtonRelease-1>", sel_pro)
fetch_data()

Bill.mainloop()
