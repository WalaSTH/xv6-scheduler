import re
import csv 
import matplotlib.pyplot as plt
import statistics as stats
import os 
import numpy as np



name = "Escenario0/Caso7_i-7-2.csv"
archivo =  open(name,'a')

def readColumn(nameFile):
    with open(nameFile) as f:
        reader = csv.reader(f,delimiter = ' ')
        
        res = []
        for row in reader: #We loop through all the rows 
            res.append(float(row[1]))
    return res

#Take a list of List and return the mean of all values 
def meanList(l,esPath):
    res = 0
    lAux = []
    
    for i in l:
        lAux = lAux + readColumn(esPath + '/' + i)
    
    return stats.mean(lAux)

#Take a list with the names of the files, and depending the form, it will return 
# a dictionary with the data required for the charts 
#Pre: {We assume that the data is sorted}
def readScenery(banchs,esPath,form):
    res = {}
    
    
    if(form == 'i'):
        for i in [0,1,2,4,5,7]:
            lAux = [j for j in banchs if j.startswith('Caso' + str(i) + '_i' )]
            res['Caso ' + str(i)] = meanList(lAux,esPath)
 
    elif(form == 'c'):

        for i in range(1,7):
            lAux = [j for j in banchs if j.startswith('Caso' + str(i) + '_c' )]
            res['Caso ' + str(i)] = meanList(lAux,esPath)
        
    return res 
path = 'Escenario0'

#Save in a list all the names of the files in the path folder  
files = os.listdir(path)
data = []


files.sort()

prueba = readScenery(files,"Escenario0",'c')
prueba2 = readScenery(files,"Escenario0",'i')
print(readScenery(files,"Escenario0",'c'))

def makeCharts(esPath,form):
    Escenario0 = readScenery(files,"Escenario0",form)
    Escenario1 = readScenery(files,"Escenario1",form)
    Escenario2 = readScenery(files,"Escenario2",form)
    Escenario3 = readScenery(files,"Escenario3",form)

    width = 0.25
    
    xIndexes = np.arange(6)
    plt.xticks(ticks = xIndexes,labels= Escemario0.keys())
    
    if(form == 'c'):
        fig, axs = plt.subplots(2)

        axs[0].bar(xIndexes,Escenario0.values(),width=width,color="#003f5c",label="Escenario 0")
        axs[0].bar(xIndexes,Escenario1.values(),width=width,color="#7a5195",label="Escenario 1")
        axs[0].bar(xIndexes,Escenario2.values(),width=width,color="#ef5675",label="Escenario 2")
   

        newEsce2 = map(lambda x: x / 10.0,Escenario2.values())
        newEsce3 = map(lambda x: x / 100.0,Escenario2.values())
        
        axs[1].bar(xIndexes,newEsce2,width=width,color="#ff6361",label="Escenario 2")
        axs[1].bar(xIndexes,newEsce2,width=width,color="#ffa600",label="Escenario 3")

    elif(form == 'i'):
 
        plt.bar(xIndexes,Escenario0.values(),width=width,color="#003f5c",label="Escenario 0")
        plt.bar(xIndexes,Escenario1.values(),width=width,color="#7a5195",label="Escenario 1")
        plt.bar(xIndexes,Escenario2.values(),width=width,color="#ef5675",label="Escenario 2")
        plt.bar(xIndexes,Escenario3.values(),width=width,color="#ffa600",label="Escenario 3")

        plt.show()

#width = 0.25

#xIndexes = np.arange(6)

#plt.figure(figsize=(18, 16), dpi=260)


#plt.xticks(ticks = xIndexes,labels=prueba.keys())

#plt.bar(xIndexes,prueba.values(),width=width)
#plt.bar(xIndexes + width,[3.2,2.7,3,2,3,1],width=width)
#plt.bar(xIndexes + width,prueba2.values(),color="#444444",width=width)
#plt.bar(xIndexes + 2*width,[40,50,45,40,47,40],width=width)

#plt.bar(xIndexes + 3*width,[100,0.2,0.3,0.4,0.3,0.1],width=width)


#plt.show()