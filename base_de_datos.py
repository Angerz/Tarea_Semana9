import sqlite3
#Script para crear la base de datos RODAMIENTOS.db
conexion= sqlite3.connect("RODAMIENTOS.db")
cursor=conexion.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS RODAMIENTOS(CODIGO INTEGER, Cr REAL, Cor REAL, f0 REAL)")
#Base de datos con los rodamientos rígidoz de bolas desde 40 hasta 85 de diámmetro
data= [(6808,5.1,4,16.3),
(6908,12.2,8.9,15.8),
(16008,12.6,9.65,16),
(6008,16.8,11.5,15.2),
(6208,29.1,17.8,14),
(6308,40.5,24,13.2),
(6408,663.5,36.5,12.3),
(6809,5.35,4.95,16.1),
(6909,13.1,10.4,16.1),
(16009,12.9,10.5,16.2),
(6009,21,15.1,15.3),
(6209,32.5,20.4,14.1),
(6309,53,32,13.1),
(6409,77,45,12.1),
(6810,6.6,6.1,16.1),
(6910,13.4,11.2,16.3),
(16010,13.2,11.3,16.4),
(6010,21.8,16.6,15.5),
(6210,35,23.2,14.4),
(6310,62,38.5,13.2),
(6410,82,49.5,12.5),
(6811,8.8,8.1,16.2),
(6911,16,13.3,16.2),
(16011,18.6,15.3,16.2),
(6011,28.3,21.2,15.3),
(6211,43.5,29.2,14.3),
(6311,71.5,45,13.2),
(6411,89,54,12.7),
(6812,11.5,10.6,16.3),
(6912,16.4,14.3,16.4),
(16012,20,17.5,16.3),
(6012,29.5,23.2,15.6),
(6212,52.5,36,14.3),
(6312,82,52,13.2),
(6412,102,64.5,12.6),
(6813,11.6,11,16.2),
(6913,17.4,16.1,16.6),
(16013,20.5,18.7,16.5),
(6013,30.5,25.2,15.8),
(6213,57.5,40,14.4),
(6313,92.5,60,13.2),
(6413,111,72.5,12.7),
(6814,12.1,11.9,16.1),
(6914,23.7,21.2,16.3),
(16014,24.4,22.6,16.5),
(6014,38,31,15.6),
(6214,62,44,14.5),
(6314,104,68,13.2),
(6414,128,89.5,12.7),
(6815,12.5,12.9,16),
(6915,24.4,22.6,16.5),
(16015,25,24,16.6),
(6015,39.5,33.5,15.8),
(6215,66,49.5,14.7),
(6315,113,77,13.2),
(6415,138,99,12.7),
(6816,12.7,13.3,16),
(6916,24.9,24,16.6),
(16016,25.4,25.1,16.4),
(6016,47.5,40,15.6),
(6216,72.5,53,14.6),
(6316,123,86.5,13.3),
(6416,164,125,12.3),
(6817,18.7,19,16.2),
(6917,32,29.6,16.4),
(16017,25.9,26.2,16.4),
(6017,49.5,43,15.8),
(6217,83.5,64,14.7),
(6317,133,97,13.3)]
cursor.execute("SELECT COUNT(*) FROM RODAMIENTOS")
registros = cursor.fetchone()[0]
if registros == 0:
    instruccion = 'INSERT INTO RODAMIENTOS VALUES(?,?,?,?)'
    cursor.executemany(instruccion, data)

# Realizar el resto de las operaciones con la base de datos

conexion.commit()
conexion.close()







'''
instruccion=f'INSERT INTO RODAMIENTOS VALUES(?,?,?,?)'
cursor.executemany(instruccion,data)
#Fa=float(input("Valor de la reaccion axial: "))
cursor.execute("SELECT * FROM RODAMIENTOS")
#cursor.execute("ALTER TABLE RODAMIENTOS ADD COLUMN FACTOR REAL")
#cursor.execute("UPDATE RODAMIENTOS SET FACTOR = (f0 * ?) / Cor",(Fa,))
##datos=cursor.fetchall()
conexion.commit()
#print(datos) 
conexion.close()

'''