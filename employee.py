import os
from tkinter import *
from tkinter import messagebox
import pyodbc
from tkinter import ttk
from PIL import Image, ImageTk
from db import Database
import smtplib
import random
from tkinter import simpledialog


screen = Tk()
screen.geometry("1280x600")
screen.configure(bg="#D0BDF0")
screen.title("Login")
screen.resizable(None)


username = StringVar()
password = StringVar()
adminType = StringVar()


def toggle_password_visibility():
    global is_password_visible
    is_password_visible = not is_password_visible
    if is_password_visible:
        entry_passwod.config(show="")
        btn_show_password.config(image=img_hide_password)
    else:
        entry_passwod.config(show="*")
        btn_show_password.config(image=img_show_password)


def clear():
    entry_username.delete(0, END)
    entry_passwod.delete(0, END)


def login():
    global username
    global password
    db = Database()

    cnxn = pyodbc.connect(db.cnxn_str)
    cursor = cnxn.cursor()

    username = entry_username.get()
    password = entry_passwod.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Please enter both username and password")

    else:
        cursor.execute("SELECT Login_Type FROM Employees WHERE Name=? and Password=?", (username, password))
        login_type = cursor.fetchone()

        if login_type:
            cursor.execute("INSERT INTO store_login VALUES(?,?)", (username, password))
            if login_type[0] == 'Sales':
                screen.withdraw()
                os.system(f"python BillingSystem.py {username}")  # Pass the username as a parameter to the command

            elif login_type[0] == 'Employee':
                screen.withdraw()
                os.system("empManagement.py")

            elif login_type[0] == 'Inventory':
                screen.withdraw()
                os.system("Stock.py")

            elif login_type[0] == 'Admin':
                screen.withdraw()
                os.system("admin.py")

            screen.deiconify()
            screen.withdraw()
            db.cnxn.commit()

        else:
            messagebox.showerror("Error", "Invalid username or password")

    db.cnxn.close()


global security_A
global sec_pwb
global txt_id_pw


def forgot_pw():
    if entry_username.get() == "":
        messagebox.showerror("Error", "please Enter Valid Username")
    else:
        root2 = Toplevel()
        root2.title("Forgot Password")
        root2.geometry("340x300+610+100")
        lo2 = Label(root2, text="Forgot Password", font=("Times New Roman", 20, "bold"), fg="Blue", bg="Grey")
        lo2.place(x=0, y=10, relwidth=1)
        table_frame = Frame(root2, bd=3, relief=RIDGE, bg="#d4d9cd")
        table_frame.place(x=0, y=60, width=338, height=300)

        def rst():
            # add this function to generate a verification code
            def generate_verification_code():
                return random.randint(100000, 999999)

            def next_page():
                root2 = Toplevel()
                root2.title("Forgot Password")
                root2.geometry("340x300+610+100")
                lo2 = Label(root2, text="Forgot Password", font=("Times New Roman", 20, "bold"), fg="Blue", bg="Grey")
                lo2.place(x=0, y=10, relwidth=1)
                table_frame = Frame(root2, bd=3, relief=RIDGE, bg="#d4d9cd")
                table_frame.place(x=0, y=60, width=338, height=295)
                security_A = StringVar()
                security_sec = Label(table_frame, text="New Password", font=("Times New Roman", 12, "bold"),
                                     bg="#d4d9cd")
                security_sec.grid(row=1, column=0, padx=2, pady=10, sticky=W)
                txt_sec = ttk.Entry(table_frame, textvariable=security_A, font=("Times New Roman", 12), show="*")
                txt_sec.grid(row=1, column=1, padx=2, pady=10, sticky=W)

                sec_pwb = StringVar()
                new_pw = Label(table_frame, text="Confirm Password", font=("Times New Roman", 12, "bold"), bg="#d4d9cd")
                new_pw.grid(row=2, column=0, padx=2, pady=6, sticky=W)
                txt_newpw = ttk.Entry(table_frame, textvariable=sec_pwb, font=("Times New Roman", 12), show="*")
                txt_newpw.grid(row=2, column=1, padx=2, pady=6, sticky=W)

                def toggle_password_visibility():
                    global is_password_visible
                    is_password_visible = not is_password_visible
                    if is_password_visible:
                        txt_sec.config(show="")
                        btn_show_password.config(image=img_hide_password)
                    else:
                        txt_sec.config(show="*")
                        btn_show_password.config(image=img_show_password)

                def togg_password_visibility():
                    global is_password_visible
                    is_password_visible = not is_password_visible
                    if is_password_visible:
                        txt_newpw.config(show="")
                        btn_access_pw.config(image=img_hide_password)
                    else:
                        txt_newpw.config(show="*")
                        btn_access_pw.config(image=img_show_password)

                img_show_password = ImageTk.PhotoImage(
                    Image.open("F:\project\ShopManagement\images\open_the_pss.png").resize((28, 15)))
                img_hide_password = ImageTk.PhotoImage(
                    Image.open("F:\project\ShopManagement\images\Eye_for_login_pss.png").resize((28, 15)))

                is_password_visible = False
                btn_show_password = Button(table_frame, image=img_show_password, bd=0,
                                           command=toggle_password_visibility,
                                           bg="white",
                                           cursor="hand2")
                btn_show_password.place(x=265, y=12)

                btn_access_pw = Button(table_frame, image=img_show_password, bd=0, command=togg_password_visibility,
                                       bg="white",
                                       cursor="hand2")
                btn_access_pw.place(x=265, y=52)

                def reset_pw():
                    db = Database()
                    cnxn = pyodbc.connect(db.cnxn_str)
                    db.cursor = cnxn.cursor()
                    vusername = var_security.get()
                    confpassword = sec_pwb.get()
                    firstpw = security_A.get()
                    if firstpw == confpassword:
                        db.cursor.execute("update Employees set Password=? where Email=?",
                                          (confpassword, vusername))
                        messagebox.showinfo("Success", "Reset the password")
                        root2.deiconify()
                        root2.withdraw()
                        db.cnxn.commit()
                    else:
                        messagebox.showerror("Error", "Passwords should be same")
                    db.cnxn.close()

                btn_reset = Button(root2, text="Reset", height="1", width=12, bg="Green", fg="white", bd=2,
                                   cursor="hand2", command=reset_pw,
                                   font=("arial", 10, "bold"))
                btn_reset.place(x=120, y=180)

            db = Database()
            cnxn = pyodbc.connect(db.cnxn_str)
            db.cursor = cnxn.cursor()
            vusername = var_security.get()
            db.cursor.execute("SELECT Login_Type FROM Employees WHERE Email=?", (vusername))
            login_type = db.cursor.fetchone()

            if var_security.get() == '':
                messagebox.showerror("Error", "All fields are required to be filled")
            elif login_type:
                # send email with verification code
                smtp_server = "smtp.gmail.com"  # or preferred email server
                smtp_port = 587  # or your preferred port
                sender_email = "n06131019@gmail.com"  # replace with email
                sender_password = "kehqnqkbbjblfutu"  # replace with email password
                recipient_email = vusername
                verification_code = generate_verification_code()
                message = f"Your verification code is {verification_code}"
                try:
                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(sender_email, sender_password)
                        server.sendmail(sender_email, recipient_email, message)
                    messagebox.showinfo("Verification",
                                        "Verification code sent to your email. Please enter the code to proceed.")
                    # prompt user to enter verification code
                    user_input = simpledialog.askstring("Verification",
                                                        "Please enter the verification code sent to your email")
                    if user_input == str(verification_code):
                        next_page()
                        root2.deiconify()
                        root2.withdraw()
                        db.cnxn.commit()
                    else:
                        messagebox.showerror("Error", "Verification code entered is invalid")
                except:
                    messagebox.showerror("Error", "Failed to send verification email")
            else:
                messagebox.showerror("Error", "Invalid login type")
            db.cnxn.close()

        lbl_secrure = Label(table_frame, text="Email Id:", font=("Times New Roman", 18, "bold"), bg="#d4d9cd")
        lbl_secrure.place(x=120, y=35)
        var_security = StringVar()

        txt_id_pw = ttk.Entry(table_frame, textvariable=var_security, font=("Times New Roman", 12), width=36)
        txt_id_pw.place(x=30, y=80)
        btn_reset = Button(table_frame, text="Next", height="1", width=11, bg="Blue", fg="white", bd=2, cursor="hand2",
                           command=rst)
        btn_reset.place(x=120, y=140)


