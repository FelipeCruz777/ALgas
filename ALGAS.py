import time
import random
import pyodbc
from sys import getsizeof

conn_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:serer-cruz.database.windows.net,1433;Database=algas-cruz;Uid=adm;Pwd=Urubu100@;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
conn = pyodbc.connect(conn_string)
cursor = conn.cursor()

cursor.execute("IF NOT EXISTS(SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'temperatura' AND COLUMN_NAME = 'memoria') ALTER TABLE temperatura ADD memoria INT")

sizes = range(200000, 200300, 10000)
l1 = []

for n in sizes:
    data = 'transaction01' * n
    b = data.encode()
    start = time.time()
    max_mem = 0
    min_mem = 0
    while b:
        if n == len(b):
            max_mem = getsizeof(b) - getsizeof(b'')
        elif len(b) == 1:
            min_mem = getsizeof(b) - getsizeof(b'')
        b = b[1:]
    stop = time.time()
    print('Valor ' + str(n) + ' ' + str(stop-start) + ' - Max mem ' + str(max_mem/10**3) + ' KB - Min mem ' + str(min_mem) + ' B')
    l1.append(stop - start)

l2 = []
for i in range(30):
    n = random.choice(sizes)
    data = b'x' * n
    b = memoryview(data)
    start = time.time()
    max_mem = 0
    min_mem = 0
    while b:
        if n == len(b):
            max_mem = getsizeof(b) - getsizeof(b'')
        elif len(b) == 1:
            min_mem = getsizeof(b) - getsizeof(b'')
        b = b[1:]
    temperature = random.randint(20, 40)
    location = "West Europe"
    sql = "INSERT INTO temperatura (temperatura, regiao, memoria) VALUES (?, ?, ?)"
    val = (temperature, location, max_mem)
    start_insert = time.time()
    cursor.execute(sql, val)
    cursor.commit()
    stop_insert = time.time()
    print(f'Temperatura {n} {stop_insert-start_insert} - Max mem {max_mem/10**3} KB - Min mem {min_mem} B')
    l2.append(stop_insert - start_insert)
    
cursor.close()
