
import os
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox

main = Tk()  # instance for tkinter
main.geometry("1300x1000")
main.title("Admin Mode")
main.resizable(0,0)


def exit():
    sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=main)
    if sure == True:
        main.withdraw()
        os.system("employee.py")




main.protocol("WM_DELETE_WINDOW", exit)


def emp():
    main.withdraw()
    os.system("EmployeeAdminManagement.py")
    main.deiconify()


def salary():
    main.withdraw()
    os.system("salary.py")
    main.deiconify()


def stock():
    main.withdraw()
    os.system("Stock.py")
    main.deiconify()


def billing():
    main.withdraw()
    os.system("billreport.py")
    main.deiconify()


image=Image.open('F:\project\ShopManagement\images\logintypes.jpg')
img=image.resize((1289, 695))
my_img=ImageTk.PhotoImage(img)
label=Label(main, image=my_img)
label.pack()

label2 = Label(main, text="Admin View", font=("times new roman", 30, "bold"),fg="Brown").place(x=550, y=120)

button1 = Button(main)
button1.place(relx=0.211, rely=0.3, width=146, height=160)
button1.configure(relief="flat")
button1.configure(overrelief="flat")
button1.configure(activebackground="#ffffff")
button1.configure(cursor="hand2")
button1.configure(foreground="#ffffff")
button1.configure(background="black")
button1.configure(borderwidth=0)
button1.configure(pady=30)
img1 = ImageTk.PhotoImage(Image.open("F:\project\ShopManagement\images\employeeimage.JPG"))
button1.configure(image=img1)
button1.configure(command=emp)

button2 = Button(main)
button2.place(relx=0.400, rely=0.3, width=146, height=160)
button2.configure(relief="flat")
button2.configure(overrelief="flat")
button2.configure(activebackground="#ffffff")
button2.configure(cursor="hand2")
button2.configure(foreground="#ffffff")
button2.configure(background="black")
button2.configure(borderwidth=0)
button2.configure(pady=30)
img2 = ImageTk.PhotoImage(Image.open("F:\project\ShopManagement\images\Salary.png"))
button2.configure(image=img2)
button2.configure(command=salary)


button3 = Button(main)
button3.place(relx=0.580, rely=0.3, width=146, height=160)
button3.configure(relief="flat")
button3.configure(overrelief="flat")
button3.configure(activebackground="#ffffff")
button3.configure(cursor="hand2")
button3.configure(foreground="#ffffff")
button3.configure(background="black")
button3.configure(borderwidth=0)
button3.configure(pady=30)
img3 =ImageTk.PhotoImage(Image.open("F:\project\ShopManagement\images\stockm.JPG"))
button3.configure(image=img3)
button3.configure(command=stock)

button4 = Button(main)
button4.place(relx=0.755, rely=0.3, width=146, height=160)
button4.configure(relief="flat")
button4.configure(overrelief="flat")
button4.configure(activebackground="#ffffff")
button4.configure(cursor="hand2")
button4.configure(foreground="#ffffff")
button4.configure(background="black")
button4.configure(borderwidth=0)
button4.configure(pady=5)
img4 = ImageTk.PhotoImage(Image.open("F:\project\ShopManagement\images\paying.JPG"))
button4.configure(image=img4)
button4.configure(command=billing)


main.mainloop()
