""" Main file of COVID Russia Stats """
import sqlite3
from datetime import datetime, timedelta
import funcs


conn = sqlite3.connect('COVID.db')
cursor = conn.cursor()
start_total = datetime.now()
f = funcs.Voids()

print('Загрузка страницы')
start = datetime.now()
text = f.get_page_code('https://стопкоронавирус.рф')
print('Операция выполнена за', datetime.now()-start)

print('Получение данных')
start = datetime.now()
data_new = f.get_data(text)
print('Операция выполнена за', datetime.now()-start)

print('Получение даты и времени')
start = datetime.now()
stat_date, stat_time = f.get_date_time(text)
print('Операция выполнена за', datetime.now()-start)

print('Проверка данных')
start = datetime.now()
SQL = """
SELECT * FROM COVID_RUSSIA WHERE DATE = ?
"""
cursor.execute(
    SQL, [(str(datetime.strftime(datetime.now(), '%d.%m.%Y')))])
print('Операция выполнена за', datetime.now()-start)
TODAY = str(datetime.strftime(datetime.now(), '%d.%m.%Y'))
if len(cursor.fetchall()) == 0 and TODAY == str(stat_date):
    SQL = """
    SELECT * FROM COVID_RUSSIA WHERE DATE = ?
    """

    print('Вычисление статистики')
    start = datetime.now()
    cursor.execute(
        SQL, [(str(datetime.strftime(datetime.now() - timedelta(1), '%d.%m.%Y')))])
    data = cursor.fetchall()
    desease_count, desease_dynamic = f.analysis(data_new[0], data[0][2])
    death_count, death_dynamic = f.analysis(data_new[3], data[0][5])
    recover_count, recover_dynamic = f.analysis(data_new[2], data[0][8])
    active = int(data_new[0])-int(data_new[2])-int(data_new[3])
    active_count, active_dynamic = f.analysis(active, data[0][11])
    print('Операция выполнена за', datetime.now()-start)

    print('Обновление данных')
    start = datetime.now()
    SQL = """
    INSERT INTO COVID_RUSSIA VALUES(
        ?,?,?,?,?,?,?,?,?,?,?,?,?,?
    )
    """
    PARAMS = [(stat_date), (stat_time), (data_new[0]), (desease_count), (desease_dynamic),
              (data_new[3]), (death_count), (death_dynamic),
              (data_new[2]), (recover_count), (recover_dynamic),
              (active), (active_count), (active_dynamic)]
    cursor.execute(SQL, PARAMS)
    conn.commit()
    print('Операция выполнена за', datetime.now()-start)
    print('Данные успешно обновлены')
    print('Общее время выполнения', datetime.now()-start_total)
else:
    print('Используются актуальные данные')
    print('Общее время выполнения', datetime.now()-start_total)
