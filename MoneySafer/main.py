from tkinter import *
from tkcalendar import *
import matplotlib
import numpy

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from datetime import date
import sqlite3
from tkinter import messagebox

root = Tk()
root.geometry("800x600")
root.title('MoneySafer')
rootWidth = root.winfo_screenwidth()
conn = sqlite3.connect("MoneySafer.db")

uname = ''


def populateTransaction(frame):
    Label(frame, text="Поиск транзакции", width=rootWidth, height=3, anchor=CENTER, bg='lightblue3', fg='snow', bd=4,
          font=('Algerian', '14', 'bold')).pack()
    searchFrame = Frame(frame, padx=10, pady=10)
    searchFrame.pack(fill=BOTH, expand=True)
    searchFrame.grid_columnconfigure(0, weight=1)
    searchFrame.grid_columnconfigure(1, weight=1)
    searchFrame.grid_columnconfigure(2, weight=1)
    searchFrame.grid_columnconfigure(3, weight=1)
    Label(searchFrame, text="С", font=('Lucida Console', '12', 'bold'), bg='salmon', fg='snow', width=10).grid(row=0,
                                                                                                               column=1)
    startDate_E = DateEntry(searchFrame, width=20, bd=3, date_pattern='yyyy/mm/dd')
    startDate_E.grid(row=0, column=2, pady=5)
    Label(searchFrame, text="По", font=('Lucida Console', '12', 'bold'), bg='salmon', width=10, fg='snow').grid(row=1,
                                                                                                                column=1)
    endDate_E = DateEntry(searchFrame, width=20, bd=3, date_pattern='yyyy/mm/dd')
    endDate_E.grid(row=1, column=2, pady=5)

    def search():
        for widget in dataFrame.winfo_children():
            widget.destroy()
        a = startDate_E.get()
        b = endDate_E.get()

        cursor = conn.execute(
            "SELECT * FROM Expense where username='%s' and edate >= '%s' and edate <= '%s'" % (uname, a, b))
        # cursor = conn.execute("SELECT * FROM Expense where edate='22/11/2019' or edate='20/11/2019' or edate='21/11/2019' or edate='01/11/2019'")
        i = 0
        for r in cursor:
            if r[3] == 'expense':
                Label(dataFrame, text="%s - (%s) :" % (r[1], r[5]), width=50, height=3, borderwidth='1', relief='solid',
                      bg='salmon', pady=3, fg='white', font=('Copperplate Gothic Bold', '13')).grid(row=i, column=1)
                Label(dataFrame, text='%s' % (r[4]), width=50, height=3, borderwidth='1', bg='salmon', relief='solid',
                      pady=3, fg='white', font=('Copperplate Gothic Bold', '13')).grid(row=i, column=2)
                i += 1
            else:
                Label(dataFrame, text="%s - (%s) :" % (r[1], r[5]), width=50, height=3, borderwidth='1', relief='solid',
                      bg='light salmon', pady=3, fg='white', font=('Copperplate Gothic Bold', '13')).grid(row=i,
                                                                                                          column=1)
                Label(dataFrame, text='%s' % (r[4]), width=50, height=3, borderwidth='1', bg='light salmon',
                      relief='solid', pady=3, fg='white', font=('Copperplate Gothic Bold', '13')).grid(row=i, column=2)
                i += 1

    Button(searchFrame, text="Поиск", width=10, command=search, bg='royal blue4', fg='snow',
           activebackground='royal blue3', font=('Brush Script MT', '18')).grid(row=2, column=2, pady=10)
    dataFrame = Frame(frame, padx=10, pady=10)
    dataFrame.pack(fill=BOTH, expand=True)
    dataFrame.grid_columnconfigure(0, weight=1)
    dataFrame.grid_columnconfigure(1, weight=2)
    dataFrame.grid_columnconfigure(2, weight=2)

    # database

    today = str(date.today()).replace("-", "/")
    cursor = conn.execute(
        "SELECT * FROM Expense WHERE edate='%s' and type='expense' and username='%s'" % (today, uname))
    i = 0
    for r in cursor:
        Label(dataFrame, text="%s - (%s)" % (r[1], r[5]), width=50, height=3, borderwidth='1', relief='solid',
              bg='salmon', pady=3, fg='white', font=('Copperplate Gothic Bold', '13')).grid(row=i, column=1)
        Label(dataFrame, text='%s' % (r[4]), width=50, height=3, borderwidth='1', bg='salmon', relief='solid', pady=3,
              fg='white', font=('Copperplate Gothic Bold', '13')).grid(row=i, column=2)
        i += 1
    cursor = conn.execute("SELECT * FROM Expense WHERE edate='%s' and type='income' and username='%s'" % (today, uname))
    for r in cursor:
        Label(dataFrame, text="%s - (%s) :" % (r[1], r[5]), width=50, height=3, borderwidth='1', relief='solid',
              bg='light salmon', pady=3, fg='white', font=('Copperplate Gothic Bold', '13')).grid(row=i, column=1)
        Label(dataFrame, text='%s' % (r[4]), width=50, height=3, borderwidth='1', bg='light salmon', relief='solid',
              pady=3, fg='white', font=('Copperplate Gothic Bold', '13')).grid(row=i, column=2)
        i += 1


