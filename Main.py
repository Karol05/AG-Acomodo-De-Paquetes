import math
import random
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import cv2
from matplotlib import image, pyplot as plt
from iteration_utilities import duplicates
from individuo import Individuo
from paquete import Paquete

categorias_de_paquetes = []
lista_paquetes = []
poblacion_inicial = []
incremento_gen = 0
aux_imagen = 0
mejor_promedio_peor = []

# individuo = Individuo()
# paquete = Paquete()
class AcomodoPaquetes(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("interfaz.ui", self)
        self.btn_agregar_paquetes.clicked.connect(self.validar_datos_agregar_paquetes)
        self.btn_paquetes_deseados.clicked.connect(self.validar_datos_paquetes_deseados)
        self.btn_iniciar.clicked.connect(self.validar_datos_poblaciones_generaciones_probabilidades)

    def validar_datos_agregar_paquetes (self) :
        try:
            tipo_de_paquetes = str (self.paquetes.text())
            tamaño_paquetes = int(self.tamano_paquete.text())
            precio_publico = int(self.precio_publico.text())
            costo_envio = int(self.costo_envio.text())
            self.guardar_tipos_de_paquetes(tipo_de_paquetes,tamaño_paquetes,precio_publico,costo_envio)
        except ValueError :
            print("Datos mal ingresados")

    def validar_datos_paquetes_deseados(self):
        try:
            tipo_paquete_deseado = str(self.tipo_paquete_deseado.text())
            cantidad = int(self.cantidad.text())
            self.guardar_paquetes_deseados()

        except ValueError:
            print("Datos mal ingresados")

    def validar_datos_poblaciones_generaciones_probabilidades(self):
        try:
            inicio_poblacion = int (self.poblacion_init.text())
            pmi = float (self.PMI.text())
            mayor_poblacion = int (self.poblacion_max.text())
            pmg = float (self.PMG.text())
            num_generaciones = int (self.generaciones.text())
            tamaño_contenedor = int(self.contenedor.text())
            self.run()

        except ValueError:
            print("Datos mal ingresados")


    def guardar_tipos_de_paquetes(self,tipo_de_paquetes, tamaño_paquetes,precio_publico,costo_envio):
        costo_final = precio_publico - costo_envio
        addPaquete = Paquete(tipo_de_paquetes,tamaño_paquetes,costo_final)
        # addPaquete = paquete.setCategoriaPaquete(tipo_de_paquetes)
        # addPaquete = paquete.setTamañoPaquete(tamaño_paquetes)
        # addPaquete = paquete.setCostoFinal(costo_final)
        categorias_de_paquetes.append(addPaquete)
        print('---------- Paquete guardado con exito ----------')

    def guardar_paquetes_deseados(self):

        for i  in range(int(self.cantidad.text())):
            if str(self.tipo_paquete_deseado.text()) in ['A']:
                lista_paquetes.append(categorias_de_paquetes[0])
            if str(self.tipo_paquete_deseado.text()) in ['B']:
                lista_paquetes.append(categorias_de_paquetes[1])
            if str(self.tipo_paquete_deseado.text()) in ['C']:
                lista_paquetes.append(categorias_de_paquetes[2])
            if str(self.tipo_paquete_deseado.text()) in ['D']:
                lista_paquetes.append(categorias_de_paquetes[3])
            print("---------- Paquete deseado guardado ----------")

    def individuo_unico(self,aux1,aux2):
        unico = True  
        for i in aux2:
            if aux1 == i:
                unico = False
                break
        return unico

    def creacion_del_individuo(self):
        for i in range(int (self.poblacion_init.text())):
            array_individuos = []
            cont = 0
            while cont < len(lista_paquetes):
                num_aleatorio = random.randint(0,len(lista_paquetes)-1)
                if self.individuo_unico(num_aleatorio,array_individuos):
                    array_individuos.append(num_aleatorio)
                    cont+=1
            object_type_indi = Individuo(array_individuos,0,i+1,0)
            poblacion_inicial.append(object_type_indi)
        print("---------- Individuos creados ----------")

    def validar_espacio_del_individuo(self):
        almacen_individuos_validos = []
        poblacion_indi_validos = []
        tamañoIndividuosValidos = 0
        costoIndividuoValidos = 0
        for i in range(len(poblacion_inicial)):
            for j in range(len(poblacion_inicial[i].getBitsIndividuo)):
                guardar_bits = lista_paquetes[poblacion_inicial[i].getBitsIndividuo[j]]
                aux_tamaño_total = tamañoIndividuosValidos + guardar_bits.getTamañoPaquete
                if aux_tamaño_total <= int(self.contenedor.text()):
                    tamañoIndividuosValidos = tamañoIndividuosValidos + guardar_bits.getTamañoPaquete
                    costoIndividuoValidos = costoIndividuoValidos + guardar_bits.getCostoFinal
                    almacen_individuos_validos.append(poblacion_inicial[i].getBitsIndividuo[j])
                else:
                    poblacion_inicial[i].setCostoFinal = costoIndividuoValidos
                    poblacion_inicial[i].setTamañoPaquete = tamañoIndividuosValidos

                    object_individuo = Individuo(almacen_individuos_validos,tamañoIndividuosValidos,i,costoIndividuoValidos)
                    poblacion_indi_validos.append(object_individuo)

                    almacen_individuos_validos.clear()
                    break
            tamañoIndividuosValidos = 0
            costoIndividuoValidos = 0
        print("---------- Individuos validados ----------")
        return poblacion_indi_validos

    def cruza(self):
        poblacion_indi_validos = self.validar_espacio_del_individuo()
        num_cruza = math.ceil(int (self.poblacion_init.text())/2) 
        total_individuos = len(poblacion_inicial)
        lista_de_cruzados = []
        puntos_de_corte = []
        individuo_mutado = []
        auxiliar = 0
        auxiliar2 = 0
        auxiliar3 = 0
        while auxiliar3 != num_cruza:
            auxiliar2 = 0
            individuo_2= []
            individuo_1= []
            bandera = 0
            auxiliar = auxiliar + 1
            puntos =  random.randint(1,3)
            puntos_de_corte=[]
            j=0
            while j<puntos:
                x=random.randint(1,len(lista_paquetes))
                if self.individuo_unico(x,puntos_de_corte):
                    puntos_de_corte.append(x)
                    j+=1
            puntos_de_corte.sort()
            individuo1=poblacion_indi_validos[auxiliar3].getBitsIndividuo
            individuo2=poblacion_indi_validos[auxiliar].getBitsIndividuo
            posicio_max = False
            for i in puntos_de_corte:
                if (i == len(lista_paquetes)):
                    posicio_max = True
                    break
            for i in range (2):
                individuo_mutado.append(round(random.random(), 2))
            
            for i in range(puntos):
                if bandera == 1:
                    auxIndividuo1 = individuo1[auxiliar2:puntos_de_corte[i]]
                    auxIndividuo2 = individuo2[auxiliar2:puntos_de_corte[i]]
                    individuo_1 = individuo_1 + auxIndividuo2
                    individuo_2 = individuo_2 + auxIndividuo1
                    bandera = 0
                    auxiliar2 = puntos_de_corte[i]
                else:
                    auxIndividuo1 = individuo1[auxiliar2:puntos_de_corte[i]]
                    auxIndividuo2 = individuo2[auxiliar2:puntos_de_corte[i]]
                    individuo_1 = individuo_1 + auxIndividuo1
                    individuo_2 = individuo_2 + auxIndividuo2
                    bandera = 1
                    auxiliar2 = puntos_de_corte[i]
            if (posicio_max == False):
                auxIndividuo1 = individuo1[auxiliar2:len(lista_paquetes)]
                auxIndividuo2 = individuo2[auxiliar2:len(lista_paquetes)]
                individuo_1 = individuo_1 + auxIndividuo1
                individuo_2 = individuo_2 + auxIndividuo2
            
            faltantes_1 = list(duplicates(individuo_1))
            faltantes_2 = list(duplicates(individuo_2))
            if (len(faltantes_1) != 0):
                auxiliar2 = 0
                for i in range(len(individuo_1)):
                    if (faltantes_1[auxiliar2] == individuo_1[i]):
                        individuo_1[i] = faltantes_2[auxiliar2]
                        auxiliar2 = auxiliar2 + 1
                        if auxiliar2 == len(faltantes_1):
                            break
                aux2 = 0
                for i in range(len(individuo_2)):
                    if (faltantes_2[aux2] == individuo_2[i]):
                        individuo_2[i] = faltantes_1[aux2]
                        aux2 = aux2 + 1
                        if aux2 == len(faltantes_2):
                            break
            else:
                print("Todo sigue igual")
            
            objeto_individuo = Individuo(individuo_1, 0, 0, 0)
            objeto_individuo2 = Individuo(individuo_2, 0, 0, 0)
            lista_de_cruzados.append(objeto_individuo)
            lista_de_cruzados.append(objeto_individuo2)
            

            if (auxiliar == total_individuos-1):
                auxiliar3 = auxiliar3 + 1
                auxiliar = auxiliar3
        for i in range(len(lista_de_cruzados)):
            lista_de_cruzados[i].setNumIndividuo = i+1
        print("---------- FUNCION DE CRUZA ----------")
        return lista_de_cruzados

    def mutacion(self):
        lista_de_cruzados = self.cruza()
        probabilidades_de_mutacionIndividuos = []
        almacen_de_posiciones = []
        individuos_mutados = []

        for i in range(len(lista_de_cruzados)):
            probabilidades_de_mutacionIndividuos.append(round(random.random(),6))

        for j in range(len(lista_de_cruzados)):
            probabilidades_de_mutacionGen = []
            datos_individuo_mutado = lista_de_cruzados[j].getBitsIndividuo
            if probabilidades_de_mutacionIndividuos[j] <= float (self.PMI.text()):
                for k in range(len(datos_individuo_mutado)):
                    probabilidades_de_mutacionGen.append(round(random.random(),6))
                bandera = 0
                cont = 0
                while cont < len(datos_individuo_mutado):
                    num_aleatorio2 = random.randint(1,len(datos_individuo_mutado))
                    if self.individuo_unico(num_aleatorio2,almacen_de_posiciones):
                        almacen_de_posiciones.append(num_aleatorio2)
                        cont+=1
                for q in probabilidades_de_mutacionGen:
                    if q <= float (self.PMG.text()):
                        while almacen_de_posiciones[bandera]-1 == bandera:
                            almacen_de_posiciones[bandera]-1 == random.shuffle(almacen_de_posiciones)
                        gen_posicion_real = datos_individuo_mutado[almacen_de_posiciones[bandera]-1]
                        gen_cambio_posicion = datos_individuo_mutado[bandera]
                        datos_individuo_mutado[bandera] = gen_posicion_real
                        datos_individuo_mutado[almacen_de_posiciones[bandera]-1] = gen_cambio_posicion
                    bandera+=1
                individuo_3 = Individuo(datos_individuo_mutado,0,j,0)
                individuos_mutados.append(individuo_3)
            else:
                individuo_3 = Individuo(lista_de_cruzados[j].getBitsIndividuos,lista_de_cruzados[j].getEspacioIndividuo,j,lista_de_cruzados[j].getCosto)
                individuos_mutados.append(individuo_3)
        print("---------- FUNCION MUTACION ----------")
        return individuos_mutados
       
    def poda(self):
        individuos_mutados2 = self.mutacion()
        individuos_mutados2.sort(key=lambda x: x.coto, reverse=True)
        cont = 0
        for i in range(len(individuos_mutados2)):
            if len(individuos_mutados2) >int (self.poblacion_max.text()):
                individuos_mutados2.pop(cont)
            else:
                break
        
        print("---------- INDIVIDUOS FINALES ----------")
        for i in individuos_mutados2:
            print(i.getBitsIndividuo, i.getEspacioIndividuo,i.getCostoFinal)
        poblacion_inicial.clear()
        poblacion_inicial = individuos_mutados2
        return individuos_mutados2

    def generarVideo(self,archivo):
        list_images = []
        for imagen in range(int (self.generaciones.text())):
            name_images = "Imagenes/generation" + str(imagen+1) + ".png"
            openCSV = cv2.imread(name_images)
        img = list_images[-1]

        alto,ancho = img.shape[:2]
        path = "Video/" + archivo + ".mp4"
        video = cv2.VideoWriter(path,cv2.VideoWriter_fourcc(*"mp4v"), 4, (ancho, alto))

        for i in list_images:
            video.write(i)
        video.release()

    def grafica_historico(self):
        suma = 0
        mejor = 0
        x = []
        y = []
        individuo_final = self.poda()
        global incremento_gen
        peor = individuo_final[len(individuo_final)-1].getCosto
        mejor = individuo_final[0].getCosto

        for k in range(len(individuo_final)):
            suma = suma + individuo_final[k].getCosto
        promedio = suma / len(individuo_final)
        mejor_promedio_peor.append([mejor, peor, promedio])

        if incremento_gen == int (self.generaciones.text()):
            cont = 0
            k = 0
            fig = plt.figure(figsize=(12,7))
            fig.tight_layout()
            plt.subplot(1, 1, 1)        
            lineas = [["Mejor", "green"], ["Peor", "red"], ["Promedio", "pink"]]      
            while cont < 3 :
                for xy in mejor_promedio_peor :
                    k += 1
                    print(f"{lineas[cont][0]}: x: {k} | y: {xy[cont]} ")
                    x.append(k)
                    y.append(xy[cont])
                k = 0
                plt.plot(x, y, label= lineas[cont][0], color = lineas[cont][1])
                x.clear()
                y.clear()
                cont += 1  
            mejor_promedio_peor.sort()
            plt.plot(incremento_gen, mejor_promedio_peor[len(mejor_promedio_peor)-1][0], "o", label="Mejor Individuo", color = "red")
            
            plt.savefig(f"Imagenes/Historico.png")
            plt.legend(loc='lower right')
            plt.show()
            
            mejor_promedio_peor.clear()
        incremento_gen += 1
    
    def run(self):
        self.creacion_del_individuo()
        for i in range(int (self.generaciones.text())):
            self.grafica_historico()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = AcomodoPaquetes()
    GUI.show()
    sys.exit(app.exec_())