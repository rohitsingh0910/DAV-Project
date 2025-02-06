import sqlite3



Connection = sqlite3.connect('C:/Users/ADMIN/PycharmProjects/PythonProject_Hiresmart_31jan_5PM/instance/data.db')

cursor = Connection.cursor()

#cursor.execute("INSERT INTO user(name,email,password) values('Rohit','rohit12@gmail.com','5678')")

cursor.execute("select * from user")
data = cursor.fetchall()
for i in data:
    print(i)
#Connection.commit()