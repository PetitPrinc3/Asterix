import sqlite3
import os

from Asterix_libs.prints import *

def db_test(path):
    try:
        conn = sqlite3.connect(path)
        cur= conn.cursor()
        success('Database connection opened.')
        sql= 'SELECT sqlite_version();'
        cur.execute(sql)
        res=cur.fetchall()
        info('SQLite Version : ' + res[0][0])
        cur.execute("""CREATE TABLE IF NOT EXISTS known_drives (idVendor TEXT, idProduct TEXT)""")
        success("Known drives table checked.")
        conn.commit()
        cur.close()
        conn.close()
        success('Database connection closed\n')
        return True
    except sqlite3.Error as error:
        fail('Database connection failed')
        return False


#get vid and pid of the usb drive plugged 
def get_ids(path):
    idProduct=os.popen(f'udevadm info -q all -a {path} | grep idProduct | cut -d "=" -f 3 | head -n 1').read().strip()
    idVendor=os.popen(f'udevadm info -q all -a {path} | grep idVendor | cut -d "=" -f 3 | head -n 1').read().strip()
    return idVendor, idProduct


#check if vid and pid of getid is in the database
def match_ids(db, Vid, Pid):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(f"""SELECT idVendor, idProduct FROM known_drives WHERE (idVendor = {Vid} AND idProduct = {Pid})""")
    data= cursor.fetchone()
    cursor.close()
    conn.close()
    
    if data is not None:
        return(True)
    else:
        return(False)