image_icon = PhotoImage(file="F:\project\ShopManagement\images\login.png")
screen.iconphoto(False, image_icon)
labelTitle = Label(text="Login System", font=("Times New Roman", 30, "bold"), fg="black", bg="#D0BDF0")
labelTitle.pack(pady=50)

bordercolor = Frame(screen, bg="black", width=550, height=250)
bordercolor.pack()

mainframe = Frame(bordercolor, bg="#d7dae2", width=800, height=400)
mainframe.pack(padx=20, pady=15)


Label(mainframe, text="Username", font=("arial", 20, "bold"), bg="#d7dae2").place(x=100, y=80)
Label(mainframe, text="(Ex:EmpNelson)", font=("arial", 9), bg="#d7dae2").place(x=100, y=110)
Label(mainframe, text="Password", font=("arial", 20, "bold"), bg="#d7dae2").place(x=100, y=150)
Label(mainframe, text="(Ex:emNad12@1)", font=("arial", 9), bg="#d7dae2").place(x=100, y=180)


# name
entry_username = Entry(mainframe, textvariable=username, width=20, bd=2, font=("arial", 14))
entry_username.place(x=400, y=90)
entry_passwod = Entry(mainframe, textvariable=password, width=20, bd=2, font=("arial", 14,), show="*")
entry_passwod.place(x=400, y=150)

img_show_password = ImageTk.PhotoImage(Image.open("F:\project\ShopManagement\images\open_the_pss.png").resize((28, 18)))
img_hide_password = ImageTk.PhotoImage(Image.open("F:\project\ShopManagement\images\Eye_for_login_pss.png").resize((28, 18)))
is_password_visible = False
btn_show_password = Button(mainframe, image=img_show_password, bd=0, command=toggle_password_visibility, bg="white",
                           cursor="hand2")
btn_show_password.place(x=585, y=155)

Button(mainframe, text="Login", height="2", width=20, bg="#006400", fg="white", borderwidth=0, cursor="hand2",
       command=login).place(
    x=300,
    y=250)

Button(mainframe, text="Clear", height="2", width=20, bg="Red", fg="white", bd=0, cursor="hand2", command=clear).\
    place(x=500, y=250)

forgort_pw = Button(mainframe, text="Forgot Password?",  width=20, bg="#d7dae2", fg="Red", cursor="hand2",
                    font=("arial", 12, "bold"), command=forgot_pw, bd=0)
forgort_pw.place(x=80, y=300)

screen.mainloop()
