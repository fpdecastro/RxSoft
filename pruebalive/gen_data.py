import csv
from distutils import text_file
import random
import time

from matplotlib.pyplot import text

x_value = 0
total_1 = 1000
total_2 = 1000

fieldnames = ["x_value", "total_1", "total_2"]


# with open('data.csv', 'w') as csv_file:
#     csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#     csv_writer.writeheader()

while True:

    with open('data.txt', 'a') as txt_file:

        txt_file.write(str(total_1) +" "+ str(total_2) + "\r")
        x_value += 1
        total_1 = total_1 + random.randint(-6, 8)
        
        total_2 = total_2 + random.randint(-5, 6)

    time.sleep(1)