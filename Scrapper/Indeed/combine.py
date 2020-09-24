import csv

new = []

jobs = ['job.csv','job2.csv','job3.csv','job4.csv','job5.csv']

for item in jobs:

    with open(item, 'r') as read:

        reads = csv.reader(read, delimiter=',')

        for item in reads:
            if item not in new:
                new.append(item)




with open('final_file.csv', 'w', newline='') as final:

    write = csv.writer(final,delimiter=',')

    for item in new:

        write.writerow(item)




            





