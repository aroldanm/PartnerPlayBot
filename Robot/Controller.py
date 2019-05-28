from adafruit_servokit import ServoKit
import time



class Controller():
    kit = None
    shouldAbort = False

    def __init__(self):
        self.initial = [178, 178, 178, 170]
        self.angSub3 = 180
        self.angBaj3 = 115
        self.angOpen4 = 140
        self.angClose4 = 170
        self.tiempoPinza = 0.01
        self.positionEat = [150, 90]
            
        self.positionAngles = {"12" : {"S1":72, "S2":123},"14" : {"S1":86, "S2":115},"16" : {"S1":97, "S2":119},"18" : {"S1":102, "S2":135},

                              "21" : {"S1":70, "S2":105},"23" : {"S1":86, "S2":94},"25" : {"S1":100, "S2":92},"27" : {"S1":109, "S2":100},

                              "32" : {"S1":83, "S2":79},"34" : {"S1":98, "S2":73},"36" : {"S1":112, "S2":75},"38" : {"S1":121, "S2":89},

                              "41" : {"S1":76, "S2":70},"43" : {"S1":93, "S2":59},"45" : {"S1":109, "S2":58},"47" : {"S1":124, "S2":65},

                              "52" : {"S1":85, "S2":51},"54" : {"S1":104, "S2":45},"56" : {"S1":123, "S2":47},"58" : {"S1":137, "S2":59},

                              "61" : {"S1":73, "S2":47},"63" : {"S1":93, "S2":38},"65" : {"S1":115, "S2":35},"67" : {"S1":137, "S2":42},

                              "72" : {"S1":79, "S2":31},"74" : {"S1":102, "S2":23},"76" : {"S1":130, "S2":26},"78" : {"S1":151, "S2":39},

                              "81" : {"S1":60, "S2":30},"83" : {"S1":79, "S2":13},"85" : {"S1":112, "S2":11},"87" : {"S1":148, "S2":21},
                              
                              "comidas" : {"S1" :170, "S2":165}
                               }
        self.positionAngles2 = {"12" : {"S1":72, "S2":123},"14" : {"S1":86, "S2":115},"16" : {"S1":97, "S2":119},"18" : {"S1":102, "S2":135},

                              "21" : {"S1":70, "S2":105},"23" : {"S1":86, "S2":94},"25" : {"S1":100, "S2":92},"27" : {"S1":109, "S2":100},

                              "32" : {"S1":83, "S2":79},"34" : {"S1":98, "S2":73},"36" : {"S1":112, "S2":75},"38" : {"S1":121, "S2":89},

                              "41" : {"S1":76, "S2":70},"43" : {"S1":93, "S2":59},"45" : {"S1":109, "S2":58},"47" : {"S1":124, "S2":65},

                              "52" : {"S1":85, "S2":51},"54" : {"S1":104, "S2":45},"56" : {"S1":123, "S2":47},"58" : {"S1":137, "S2":59},

                              "61" : {"S1":73, "S2":47},"63" : {"S1":93, "S2":38},"65" : {"S1":115, "S2":35},"67" : {"S1":137, "S2":42},

                              "72" : {"S1":79, "S2":31},"74" : {"S1":102, "S2":23},"76" : {"S1":130, "S2":26},"78" : {"S1":151, "S2":39},

                              "81" : {"S1":60, "S2":30},"83" : {"S1":79, "S2":13},"85" : {"S1":112, "S2":11},"87" : {"S1":148, "S2":21},
                              
                              "comidas" : {"S1" :170, "S2":165}
                               }
        self.kit = ServoKit(channels=16)
        self.kit.servo[0].angle = self.initial[0]
        self.kit.servo[1].angle = self.initial[1]
        self.kit.servo[3].angle = self.initial[2]
        self.kit.servo[4].angle = self.initial[3]

    def movToInit(self, desde):
        return self.movTo(desde,[180,180])
    
    def movToEat(self, desde):
        return self.movTo(desde, [150, 150])

    def movFromInit(self, hasta):
        return self.movTo([180,180], hasta)
        
    def movTo(self,desde, hasta):
        for i in range(2):
            fin = hasta[i]
            if i == 0:
                tiempo = 0.02
            if i == 1:
                tiempo = 0.01
            while self.shouldAbort == False and fin != desde[i]:
                if desde[i] > hasta[i]:
                    desde[i] = desde[i] - 1
                else:
                    desde[i] = desde[i] + 1
                self.kit.servo[i].angle = desde[i]
                time.sleep(tiempo)
        return desde
                
    def mov(self, desde, hasta, tiempo, serv):
        inicio = desde
        if tiempo == 0:
            print('Servo: ', serv)
            self.kit.servo[serv].angle = hasta
        else:
            while self.shouldAbort == False and hasta != inicio:
                if desde > hasta:
                    inicio = inicio - 1
                    self.kit.servo[serv].angle = inicio
                    time.sleep(tiempo)
                else:
                    inicio = inicio + 1
                    self.kit.servo[serv].angle = inicio
                    time.sleep(tiempo)
        return inicio
                
    def recoge(self):
        #Abrir servo 4
        self.mov(self.angClose4, self.angOpen4, self.tiempoPinza, 4)
        time.sleep(0.5)
        #bajar servo 3
        self.mov(self.angSub3, self.angBaj3, 0.007, 3)
        time.sleep(0.5)
        #cerrar servo 4
        self.mov(self.angOpen4, self.angClose4, self.tiempoPinza, 4)
        time.sleep(0.5)
        #subir servo 3
        self.mov(self.angBaj3, self.angSub3, 0.001, 3)
        time.sleep(0.5)
                
                                                                                                                                 

    def suelta(self):
        #bajar servo 3
        self.mov(self.angSub3, self.angBaj3, 0.007, 3)
        time.sleep(0.5)
        #Abrir servo 4
        self.mov(self.angClose4, self.angOpen4,self. tiempoPinza, 4)
        time.sleep(0.5)
        #subir servo 3
        self.mov(self.angBaj3, self.angSub3, 0.001, 3)
        time.sleep(0.5)
        #cerrar servo 4
        self.mov(self.angOpen4, self.angClose4, self.tiempoPinza, 4)
        time.sleep(0.5)
        
    def abort(self):
        self.shouldAbort = True

    def move(self, stringJugada, stringComidas):
        self.shouldAbort = False
    
        origen = stringJugada[0] + stringJugada[1]
        end = len(stringJugada)
        final = stringJugada[end-2] + stringJugada[end-1]

        dic1 = self.positionAngles.get(origen)
        dic2 = self.positionAngles2.get(final)
        
        mov1 = [dic1.get('S1'), dic1.get('S2')-1]
        mov2 = [dic2.get('S1')-1, dic2.get('S2')+6]
        
        #print ('Jugada: ', stringJugada , ', Posicion: ',mov1, mov2)

        position = 0
        steps = 5
        i = 0
        while self.shouldAbort == False and i < steps:
            if i == 0:
                position = self.movFromInit(mov1)
                time.sleep(0.5)
            
            elif i == 1:
                self.recoge()
                time.sleep(0.5)
                
            elif i == 2:
                position = self.movTo(mov1, mov2)
                
            elif i == 3:
                self.suelta()
                
            elif i == 4:
                movAux = mov2
                if(len(stringComidas) == 0):
                    position = self.movToInit(mov2)
                else:
                    self.shouldAbort = False
                    while self.shouldAbort == False and len(stringComidas) != 0:
                        comida = stringComidas[0] + stringComidas[1]
                        dic3 = self.positionAngles.get(comida)
                        mov3 = [dic3.get('S1'), dic3.get('S2')]
                        print('Comida: ', stringComidas, ', Posicion: ', mov3)
                        stringComidas = stringComidas[2:]
                        self.movTo(movAux, mov3)
                        self.recoge()
                        time.sleep(0.5)
                        position = self.movToEat(mov3)
                        self.suelta()
                    if self.shouldAbort == False:
                        self.movToInit(position)
            i+=1
        if self.shouldAbort == True:
            self.shouldAbort = False
            # Si ha cogido una ficha > suelta + init:
            if i == 2:
                self.suelta()
                self.movToInit(position)
            # Si se desplaza con una ficha > init + suelta:
            elif i == 3 or i == 5:
                self.movToInit(position)
                self.suelta()
            # Si se desplaza sin ficha > init:
            else:
                self.movToInit(position)
                
                

#p1 = [93, 38]
#p2 = [104, 45+6]
#p3 = [85, 51+6]
#x.movTo([170, 170], p1)
#x.recoge()
#x.movTo(p1, p3)
#x.suelta()
#x.movTo(p3, [170, 170])
