import sqlite3
from tkinter import *

conn = sqlite3.connect("MoneySafer.db")

root = Tk()
root.title("Страница операций")
root.geometry("600x600")

canvas = Canvas(root, borderwidth=0)
frame = Frame(canvas)
vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas_frame = canvas.create_window((0, 0), anchor="nw")
canvas.itemconfigure(canvas_frame, window=frame)


def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))


def FrameWidth(event):
    canvas_width = event.width
    canvas.itemconfig(canvas_frame, width=canvas_width)


frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
canvas.bind('<Configure>', lambda event: FrameWidth(event))

rootWidth = root.winfo_screenwidth()


def populate(frame):
    frameTab = Frame(frame, width=root.winfo_screenwidth())
    frameTab.pack(side="top", fill="both", expand=True)
    frameTab.grid_columnconfigure(0, weight=1)
    frameTab.grid_columnconfigure(1, weight=1)
    frameTab.grid_columnconfigure(2, weight=1)
    frameTab.grid_columnconfigure(3, weight=1)
    Button(frameTab, text="Главная", relief="solid", width=10, bd=1).grid(row=0, column=0)
    Button(frameTab, text="Операции", relief="solid", width=13, bd=1).grid(row=0, column=1)
    Button(frameTab, text="Суммарные расходы", relief="solid", width=20, bd=1).grid(row=0, column=2)
    Button(frameTab, text="Бюджет", relief="solid", width=15, bd=1).grid(row=0, column=3)
    Label(frame, text="Этот месяц", width=rootWidth, height=3, anchor=CENTER, bg='lightblue3', bd=4).pack()

    scaleFrame = Frame(frame)
    scaleFrame.pack(fill=BOTH, expand=True)
    scaleFrame.grid_columnconfigure(0, weight=1)
    scaleFrame.grid_columnconfigure(1, weight=1)

    # database
    cursor = conn.execute("SELECT * FROM Expense WHERE lim != 0")
    i = 0
    for r in cursor:
        Label(scaleFrame, text='%s' % r[1], pady=5, width=50, height=3, borderwidth='1', relief='solid',
              bg='lightblue3').grid(row=i, column=0)
        s = Scale(scaleFrame, orient=HORIZONTAL, length=300, from_=1, to=100, fg='snow', bg='lightblue3')
        s.grid(row=i, column=1)
        a = (r[4] / r[6]) * 100
        s.set(a)
        # s.set(50/2)
        i += 1

    #

    def setBudget():
        top = Toplevel()
        top.title('Установите тип бюджета')
        top.grid_columnconfigure(0, weight=1)
        top.grid_columnconfigure(1, weight=2)
        top.grid_columnconfigure(2, weight=2)
        top.grid_columnconfigure(3, weight=1)
        Label(top, text='Введите тип', pady=5, padx=5).grid(row=0, column=1)
        Entry(top, width=30).grid(row=0, column=2)
        Label(top, text='Установите бюджет', pady=5, padx=5).grid(row=1, column=1)
        Entry(top, width=30).grid(row=1, column=2)

        def change():
            top.destroy()

        Button(top, text='Установить', command=change, width=10, height=1, bd=2, fg='blue', pady=4).grid(row=2,
                                                                                                         column=2)
        top.minsize(400, 150)
        top.mainloop()

    Button(scaleFrame, text='Установить бюджет', command=setBudget, fg='snow', bg='royalblue4', width=20, height=2,
           relief='solid').grid(row=i + 1, column=0)


populate(frame)
root.mainloop()
