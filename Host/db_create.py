import sqlite3

from Asterix_libs.log import *

def create():
        dblogfile = init_log()
        try:
                conn=sqlite3.connect('USB_ID.db')
                cur= conn.cursor()
                print('Database connection opened.')
                log('Database connection opened.', dblogfile)
                sql= 'SELECT sqlite_version();'
                cur.execute(sql)
                res=cur.fetchall()
                print('SQLite Version : ' + res[0][0])
                log('SQLite Version : ' + res[0][0], dblogfile)
                cur.execute("""CREATE TABLE IF NOT EXISTS known_drives (idVendor TEXT, idProduct TEXT)""")
                print("Known drives table checked.")
                log("Known drives table checked.", dblogfile)
                cur.execute("""INSERT INTO known_drives(idVendor,idProduct) VALUES (?,?)""",("058f","6387"))
                print('Inserted ("058f","6387")')
                log('Inserted ("058f","6387")', dblogfile)
                conn.commit()
                cur.close()
                conn.close()
                log('Database connection closed', dblogfile)
                print('Database connection closed\n')
        except sqlite3.Error as error:
                print('Database initialization failed')
                log('Database initialization failed with error : ' + str(error), dblogfile)

        return dblogfile

if __name__ == "__main__":

        dblogfile = create()

        import subprocess

        subprocess.run('/usr/bin/cp USB_ID.db /var/lib/docker/volumes/DataShare/_data/', shell = True)

        subprocess.run(f'/usr/bin/mv {dblogfile} /opt/asterix/dblog.txt && chown asterix:asterix /opt/asterix/dblog.txt && chmod 600 /opt/asterix/dblog.txt', shell = True)