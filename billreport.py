
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import os
import pyodbc
from reportlab.pdfgen import canvas
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.pagesizes import A4
from openpyxl import Workbook
import matplotlib.pyplot as plt
from datetime import datetime
from db import Database


class BillReport:
    def __init__(self, bill_rep):
        self.bill_rep = bill_rep
        self.bill_rep.geometry("1000x600")
        self.bill_rep.title("Stock Management System")
        self.bill_rep.resizable(0, 0)
        self.lbl_title = Label(self.bill_rep, text="Bill Reports", font=('times new roman', 20, 'bold'), fg='darkblue',
                          bg="lightblue")
        self.lbl_title.place(x=0, y=0, width=1000, height=50)

        def back():
            self.bill_rep.destroy()

        # load the image
        img = Image.open(r"F:\project\ShopManagement\images\back_conn.png")
        img = img.resize((40, 40))  # adjust the size of the image
        img = ImageTk.PhotoImage(img)

        # create the button with the image
        button_back = Button(self.bill_rep, image=img, command=back, width=40, height=40, bd=0, cursor='hand2',  bg="lightblue")
        button_back.image = img  # keep a reference to the image to prevent garbage collection
        button_back.place(x=4, y=4)

        first_frame = LabelFrame(self.bill_rep, bd=2, relief=RIDGE, bg="#d4d9cd", font=('times new roman', 10, 'bold'),
                                 fg='darkblue')
        first_frame.place(x=0, y=50, width=995, height=543)

        def search_data():
            if not var_search.get():
                messagebox.showerror("Error", "Please enter data to search", parent=bill_rep)
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
                            sales_table.insert("", END,
                                               values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
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
                            sales_table.insert("", END,
                                               values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
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
                            sales_table.insert("", END,
                                               values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
                                                       i[10], i[11], i[12], i[13], i[14]))

                        db.cnxn.commit()
                else:
                    messagebox.showerror("Warning", "Invalid Search record", parent=bill_rep)

                db.cnxn.close()
            except Exception as es:
                messagebox.showerror("Error", f'Due to:{str(es)}', parent=bill_rep)

        def fetch_data():
            db = Database()
            cnxn = pyodbc.connect(db.cnxn_str)
            db.cursor = cnxn.cursor()
            db.cursor.execute(
                'SELECT sales.*, items.items FROM sales LEFT JOIN (SELECT Bill_No, STRING_AGG(CONCAT(P_Name, '
                "', Price: ', CAST(Price AS VARCHAR(10)), ', Count: ', CAST(Count AS VARCHAR(10)), ', "
                "SubTotal: ', CAST(SubTotal AS VARCHAR(10))), ', ') AS items FROM salesDetails GROUP BY "
                "Bill_No) AS items ON sales.Bill_No = items.Bill_No")

            data = db.cursor.fetchall()
            if len(data) != 0:
                sales_table.delete(*sales_table.get_children())

                # Sort data by date column
                data = sorted(data, key=lambda x: x[2], reverse=True)

                for i in reversed(data):
                    sales_table.insert("", 0, values=(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
                                                      i[10], i[11], i[12], i[13], i[14]))

                db.cnxn.commit()
            db.cnxn.close()

        def save():
            if len(sales_table.get_children()) < 1:
                messagebox.showinfo("Error", "No data available")
                return
            file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save Excel",
                                                filetypes=(("Excel File", "*.xlsx"),
                                                           ("All Files", "*.*")))
            wb = Workbook()
            ws = wb.active
            cols = ['Bill_No', 'Username', 'Date', 'Name', 'PhoneNo', 'Email', 'CategeoryName', 'SubCategory',
                    'NetTotal',
                    'Discount', 'Total', 'Paid', 'Change', 'Before Discount', 'Purchased Items']
            ws.append(cols)
            for i in sales_table.get_children():
                data = sales_table.item(i)['values']
                ws.append(data)
            wb.save(file)
            messagebox.showinfo("Saved", "Record saved successfully")

        def del_bill():
            global cnxn, db
            global bill_no
            try:
                selected_item = sales_table.selection()[0]
            except IndexError:
                messagebox.showerror("Error", "Please select a record to delete", parent=bill_rep)
                return
            bill_no = sales_table.item(selected_item)['values'][0]
            try:
                Delete = messagebox.askyesno('Delete', 'Are you sure you want to delete this record?', parent=bill_rep)
                if Delete > 0:
                    db = Database()
                    cnxn = pyodbc.connect(db.cnxn_str)
                    db.cursor = cnxn.cursor()
                    value = (bill_no,)
                    db.cursor.execute("DELETE FROM sales WHERE Bill_No=?", value)
                    sales_table.delete(selected_item)
                else:
                    if not Delete:
                        return
                db.cnxn.commit()
                fetch_data()
                db.cnxn.close()
                messagebox.showinfo("Delete", "Sales record successfully deleted")
            except Exception as es:
                messagebox.showerror("Error", f'Due to:{str(es)}', parent=bill_rep)
            textarea.delete('1.0', END)

        def clr_bill():
            var_search.set('')
            textarea.delete('1.0', END)

        def get_cursor(event):
            cursor_row = sales_table.focus()
            content = sales_table.item(cursor_row)
            row = content['values']
            bill_text = f"\t \t New Silver Line Traders (Pvt) Ltd \n" \
                        f"\t \t    Hirimbura Cross Road Galle\n " \
                        f"********************************************************************\n" \
                        f" Bill No: {row[0]}\n Username: {row[1]}\n Date: {row[2]}\n " \
                        f"********************************************************************\n" \
                        f" Name: {row[3]}\n Phone No: {row[4]}\n Email: {row[5]}\n" \
                        f"********************************************************************\n" \
                        f" Product Category: {row[6]}\n Product Subcategory: {row[7]}\n Product Name: {row[8]}\n" \
                        f"********************************************************************\n" \
                        f" Price: {row[9]}\n Count: {row[10]}\n Sub Total: {row[11]}\n Net Total: {row[12]}\n" \
                        f" Discount: {row[13]}\n \nTotal: {row[14]}\n"
            textarea.delete('1.0', END)
            textarea.insert(END, bill_text)

        def save_pdf():
            text = textarea.get('1.0', END).strip()  # get the text and remove any leading/trailing whitespace
            if not text:
                messagebox.showerror("Error", "Text area is empty")
                return
            my_style = ParagraphStyle('Para style', fontName="Times-Roman",
                                      fontSize=12,
                                      alignment=0,
                                      borderWidth=0,
                                      leading=20)
            width, height = A4
            text = textarea.get('1.0', END)
            text = text.replace('\n', '<BR/>')
            p1 = Paragraph(text, my_style)
            file = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Save PDF",
                                                filetypes=(("PDF File", "*.pdf"),
                                                           ("All Files", "*.*")))
            c = canvas.Canvas(file, pagesize=A4)
            p1.wrapOn(c, 400, 400)
            p1.drawOn(c, width - 500, height - 500)
            c.save()
            messagebox.showinfo("Saved", " Bill Saved successfully")
            textarea.delete('1.0', END)

        def nxt_page():
            if not sales_table.get_children():
                messagebox.showerror("Error", "No Record Available", parent=bill_rep)
            else:
                data = []
                for child in sales_table.get_children():
                    record = sales_table.item(child)['values']
                    date_str = record[2].split(' - ')[-1]  # Extract the date string from the column
                    date_obj = datetime.strptime(date_str, '%m/%d/%y')  # Parse the date string as a datetime object
                    data.append((date_obj.date(), float(record[10])))  # Append date and sales total as float

                # Sort data by date
                data.sort()
                # Create a bar chart with highlighted bars
                fig, ax = plt.subplots()
                ax.bar([date for date, total in data], [total for date, total in data], color='blue')

                # Add red points and connecting lines
                for i, (date, total) in enumerate(data):
                    if total > 0:
                        ax.plot(date, total, marker='o', markersize=8, color='red', zorder=3)
                        if i > 0:
                            ax.plot([data[i - 1][0], date], [data[i - 1][1], total], color='black', linewidth=1,
                                    zorder=1)
                ax.set_xlabel('Date')
                ax.set_ylabel('Sales Total (LKR)')
                ax.set_title('Sales by Date')
                plt.xticks(rotation=90)  # Rotate x-axis labels to avoid overlapping
                plt.show()
        # search frame
        search_frame = LabelFrame(first_frame, bd=2, relief=RIDGE, bg="#d4d9cd", text="Search Billing Information",
                                  font=('times new roman', 11, 'bold'), fg='darkblue')
        search_frame.place(x=0, y=1, width=630, height=60)

        search_by = Label(search_frame, text="Search by", font=('arial', 11, 'bold'))
        search_by.grid(row=0, column=0, padx=2, pady=2, sticky=W)
        # search details
        var_com_search = StringVar()
        combo_search = ttk.Combobox(search_frame, textvariable=var_com_search, font=('times new roman', 11), width=15,
                                    state='readonly')
        combo_search['value'] = ('Bill_No', 'Date', 'PhoneNo')
        combo_search.current(0)
        combo_search.grid(row=0, column=1, padx=2, pady=2, sticky=W)

        var_search = StringVar()
        txt_search = ttk.Entry(search_frame, textvariable=var_search, width=20, font=('arial', 11))
        txt_search.grid(row=0, column=2, padx=2, pady=2)

        button_search = Button(search_frame, text='Search', command=search_data, font=('arial', 10, 'bold'), width=8,
                               bg='#ebdb34', cursor='hand2')
        button_search.grid(row=0, column=3, padx=3, pady=2)

        button_showall = Button(search_frame, text='Show All', command=fetch_data, font=('arial', 10, 'bold'), width=8,
                                bg='light blue', fg='black', cursor='hand2')
        button_showall.grid(row=0, column=4, padx=3, pady=3)
        # save button
        button_report = Button(search_frame, text='Export', command=save, font=('arial', 10, 'bold'), width=8,
                               bg='#8f5d36', fg='white', cursor='hand2')
        button_report.grid(row=0, column=5, padx=3, pady=3)

        # 2nd  frame
        del_frame = LabelFrame(first_frame, bd=2, relief=RIDGE, bg="#d4d9cd")
        del_frame.place(x=632, y=11, width=355, height=52)

        # delete button
        button_delete = Button(del_frame, text='Delete', command=del_bill, font=('arial', 10, 'bold'), width=8,
                               bg='red', fg='white', cursor='hand2')
        button_delete.grid(row=0, column=1, padx=6, pady=9)

        # clr button
        button_clr = Button(del_frame, text='Clear', command=clr_bill, font=('arial', 10, 'bold'), width=8,
                            bg='brown', fg='white', cursor='hand2')
        button_clr.grid(row=0, column=2, padx=6, pady=9)

        button_save_bill = Button(del_frame, text='Save Bill', command=save_pdf, font=('arial', 10, 'bold'), width=8,
                               bg='#423d18', fg='white', cursor='hand2')
        button_save_bill.grid(row=0, column=3, padx=6, pady=9)

        self.insideimage = Image.open('F:\project\ShopManagement\images\phtotothe.png')
        self.insideimage = self.insideimage.resize((50, 38))
        self.insideimage = ImageTk.PhotoImage(self.insideimage)

        Button(del_frame, image=self.insideimage, compound=LEFT, padx=6, anchor="w",
               font=('arial', 11, 'bold'),
               height=35, bd=0, cursor="hand2", command=nxt_page, bg='#d4d9cd').place(x=270, y=6)

        table_frame = Frame(first_frame, bd=2, relief=RIDGE, bg="#d4d9cd")
        table_frame.place(x=2, y=80, width=598, height=200)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        sales_table = ttk.Treeview(table_frame, columns=("Bill_No", "Username", "Date", "Name", "PhoneNo",
                                                         "Email", "CategeoryName", "SubCategory", "NetTotal",
                                                         "Discount",
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
        fetch_data()

        # 3rd  frame
        bill_frame = LabelFrame(first_frame, bd=2, relief=RIDGE, bg="#d4d9cd")
        bill_frame.place(x=610, y=70, width=380, height=470)

        area = Label(bill_frame, text="Bill Area", font=('arial', 11, 'bold'), bg="lightblue")
        area.pack(side=TOP, fill=X)
        scrolly2=Scrollbar(bill_frame, orient=VERTICAL)
        textarea = Text(bill_frame, font=('arial', 10, 'bold'),yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=textarea.yview)
        textarea.pack(fill=BOTH, expand=1)

        # image 1
        self.image2 = Image.open("F:\project\ShopManagement\images\stockphoto.jpg")
        self.image2 = self.image2.resize((592, 255))
        self.image2 = ImageTk.PhotoImage(self.image2)
        self.lbl_image2 = Label(first_frame, image=self.image2, bd=1, relief=RAISED)
        self.lbl_image2.place(x=3, y=280)


if __name__=="__main__":
    bill_rep = Tk()
    obj = BillReport(bill_rep)
    bill_rep.mainloop()