def populateHome(frame):
    Label(frame, text="Ваши транзакции", width=rootWidth, height=3, anchor=CENTER, bg='lightblue3', fg='snow', bd=4,
          font=('Algerian', '14', 'bold')).pack()
    userInfo = Frame(frame, pady=5)
    userInfo.pack(fill=BOTH, expand=True)
    userInfo.grid_columnconfigure(0, weight=1)
    userInfo.grid_columnconfigure(1, weight=1)

    def transaction1():
        global tran_win
        tran_win = Toplevel(userInfo)
        tran_win.title("Добавить транзакцию")
        tran_win.geometry("500x300")
        Label(tran_win, text="Добавить транзакцию : ").grid(row=0, column=0, sticky=W, pady=2)
        v = StringVar()  # for type
        v.set(1)
        name = StringVar()  # for name of expense
        amt = StringVar()
        tg = StringVar()
        typ = StringVar()
        typ.set("expense")

        def event():
            if v.get() == "1":
                nl.config(text="Тип расходов : ")
                radio1.config(text="Нужды")
                radio2.config(text="Развлечения")
                radio3.config(text="Образование")
                radio4.config(text="Другое")
                radioVar.set(0)
                typ.set("expense")
            else:
                nl.config(text="Тип доходов : ")
                radio1.config(text="Зарплата")
                radio2.config(text="Стипендия") 
                radio3.config(text="Доп.заработок")
                radio4.config(text="Другое")
                radioVar.set(0)
                typ.set("income")

        def update():
            if radioVar.get() == '1':
                tg.set(radio1.cget("text"))
            if radioVar.get() == '2':
                tg.set(radio2.cget("text"))
            if radioVar.get() == '3':
                tg.set(radio3.cget("text"))
            if radioVar.get() == '4':
                tg.set(radio4.cget("text"))

        Radiobutton(tran_win, text="Расходы", variable=v, value=1, command=event).grid(row=2, column=0, sticky=W,
                                                                                       pady=2)
        Radiobutton(tran_win, text="Доходы", variable=v, value=2, command=event).grid(row=2, column=3, sticky=W, pady=2)
        nl = Label(tran_win, text="Тип расходов : ")
        nl.grid(row=3, column=0, sticky=W, pady=2)
        Entry(tran_win, textvariable=name).grid(row=3, column=3, sticky=W, pady=2)
        Label(tran_win, text="Сумма : ").grid(row=4, column=0, sticky=W, pady=2)
        Entry(tran_win, textvariable=amt).grid(row=4, column=3, sticky=W, pady=2)
        Label(tran_win, text="Тип : ").grid(row=5, column=0, sticky=W, pady=2)
        radioVar = StringVar()
        radioVar.set(0)
        radio1 = Radiobutton(tran_win, text="Нужды", variable=radioVar, command=update, value=1)
        radio1.grid(row=5, column=3, sticky=W, padx=2, pady=2)
        radio2 = Radiobutton(tran_win, text="Развлечения", variable=radioVar, command=update, value=2)
        radio2.grid(row=5, column=5, sticky=W, padx=2, pady=2)
        radio3 = Radiobutton(tran_win, text="Образование", variable=radioVar, command=update, value=3)
        radio3.grid(row=6, column=3, sticky=W, padx=2, pady=2)
        radio4 = Radiobutton(tran_win, text="Другое", variable=radioVar, command=update, value=4)
        radio4.grid(row=6, column=5, sticky=W, padx=2, pady=2)

        def add_to_database():
            try:
                conn.execute(
                    "INSERT into Expense(username,item,tag,type,amount,edate) VALUES ('%s','%s','%s','%s','%d','%s');" %
                    (uname, name.get(), tg.get(), typ.get(), int(amt.get()), today))
                conn.commit()
                Label(tran_win, text="Транзакция добавлена", fg="light salmon", font=("calibri", 11)).grid(row=8,
                                                                                                           column=3,
                                                                                                           sticky=W,
                                                                                                           pady=2)
                tran_win.destroy()
            except:
                Label(tran_win, text="Транзакция не удалась!", fg="salmon", font=("calibri", 11)).grid(row=8, column=3,
                                                                                                       sticky=W, pady=2)

        add = Button(tran_win, text="Добавить", width=10, command=add_to_database)
        add.grid(row=7, column=3, sticky=W, pady=2)

    # user_info
    cursor1 = conn.execute("Select budget from User where username='%s'" % (uname))
    amtBal = 0
    for r in cursor1:
        amtBal = r[0]

    cursor2 = conn.execute("Select SUM(amount) from Expense where type='expense' and username='%s'" % (uname))
    expBal = 0
    for r in cursor2:
        if r[0] == None:
            expBal = 0
        else:
            expBal = r[0]
    Label(userInfo, text="Имя : ", width=20, bg='salmon', fg='snow', font=('Copperplate Gothic Bold', '10')).grid(row=0,
                                                                                                                  pady=5,
                                                                                                                  column=0)
    Label(userInfo, text="%s" % (uname), width=20, bg='salmon', fg='snow', font=('Copperplate Gothic Bold', '10')).grid(
        row=0, column=1, pady=5)
    Label(userInfo, text="Баланс : ", width=20, bg='salmon', fg='snow', font=('Copperplate Gothic Bold', '10')).grid(
        row=1, column=0, pady=5)
    Label(userInfo, text="%d" % (amtBal), width=20, bg='salmon', fg='snow',
          font=('Copperplate Gothic Bold', '10')).grid(row=1, column=1, pady=5)
    Label(userInfo, text="Общие расходы : ", width=20, bg='salmon', fg='snow',
          font=('Copperplate Gothic Bold', '10')).grid(row=2, column=0, pady=5)
    Label(userInfo, text="%d" % (expBal), width=20, bg='salmon', fg='snow',
          font=('Copperplate Gothic Bold', '10')).grid(row=2, column=1, pady=5)
    Button(userInfo, text='Добавить транзакцию', command=transaction1, width=20, bg='royalblue4', fg='snow',
           font=('Broadway', '10')).grid(row=3, column=1, pady=10)

    # date-time work
    today = str(date.today()).replace("-", "/")
    tdate = int(today[-2:])
    startdate = today[:8] + '01'  # start date of current month (format : yyyy/mm/dd)
    m = int(today[5:7])
    mon = []
    endmon = []
    mon.append(startdate)
    temp = m
    for i in range(3):
        if temp <= 10:
            if m - i - 1 < 1:
                mon.append(
                    str(int(today[:4]) - 1) + "/" + str((m - i - 1) % 12 if (m - i - 1) % 12 != 0 else 12) + "/01")
            else:
                mon.append(today[:5] + "0" + str(m - i - 1) + '/01')
                temp -= 1
        else:
            mon.append(today[:5] + str(m - i - 1) + '/01')
            temp -= 1
    for x in mon:
        endmon.append(x[:8] + "31")
    mon.reverse()
    endmon.reverse()
    endmon.pop()
    endmon.append(today)
    ##
    Ecat = ["Нужды", "Развлечения", "Образование", "Другое"]
    Icat = ["Зарплата", "Стипендия", "Доп.заработок", "Другое"]
    count = [0, 0, 0, 0]

    # daily summary
    daily_sum = Frame(frame, width=100, height=100)
    # data retrival
    dt = []
    for i in range(7):
        d = today[:8] + str(tdate - i)
        dt.append(d)
    dt.reverse()
    val = []
    for i in range(7):
        cursor = conn.execute(
            "SELECT sum(amount) FROM Expense where  type = \"expense\" and edate='%s' and username='%s'" % (
                dt[i], uname))
        row = cursor.fetchone()
        if row[0] is None:
            val.append(0)
        else:
            val.append(int(row[0]))

    # graph
    f = Figure(figsize=(4, 4), dpi=100)
    ax = f.add_subplot(111)
    ind = numpy.arange(7)  # the x locations for the groups
    width = .25
    for i in range(7):
        dt[i] = dt[i][5:].split("/")
        dt[i].reverse()
        dt[i] = "/".join(dt[i])
    rects1 = ax.bar(ind, val, width, tick_label=dt, color=['red', 'green', 'blue', 'black'])
    ax.set_xlabel('Дата')
    ax.set_ylabel('Расходы')
    ax.set_title('Ежедневные расходы')
    canvas = FigureCanvasTkAgg(f, master=daily_sum)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH)
    #
    daily_sum.pack(fill=BOTH, expand=True)

    # budget_summary
    bud_sum = Frame(frame)
    # <data retrival>
    cursor = conn.execute(
        "SELECT amount,tag from Expense where type=\"expense\" and username='%s' and edate>='%s' and edate<='%s'" % (
            uname, startdate, today))
    rows = cursor.fetchall()
    for row in rows:
        for i in range(len(Ecat)):
            if row[1].lower() == Ecat[i].lower():
                count[i] += row[0]
                break
    value = []
    tag = []
    for i in range(len(Ecat)):
        if count[i] != 0:
            value.append(count[i])
            tag.append(Ecat[i])
    # <graph>
    f = Figure(figsize=(4, 4), dpi=100)
    ax = f.add_subplot(111)
    rects1 = ax.pie(value, labels=tag)
    ax.set_title('Месячные расходы')
    canvas = FigureCanvasTkAgg(f, master=bud_sum)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH)
    #
    bud_sum.pack(fill=BOTH, expand=True)

    # earning_summary
    ear_sum = Frame(frame)
    # data retrival
    inc = [0, 0, 0, 0]
    exp = [0, 0, 0, 0]
    for i in range(4):
        cursor = conn.execute("SELECT type,amount from Expense where username='%s' and edate>='%s' and edate<='%s'" % (
            uname, mon[i], endmon[i]))
        rows = cursor.fetchall()
        for row in rows:
            if row[0].lower() == "expense":
                exp[i] += row[1]
            elif row[0].lower() == "income":
                inc[i] += row[1]
    #
    l = []
    for x in mon:
        x = x[2:7].split("/")
        x.reverse()
        l.append("/".join(x))
    # graph
    f = Figure(figsize=(4, 4), dpi=100)
    ax = f.add_subplot(111)
    ind = numpy.arange(4)  # the x locations for the groups
    width = .25
    rects1 = ax.bar(ind, exp, width, tick_label=l, color=['red'])
    rects1 = ax.bar(ind + width, inc, width, tick_label=l, color=['green'])
    ax.set_xlabel('Месяца')
    ax.set_ylabel('Сумма')
    ax.set_title('Чистый доход')
    canvas = FigureCanvasTkAgg(f, master=ear_sum)
    canvas.draw()
    canvas.get_tk_widget().pack(side=TOP, fill=BOTH)
    ear_sum.pack(fill=BOTH, expand=True)


