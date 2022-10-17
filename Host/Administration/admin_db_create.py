import sqlite3

from Asterix_libs.log import *

def create():
    conn=sqlite3.connect('ASTERIX_ADMIN.db')
    cur= conn.cursor()
    print('Database connection opened.')
    sql= 'SELECT sqlite_version();'
    cur.execute(sql)
    res=cur.fetchall()
    print('SQLite Version : ' + res[0][0])
    cur.execute("""CREATE TABLE IF NOT EXISTS containers (name TEXT, id TEXT)""")
    cur.execute("""INSERT INTO containers(name, id) VALUES (?,?)""",("frontend","21795d8763cf"))
    cur.execute("""INSERT INTO containers(name, id) VALUES (?,?)""",("backend","397a5e3ed23b"))
    cur.execute("""INSERT INTO containers(name, id) VALUES (?,?)""",("brain","757c54e6cbd0"))
    
    cur.execute("""CREATE TABLE IF NOT EXISTS vms (name TEXT, disk TEXT, hash TEXT)""")
    cur.execute("""INSERT INTO vms(name, disk, hash) VALUES (?,?,?)""",("AC-CENTER","/src/win10_VM/system.vhdx", "x5b902ffa10efb18d8066b40cbed89e9a"))
 
    conn.commit()
    cur.close()
    conn.close()
    print('Database connection closed\n')


if __name__ == "__main__":
    create()

