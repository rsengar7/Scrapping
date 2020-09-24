import csv

Final = []

with open('Linked jobs.csv','r') as linked:

    read = csv.reader(linked)

    for item in read:
        print(item)
        if item not in Final:
            Final.append(item)



with open('Final.csv','w',newline='') as final:

    w = csv.writer(final)

    for item in Final:
        w.writerow(item)


print(len(Final))