def populateItem(frame):
    Label(frame, text="Трекеринг бюджета на месяц", width=rootWidth, height=3, anchor=CENTER, bg='lightblue3',
          fg='snow', bd=4, font=('Algerian', '14', 'bold')).pack()
    scaleFrame = Frame(frame, pady=10)
    scaleFrame.pack(fill=BOTH, expand=True)
    scaleFrame.grid_columnconfigure(0, weight=1)
    scaleFrame.grid_columnconfigure(1, weight=1)

    # database
    cursor = conn.execute(
        "SELECT SUM(amount), item from Expense where username='%s' and LOWER(item) IN (SELECT LOWER(item) from Budget "
        "where username='%s') GROUP BY item" % (
            uname, uname))
    i = 0
    for r in cursor:
        Label(scaleFrame, text='%s' % r[1], width=20, height=3, borderwidth='1', relief='solid', bg='magenta4',
              fg='white', font=('Copperplate Gothic Bold', '13')).grid(row=i, column=0, pady=5)
        s = Scale(scaleFrame, orient=HORIZONTAL, length=300, from_=1, to=100, fg='brown4', troughcolor='salmon1',
                  bg='khaki1')
        s.grid(row=i, column=1, pady=5)
        a = r[0]
        cursor1 = conn.execute("SELECT lim from Budget Where item = '%s' and username='%s'" % (r[1], uname))
        for r1 in cursor1:
            a = (a / r1[0]) * 100
        s.set(a)
        i += 1

    def setBudget():
        top = Toplevel(bg='lightblue3')
        top.title('Установить бюджет')
        top.grid_columnconfigure(0, weight=1)
        top.grid_columnconfigure(1, weight=2)
        top.grid_columnconfigure(2, weight=2)
        top.grid_columnconfigure(3, weight=1)
        Label(top, text='Введите тип', pady=5, padx=5, font=('Britannic Bold', '10'), fg='snow', bg='salmon').grid(
            row=0, column=1, pady=5)
        setE1 = Entry(top, width=30)
        setE1.grid(row=0, column=2, pady=5)
        Label(top, text='Установить', pady=5, padx=5, font=('Britannic Bold', '10'), fg='snow', bg='salmon').grid(row=1,
                                                                                                                  column=1,
                                                                                                                  pady=5)
        setE2 = Entry(top, width=30)
        setE2.grid(row=1, column=2, pady=5)

        def change():
            a = setE1.get()
            b = setE2.get()
            conn.execute("INSERT INTO Budget values('%s','%s','%s')" % (uname, a, b))
            conn.commit()
            top.destroy()

        Button(top, text='Установить', command=change, width=10, height=1, bd=2, fg='snow', bg='royalblue4', pady=4,
               font=('Britannic Bold', '13')).grid(row=2, column=2, pady=10)
        top.minsize(400, 150)
        top.mainloop()

    Button(scaleFrame, text='Установить бюджет', command=setBudget, fg='snow', bg='royalblue4', width=20, height=2,
           relief='solid', font=('Broadway', '16')).grid(row=i + 1, column=0, columnspan=3, pady=20, padx=20)


