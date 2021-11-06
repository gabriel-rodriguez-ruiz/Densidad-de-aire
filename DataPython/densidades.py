# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 09:38:41 2021

@author: INTI
"""

import csv
import statistics
import math
import numpy as np
import matplotlib.pyplot as plt

with open('../DataPython/202109-06.csv') as File:
    reader = csv.reader(File, delimiter=';')
    hora=[]
    temperatura=[]
    presion=[]
    humedad=[]
    densidad=[]
    for i,line in enumerate(reader):
        hora.append(line[18])
        temperatura.append(float(line[1]))
        humedad.append(float(line[15]))
        presion.append(float(line[16]))
        densidad.append((0.34848*float(line[16])-0.009*float(line[15])*math.exp(0.061*float(line[1])))/(273.15+float(line[1])))    
    print('la temperatura es: \n',temperatura)
    print('la presion es: \n', presion)
    print('la hora es: \n',hora)
    print('la humedad es: \n', humedad) 
    print('La densidad es: \n', densidad)

#%% Grafico Densidad
indMaxHora=densidad.index(max(densidad))
indMinHora=densidad.index(min(densidad))
plt.figure(figsize=(10, 8), dpi=80)
plt.xticks([indMaxHora,indMinHora])
plt.yticks([min(densidad),max(densidad),statistics.mean(densidad)])
#plt.xlim(X.min() * 1.1, X.max() * 1.1)
plt.xlabel('Tiempo')
plt.ylabel('Densidad')
plt.title('Densidad vs Tiempo')
plt.ylim(min(densidad)-0.0003 , max(densidad)+0.0003 )
plt.plot(densidad)
plt.annotate(f'{hora[indMaxHora]}',xy=(indMaxHora,max(densidad)+0.0001))
plt.annotate(f'{hora[indMinHora]}',xy=(indMinHora,min(densidad)-0.0001))
print(hora[indMaxHora])

#%% Grafico Temperatura
plt.figure(figsize=(10, 8), dpi=80)
plt.plot(temperatura)
indMaxHoraTem=temperatura.index(max(temperatura))
indMinHoraTem=temperatura.index(min(temperatura))
plt.xticks([indMaxHoraTem,indMinHoraTem])
plt.yticks([min(temperatura),max(temperatura),statistics.mean(temperatura)])
plt.xlabel('Tiempo')
plt.ylabel('Temperatura')
plt.title('Temperatura vs Tiempo')
plt.ylim(min(temperatura)-0.1 , max(temperatura)+0.1 )
plt.annotate(f'{hora[indMaxHoraTem]}',xy=(indMaxHoraTem,max(temperatura)+0.05))
plt.annotate(f'{hora[indMinHoraTem]}',xy=(indMinHoraTem,min(temperatura)-0.05))

#%% Grafico Humedad
plt.figure(figsize=(10, 8), dpi=80)
plt.plot(humedad)
indMaxHoraHum=humedad.index(max(humedad))
indMinHoraHum=humedad.index(min(humedad))
plt.xticks([indMaxHoraHum,indMinHoraHum])
plt.yticks([min(humedad),max(humedad),statistics.mean(humedad)])
plt.xlabel('Tiempo')
plt.ylabel('Humedad')
plt.title('Humedad vs Tiempo')
plt.ylim(min(humedad)-1 , max(humedad)+1 )
plt.annotate(f'{hora[indMaxHoraHum]}',xy=(indMaxHoraHum,max(humedad)+0.05))
plt.annotate(f'{hora[indMinHoraHum]}',xy=(indMinHoraHum,min(humedad)-0.05))
if min(humedad)<40:
    plt.annotate(f'{hora[indMinHoraHum]} no cumple Humedad Minima',xy=(indMinHoraHum,min(humedad)-0.3))
if max(humedad)>60:
    plt.annotate(f'{hora[indMaxHoraHum]} no cumple Humedad Maxima',xy=(indMaxHoraHum,max(humedad)+0.3))
    
#%% Grafico Presion
plt.figure(figsize=(10, 8), dpi=80)
plt.plot(presion)
indMaxHoraPre=presion.index(max(presion))
indMinHoraPre=presion.index(min(presion))
plt.xticks([indMaxHoraPre,indMinHoraPre])
plt.yticks([min(presion),max(presion),statistics.mean(presion)])
plt.xlabel('Tiempo')
plt.ylabel('presion')
plt.title('Presion vs Tiempo')
plt.ylim(min(presion)-1 , max(presion)+1 )
plt.annotate(f'{hora[indMaxHoraPre]}',xy=(indMaxHoraPre,max(presion)+0.2))
plt.annotate(f'{hora[indMinHoraPre]}',xy=(indMinHoraPre,min(presion)-0.2))