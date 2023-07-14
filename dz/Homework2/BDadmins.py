import sqlite3
import datetime
try:
    connection = sqlite3.connect('AllBD.db')
    cur = connection.cursor()
    cur.execute("'CREATE TABLE IF NOT EXISTS tUsers(Name PRIMARY KEY, Password, Admin)'")
    cur.execute('CREATE TABLE IF NOT EXISTS tCars(Name, id, Length, Width, Height, Lifting_capacity, Busy)')
    cur.execute('CREATE TABLE IF NOT EXISTS tOrders(Name_of_customer, id_car, cargo, end_datetime, FOREIGN KEY(Name_of_customer) REFERENCES tUsers(Name), '
                'FOREIGN KEY(id_car) REFERENCES tCars(id))')
    cur.execute("""INSERT INTO tUsers VALUES
    ('IgorSmir', 368813, 1),
    ('VeraShal', 367733, 1),
    ('NatashaPetr', 368646, 1)""")
    new_item = ('Kirill', 630456, 0)
    cur.execute("""INSERT INTO tUsers VALUES(?, ?, ?)""", new_item)
    cur.execute("""INSERT INTO tCars VALUES
    ('MAN-10', 111111, 600, 245, 230, 10000, 0),
    ('MAN-10', 111112, 600, 245, 230, 10000, 1),
    ('ГАЗ-3302 «Газель»', 111113, 300, 200, 170, 2000, 0),
    ('ГАЗ-3302 «Газель»', 111115, 300, 200, 170, 2000, 1),
    ('ЗИЛ-5301 (Бычок)', 111116, 420, 200, 200, 3000, 0), 
    ('ЗИЛ-5301 (Бычок)', 111117, 420, 200, 200, 3000, 0),
    ('ЗИЛ-5301 (Бычок)', 111118, 420, 200, 200, 3000, 1),
    ('Фура Mercedes-Benz Actros', 111119, 1360, 246, 250, 20000, 0)
    """)
    new_item = ('Глеб', 2320, 0)
    cur.execute("""INSERT INTO tUsers VALUES(?, ?, ?)""", new_item)
    new_orders = [('IgorSmir', 111112, 'Кирпичи', datetime.datetime(2023, 6, 6, 14, 10, 0)),
    ('VeraShal', 111115, 'Молоко', datetime.datetime(2023, 6, 7, 10, 0, 0)),
    ('Kirill', 111118, 'Шифер', datetime.datetime(2023, 6, 6, 12, 30, 00))]
    cur.executemany("""INSERT INTO tOrders VALUES (?,?,?,?)""", new_orders)
    cur.close()
finally:
    if (connection):
        connection.commit()
        connection.close()
        print('Соединение закрыто')