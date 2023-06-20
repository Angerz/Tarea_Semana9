import sqlite3
def obtener_valores_por_codigo():
    # Conexión a la base de datos
    conn = sqlite3.connect('RODAMIENTOS.db')
    cursor = conn.cursor()

    # Solicitar al usuario el valor de CODIGO
    codigo_valido = False
    while not codigo_valido:
        codigo = input("Ingrese el valor de CODIGO: ")
        cursor.execute("SELECT * FROM RODAMIENTOS WHERE CODIGO=?", (codigo,))
        result = cursor.fetchone()
        if result:
            codigo_valido = True
        else:
            print("El código ingresado no está en la tabla. Intente nuevamente.")

    # Obtener los valores correspondientes a CODIGO
    co = result[1]
    cor = result[2]
    fo = result[3]

    # Cerrar cursor y conexión
    cursor.close()
    conn.close()

    return co,cor,fo



def obtener_valores_fila(n):
    # Conexión a la base de datos
    conn = sqlite3.connect('RODAMIENTOS.db')
    cursor = conn.cursor()

    # Consulta para seleccionar los valores de la fila "n"
    cursor.execute("SELECT * FROM RODAMIENTOS WHERE rowid = ?", (n,))

    # Obtener el resultado
    resultado = cursor.fetchone()

    # Verificar si se encontró un resultado
    if resultado is not None:
        # Convertir el resultado a una lista
        valores = list(resultado)
        return valores
    else:
        print("No se encontró la fila", n)

    # Cerrar cursor y conexión
    cursor.close()
    conn.close()


def imprimir_codigos():
    # Conexión a la base de datos
    conn = sqlite3.connect('RODAMIENTOS.db')
    cursor = conn.cursor()

    # Consulta para seleccionar los valores de la columna "CODIGO"
    cursor.execute("SELECT CODIGO FROM RODAMIENTOS")

    # Obtener todos los resultados
    resultados = cursor.fetchall()

    # Cerrar cursor y conexión
    cursor.close()
    conn.close()
    return resultados
