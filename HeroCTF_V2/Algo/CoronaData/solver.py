import csv
cases2 = list()
with open('corona.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        cases=row[0].split(',')
        while ("" in cases):
            cases.remove("")
        try:
            cases2.append(cases[4])
        except:
            print("")
    i = 1
    new_list = list()
    while(i<len(cases2)):
        new_list.append(int(cases2[i]))
        i+=1
    new_list.sort()
    print(new_list[-1])
