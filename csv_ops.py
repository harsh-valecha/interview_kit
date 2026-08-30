# read data from a csv file
from csv import reader , writer , DictReader , DictWriter

def csv_reader(file):
    values = []
    with open(file,'r') as f:
        for row in reader(f):
            # print(row)
            values.append(row)
    return values

# print(csv_reader('testdata.csv'))
# print(values[1][1])


row = [['hullad',23,13],['jaskirat',20,8]]
# write a row to csv file

def csv_writerow(file,row):
    with open(file,'a') as f:
        writer(f).writerow(row)

def csv_writerows(file,rows):
    with open(file,'a') as f:
        writer(f).writerows(rows)


def csv_readrows_dict(file):
    values = []
    with open(file,'r') as f:
        for row in DictReader(f):
            values.append(row)
    return values

def csv_writerows_dict(file,rows,fields):
    with open(file,'a') as f:
        DictWriter(f,fieldnames=fields).writerows(rows)


# print(csv_dictrows('testdata.csv'))
person = [{'name':'gurmeet','age':18},{'age':20,'class':10}]
fields = ['name','age','class']
csv_writerows_dict('testdata.csv',person,fields)

print(csv_reader('testdata.csv'))
