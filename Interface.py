from tkinter import *
from tkinter import ttk
import pandas as pd
import numpy as np
from sympy import symbols, Eq, solve
from sympy.vector import CoordSys3D
import numpy as np
import pandas as pd
import tabla_carga_equivalente
from Esfuerzos_medios import X_Y
import obtener_data
diametros = []

class Grafica(Frame):
    
    def __init__(self, master, *args):
        super().__init__(master,*args)
        # Creaación del frame principal
        self.Principalframe = Frame(self.master,  bg='#5484c7', bd=2)
        self.Principalframe.config(bg="white", width=800, height=530)     
        self.Principalframe.pack()
        #Llamar las configuraciones del Principalframe
        self.widgets()
        self.Label_Entradas()
        self.Label_Salidas()
        

    def widgets(self):
        #Tres Frame, para el llenado de los datos 
        self.Decframe = Frame(self.Principalframe)
        self.Izqframe = Frame(self.Principalframe)
        self.bajoframe = Frame(self.Principalframe)
        self.config_frame()
    
    def config_frame(self):
        #configuración de los tres frames
        self.bajoframe.config(bg="#e03e53", width=800, height=100)     
        self.bajoframe.pack(side="bottom")        
        self.Decframe.config(bg="#37d4cc", width=400, height=430)     
        self.Decframe.pack(side="left")
        self.Izqframe.config(bg="#00a5b5", width=400, height=430)     
        self.Izqframe.pack(side="right")
        self.Title_entrada = Label(self.Decframe, text =  'Ingrese los valores').place(x = 58, y = 20 , width=284, height=25)
        self.Title_salida  = Label(self.Izqframe, text = 'Respuestas obtenidas').place(x = 50, y = 50 , width=300, height=25)
    
    def Label_Entradas(self):
        #Label para los datos a pedir
        self.Hp = Label(self.Decframe, text =   'Potencia [Hp]').place(x = 60, y = 70 , width=100, height=25)
        self.n  = Label(self.Decframe, text = 'Velocidad [rpm]').place(x = 60, y = 120, width=100, height=25)
        self.L5 = Label(self.Decframe, text       = 'L5 [pies]').place(x = 60, y = 170, width=100, height=25)
        self.L6 = Label(self.Decframe, text       = 'L6 [pies]').place(x = 60, y = 220, width=100, height=25)
        self.L7 = Label(self.Decframe, text       = 'L7 [pies]').place(x = 60, y = 270, width=100, height=25)
        self.L10= Label(self.Decframe, text       =      'L10h').place(x = 60, y = 320, width=100, height=25)
        self.Entradas()

    def Entradas(self):
        # bloques, para introducir los valores pedidos
        self.Hp_e = Entry(self.Decframe)
        self.n_e  = Entry(self.Decframe)
        self.L5_e = Entry(self.Decframe)
        self.L6_e = Entry(self.Decframe)
        self.L7_e = Entry(self.Decframe)
        self.L10_e= Entry(self.Decframe)
        #configuración de la ubicación de los frame
        self.Hp_e.place(x = 190, y = 70 , width=150, height=25)
        self.n_e.place (x = 190, y = 120, width=150, height=25)
        self.L5_e.place(x = 190, y = 170, width=150, height=25)
        self.L6_e.place(x = 190, y = 220, width=150, height=25)
        self.L7_e.place(x = 190, y = 270, width=150, height=25)
        self.L10_e.place(x =190, y = 320, width=150, height=25)
        self.boton()

    # Botones que se utilizarán en la interfaz
    def boton(self):
        self.calcular = Button(self.Decframe, text = 'Calcular', font=('Arial',12), command = self.calculos).place(x = 150, y = 365, width=100, height=25)
        self.table_compat = Button(self.bajoframe, text = 'Cuadro de comparación', font=('Arial',12), command = self.new_table_comp).place(x = 130, y = 37, width=200, height=26)
        self.table_compat2 = Button(self.bajoframe, text = 'Cuadro de comparación2', font=('Arial',12), command = self.new_table_comp2).place(x =466, y = 37, width=200, height=26)

    #Label_de_los_valores_que_se_nos_dara
    def Label_Salidas(self):
        self.Axial_E = Label(self.Izqframe, text =  'Reacción Axial en E [lbf]').place(x = 47, y = 110, width=140, height=25)
        self.Radia_E = Label(self.Izqframe, text = 'Reacción Radial en E [lbf]').place(x = 47, y = 170, width=140, height=25)
        self.Axial_F = Label(self.Izqframe, text =  'Reacción Axial en F [lbf]').place(x = 47, y = 230, width=140, height=25)
        self.Radia_F = Label(self.Izqframe, text = 'Reacción Radial en F [lbf]').place(x = 47, y = 290, width=140, height=25)
        self.Salidas()

    #Valores de salida, que son calculados
    def Salidas(self):
        self.Axial_E_s = Entry(self.Izqframe)
        self.Radia_E_s = Entry(self.Izqframe)   
        self.Axial_F_s = Entry(self.Izqframe)
        self.Radia_F_s = Entry(self.Izqframe)
        self.Axial_E_s.place(x = 205, y = 110, width=150, height=25)
        self.Radia_E_s.place(x = 205, y = 170, width=150, height=25)
        self.Axial_F_s.place(x = 205, y = 230, width=150, height=25)
        self.Radia_F_s.place(x = 205, y = 290, width=150, height=25)
    
    #Delete para cuando se cambien los valores  se puedan volver a calcular y no se sobre escriba
    def Delete_Entry(self):
        self.Axial_E_s.delete(0, END)
        self.Radia_E_s.delete(0, END)
        self.Axial_F_s.delete(0, END)
        self.Radia_F_s.delete(0, END)

    #Calculo de las Fuerzas que obtuvieron de los valores ingresados
    def calculos(self):
        self.Delete_Entry()
        self.Numero_dientes,self.Angulo_presion, self.Angulo_paso_helice, self.Paso_diametral, self.Ancho_cara = self.leer_datos_excel()
        self.obte_Hp = float(self.Hp_e.get())
        self.obte_n  = float( self.n_e.get()) 
        self.obte_L5 = float(self.L5_e.get())
        self.obte_L6 = float(self.L6_e.get())
        self.obte_L7 = float(self.L7_e.get())
        self.obte_L10= float(self.L10_e.get())

        N2, N3, N4, N5, N6, N7 = self.Numero_dientes
        
        #Calcula los diámetros de los engranajes
        for i in range(6):
            diametro = self.diametro_paso(self.Numero_dientes[i],self.Paso_diametral[i])
            diametros.append(diametro)

        #Velocidad angular de los engranajes necesario
        self.w_5 = self.obte_n*(N2/N3)*(N4/N5)
        w_6 = self.w_5

        #Velocidad de línea de los engranajes necesarios
        v_5 = self.velocidad_linea(self.w_5,diametros[3]) #Velocidad angular de 5 usando relación de engranes
        v_6 = self.velocidad_linea(w_6,diametros[4]) #Al estar en el mismo eje
        ##Encontradas las velocidades, procedemos a encontrar las fuerzas.
        
        #Fuerzas para engrane cónico 5
        ft_5 = self.fuerza_tangencial(self.obte_Hp,v_5)        #Fuerza tangencial del engrane cónico 5 
        fr_5 = ft_5*np.tan(np.deg2rad(self.Angulo_presion[3]))*np.cos(np.deg2rad(self.Angulo_paso_helice[3]))    #Fuerza radial del engrane cónico 5 , a partir del angulo de presion y de paso obtenidos de excel
        fa_5 = fr_5*np.tan(np.deg2rad(self.Angulo_presion[3]))*np.sin(np.deg2rad(self.Angulo_paso_helice[3]))    #Fuerza axial del engrane cónico 5 , a partir del angulo de presion y de paso obtenidos de excel    

        #Fuerzas para engrane recto 6
        ft_6 = self.fuerza_tangencial(self.obte_Hp,v_6)        #Fuerza tangencial del engrane recto 6  
        fr_6 = ft_6*np.tan(np.deg2rad(self.Angulo_presion[4]))

        ## Encontradas las fuerzas de los engranes involucradas, realizaremos análisis estático para encontrar reacciones en los cojinetes.
        # Asignamos nuestros vectores fuerza en los cojinetes
        # E= [Ex,Ey,0]     pues por dato solo tendrá fuerza radial y axial
        # F= [0,Fy,0]      pues por dato solo tendrá fuerza radial

        # Definir las variables desconocidas como simbólicas
        Ey, Fy = symbols('Ey Fy')
        # Definir el sistema de coordenadas
        N = CoordSys3D('N')

        #Inicamos el análisis estático con Sumatoria de fuerzas en X: Ex - fa_5 = 0
        self.Ex = abs(fa_5*0.00444822) #Valor absoluto y se pasa  a KN
        
        #Sumatoria de fuerzas en Y: 
            # Ey + fr_5 - fr_6 + Fy = 0        Ec1 (su mención es solo como guía para proseguir con el desarollo)
        
        #Sumatoria de momentos en E: 
        #  FE x F + f6E x f6 + f5E x f5 = 0        Ec2 (su mención es solo como guía para proseguir con el desarollo)
        
        #Creamos los vectores de Fuerzas de los engranes en forma vectorial:
        f6 = -fr_6*N.j + ft_6*N.k
        f5 = -fa_5*N.i + fr_5*N.j + ft_5*N.k
        F = Fy*N.j
        
        #Creamos los vectores de posición desde el cojinete E a cada una de las fuerzas:
        F_E = (self.obte_L5+self.obte_L6)*N.i                             #F_E = (l5+l6)*N.i
        f6_E = -self.obte_L7*N.i + (diametros[4]/2)*N.j                   #f6_E = -l7*N.i + (diametros[4]/2)*N.j
        f5_E = (self.obte_L6-diametros[2])*N.i - diametros[3]*N.j         #f5_E = (l6-diametros[2])*N.i - diametros[3]*N.j

        # Definimos las ecuaciones Ec1 y Ec2 que se mencionaron anteriormente:
        eq1 = Eq(Ey + fr_5 - fr_6 + Fy, 0)
        eq2 = Eq(F_E.dot(N.i) * F.dot(N.j) + f6_E.dot(N.i) * f6.dot(N.j) + f5_E.dot(N.i) * f5.dot(N.k), 0)

        # Resolvemos el sistema de ecuaciones para encontrar Ey , Fy
        sol = solve((eq1, eq2), (Ey, Fy))

        # Obtener las soluciones
        Ey_sol = abs(sol[Ey]*0.00444822)#Valor absoluto y se pasa  a KN
        Fy_sol = abs(sol[Fy]*0.00444822)#Valor absoluto y se pasa  a KN
        
        self.fE = [self.Ex, Ey_sol]
        self.fF = [0, Fy_sol]
        
        #Insertar los valores encontrados en se respectivo Entry
        self.Axial_E_s.insert(0, round(self.Ex,2))
        self.Radia_E_s.insert(0, round(Ey_sol,2))
        self.Axial_F_s.insert(0, 0)
        self.Radia_F_s.insert(0, round(Fy_sol,2))
    
    #Creación de la nueva pestaña  e impresion del cojinete E
    def new_table_comp(self):
        self.new_pest = Toplevel(self.Principalframe)
        self.config_new_pest()
        self.cojineteE()
        self.destro()
    
    #Armado de la tabla del cojinete E
    def cojineteE(self):
        table2 = ttk.Treeview(self.new_principal)
        # Definir las columnas de la tabla
        table2["columns"] = ("column1", "column2", "column3", "column4", "column5", "column6","column7","column8","column9","column10")

        # Configurar encabezados de columnas
        text = ["C [KN]", "Cor [KN]","Fo","fo.Fa/Cor","e","Fa/Fr","Y","P [KN]","Creq [KN]", "Creq < C"]
        for i in range(len(text)):
            table2.heading(f"column{i+1}", text=text[i])
        lista_final = []
        self.actualizacion(self.fE,lista_final)
        # Agregar filas de datos
        for i in range(69):
            table2.insert('', index='end', text=f"{i+1}", values=(lista_final[i][0], lista_final[i][1], lista_final[i][2], lista_final[i][3],
                           lista_final[i][4], lista_final[i][5], lista_final[i][6], lista_final[i][7],
                           lista_final[i][8], lista_final[i][9]))
        # Ajustar el tamaño de las columnas
        table2.column("#0", width=40)    
        for i in range(1, 11):
            table2.column(f"column{i}", width=60)
        # Cambiar el nombre de las filas
        for i, row_id in enumerate(table2.get_children(), start=1):
            table2.item(row_id, text=f"{i}")
        # Mostrar la tabla
        table2.place(width=780, height=180 ,x = 5, y = 5)
    
    #Configuración de la pestaña para el cojinete E
    def config_new_pest(self):
        self.new_pest.title('Tabla comparativa E')
        self.new_pest.geometry('800x250')
        self.new_pest.config(bg='#515d6e', bd=4)
        self.new_principal = Frame(self.new_pest)
        self.new_principal.config(bg="#f0cf59", width=800, height=250)     
        self.new_principal.pack() 

    #creación de la pestaña  e impresion del cojitene F
    def new_table_comp2(self):
        self.new_pest2 = Toplevel(self.Principalframe)
        self.config_new_pest2()
        self.cojineteF()
        self.destro2()
    
    #configuración de la pestaña para el cojitene F
    def config_new_pest2(self):
        self.new_pest2.title('Tabla comparativa F')
        self.new_pest2.geometry('800x250')
        self.new_pest2.config(bg='#515d6e', bd=4)
        self.new_principal2 = Frame(self.new_pest2)
        self.new_principal2.config(bg="#f0cf59", width=800, height=250)     
        self.new_principal2.pack()

    #Armado de la tabla del cojinete F
    def cojineteF(self):
        table3 = ttk.Treeview(self.new_principal2)
        # Definir las columnas de la tabla
        table3["columns"] = ("column1", "column2", "column3", "column4", "column5", "column6","column7","column8","column9","column10")

        # Configurar encabezados de columnas
        text3 = ["C [KN]", "Cor [KN]","Fo","fo.Fa/Cor","e","Fa/Fr","Y","P [KN]","Creq [KN]", "Creq < C"]
        for i in range(len(text3)):
            table3.heading(f"column{i+1}", text=text3[i])
        lista_final2 = []
        self.actualizacion(self.fF,lista_final2)
        # Agregar filas de datos
        for i in range(69):
            table3.insert('', index='end', text=f"{i+1}", values=(lista_final2[i][0], lista_final2[i][1], lista_final2[i][2], lista_final2[i][3],
                           lista_final2[i][4], lista_final2[i][5], lista_final2[i][6], lista_final2[i][7],
                           lista_final2[i][8], lista_final2[i][9]))
        # Ajustar el tamaño de las columnas
        table3.column("#0", width=40)    
        for i in range(1, 11):
            table3.column(f"column{i}", width=60)
        # Cambiar el nombre de las filas
        for i, row_id in enumerate(table3.get_children(), start=1):
            table3.item(row_id, text=f"{i}")
        # Mostrar la tabla
        table3.place(width=780, height=180 ,x = 5, y = 5)

    #Cerrar la pestaña del cojinete E
    def destro(self):
        boton_cerrar = Button(self.new_principal, text="Cerrar", command=self.new_pest.destroy)
        boton_cerrar.place(x = 350, y = 200, width=150, height=25)
    
    #Cerrar la pestaña del cojinete E
    def destro2(self):
        boton_cerrar2 = Button(self.new_principal2, text="Cerrar", command=self.new_pest2.destroy)
        boton_cerrar2.place(x = 350, y = 200, width=150, height=25)
        # Agregar contenido y widgets a la nueva ventana
        #etiqueta = Label(, text="¡Esta es una nueva pestaña!")
        #etiqueta.pack()
    
    def leer_datos_excel(self):
        # Lee el archivo de Excel
        df = pd.read_excel('Datos_engranajes.xlsx')
        # Crea los vectores con los nombres de las filas
        Numero_dientes = df.iloc[0, 1:].tolist()
        Angulo_presion = df.iloc[1, 1:].tolist()
        Angulo_paso_helice = df.iloc[2, 1:].tolist()
        Paso_diametral = df.iloc[3, 1:].tolist()
        Ancho_cara = df.iloc[4, 1:].tolist()

        return Numero_dientes,Angulo_presion, Angulo_paso_helice, Paso_diametral, Ancho_cara

    # Función para calcular la velocidad de salida del sistema de transmisión
    def velocidad_salida(self,velocidad_entrada,N2,N3,N4,N5,N6,N7):
        return velocidad_entrada*(N2/N3)*(N4/N5)*(N6/N7)

    # Función para calcular el diametro de paso a partir del numero de dientes y paso diametral
    def diametro_paso(self,num_dientes, P):
        diametro_paso = num_dientes/P 
        return diametro_paso

    # Función para encontrar la velocidad lineal en cada engrane
    def velocidad_linea(self,w,d):
        return (np.pi*d*w)/12

    # Función para encontrar la fuerza tangencial 'Wt' en cada engrane a partir de su potencia y velocidad lineal
    def fuerza_tangencial(self,p,v):
        return (33000*p)/v

    def create_table(self):
        table = ttk.Treeview(self.bajoframe)
        # Definir las columnas de la tabla
        table["columns"] = ("column1", "column2", "column3", "column4", "column5", "column6", "column7", "column8", "column9")

        text1 = ["N° Rodamiento", "C(kN)", "Cor(kN)", "fo", "f0.Fa/Cor", "e", "Fa/Fr", "Y", "P(kN)"]

        for i in range(len(text1)):
            table.heading(f"column{i+1}", text=text1[i])
        # Configurar encabezados de columnas

        # Agregar filas de datos
        for i in range(5):
            table.insert('', index='end', text=f"{i+1}", values=(f"Dato {i+1}", f"Dato {i+2}", f"Dato {i+3}", f"Dato {i+4}",
                                                                f"Dato {i+5}", f"Dato {i+6}", f"Dato {i+7}", f"Dato {i+8}",
                                                                f"Dato {i+9}"))
        # Ajustar el tamaño de las columnas
        table.column("#0", width=40) 
        table.column("column1", width=120)   
        for i in range(2, 10):
            table.column(f"column{i}", width=77)
        # Cambiar el nombre de las filas
        for i, row_id in enumerate(table.get_children(), start=1):
            table.item(row_id, text=f"{i}")
        # Mostrar la tabla
        table.place(width=780, height=160, x = 5, y = 3)
    
    #Función con el fin de obtener los valores de evaluación del cojinete
    def actualizacion(self,term,lista_final):
        L10h = self.obte_L10

        for i in range(69):
            Fa = term[0]
            Fr = term[1]
            fila_deseada = i + 1  # Número de fila deseada
            valores_fila = obtener_data.obtener_valores_fila(fila_deseada)
            #print("Valores de la fila:", valores_fila)

            # Valores de tabla
            C = valores_fila[1]
            Cor = valores_fila[2]
            f0 = valores_fila[3]
            
            def relacion(Fa, Fr):
                return Fa / Fr

            def factor(fo, fa,cor):
                return round((fo*fa)/cor,3)

            def creq(P, n, L10h):
                return P * (((60 * n * L10h) / 10 ** 6) ** (1 / 3))

            def carga_equivalente(fa, fr, x, y):
                return x * fr + y * fa

            tabla = tabla_carga_equivalente.tabla
            valor = factor(f0, Fa, Cor)

            x, y, e = X_Y(tabla, valor, Fa, Fr)
            y = round(y,3)
            e = round(e,3)

            P = round(carga_equivalente(Fa, Fr, x, y),3)

            Rela = round(relacion(Fa, Fr),3)
            Factor = factor(f0, Fa, Cor)
            c_req = round(creq(P, L10h, self.w_5),3)

            if c_req < C:
                caso = "Si"
            else:
                caso = "No"

            lista_tabla = [C,Cor, f0, Factor,e,Rela,y,P,c_req,caso]
            lista_final.append(lista_tabla)
        return lista_final

#Inicialización del codigo
if __name__ == "__main__":
    ventana = Tk()
    ventana.geometry('800x530')
    ventana.wm_title('Calculos de Rodamiento')
    ventana.config(bg='#515d6e', bd=4)
    #ventana.iconbitmap('roda.ico')
    app = Grafica(ventana)
    app.mainloop()