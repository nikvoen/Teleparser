import os
import time
from dubnium import data_update
from datetime import datetime, timedelta


today = datetime.now()
hour = int(time.strftime("%H", time.localtime()))
file_date = today + timedelta(days=2)
file_date = '.'.join(file_date.strftime("%d %m").split())
path = f'D:/database/{file_date}.txt'

if hour >= 20:
    file_date = today + timedelta(days=9)
else:
    file_date = today + timedelta(days=8)

file_date = '.'.join(file_date.strftime("%d %m").split())
new_path = f'D:/database/{file_date}.txt'
error_file = 'D:/database/errors.txt'

if os.path.exists(path):
    data_update(path, new_path)
    os.remove(path)

if os.path.exists(error_file):
    fix_errors()