def populateTagSummary(frame):
    Label(frame, text="Это месячные расходы", width=rootWidth, height=3, anchor=CENTER, bg='lightblue3', fg='snow',
          bd=4, font=('Algerian', '13', 'bold')).pack()
    expenseFrame = Frame(frame, padx=10, pady=10)
    expenseFrame.pack(fill=BOTH, expand=True)
    expenseFrame.grid_columnconfigure(0, weight=1)
    expenseFrame.grid_columnconfigure(1, weight=1)
    today = str(date.today()).replace("-", "/")
    sdate = today[:8] + '01'  # start date of current month (format : yyyy/mm/dd)
    cursor = conn.execute(
        "SELECT SUM(amount) FROM Expense WHERE type='expense' and username='%s' and edate>='%s' and edate<='%s'" % (
            uname, sdate, today))
    sum = 0
    flag1 = 0
    flag2 = 0
    for r in cursor:
        if r[0] is None:
            sum += 0
        else:
            sum += r[0]
            flag1 = 1
    Label(expenseFrame, text='Расходы', pady=5, width=50, height=3, borderwidth='1', relief='solid', bg='salmon',
          fg='snow', font=('Copperplate Gothic Bold', '13')).grid(row=0, column=0)
    Label(expenseFrame, text='%s' % str(sum), pady=5, width=50, height=3, borderwidth='1', relief='solid', bg='salmon',
          fg='snow', font=('Copperplate Gothic Bold', '13')).grid(row=0, column=1)

    # database
    i = 1
    if flag1 == 1:
        cursor = conn.execute(
            "SELECT * FROM Expense WHERE type='expense' and username='%s'  and edate>='%s' and edate<='%s'" % (
                uname, sdate, today))
        for r in cursor:
            Label(expenseFrame, text="%s" % r[2], pady=5, width=50, height=3, borderwidth='1', relief='solid',
                  bg='salmon', fg='snow', font=('Copperplate Gothic Bold', '13')).grid(row=i, column=0)
            Label(expenseFrame, text="%s" % r[4], pady=5, width=50, height=3, borderwidth='1', relief='solid',
                  bg='salmon', fg='snow', font=('Copperplate Gothic Bold', '13')).grid(row=i, column=1)
            i += 1

    cursor = conn.execute(
        "SELECT SUM(amount) FROM Expense WHERE type='income' and username='%s'  and edate>='%s' and edate<='%s'" % (
        uname, sdate, today))
    sum = 0
    for r in cursor:
        if r[0] is None:
            sum += 0
        else:
            sum += r[0]
            flag2 = 1
    Label(expenseFrame, text='Доходы', pady=5, width=50, height=3, borderwidth='1', relief='solid', bg='light salmon',
          fg='white', font=('Copperplate Gothic Bold', '13')).grid(row=i, column=0)
    Label(expenseFrame, text='%s' % str(sum), pady=5, width=50, height=3, borderwidth='1', relief='solid',
          bg='light salmon', fg='white', font=('Copperplate Gothic Bold', '13')).grid(row=i, column=1)
    i += 1

    if flag2 == 1:
        cursor = conn.execute(
            "SELECT * FROM Expense WHERE type='income' and username='%s'  and edate>='%s' and edate<='%s'" % (
                uname, sdate, today))

        for r in cursor:
            Label(expenseFrame, text="%s" % r[2], pady=5, width=50, height=3, borderwidth='1', relief='solid',
                  bg='light salmon', fg='snow', font=('Copperplate Gothic Bold', '13')).grid(row=i, column=0)
            Label(expenseFrame, text="%s" % r[4], pady=5, width=50, height=3, borderwidth='1', relief='solid',
                  bg='light salmon', fg='snow', font=('Copperplate Gothic Bold', '13')).grid(row=i, column=1)
            i += 1


