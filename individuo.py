class Individuo:

    def __init__(self, bits_del_individuo, espacio_individuo,num_individuo, costo):
        self.bits_del_individuo = bits_del_individuo
        self.espacio_individuo = espacio_individuo
        self.num_individuo = num_individuo
        self.costo = costo

    @property
    def getBitsIndividuo(self):
        return self.bits_del_individuo
    
    @getBitsIndividuo.setter
    def setBitsIndividuo(self, bits):
        self.bits_del_individuo = bits
    
    @property
    def getEspacioIndividuo(self):
        return self.espacio_individuo

    @getEspacioIndividuo.setter
    def setEspacioIndividuo(self,espacio):
        self.espacio_individuo = espacio
    
    @property
    def getNumIndividuo(self):
        return self.num_individuo

    @getNumIndividuo.setter
    def setNumIndividuo(self,id):
        self.num_individuo = id

    @property
    def getCosto(self):
        return self.costo

    @getCosto.setter
    def setCosto(self,costo):
        self.costo = costo

        
        