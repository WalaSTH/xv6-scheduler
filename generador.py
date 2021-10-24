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
def readScenery(esPath,form):
    res = {}
    
    banchs = os.listdir(esPath)
    banchs.sort()

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

#prueba = readScenery(files,"Escenario0",'c')
#prueba2 = readScenery(files,"Escenario0",'i')
#print(readScenery(files,"Escenario0",'c'))

def makeCharts(esPath,form):
    Escenario0 = readScenery("Escenario0",form)
    Escenario1 = readScenery("Escenario1",form)
    Escenario2 = readScenery("Escenario2",form)
    Escenario3 = readScenery("Escenario3",form)

    width = 0.2
    
    xIndexes = np.arange(6)
    
    if(form == 'c'):

        plt.subplot(121)
        plt.xticks(ticks=xIndexes,labels=Escenario0.keys())
        plt.bar(xIndexes,Escenario0.values(),width=width,color="#003f5c",label="Quantum por defecto")
        plt.bar(xIndexes + width,Escenario1.values(),width=width,color="#7a5195",label="Quantum/10")
        plt.bar(xIndexes + 2*width,Escenario2.values(),width=width,color="#ef5675",label="Quantum/100")

        plt.title("CPUBENCH metricas para Round Robin")
        plt.grid()
        plt.xlabel("casos")
        plt.ylabel("KFPT")
        plt.legend()

        newEsce2 = list(map(lambda x: x / 10.0,Escenario2.values()))
        newEsce3 = list(map(lambda x: x / 100.0,Escenario2.values()))
        
        plt.subplot(122)
        plt.xticks(ticks=xIndexes,labels=Escenario0.keys())
        plt.bar(xIndexes,newEsce2,width=width,color="#ef5675",label="Quantum/100")
        plt.bar(xIndexes+width,newEsce3,width=width,color="#ffa600",label="Quantum/1000")

        plt.title("Comparación solo del escenario 2 y 3")
        plt.grid()
        plt.xlabel("casos")
        plt.ylabel("KFPT")
        plt.legend()

    elif(form == 'i'):
        plt.figure(figsize=(18, 16), dpi=200)
        plt.xticks(ticks=xIndexes,labels=Escenario0.keys())

        plt.bar(xIndexes - width,Escenario0.values(),width=width,color="#003f5c",label="Quantum por defecto")
        plt.bar(xIndexes ,Escenario1.values(),width=width,color="#7a5195",label="Quantum/10")
        plt.bar(xIndexes + width,Escenario2.values(),width=width,color="#ef5675",label="Quantum/100")
        plt.bar(xIndexes + 2*width,Escenario3.values(),width=width,color="#ffa600",label="Quantum/1000")

        plt.title("IOBENCH metricas para Round Robin")
        plt.grid()
        plt.xlabel("casos")
        plt.ylabel("IOPT")
        plt.legend()

    plt.show()


#width = 0.25
makeCharts("hola",'c')
#xIndexes = np.arange(6)

#


#plt.xticks(ticks = xIndexes,labels=prueba.keys())

#plt.bar(xIndexes,prueba.values(),width=width)
#plt.bar(xIndexes + width,[3.2,2.7,3,2,3,1],width=width)
#plt.bar(xIndexes + width,prueba2.values(),color="#444444",width=width)
#plt.bar(xIndexes + 2*width,[40,50,45,40,47,40],width=width)

#plt.bar(xIndexes + 3*width,[100,0.2,0.3,0.4,0.3,0.1],width=width)


#plt.show()
