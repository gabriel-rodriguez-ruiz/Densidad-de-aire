# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 09:08:27 2021

@author: ltouc
"""

import pandas as pd
import csv
import statistics
import math
import matplotlib.pyplot as plt
from datetime import datetime


#%% Funciones

def leer_csv(nombre_archivo):
    """
    Lee archivo csv 'nombre_archivo' y devuelve listas con el contenido
    de: hora, temperatura, presion, humedad, densidad, fecha, tiempo
    """
    with open(nombre_archivo) as File:
        reader = csv.reader(File, delimiter=';')
        hora=[]
        temperatura=[]
        presion=[]
        humedad=[]
        densidad=[]
        fecha=[]
        tiempo=[]
        fecha_hora = []
        for i,line in enumerate(reader):
            listahora=line[18].split(':')
            listafecha=line[17].split('/')
            tiempo.append(datetime(int(listafecha[2]),int(listafecha[1]),int(listafecha[0]),int(listahora[0]),int(listahora[1]), int(listahora[2])).timestamp())
            hora.append(line[18].split(':'))
            fecha.append(line[17].split('/'))
            fecha_hora.append(datetime(*list(map(int,line[17].split("/")[::-1]+line[18].split(":")))))
            temperatura.append((float(line[0])+float(line[1])+float(line[2])+float(line[4])+float(line[5])+float(line[6])+float(line[7])+float(line[9])+float(line[10])+float(line[13])+float(line[14]))/11)
            humedad.append(float(line[15]))
            presion.append(float(line[16]))
            densidad.append((0.34848*float(line[16])-0.009*float(line[15])*math.exp(0.061*float(line[1])))/(273.15+float(line[1])))    
    return fecha_hora, hora, temperatura, presion, humedad, densidad, tiempo

# Manejo de csv con Pandas    

def mediciones_durante_calibracion(inicio, final, nombre_archivo1, nombre_archivo2):
    """
    Devuelve un DataFrame a partir de dos archivos csv con los datos restringidos
    a las horas de 'inicio' y 'final'.    
    Parameters
    ----------
    inicio : datetime.datetime
        Incio de la calibración.
    final : datetime.datetime
        Fin de la calibración.
    nombre_archivo1 : str
        Ruta del primer archivo csv.
    nombre_archivo2 : str
        Ruta del segundo archivo csv.
    Returns
    -------
    df : pandas.DataFrame
    """
    fecha_hora1, hora1, temperatura1, presion1, humedad1, densidad1, tiempo1 = leer_csv(nombre_archivo1)
    columnas = ["Hora", "Temperatura", "Presión", "Humedad", "Densidad", "Tiempo"]
    df1 = pd.DataFrame(zip(fecha_hora1, temperatura1, presion1, humedad1, densidad1, tiempo1),
                       columns = columnas)
    fecha_hora2, hora2, temperatura2, presion2, humedad2, densidad2, tiempo2 = leer_csv(nombre_archivo2)
    df2 = pd.DataFrame(zip(fecha_hora2, temperatura2, presion2, humedad2, densidad2, tiempo2),
                       columns = columnas)
    df = pd.concat([df1, df2], ignore_index = True)      #Concatenamos los DataFrames
    df = df[(df["Hora"] >= inicio) & (df["Hora"]<= final)]
    return df


def verificaciones(dfTiempo, dfTemp, dfHum, dfDen, clase):
    '''Esta funcion imprime en pantalla si se cumple o no con los requerimientos de la normativa OIML R111-1
    
    Pre: recibe las columnas del dataFrame correspondientes al timestamp, temperatura, humedad y densidad
         y la clase de pesa en formato string ('e1', 'e2', 'f1', 'f2' o 'm1')
    Pos: la funcion no retorna nada, solo imprime los resultados en pantalla'''
    
    # Definicion de Clase de Pesa
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
    elif clase=='m1':
        deltaMaxTemHora=3
        deltaMaxTemdoceHoras=5
        deltaMaxHum=100  
        
    print('\nRequerimientos OIML R111-1:\n')
   
    if min(dfDen)<(1.2*0.9): 
        print(f'Se excedio el limite inferior de densidad, ya que la minima densidad registrada fue: {min(dfDen)} ')
    else:
        print('No se excedio el limite inferior de densidad')
    if max(dfDen)>(1.2*1.1):
        print(f'Se excedio el limite superior de densidad, ya que la maxima densidad registrada fue: {max(dfDen)}')
    else:
        print('No se excedio el limite superior de densidad')
    if min(dfHum)<=40:
        print(f'Se excedio el minimo de humedad, la minima humedad registrada fue: {min(dfHum)}%')
    else:
        print('No se excedio el minimo de humedad')
    
    if max(dfHum)>=60:
        print(f'Se excedio el maximo de humedad, la maxima humedad registrada fue: {max(dfHum)}%')
    else:
        print('No se excedio el maximo de humedad')  
        
    if (clase=='e1' or clase=='e2') and min(dfTemp)<=18:
        print(f'Se excedio el minimo de temperatura, la minima temperatura registrada fue: {min(dfTemp)}')
        
    if (clase=='e1' or clase=='e2') and max(dfTemp)>=27:
        print(f'Se excedio el maximo de temperatura, la maxima temperatura registrada fue: {max(dfTemp)}')
              
    primerIndice=dfTiempo.index[0]    
    iHora=0    # iHora es la cantidad de mediciones que se hacen en una hora 
    unaHora=0
    while unaHora<1:
        iHora+=1
        unaHora=(dfTiempo[primerIndice+iHora]-dfTiempo[primerIndice])/3600    
    
    iCuatroHoras=0  #iCuatroHoras es la cantidad de mediciones que se hacen en 4 horas
    cuatroHoras=0
    while cuatroHoras<4:
        iCuatroHoras+=1
        cuatroHoras=(dfTiempo[primerIndice+iCuatroHoras]-dfTiempo[primerIndice])/3600    
    
    idoceHoras=0
    doceHoras=0
    while doceHoras<12:
        idoceHoras+=1
        doceHoras=(dfTiempo[primerIndice+idoceHoras]-dfTiempo[primerIndice])/3600       
  
    lista=list(dfTemp)
    while True:
        delta=max(lista[:iHora])-min(lista[:iHora])
        if delta>deltaMaxTemHora:
            print(f'Hay exceso de variacion de temperatura en una hora, se registro una variacion de {delta}')
            break
        elif len(lista)<iHora:
            print('No hay exceso de variacion de temperatura en una hora')
            break
        else:
            lista.pop(0)
    
    lista=list(dfTemp)
    while True:
        delta=max(lista[:idoceHoras])-min(lista[:idoceHoras])
        if delta>deltaMaxTemdoceHoras:
            print(f'Hay exceso de variacion de temperatura en doce horas, se registro una variacion de: {delta}')
            break
        elif len(lista)<idoceHoras:
            print('No hay exceso de variacion de temperatura en doce horas')
            break
        else:
            lista.pop(0)   
  
    lista=list(dfHum)
    while True:
        delta=max(lista[:iCuatroHoras])-min(lista[:iCuatroHoras])
        if delta>deltaMaxHum:
            print(f'Hay exceso de variacion de humedad en cuatro horas, se registro: {delta}')
            break
        elif len(lista)<iCuatroHoras:
            print('No hay exceso de variacion de humedad en cuatro horas')
            break
        else:
            lista.pop(0)
 
# Graficos 
def graficos(densidad,temperatura,humedad,presion):
    '''Grafica la densidad, temperatura, humedad y presion en funcion del tiempo
    sobre el eje de ordenadas indica el valor maximo, medio y minimo 
    indica en el grafico en que horario se produjeron los valores maximos y minimos de 
    la variable que esta midiendo
    
    Pre: recibe los valores de densidad, temperatura, humedad y presion en forma de lista
    Pos: No devuelve nada, solo realiza los graficos'''
    # Grafico Densidad
    indMaxHora=densidad.index(max(densidad))
    indMinHora=densidad.index(min(densidad))
    plt.figure(figsize=(10, 8), dpi=80)
    plt.xticks([indMaxHora,indMinHora])
    plt.yticks([min(densidad),max(densidad),statistics.mean(densidad)])
    plt.xlabel('Tiempo')
    plt.ylabel('Densidad')
    plt.title('Densidad vs Tiempo')
    plt.ylim(min(densidad)-0.0003 , max(densidad)+0.0003 )
    plt.plot(densidad)
    plt.annotate(f'{hora[indMaxHora][0]}:{hora[indMaxHora][1]}:{hora[indMaxHora][2]}',xy=(indMaxHora,max(densidad)+0.0001))
    plt.annotate(f'{hora[indMinHora][0]}:{hora[indMinHora][1]}:{hora[indMinHora][2]}',xy=(indMinHora,min(densidad)-0.0001))

    # Grafico Temperatura
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
    plt.annotate(f'{hora[indMaxHoraTem][0]}:{hora[indMaxHoraTem][1]}:{hora[indMaxHoraTem][2]}',xy=(indMaxHoraTem,max(temperatura)+0.05))
    plt.annotate(f'{hora[indMinHoraTem][0]}:{hora[indMinHoraTem][1]}:{hora[indMinHoraTem][2]}',xy=(indMinHoraTem,min(temperatura)-0.05))

    # Grafico Humedad
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
    plt.annotate(f'{hora[indMaxHoraHum][0]}:{hora[indMaxHoraHum][1]}:{hora[indMaxHoraHum][2]}',xy=(indMaxHoraHum,max(humedad)+0.05))
    plt.annotate(f'{hora[indMinHoraHum][0]}:{hora[indMinHoraHum][1]}:{hora[indMinHoraHum][2]}',xy=(indMinHoraHum,min(humedad)-0.05))

    # Grafico Presion
    plt.figure(figsize=(10, 8), dpi=80)
    plt.plot(presion)
    indMaxHoraPre=presion.index(max(presion))
    indMinHoraPre=presion.index(min(presion))
    plt.xticks([indMaxHoraPre,indMinHoraPre])
    plt.yticks([min(presion),max(presion),statistics.mean(presion)])
    plt.xlabel('Tiempo')
    plt.ylabel('Presion')
    plt.title('Presion vs Tiempo')
    plt.ylim(min(presion)-1 , max(presion)+1 )
    plt.annotate(f'{hora[indMaxHoraPre][0]}:{hora[indMaxHoraPre][1]}:{hora[indMaxHoraPre][2]}',xy=(indMaxHoraPre,max(presion)+0.2))
    plt.annotate(f'{hora[indMinHoraPre][0]}:{hora[indMinHoraPre][1]}:{hora[indMinHoraPre][2]}',xy=(indMinHoraPre,min(presion)-0.2))            
    

    
#%% Ejecucion de Funciones
fecha_hora, hora, temperatura, presion, humedad, densidad, tiempo = leer_csv('../DataPython/202109-06.csv')
nombre_archivo1 = "../DataPython/202109-05.csv"
nombre_archivo2 = '../DataPython/202109-06.csv'
inicio = datetime(2021, 9, 5, 8, 0, 0)
final = datetime(2021, 9, 6, 8, 0, 0)
df = mediciones_durante_calibracion(inicio, final, nombre_archivo1, nombre_archivo2)
verificaciones(df["Tiempo"], df["Temperatura"], df["Humedad"],df["Densidad"],'e1')
graficos(densidad,temperatura,humedad,presion)