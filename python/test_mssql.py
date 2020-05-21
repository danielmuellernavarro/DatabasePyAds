import pyodbc
from utils.db_result import dbResult

result = dbResult()
config = dict()

config['host'] = '192.168.1.2'
config['database'] = 'test'
config['user'] = 'test'
config['password'] = '123'

str_connection = ("DRIVER={SQL Server};"
                "SERVER=" + config['host'] + ";"
                "DATABASE=" + config['database'] + ";"
                "UDI=" + config['user'] + ";"
                "PWD=" + config['password'])
driver = '{SQL Server}'
str_connection = 'DRIVER={0};SERVER={1};DATABASE={2};UID={3};PWD={4}'.format(
    driver,
    config['host'],
    config['database'],
    config['user'],
    config['password']
    )

connection = pyodbc.connect(str_connection)
cursor = connection.cursor()

request = """
SELECT TOP 1 Status FROM test.test.test WHERE MachineID=123
"""

cursor.execute(request)
records = cursor.fetchall()

result.rowcount = cursor.rowcount
# result.colums = cursor.column_names
result.columncount = len(result.colums)
for i, row in enumerate(records):
    row_result = list()
    print(row)
    for val in row:
        row_result.append(str(val))
    result.values.append(row_result)

result.ok = True
