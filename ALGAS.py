import time
import random
import pyodbc
from sys import getsizeof
import matplotlib.pyplot as plt
from datetime import datetime

conn_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:wordserver.database.windows.net,1433;Database=word-database;Uid=urubu100;Pwd=14052002Kb4_;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
conn = pyodbc.connect(conn_string)
cursor = conn.cursor()


sizes = range(100, 130, 5)
l1 = []
l2 = []

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
    print(f'Valor {n} {stop-start} - Max mem {max_mem/10**3} KB - Min mem {min_mem} B')
    l1.append(stop - start)

for n in sizes:
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
    temperature = random.randint(20, 30)
    capture_date = datetime.now()
    sensor_name = 'thd11'
    sql = "INSERT INTO SensorData (SensorName, SensorValue, CaptureDate) VALUES (?, ?, ?)"
    val = (sensor_name, temperature, capture_date)
    start_insert = time.time()
    cursor.execute(sql, val)
    cursor.commit()
    stop_insert = time.time()
    print(f'Temperatura {temperature} {stop_insert-start_insert} - Max mem {max_mem/10**3} KB - Min mem {min_mem} B')
    l2.append(stop_insert - start_insert)

cursor.close()

plt.plot(sizes, l1, label='Loop 1')
plt.plot(sizes, l2, label='Loop 2')
plt.xlabel('Tamanho da entrada (bytes)')
plt.ylabel('Tempo de execução (s)')
plt.title('Gráfico de tempo de execução')
plt.legend()
plt.show()