def transactionHelper():
    home.grid_forget()
    itemTracker.grid_forget()
    tagSummary.grid_forget()
    # transaction.grid_forget()
    for Widget in transaction.winfo_children():
        Widget.destroy()
    transaction.grid(row=0, column=1, pady=5)
    populateTransaction(transaction)
    transaction.tkraise()


def homeHelper():
    # home.grid_forget()
    itemTracker.grid_forget()
    tagSummary.grid_forget()
    transaction.grid_forget()
    for Widget in home.winfo_children():
        Widget.destroy()
    home.grid(row=0, column=1)
    populateHome(home)
    home.tkraise()


def tagSummaryHelper():
    home.grid_forget()
    itemTracker.grid_forget()
    # tagSummary.grid_forget()
    transaction.grid_forget()
    for Widget in tagSummary.winfo_children():
        Widget.destroy()
    tagSummary.grid(row=0, column=1, pady=5)
    populateTagSummary(tagSummary)
    tagSummary.tkraise()


def itemHelper():
    home.grid_forget()
    # itemTracker.grid_forget()
    tagSummary.grid_forget()
    transaction.grid_forget()
    for Widget in itemTracker.winfo_children():
        Widget.destroy()
    itemTracker.grid(row=0, column=1, pady=5)
    populateItem(itemTracker)
    itemTracker.tkraise()


