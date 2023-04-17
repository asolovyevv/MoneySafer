import sqlite3

conn = sqlite3.connect("MoneySafer.db")

print("База данных открылась отлично!")
try:
    conn.execute("""CREATE TABLE IF NOT EXISTS Expense
    (username CHAR(10)  NOT NULL,
    item CHAR(20) NOT NULL,
    tag TEXT NOT NULL,
    type TEXT NOT NULL,
    amount INT ,
    edate CHAR(10)
    );""")
except:
    print()

print("Таблица создана вврно")

conn.execute('''CREATE TABLE IF NOT EXISTS User
    (
    username CHAR(20) NOT NULL,
    passwrod CHAR(20) NOT NULL,
    budget INT NOT NULL
    );''')
print("Таблица создана вврно")

try:
    conn.execute('''CREATE TABLE IF NOT EXISTS Budget
    (
    username CHAR(20) NOT NULL,
    item CHAR(20) NOT NULL,
    lim INT
    );''')

except:
    print()

print("Таблица создана вврно")

li = [['asolovyevv', 'продукты', 'другое', 'расход', 200, '2021/11/03'],
      ['asolovyevv', 'фильм', 'развлечение', 'расход', 300, '2019/11/22'],
      ['asolovyevv', 'учеба', 'образование', 'доход', 1000, '2022/11/25'],
      ['asolovyevv', 'развлечения', 'образование', 'расход', 500, '2020/10/02'],
      ['asolovyevv', 'diwali', 'gift income', 'доход', 500, '2018/10/02'],
      ['asolovyevv', 'стипендия', 'зарплата', 'доход', 10000, '2022/09/01'],
      ['asolovyevv', 'школа', 'образование', 'расход', 5000, '2022/09/01'],
      ['asolovyevv', 'подарок', 'другое', 'доход', 2000, '2022/08/28'],
      ['asolovyevv', 'развлечения', 'другое', 'доход', 1000, '2020/08/28']]

for i in li:
    conn.execute("""INSERT INTO Expense VALUES(?,?,?,?,?,?);""", i)
    print("Дата введена верно!")
conn.commit()
print("Показываю дату: ")

conn.execute("""INSERT INTO User VALUES('asolovyevv','123',10000)""")
conn.commit()

conn.execute("INSERT INTO Budget VALUES('asolovyevv','movie',1000)")
conn.commit()
