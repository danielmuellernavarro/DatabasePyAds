from .db_result import dbResult
import mysql.connector


def mysql_query(config, request):
    result = dbResult()

    connection = mysql.connector.connect(
        host      = config['host'],
        database  = config['database'],
        user      = config['user'],
        password  = config['password'],
        autocommit=True
    )
    cursor = connection.cursor()
    cursor.execute(request)
    records = cursor.fetchall()

    result.rowcount = cursor.rowcount
    result.colums = cursor.column_names
    result.columncount = len(result.colums)
    for i, row in enumerate(records):
        row_result = list()
        for val in row:
            row_result.append(str(val))
        result.values.append(row_result)

    result.ok = (cursor.rowcount > 0)

    return result