def registration():
    top = Toplevel(bg='lightblue3')
    top.title('User Registration')
    top.grid_columnconfigure(0, weight=1)
    top.grid_columnconfigure(1, weight=2)
    top.grid_columnconfigure(2, weight=2)
    top.grid_columnconfigure(3, weight=1)
    Label(top, text='Введите имя', pady=5, height=1, padx=5, font=('Britannic Bold', '10'), fg='snow',
          bg='salmon').grid(row=0, column=1, pady=10)
    regE1 = Entry(top, width=30)
    regE1.grid(row=0, column=2, pady=5)
    Label(top, text='Введите пароль', pady=5, height=1, padx=5, font=('Britannic Bold', '10'), fg='snow',
          bg='salmon').grid(row=1, column=1, pady=5)
    regE2 = Entry(top, width=30)
    regE2.grid(row=1, column=2, pady=5)
    Label(top, text='Введите баланс', pady=5, height=1, padx=5, font=('Britannic Bold', '10'), fg='snow',
          bg='salmon').grid(row=2, column=1, pady=5)
    regE3 = Entry(top, width=30)
    regE3.grid(row=2, column=2, pady=5)

    def change():
        a = regE1.get()
        b = regE2.get()
        c = regE3.get()
        conn.execute("insert into User values('%s','%s',%d)" % (a, b, int(c)))
        conn.commit()
        global uname
        uname = a
        for Widget in user.winfo_children():
            Widget.destroy()
        top.destroy()
        home.grid(row=0, column=1, pady=5)
        populateHome(home)
        home.tkraise()

    Button(top, text='Регистрация', command=change, width=12, height=1, bd=2, fg='snow', bg='royalblue4', pady=4,
           font=('Britannic Bold', '13')).grid(row=3, column=2, pady=20)
    top.minsize(400, 200)
    top.mainloop()


