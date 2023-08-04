import os
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox


main = Tk()  # instance for tkinter
main.geometry("1300x1000")
main.title("Management System")
main.resizable(0, 0)


def exit():
    sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=main)
    if sure == True:
        main.destroy()


main.protocol("WM_DELETE_WINDOW", exit)


def click():
    main.withdraw()
    os.system("employee.py")
    main.deiconify()


image = Image.open('F:\project\ShopManagement\images\silver.jpg')
img = image.resize((1289, 695))
my_img = ImageTk.PhotoImage(img)
label = Label(main, image=my_img)
label.pack()

Label(main, text="New Silver Line Traders (Pvt)Ltd", font=("Times new roman", 34, "bold"), bg="#fef0c2").place(x=300,
                                                                                                               y=30)

# Create a button with border radius
btn = Button(main, text='Welcome!', command=click, font=('Times New Roman', 30, 'bold'), width=10, bg='#FADDA0',
             bd=0, highlightthickness=0, cursor='hand2')
btn.config(border=10, relief='solid')

# Position the button on the window
btn.place(x=490, y=300)


main.mainloop()
