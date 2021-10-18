import re
import csv 
import matplotlib.pyplot as plt
import statistics as stats

name = "prueba.csv"
archivo =  open(name,'a')

def readColumn(nameFile):
    with open(nameFile) as f:
        reader = csv.reader(f,delimiter = ' ')
        
        res = []
        for row in reader: #We loop through all the rows 
            res.append(int(row[1]))
    return res

res = readColumn(name)
print(res)

tiempo = [i for i in range(241)]

promedio = stats.mean(res)

#plt.plot(tiempo,res)
#plt.show()






