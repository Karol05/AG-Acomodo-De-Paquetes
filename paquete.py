class Paquete:

    def __init__(self, categoria_paquete, tamaño_paquete, costo_final):
        self.categoria_paquete = categoria_paquete
        self.tamaño_paquete = tamaño_paquete
        self.costo_final = costo_final

    @property
    def getCategoriaPaquete(self):
        return self.categoria_paquete

    @getCategoriaPaquete.setter
    def setCategoriaPaquete(self,categoria):
        self.categoria_paquete = categoria

    @property
    def getTamañoPaquete(self):
        return self.tamaño_paquete

    @getTamañoPaquete.setter
    def setTamañoPaquete(self, tamaño_paquete):
        self.tamaño_paquete = tamaño_paquete

    @property
    def getCostoFinal(self):
        return self.costo_final
    
    @getCostoFinal.setter
    def setCostoFinal(self,costo_final):
        self.costo_final = costo_final

        