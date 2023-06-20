import tabla_carga_equivalente
import pandas as pd
import sys
import obtener_data
import tkinter as tk
from tkinter import ttk
import os.path
import openpyxl

def elejir_rodamiento():
    #Elige el tipo de rodamiento y se asigna el valor de p correspondiente
    while True:
        p = int(input("¿Qué tipo de rodamiento se va a analizar?\n1. Rodamiento de bolas\n2. Rodamiento de cilindros\nIngrese el número correspondiente: "))

        if p == 1:
            print("Has seleccionado el rodamiento de bolas.")
            p = 3
            break
        elif p == 2:
            print("Has seleccionado el rodamiento de cilindros.")
            print("El programa no está habilitado para trabajar con engranajes cilíndricos")
            sys.exit()
            p = 10/3
            break
        else:
            print("Opción inválida. Por favor, ingresa 1 o 2.")

    return p

def leer_esfuerzos_excel():
    # Lee el archivo de Excel
    df = pd.read_excel('condicion_funcionamiento.xlsx')

    # Crea los vectores con los nombres de las filas
    tiempos = df.iloc[0, 3:].tolist()
    velocidades = df.iloc[1, 3:].tolist()
    radiales = df.iloc[2, 3:].tolist()
    axiales = df.iloc[3, 3:].tolist()

    #print(f'Tiempos: {tiempos}\nVelocidades: {velocidades}\nFuerzas radiales: {radiales}\nFuerzas axiales: {axiales}')
    return tiempos, velocidades, radiales, axiales

def esfuerzo_medio(f,n,t,p,l):
    #Se crea un for por si se deseara ampliar el cálculo a más de 3 instancias de tiempo
    for i in range(l):
        #Se hace la operación para hallar el numerador
        numerador = (f[i]**p)*n[i]*t[i]
        #Se hace la operación para hallar el numerador
        denominador = n[i]*t[i]
        #Ambos valores se apilan en listas correspondientes
        numeradores.append(numerador)
        denominadores.append(denominador)
    return (sum(numeradores)/sum(denominadores))**(1/p)

def interpolacion(x1, y1, x2, y2, x):
    """
    Realiza una interpolación lineal entre dos puntos (x1, y1) y (x2, y2) para un valor x dado.
    """
    y = y1 + (x - x1) * (y2 - y1) / (x2 - x1)
    return y

def factor(fo, fa,cor):
    #Obtiene el valor redondeado de fo.fa/Cor
    return round((fo*fa)/cor,3)

def X_Y(tabla, valor, fa, fr):
    #Compara el valor de "Factor" de cada fila de la lista con el valor ingresado
    for fila in tabla:
        #Verifica si el valor se encontró en la tabla y retorno el x y y correspondiente a cada caso
        if fila["Factor"] == valor:
            if fa/fr <= fila["e"]:
                x, y = 1, 0
            else: 
                x, y = 0.56, fila["Y"]
            return x, y
    # Si no se encuentra un valor exacto, buscar el inmediato superior e inferior
    superior = None
    inferior = None

    for fila in tabla:
        if fila["Factor"] > valor:
            superior = fila
            break
        inferior = fila

    if inferior is None or superior is None:
        #Si resultase que el valor ingresado no tiene una fila superior o una inferior se interpolan con respecto a 2 filas contiguas de la tabla
        e = interpolacion(0.172,0.19,0.345,0.22,valor)

    else:
        e = interpolacion(inferior["Factor"], inferior["e"], superior["Factor"], superior["e"], valor)
    
    if fa/fr <= e:
        x, y = 1, 0
    else:
        if inferior is None or superior is None:
        #Si resultase que el valor ingresado no tiene una fila superior o una inferior se interpolan con respecto a 2 filas contiguas de la tabla
            x = 0.56
            y = interpolacion(0.19,2.3,0.22,1.99,e)
        else: 
            x, y = 0.56, round(interpolacion(inferior["e"], inferior["Y"], superior["e"], superior["Y"], e),3)
    return x, y, e

def carga_equivalente(fa, fr,x , y):
    #Calcula el valor de carga
    return x*fr + y*fa


def L10h(C,P,p):
    #Se calcula L10
    l10 = (C/P)**p 
    #La velocidad promedio corresponde a la suma de los elementos del vector "denominadores"
    l10h = (1e6*l10)/(60*sum(denominadores))
    return l10h

def create_table(resultados):
    # Crear la ventana principal
    window = tk.Tk()

    # Crear el objeto tabla
    table = ttk.Treeview(window)
    window.title("Codigos de Rodamientos")
    window.geometry("200x600")

    # Definir las columnas de la tabla
    table["columns"] = ("column1")

    # Configurar encabezados de columnas
    table.heading("column1", text="Numero de Rodamiento")
    

    # Agregar filas de datos
    for i in range(len(resultados)):
        table.insert(parent='', index='end', text=f"{i+1}", values=(resultados[i]))

    # Ajustar el tamaño de las columnas
    table.column("#0", width=50)  
    table.column(f"column{1}", width=150)

    # Cambiar el nombre de las filas
    for i, row_id in enumerate(table.get_children(), start=1):
        table.item(row_id, text=f"{i}")

    # Mostrar la tabla
    table.place(width=200, height=600)

    # Ejecutar el bucle de eventos de la interfaz
    window.update()

    
