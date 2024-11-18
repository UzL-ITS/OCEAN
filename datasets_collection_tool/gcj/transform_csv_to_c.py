import csv
import os

folder = 'eval'
os.makedirs(folder)
with open(f'gcj_{folder}.csv', newline='') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    counter = 0
    for row in data:
        counter += 1
        if counter == 1:
            continue
        with open(f"{folder}/" + '_'.join(row[1].split('/')[1:]).strip('\''), 'w') as f:
            f.write(row[2])

