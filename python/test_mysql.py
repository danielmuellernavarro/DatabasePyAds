import mysql.connector


str_input = """
SELECT seriennummer_setzen (197)
"""

connection = mysql.connector.connect(host='192.168.1.1',
                                    database='test',
                                    user='test',
                                    password='123',
                                    autocommit=True)
                                    
cursor = connection.cursor()
cursor.execute(str_input)
records = cursor.fetchall()

for row in records:
    print(row)

num_fields = len(cursor.description)
field_names = [i[0] for i in cursor.description]
for x in field_names:
    print(x)