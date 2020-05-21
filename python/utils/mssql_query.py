from .db_result import dbResult
import pyodbc 

def mssql_query(config, request):

    result = dbResult()

    driver = '{SQL Server}'
    connection = pyodbc.connect('DRIVER={0};SERVER={1};DATABASE={2};UID={3};PWD={4}'.format(
        driver,
        config['host'],
        config['database'],
        config['user'],
        config['password']
        ))
    cursor = connection.cursor()

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

    result.ok = (cursor.rowcount > 0)

    return result