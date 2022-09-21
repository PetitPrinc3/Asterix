import sqlite3

try:
        conn=sqlite3.connect('USB_ID.db')
        cur= conn.cursor()
        print('Database connection opened.')
        sql= 'SELECT sqlite_version();'
        cur.execute(sql)
        res=cur.fetchall()
        print('SQLite Version : ' + res[0][0])
        cur.execute("""CREATE TABLE IF NOT EXISTS known_drives (idVendor TEXT, idProduct TEXT)""")
        print("Known drives table checked.")
        cur.execute("""INSERT INTO known_drives(idVendor,idProduct) VALUES (?,?)""",("058f","6387"))
        print('Inserted ("058f","6387")')
        conn.commit()
        cur.close()
        conn.close()
        print('Database connection closed\n')
except sqlite3.Error as error:
        print('Database initialization failed')