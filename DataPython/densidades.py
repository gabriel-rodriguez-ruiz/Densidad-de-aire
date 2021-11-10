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
from datetime import datetime

#%% defino las condiciones de variacion maxima de temperatura y humedad para cada clase de pesa (de la R11)
#   por defecto queda seleccionada la clase m1
clase='m1'
if clase=='e1':
    deltaMaxTemHora=0.3
    deltaMaxTemdoceHoras=0.5
    deltaMaxHum=5
elif clase=='e2':
    deltaMaxTemHora=0.7
    deltaMaxTemdoceHoras=1
    deltaMaxHum=10
elif clase=='f1':
    deltaMaxTemHora=1.5
    deltaMaxTemdoceHoras=2
    deltaMaxHum=15
elif clase=='f2':
    deltaMaxTemHora=2
    deltaMaxTemdoceHoras=3.5
    deltaMaxHum=15    
else:
    deltaMaxTemHora=3
    deltaMaxTemdoceHoras=5
    deltaMaxHum=100      
    
class Clase:
    """Clase de precisión del INTI."""
    def __init__(self, nombre, deltaMaxTemHora, deltaMaxTemdoceHoras, deltaMaxHum):
        self.nombre = nombre
        self.deltaMaxTemHora = deltaMaxTemHora
        self.deltaMaxTemdoceHoras = deltaMaxTemdoceHoras
        self.deltaMaxHum = deltaMaxHum
    def __str__(self):
        return f"{self.nombre}"
    def __repr__(self):
        return f"Clase({self.nombre}, {self.deltaMaxTemHora}, {self.deltaMaxTemdoceHoras}, {self.deltaMaxHum})"
    
#%% en este bloque agregue la lista tiempo, en la que se define el tiempo en segundos en que se realiza cada medicion
   # usando la funcion timestamp()
    
    
with open('../DataPython/202109-06.csv') as File:
    reader = csv.reader(File, delimiter=';')
    hora=[]
    temperatura=[]
    presion=[]
    humedad=[]
    densidad=[]
    fecha=[]
    tiempo=[]
    for i,line in enumerate(reader):
        listahora=line[18].split(':')
        listafecha=line[17].split('/')
        tiempo.append(datetime(int(listafecha[2]),int(listafecha[1]),int(listafecha[0]),int(listahora[0]),int(listahora[1]), int(listahora[2])).timestamp())
        hora.append(line[18].split(':'))
        fecha.append(line[17].split('/'))
        temperatura.append(float(line[1]))
        humedad.append(float(line[15]))
        presion.append(float(line[16]))
        densidad.append((0.34848*float(line[16])-0.009*float(line[15])*math.exp(0.061*float(line[1])))/(273.15+float(line[1])))    

    #First Term => CIPM 1981/91: 0.34848      CIPM 2007:0.3483740
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




#%% En este bloque se calculan las variables iHora e idoceHoras, indican la cantidad de mediciones que se hacen 
#   para alcanzar una hora y doce horas, respectivamente. Esta variables despues se van a usar en las funciones
#   verificarTempHora y verificarTempdoceHoras 
iHora=0
unaHora=0
while unaHora<1:
    iHora+=1
    unaHora=(tiempo[iHora]-tiempo[0])/3600
idoceHoras=0
doceHoras=0
while doceHoras<12:
    idoceHoras+=1
    doceHoras=(tiempo[idoceHoras]-tiempo[0])/3600

#%%
def verificarTempHora(lista):
    '''recibe la lista de temperaturas, calcula la variacion maxima que se produce en la primer
    hora de mediciones y verifica si supera o no el maximo permitido
    en caso de cumplir, elimina el primer elemento de la lista y vuelve a verificar de manera recursiva.
    por ultimo, imprime en pantalla si cumple o no con dicho requisito'''
    delta=max(lista[:iHora])-min(lista[:iHora])
    if delta>deltaMaxTemHora:
        print('hay exceso de variacion de temperatura en una hora')
    elif len(lista)<iHora:
        print('no hay exceso de variacion de temperatura en una hora')
    else:
        lista.pop(0)
        verificarTempHora(lista)
        
def verificarTempdoceHoras(lista):
    '''idem funcion verificarTempHora, la diferencia es que en lugar de una hora en este caso son 12 horas'''
    
    delta=max(lista[:idoceHoras])-min(lista[:idoceHoras])
    if delta>deltaMaxTemdoceHoras:
        print('hay exceso de variacion de temperatura en doce horas')
    elif len(lista)<idoceHoras:
        print('no hay exceso de variacion de temperatura en doce horas')
    else:
        lista.pop(0)
        verificarTempdoceHoras(lista)


print()
#clase='e1'
verificarTempHora(temperatura)
verificarTempdoceHoras(temperatura)


#%% Esta funcion todavia no funciona, estuve viendo si podia hacer una funcion que haga todos los graficos
    # no funciona porque no puedo modificar lo que imprime plt.ylabel ni tampoco plt.title, trate de usar 
    # f-strings pero no sirvio
    
def grafico(columna):
    plt.figure(figsize=(10, 8), dpi=80)
    plt.plot(columna)
    indMaxHoraTem=columna.index(max(columna))
    indMinHoraTem=columna.index(min(columna))
    plt.xticks([indMaxHoraTem,indMinHoraTem])
    plt.yticks([min(columna),max(columna),statistics.mean(columna)])
    plt.xlabel('Tiempo')
    plt.ylabel(f'{columna}')
    plt.title('Temperatura vs Tiempo')
    plt.ylim(min(columna)-0.1 , max(columna)+0.1 )
    plt.annotate(f'{hora[indMaxHoraTem]}',xy=(indMaxHoraTem,max(columna)+0.05))
    plt.annotate(f'{hora[indMinHoraTem]}',xy=(indMinHoraTem,min(columna)-0.05))