def populateUser(frame):
    Label(frame, text="MoneySafer", width=rootWidth, height=2, anchor=CENTER, bg='lightblue3', fg='royalblue4', bd=4,
          font=('Algerian', '24', 'bold')).pack()
    Label(frame, text='Пожалуйста войдите/зарегестрируйтесь, чтобы продолжить', pady=5, width=rootWidth, height=3,
          anchor=CENTER, bg='lightblue3', fg='snow', bd=4, font=('Algerian', '13', 'bold')).pack()
    login = Frame(frame, pady=10)
    login.pack(fill=BOTH, expand=True)
    login.grid_columnconfigure(0, weight=1)
    login.grid_columnconfigure(1, weight=1)
    Label(login, text='Имя пользователя :', width=30, fg="snow", bg='salmon', font=('Bernard MT Condensed', '14')).grid(
        row=0, column=0, pady=10)
    ue1 = Entry(login, width=30, bg='light salmon')
    ue1.grid(row=0, column=1, pady=10)
    Label(login, text='Пароль :', width=30, fg="snow", bg='salmon', font=('Bernard MT Condensed', '14')).grid(row=1,
                                                                                                              column=0,
                                                                                                              pady=10)
    ue2 = Entry(login, show='*', width=30, bg='light salmon')
    ue2.grid(row=1, column=1, pady=10)

    def userHelper():

        a1 = ue1.get()
        b1 = ue2.get()

        cursor = conn.execute("Select * from User where username='%s' and passwrod='%s'" % (a1, b1))
        if len(cursor.fetchall()) > 0:
            for Widget in user.winfo_children():
                Widget.destroy()
            home.grid(row=0, column=1, pady=5)
            home.tkraise()
            global uname
            uname = a1
            populateHome(home)
        else:
            messagebox.showerror("Ошибка", "Данные неверны!")

    Button(login, text='Войти', width=20, height=2, fg="snow", bg='RoyalBlue4', command=userHelper,
           font=('Broadway', '14')).grid(row=2, column=0, pady=10)
    Button(login, text='Регистрация', width=20, height=2, fg="snow", bg='RoyalBlue4', command=registration,
           font=('Broadway', '14')).grid(row=2, column=1, pady=10)


def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))


def FrameWidth(event):
    canvas_width = event.width
    canvas.itemconfig(canvas_frame, width=canvas_width)


canvas = Canvas(root, borderwidth=0)
frame = Frame(canvas)
vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas_frame = canvas.create_window((0, 0), anchor="nw")
canvas.itemconfigure(canvas_frame, window=frame)
frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
canvas.bind('<Configure>', lambda event: FrameWidth(event))

frameTab = Frame(frame)
frameTab.pack(side="top", fill="both", expand=True)
frameTab.grid_columnconfigure(0, weight=1)
frameTab.grid_columnconfigure(1, weight=1)
frameTab.grid_columnconfigure(2, weight=1)
frameTab.grid_columnconfigure(3, weight=1)
Button(frameTab, text="Главная", relief="solid", width=50, height=2, bd=1, bg='RoyalBlue4', fg='snow',
       command=homeHelper, font=("Times", "13", "bold italic")).grid(row=0, column=0)
Button(frameTab, text="Транзакции", relief="solid", width=50, height=2, bd=1, bg='RoyalBlue4', fg='snow',
       command=transactionHelper, font=("Times", "13", "bold italic")).grid(row=0, column=1)
Button(frameTab, text="Общая сумма", relief="solid", width=50, height=2, bd=1, bg='RoyalBlue4', fg='snow',
       command=tagSummaryHelper, font=("Times", "13", "bold italic")).grid(row=0, column=2)
Button(frameTab, text="Бюджет", relief="solid", width=50, height=2, bd=1, bg='RoyalBlue4', fg='snow',
       command=itemHelper, font=("Times", "13", "bold italic")).grid(row=0, column=3)

f = Frame(frame)
f.pack(fill=BOTH, expand=True)
f.grid_columnconfigure(0, weight=1)
f.grid_columnconfigure(1, weight=8)
f.grid_columnconfigure(2, weight=1)

home = Frame(f)
transaction = Frame(f)
tagSummary = Frame(f)
itemTracker = Frame(f)
user = Frame(f)
user.grid(row=0, column=1, pady=10)
populateUser(user)
user.tkraise()
root.mainloop()
