import os
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import time
import pyodbc
from db import Database
from supplier import SupplierDetails
from category import CategoryProduct
from product import ProductDetails
from billreport import BillReport


class stock:
    def __init__(self, inv):
        self.inv = inv
        self.inv.geometry("1300x1000")
        self.inv.title("Stock Management System")
        self.inv.resizable(0, 0)

        def exit():
            inv.destroy()

        inv.protocol("WM_DELETE_WINDOW", exit)

        def logout():
            sure = messagebox.askyesno("Exit", "Are you sure you want to Logout?", parent=self.inv)
            if sure == True:
                self.inv.destroy()
                os.system("employee.py")

        def supplier():
            self.new_win = Toplevel(self.inv)
            self.new_obj = SupplierDetails(self.new_win)

        def category():
            self.newin = Toplevel(self.inv)
            self.newobject = CategoryProduct(self.newin)

        def prdetail():
            self.new_windows = Toplevel(self.inv)
            self.productobj = ProductDetails(self.new_windows)

        def bill():
            self.new_bill_windows = Toplevel(self.inv)
            self.bill_obj = BillReport(self.new_bill_windows)
        
        def update_datetime():
            time_= time.strftime("%I:%M:%S")
            date_= time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f" New Silverline Traders (Pvt)Ltd\t\t Date:{str(date_)}\t\t Time:{str(time_)}")
            self.lbl_clock.after(200, update_datetime)

        def update_conternt():
            # set initial status for alert
            self.alert_status = False
            def check_threshold(label, data, threshold, message):
                if len(data) < threshold:
                    # turn on the alert status and change the border color to red
                    self.alert_status = True
                    label.configure(borderwidth=3, relief="solid", foreground="red")
                    messagebox.showwarning("Alert", message)
                else:
                    # turn off the alert status and change the border color to default
                    self.alert_status = False
                    label.configure(borderwidth=3, relief="flat", foreground="black")
            db = Database()
            cnxn = pyodbc.connect(db.cnxn_str)
            db.cursor = cnxn.cursor()
            try:
                db.cursor.execute("select * from product ")
                product = db.cursor.fetchall()
                self.lbl_product.config(text=f"Total Product\n[{str(len(product))}]")

                db.cursor.execute("select * from supplier ")
                supplier = db.cursor.fetchall()
                check_threshold(self.lbl_product, product, 10,
                                f"There are only {len(product)} products remaining. Consider contacting the following "
                                f"suppliers:\n{', '.join([s[4] for s in supplier])}")

                self.lbl_supplier.config(text=f"Total Supplier\n[{str(len(supplier))}]")
                check_threshold(self.lbl_supplier, supplier, 3,
                                f"There are only {len(supplier)} suppliers remaining. Contract with new suppliers.")

                db.cursor.execute("select * from category ")
                category = db.cursor.fetchall()
                self.lbl_category.config(text=f"Total Category\n[{str(len(category))}]")
                check_threshold(self.lbl_category, category, 10,
                                f"There are only {len(category)} categories remaining.")

                db.cursor.execute("select * from Employees ")
                sales = db.cursor.fetchall()
                self.lbl_sales.config(text=f"Total Employee\n[{str(len(sales))}]")
                check_threshold(self.lbl_sales, sales, 5,
                                f"There are only {len(sales)} employees remaining. Recruit new employees soon.")

            except Exception as es:
                messagebox.showerror("Error", f"Due to:{str(es)}", parent=self.inv)

        self.lbl_title = Label(self.inv, text="Inventory Management", font=('times new roman', 30, 'bold'),
                               fg='darkblue', bg="lightblue")
        self.lbl_title.place(x=0, y=0, width=1300, height=50)
        self.button_logout = Button(self.inv, text='Logout', command=logout, font=('arial', 10, 'bold'), width=10,
                                    bg='brown', fg='white', cursor='hand2')
        self.button_logout.place(x=2, y=4)
        # logo
        self.logoimage = Image.open(
            'F:\project\electrochip-html\electrochip-html\images\Screenshot_2022-07-13_081400-removebg-preview.png')
        self.logoimage = self.logoimage.resize((50, 50))
        self.photo = ImageTk.PhotoImage(self.logoimage)

        self.logo = Label(self.inv, image=self.photo, bg="lightblue")
        self.logo.place(x=270, y=50, width=50, height=50)

        self.img_frame = Frame(self.inv, bd=2, relief=RIDGE, bg="#d4d9cd")
        self.img_frame.place(x=0, y=50, width=1300, height=85)

        # 1st image
        self.img1 = Image.open('F:\project\ShopManagement\images\psettinground.jpg')
        self.img1 = self.img1.resize((200, 100))
        self.photo1in = ImageTk.PhotoImage(self.img1)

        self.img_photo = Label(self.img_frame, image=self.photo1in, bg="#d4d9cd")
        self.img_photo.place(x=0, y=0, width=200, height=84)

        # 2nd image
        self.img2 = Image.open('F:\project\ShopManagement\images\imageside.png')
        self.img2 = self.img2.resize((230, 100))
        self.photo2nd = ImageTk.PhotoImage(self.img2)

        self.img2photo = Label(self.img_frame, image=self.photo2nd, bg="#d4d9cd")
        self.img2photo.place(x=200, y=0, width=230, height=85)

        # 3rd image
        self.img3 = Image.open('F:\project\ShopManagement\images\photoshop.jpg')
        self.img3 = self.img3.resize((250, 100))
        self.photo3rd = ImageTk.PhotoImage(self.img3)

        self.img3rdphoto = Label(self.img_frame, image=self.photo3rd, bg="white")
        self.img3rdphoto.place(x=431, y=0, width=250, height=85)

        # 4rd image
        self.img4 = Image.open('F:\project\ShopManagement\images\phtoset.jpg')
        self.img4 = self.img4.resize((250, 100))
        self.photo4rd = ImageTk.PhotoImage(self.img4)

        self.img4rdphoto = Label(self.img_frame, image=self.photo4rd, bg="white")
        self.img4rdphoto.place(x=682, y=0, width=250, height=85)

        # 5th image
        self.img5 = Image.open('F:\project\ShopManagement\images\hardware.png')
        self.img5 = self.img5.resize((280, 100))
        self.photo5th = ImageTk.PhotoImage(self.img5)

        self.img5thphoto = Label(self.img_frame, image=self.photo5th, bg="white")
        self.img5thphoto.place(x=933, y=0, width=280, height=85)

        # 6th image
        self.img6 = Image.open('F:\project\ShopManagement\images\screwphto.jpg')
        self.img6 = self.img6.resize((100, 100))
        self.photo6th = ImageTk.PhotoImage(self.img6)

        self.img6thphoto = Label(self.img_frame, image=self.photo6th, bg="white")
        self.img6thphoto.place(x=1200, y=0, width=100, height=85)

        # main frame
        self.main_frame = Frame(self.inv, bd=2, relief=RIDGE, bg="#d4d9cd")
        self.main_frame.place(x=0, y=135, width=1300, height=600)
        self.lbl_clock = Label(self.main_frame,  font=('arial', 12, 'bold'), bg='light blue', bd=3, fg='darkblue')
        self.lbl_clock.place(x=0, y=1, relwidth=1, height=30)
        update_datetime()

        # upperFrame
        self.upper_frame = LabelFrame(self.main_frame,bd=2, relief=RIDGE, bg="#d4d9cd", font=('times new roman', 11, 'bold'),
                                 fg='darkblue')
        self.upper_frame.place(x=2, y=60, width=160, height=400)

        Label(self.upper_frame, text="Menu", font=('arial', 12, 'bold'), height=3, bg='#BDB76B', bd=3).pack(side=TOP, fill=X)

        self.insideimage = Image.open('F:\project\ShopManagement\images\sadarrow-removebg-preview.png')
        self.insideimage = self.insideimage.resize((30, 30))
        self.insideimage = ImageTk.PhotoImage(self.insideimage)

        Button(self.upper_frame, text="Supplier", image=self.insideimage, compound=LEFT, padx=2, anchor="w", font=('arial', 11, 'bold'),
               height=50, bg='#d4d9cd', bd=3, cursor="hand2", command=supplier).pack(side=TOP, fill=X)

        Button(self.upper_frame, text="Category", image=self.insideimage, compound=LEFT, padx=2, anchor="w",
               font=('arial', 11, 'bold'),
               height=50, bg='#d4d9cd', bd=3, cursor="hand2", command=category).pack(side=TOP, fill=X)

        Button(self.upper_frame, text="Product", image=self.insideimage, compound=LEFT, padx=2, anchor="w",
               font=('arial', 11, 'bold'),
               height=50, bg='#d4d9cd', bd=3, cursor="hand2", command=prdetail).pack(side=TOP, fill=X)

        Button(self.upper_frame, text="Sales", image=self.insideimage, compound=LEFT, padx=2, anchor="w",
               font=('arial', 11, 'bold'),
               height=50, bg='#d4d9cd', bd=3, cursor="hand2",  command=bill).pack(side=TOP, fill=X)

        self.lbl_supplier = Label(self.inv, text="Total Supplier\n[0]", bg="#BDB76B", font=("arial", 20, "bold"), relief=RIDGE,
                             bd=3)
        self.lbl_supplier.place(x=300, y=200, height=150, width=300)
        self.lbl_product = Label(self.inv, text="Total Product\n[0]", bg="#BDB76B", font=("arial", 20, "bold"), relief=RIDGE,
                            bd=3)
        self.lbl_product.place(x=800, y=200, height=150, width=300)

        self.lbl_category = Label(self.inv, text="Total Category\n[0]", bg="#BDB76B", font=("arial", 20, "bold"), relief=RIDGE,
                             bd=3)
        self.lbl_category.place(x=300, y=400, height=150, width=300)
        self.lbl_sales = Label(self.inv, text="Total Sales\n[0]", bg="#BDB76B", font=("arial", 20, "bold"), relief=RIDGE, bd=3)
        self.lbl_sales.place(x=800, y=400, height=150, width=300)

        self.sideimage = Image.open('F:\project\ShopManagement\images\winges.jpg')
        self.sideimage = self.sideimage.resize((200, 100))
        self.sideimage = ImageTk.PhotoImage(self.sideimage)
        Frame(self.upper_frame, bd=4, relief=RIDGE, bg="#d4d9cd").place(x=0, y=500, width=200, height=200)
        Label(self.upper_frame, image=self.sideimage).pack(side=TOP, fill=X)

        update_conternt()


if __name__ == "__main__":
    inv = Tk()
    obj = stock(inv)
    inv.mainloop()
