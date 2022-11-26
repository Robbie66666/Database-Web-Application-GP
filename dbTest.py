import sqlite3



'''
conn = sqlite3.connect("payvand.db")
print("DB Created/opened")
conn.close()
'''

with sqlite3.connect("payvand.db") as conn:
    # print("DB created/Opened")
    # sql = 'create table user(name text, email text, password text)'

    # conn.execute(sql)
    # print("table created")

    sql = 'insert into user (name, email, password) values (?,?,?)'     
    conn.execute(sql, ("marc","marc@marc.com","password"))

# i_name = "'dsfsdffsdsfdsfdsfdfsdsfdsfdsfdsfdsfdsfd' or 1=1"
# #i_name = "marc"

# with sqlite3.connect("marc.db") as conn:
#     cur = conn.cursor()
#     #cur.execute("SELECT * FROM user where name = " + i_name)  #BAD PRACTICE
#     cur.execute("SELECT * FROM user where name = ?", ( i_name,)) #CORRECT WAY
#     data = cur.fetchone()
#     print(data)