if __name__ == '__main__':
    #Carga la tabla
    tabla = tabla_carga_equivalente.tabla
    #Se inician los vectores necesarios
    numeradores = []
    denominadores = []
    #Obtenemos el valor de p
    p = elejir_rodamiento()
    #Elegir como se obtendrán los datos para los cálculos
    while True:
        elegir = int(input("¿Como desea obtener los datos?\n1. Ingresar código de rodamiento:\n2. Ingresar valores manualmente\nElija una opción: "))
        #2 formas diferentes
        if elegir == 1:
            print("Los rodamientos disponibles son: ")
            #Guarda en resultados toda la columna de códigos de la base de datos.
            resultados = obtener_data.imprimir_codigos()
            #Muestra la tabla de los códigos disponibles
            create_table(resultados)
            #Obtiene valores necesarios de la base de datos
            c, cor, fo = obtener_data.obtener_valores_por_codigo()
            break
        elif elegir == 2:
            #Pide el ingreso manual de los datos
            c = float(input("Ingresa el valor de C: "))
            cor = float(input("Ingresa el valor de Cor: "))
            fo = float(input("Ingresa el valor de fo: "))
            break
        else:
            print("Opción inválida. Por favor, ingresa 1 o 2.")
    #Lee los valores del excel de lectura.
    tiempos, velocidades, radiales, axiales = leer_esfuerzos_excel()
    #Calcula el esfuerzo medio axial
    esfuerzo_medio_axial = round((esfuerzo_medio(axiales,velocidades,tiempos,p,len(axiales)))/1000,3)
    #Se limpian los vectores para ser reutilizados
    numeradores.clear()
    denominadores.clear()
    #Calcula el esfuerzo medio radial
    esfuerzo_medio_radial = round((esfuerzo_medio(radiales,velocidades,tiempos,p,len(radiales)))/1000,3)
    #Imprime los esfuerzos
    print(f'Esfuerzo medio axial: {esfuerzo_medio_axial} kN\nEsfuerzo medio radial: {esfuerzo_medio_radial} kN')
    #Obtiene el valor de fo.fa/Cor
    valor = factor(fo, esfuerzo_medio_axial, cor)
    #Obtiene los valores de x, y y e
    x, y, e = X_Y(tabla, valor, esfuerzo_medio_axial, esfuerzo_medio_radial)
    #Los imprime
    print(f'El valor de X es: {x}\nEl valor de Y es: {y}')
    #Calcula la carga equivalente
    carga = round(carga_equivalente(esfuerzo_medio_axial, esfuerzo_medio_radial, x, y),3)
    print(f'La carga equivalente es: {carga}')
    #Calcula he imprime el valor de L10h
    L10_h = L10h(c,carga,p)
    print(L10_h)


    #GUARDANDO LOS RESULTAODS EN EXCEL

    #Nombre del archivo
    nombre_archivo = "resultados_esfuerzos.xlsx"

    #Agregamos todos los datos obtenidos que sean relevantes al array "datos_engranajes"
    datos = [esfuerzo_medio_axial,esfuerzo_medio_radial,valor,x,y,e,carga,L10_h]
    # Nombres de las columnas y filas
    nombres_columnas = ["Ema", "Emr" ,"fo.fa/Cor", "X", "Y", "e","P","L10h"]

    # Crea un DataFrame con los datos y los nombres de filas y columnas
    df = pd.DataFrame([datos], columns=nombres_columnas)

    # Verifica si el archivo de Excel existe
    if os.path.isfile(nombre_archivo):
        # Si el archivo existe, carga el libro de trabajo existente y agrega una nueva hoja
        book = openpyxl.load_workbook(nombre_archivo)
        writer = pd.ExcelWriter(nombre_archivo, engine='openpyxl')
        writer.book = book
        
        #El nombre de cada hoja se titula igual que la velocidad ingresada
        hoja_nombre = f"Carga {carga}"
        
        # Agrega el DataFrame a la nueva hoja
        df.to_excel(writer, sheet_name=hoja_nombre)

        #Trae la hojas actual para escribir en ella
        sheet = book[hoja_nombre]
        
    else:
        # Si el archivo no existe, crea un nuevo libro de trabajo y guarda el DataFrame en la primera hoja
        writer = pd.ExcelWriter(nombre_archivo, engine='openpyxl')
        df.to_excel(writer, sheet_name=f"Carga {carga}")

        #Jala la hoja actual
        book = writer.book
        sheet = book[f"Carga {carga}"]

    # Guarda el archivo de Excel
    writer.save()
    writer.close()
