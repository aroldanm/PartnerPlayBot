import operator
import numpy as np
from VC import VCModule
from time import sleep

class AIModule():
    vc = None
    
    def __init__(self):
        print("init aimodule")
        self.vc = VCModule()
    
#################################################################################
# MÉTODOS PÚBLICO
#################################################################################
    
    def scanf(self, tableroPrevio):
        haveChanged = False
        while haveChanged == False:
            print("Esperando a que el tablero cambie")
            haveChanged = self.anyChange(tableroPrevio)

    def getTablero(self):
        return self.vc.getTablero()

    def getMovimiento(self):
        #Calcular movimiento
        tablero = self.getTablero()
        tirada = self.minimax(tablero, 2, 0, 99, 'b')
        print(tirada)
        print("--------------")
        print(tablero)
        #Calcular eliminadas
        if len(tirada) > 0:
            movimiento = tirada[0]
            fichas_muertas = self.fichas_comidas(movimiento)
        return movimiento, fichas_muertas

#################################################################################
# MÉTODOS PRIVADOS
#################################################################################

    def anyChange(self, tableroPrevio):
        # Miramos si la ultima matrix y la última ha cambiado
        tableroActual = self.getTablero()
        print(tableroPrevio)
        print("-------")
        print(tableroActual)
        changed = False
        #if self.vc.comprobacionRuido() == False
        i = 0
        j = 0
        while changed == False and i < 8:
            if tableroPrevio[i][j] != tableroActual[i][j]:
                changed = True
            j += 1
            if j >= 8:
                j = 0
                i += 1
        return changed
                
#################################################################################

    #Una jugada será un string tal que origen-destino: c3b2
    def minimax(self, tablero, profundidad, a, b, jugador):
        if profundidad == 0:
            
            if jugador == 'N':
                dict_movimientos_negras = {"n1" : "-", "n2" : "-", "n3" : "-", "n4" : "-", "n5" : "-",
                            "n6" : "-", "n7" : "-", "n8" : "-", "n9" : "-", "n10" : "-",
                            "n11" : "-", "n12" : "-"}
                dict_movimientos_negras = self.posibles_movimientos(tablero, dict_movimientos_negras, 'n')
                ordenacion_move = self.ordenar_movimientos(dict_movimientos_negras, 'n')
                movimiento_negro = ordenacion_move[0]
                
                return movimiento_negro
            else:
                dict_movimientos_blancas = {"b1" : "-", "b2" : "-", "b3" : "-", "b4" : "-", "b5" : "-",
                            "b6" : "-", "b7" : "-", "b8" : "-", "b9" : "-", "b10" : "-",
                            "b11" : "-", "b12" : "-"}
                dict_movimientos_blancas = self.posibles_movimientos(tablero, dict_movimientos_blancas, 'b')
                ordenacion_move = self.ordenar_movimientos(dict_movimientos_blancas, 'b')
                movimiento_blanco = ordenacion_move[0]
                
                return movimiento_blanco
        else:    
            best_move = None
            
            
            if jugador == 'N':
                dict_negras_posteriori = {"n1" : "-", "n2" : "-", "n3" : "-", "n4" : "-", "n5" : "-",
                            "n6" : "-", "n7" : "-", "n8" : "-", "n9" : "-", "n10" : "-",
                            "n11" : "-", "n12" : "-"}
                dict_negras_posteriori = self.posibles_movimientos(tablero, dict_negras_posteriori, 'n')
                ordenacion_move_negras = self.ordenar_movimientos(dict_negras_posteriori, 'n')
                    
                for i in ordenacion_move_negras:
                    tablero_aux = np.copy(tablero)
                    tablero_aux = self.realizar_movimiento(tablero_aux, ordenacion_move_negras[0][0])
                    valor = self.minimax(tablero_aux, profundidad - 1, a, b, 'b')
                    b = max(int(ordenacion_move_negras[0][1]), int(valor[0][1]))
                    if b == ordenacion_move_negras[0][1]:
                        best_move = ordenacion_move_negras[0]
                    else:
                        best_move = valor
            else:
                dict_blancas_posteriori = {"b1" : "-", "b2" : "-", "b3" : "-", "b4" : "-", "b5" : "-",
                                            "b6" : "-", "b7" : "-", "b8" : "-", "b9" : "-", "b10" : "-",
                                            "b11" : "-", "b12" : "-"}
                dict_blancas_posteriori = self.posibles_movimientos(tablero, dict_blancas_posteriori, 'b')
                ordenacion_move_blancas = self.ordenar_movimientos(dict_blancas_posteriori, 'b')
                    
                for i in ordenacion_move_blancas:
                    tablero_aux = np.copy(tablero)
                    
                    tablero_aux = self.realizar_movimiento(tablero_aux, ordenacion_move_blancas[0][0])
                    valor = self.minimax(tablero_aux, profundidad - 1, a, b, 'N')
                    b = min(int(ordenacion_move_blancas[0][1]), int(valor[0][1]))
                    if b == ordenacion_move_blancas[0][1]:
                        best_move = ordenacion_move_blancas[0]
                    else:
                        best_move = valor 
                
        return best_move
    
    
    def ordenar_movimientos(self, diccionario, jugador):
        aux= {}
        lista = []
        if jugador == 'b':
            lista = ["b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9","b10", "b11", "b12"]
        else:
            lista = ["n1", "n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9","n10", "n11", "n12"]
        
        for ficha in lista:
            #value = diccionario.pop(ficha)
            if diccionario.get(ficha) != '-': #not empty
                aux.update(diccionario.pop(ficha))
        
        resultado = sorted(aux.items(), key=operator.itemgetter(1))
        resultado.reverse()
        return resultado
     
    
    def comprobar_movimiento(self, tablero, x, y, ficha):
        dict2 = {}
        
        #MOVIMIENTOS FICHAS BLANCAS
        if "b" in ficha:
            
            #COMER 3 FICHAS
            if x>=6 and x<=7:
                if y>=0 and y<=5:
                    #id1
                    if (("n" in tablero[x-1][y+1]) and tablero[x-2][y+2] == "-" and "n" in tablero[x-3][y+1] 
                    and tablero[x-4][y] == "-" and "n" in tablero[x-5][y+1] and tablero[x-6][y+2] == "-"):
                        dict2.update({(str(x+1)+str(y+1)+str(x-2+1)+str(y+2+1)+str(x-4+1)+str(y+1)+str(x-6+1)+str(y+2+1)) : 3 })
                if y>=2 and y<=7:
                    #id2
                    if (("n" in tablero[x-1][y-1]) and tablero[x-2][y-2] == "-" and "n" in tablero[x-3][y-1] 
                    and tablero[x-4][y] == "-" and "n" in tablero[x-5][y-1] and tablero[x-6][y-2] == "-"):
                        dict2.update({(str(x+1)+str(y+1)+str(x-2+1)+str(y-2+1)+str(x-4+1)+str(y+1)+str(x-6+1)+str(y-2+1)) : 3 })
                if y>=6 and y<=7:
                    #id3
                    if (("n" in tablero[x-1][y-1]) and tablero[x-2][y-2] == "-" and "n" in tablero[x-3][y-3] 
                    and tablero[x-4][y-4] == "-" and "n" in tablero[x-5][y-5] and tablero[x-6][y-6] == "-"):
                        dict2.update({(str(x+1)+str(y+1)+str(x-2+1)+str(y-2+1)+str(x-4+1)+str(y-4+1)+str(x-6+1)+str(y-6+1)) : 3 })
                if y>=0 and y <=1:
                    #id4
                    if (("n" in tablero[x-1][y+1]) and tablero[x-2][y+2] == "-" and "n" in tablero[x-3][y+3] 
                    and tablero[x-4][y+4] == "-" and "n" in tablero[x-5][y+5] and tablero[x-6][y+6] == "-"):
                        dict2.update({(str(x+1)+str(y+1)+str(x-2+1)+str(y+2+1)+str(x-4+1)+str(y+4+1)+str(x-6+1)+str(y+6+1)) : 3 })
                if y>=0 and y<=3:
                    #id5
                    if (("n" in tablero[x-1][y+1]) and tablero[x-2][y+2] == "-" and "n" in tablero[x-3][y+3] 
                    and tablero[x-4][y+4] == "-" and "n" in tablero[x-5][y+3] and tablero[x-6][y+2] == "-"):
                        dict2.update({(str(x+1)+str(y+1)+str(x-2+1)+str(y+2+1)+str(x-4+1)+str(y+4+1)+str(x-6+1)+str(y+2+1)) : 3 })
                if y>=4 and y<=7:
                    #id6
                    if (("n" in tablero[x-1][y-1]) and tablero[x-2][y-2] == "-" and "n" in tablero[x-3][y-3] 
                    and tablero[x-4][y-4] == "-" and "n" in tablero[x-5][y-3] and tablero[x-6][y-2] == "-"):
                        dict2.update({(str(x+1)+str(y+1)+str(x-2+1)+str(y-2+1)+str(x-4+1)+str(y-4+1)+str(x-6+1)+str(y-2+1)) : 3 })
                if y>=2 and y<=5:
                    #id7
                    if (("n" in tablero[x-1][y+1]) and tablero[x-2][y+2] == "-" and "n" in tablero[x-3][y+1] 
                    and tablero[x-4][y] == "-" and "n" in tablero[x-5][y-1] and tablero[x-6][y-2] == "-"):                     
                        dict2.update({(str(x+1)+str(y+1)+str(x-2+1)+str(y+2+1)+str(x-4+1)+str(y+1)+str(x-6+1)+str(y-2+1)) : 3 })
                    #id8
                    if (("n" in tablero[x-1][y-1]) and tablero[x-2][y-2] == "-" and "n" in tablero[x-3][y-1] 
                    and tablero[x-4][y] == "-" and "n" in tablero[x-5][y+1] and tablero[x-6][y+2] == "-"):
                        dict2.update({(str(x+1)+str(y+1)+str(x-2+1)+str(y-2+1)+str(x-4+1)+str(y+1)+str(x-6+1)+str(y+2+1)) : 3 })
            
            #COMER 2 FICHAS
            if x>=4 and x<=7:
                if y>=2 and y<=7:
                    #id9
                    if (("n" in tablero[x-1][y-1]) and tablero[x-2][y-2] == "-" and "n" in tablero[x-3][y-1] 
                    and tablero[x-4][y] == "-"):
                        dict2.update({(str(x+1)+str(y+1)+str(x-2+1)+str(y-2+1)+str(x-4+1)+str(y+1)) : 2 })
                if y>=0 and y<=5:
                    #id10
                    if (("n" in tablero[x-1][y+1]) and tablero[x-2][y+2] == "-" and "n" in tablero[x-3][y+1] 
                    and tablero[x-4][y] == "-"):
                        dict2.update({(str(x+1)+str(y+1)+str(x-2+1)+str(y+2+1)+str(x-4+1)+str(y+1)) : 2 })
                if y>=0 and y<=3:
                    #id11
                    if (("n" in tablero[x-1][y+1]) and tablero[x-2][y+2] == "-" and "n" in tablero[x-3][y+3] 
                    and tablero[x-4][y+4] == "-"):
                        dict2.update({(str(x+1)+str(y+1)+str(x-2+1)+str(y+2+1)+str(x-4+1)+str(y+4+1)) : 2 })
                if y>=4 and y<=7:
                    #id12
                    if (("n" in tablero[x-1][y-1]) and tablero[x-2][y-2] == "-" and "n" in tablero[x-3][y-3] 
                    and tablero[x-4][y-4] == "-"):
                        dict2.update({(str(x+1)+str(y+1)+str(x-2+1)+str(y-2+1)+str(x-4+1)+str(y-4+1)) : 2 })
            
            #COMER 1 FICHA
            if x>=2 and x<=7:
                if y>=0 and y<=5:
                    #id13
                    if (("n" in tablero[x-1][y+1]) and tablero[x-2][y+2] == "-"):
                        dict2.update({(str(x+1)+str(y+1)+str(x-2+1)+str(y+2+1)) : 1 })
                if y>=2 and y<=7:
                    #id14
                    if (("n" in tablero[x-1][y-1]) and tablero[x-2][y-2] == "-"):
                        dict2.update({(str(x+1)+str(y+1)+str(x-2+1)+str(y-2+1)) : 1 })
            
            #COMER 0 FICHAS
            if x>=1 and x<=7:
                if y>=0 and y<=6:
                    #id15
                    if tablero[x-1][y+1] == '-':
                        dict2.update({(str(x+1)+str(y+1)+str(x-1+1)+str(y+1+1)) : 0 })
                if y>=1 and y<=7:
                    #id16
                    if tablero[x-1][y-1] == '-':
                        dict2.update({(str(x+1)+str(y+1)+str(x-1+1)+str(y-1+1)) : 0 })
            
        #MOVIMIENTOS FICHAS NEGRAS            
        else:
            #COMER 3 FICHAS
            if x>=0 and x<=1: 
                #id1
                if y>=2 and y<=7:
                    if( "b" in tablero[x+1][y-1] and tablero[x+2][y-2] == '-' and "b" in tablero[x+3][y-1] 
                    and tablero[x+4][y] == '-' and "b" in tablero[x+5][y-1] and tablero[x+6][y-2] == '-'):
                        dict2.update({(str(x+1)+str(y+1)+str(x+2+1)+str(y-2+1)+str(x+4+1)+str(y+1)+str(x+6+1)+str(y-2+1)) : 3 })
                
                #id2
                if y>=0 and y<=5:
                    if( "b" in tablero[x+1][y+1] and tablero[x+2][y+2] == '-' and "b" in tablero[x+3][y+1] 
                    and tablero[x+4][y] == '-' and "b" in tablero[x+5][y+1] and tablero[x+6][y+2] == '-'):
                        dict2.update({(str(x+1)+str(y+1)+str(x+2+1)+str(y+2+1)+str(x+4+1)+str(y+1)+str(x+6+1)+str(y+2+1)) : 3 })
            
            
            
                #id3
                if y<=6 and y>=7:
                    if( "b" in tablero[x+1][y-1] and tablero[x+2][y-2] == '-' and "b" in tablero[x+3][y-3] 
                    and tablero[x+4][y-4] == '-' and "b" in tablero[x+5][y-5] and tablero[x+6][y-6] == '-'):
                        dict2.update({(str(x+1)+str(y+1)+str(x+2+1)+str(y-2+1)+str(x+4+1)+str(y-4+1)+str(x+6+1)+str(y-6+1)) : 3 })
            
                #id4
                if y<=0 and y>=1:
                    if( "b" in tablero[x+1][y+1] and tablero[x+2][y+2] == '-' and "b" in tablero[x+3][y+3] 
                    and tablero[x+4][y+4] == '-' and "b" in tablero[x+5][y+5] and tablero[x+6][y+6] == '-'):
                        dict2.update({(str(x+1)+str(y+1)+str(x+2+1)+str(y+2+1)+str(x+4+1)+str(y+4+1)+str(x+6+1)+str(y+6+1)) : 3 })
                    
                #id5
                if y<=0 and y>=1:
                    if( "b" in tablero[x+1][y-1] and tablero[x+2][y-2] == '-' and "b" in tablero[x+3][y-3] 
                    and tablero[x+4][y-4] == '-' and "b" in tablero[x+5][y+1] and tablero[x+6][y+2] == '-'):
                        dict2.update({(str(x+1)+str(y+1)+str(x+2+1)+str(y-2+1)+str(x+4+1)+str(y-4+1)+str(x+6+1)+str(y+2+1)) : 3 })
                #id6  
                if y<=0 and y>=3:
                    if( "b" in tablero[x+1][y+1] and tablero[x+2][y+2] == '-' and "b" in tablero[x+3][y+3] 
                    and tablero[x+4][y+4] == '-' and "b" in tablero[x+5][y+4] and tablero[x+6][y+2] == '-'):
                        dict2.update({(str(x+1)+str(y+1)+str(x+2+1)+str(y+2+1)+str(x+4+1)+str(y+4+1)+str(x+6+1)+str(y+2+1)) : 3 })
                    
                if y<=2 and y>=5:
                    #id7
                    if( "b" in tablero[x+1][y+1] and tablero[x+2][y+2] == '-' and "b" in tablero[x+3][y+1] 
                    and tablero[x+4][y] == '-' and "b" in tablero[x+5][y-1] and tablero[x+6][y-2] == '-'):
                        dict2.update({(str(x+1)+str(y+1)+str(x+2+1)+str(y+2+1)+str(x+4+1)+str(y+1)+str(x+6+1)+str(y-2+1)) : 3 })
                    
                    #id8
                    if( "b" in tablero[x+1][y-1] and tablero[x+2][y-2] == '-' and "b" in tablero[x+3][y-1] 
                    and tablero[x+4][y] == '-' and "b" in tablero[x+5][y+1] and tablero[x+6][y+2] == '-'):
                        dict2.update({(str(x+1)+str(y+1)+str(x+2+1)+str(y-2+1)+str(x+4+1)+str(y+1)+str(x+6+1)+str(y+2+1)) : 3 })
                    
            #COMER 2 FICHAS
            if x>=0 and x<=3: 
                #id9
                if y>=2 and y<=7:
                    if( "b" in tablero[x+1][y-1] and tablero[x+2][y-2] == '-' and "b" in tablero[x+3][y-1] 
                    and tablero[x+4][y] == '-'):
                        dict2.update({(str(x+1)+str(y+1)+str(x+2+1)+str(y-2+1)+str(x+4+1)+str(y+1)) : 2 })
                
                #id10
                if y>=0 and y<=5:
                    if( "b" in tablero[x+1][y+1] and tablero[x+2][y+2] == '-' and "b" in tablero[x+3][y+1] 
                    and tablero[x+4][y] == '-'):
                            dict2.update({(str(x+1)+str(y+1)+str(x+2+1)+str(y+2+1)+str(x+4+1)+str(y+1)) : 2 })
                #id11
                if y>=4 and y<=7:
                    if( "b" in tablero[x+1][y-1] and tablero[x+2][y-2] == '-' and "b" in tablero[x+3][y-3] 
                    and tablero[x+4][y-4] == '-'):
                        dict2.update({(str(x+1)+str(y+1)+str(x+2+1)+str(y-2+1)+str(x+4+1)+str(y-4+1)) : 2 })
            
                    
                #id12
                if y>=0 and y<=3:
                    if( "b" in tablero[x+1][y+1] and tablero[x+2][y+2] == '-' and "b" in tablero[x+3][y+3] 
                    and tablero[x+4][y+4] == '-'):
                        dict2.update({(str(x+1)+str(y+1)+str(x+2+1)+str(y+2+1)+str(x+4+1)+str(y+4+1)) : 2 })
                    
            #COMER 1 FICHAS    
            if x>=0 and x<=5:    
                #id13
                if y>=2 and y<=7:
                    if( "b" in tablero[x+1][y-1] and tablero[x+2][y-2] == '-'):
                        dict2.update({(str(x+1)+str(y+1)+str(x+2+1)+str(y-2+1)) : 1 })
                #id14
                if y>=0 and y<=5:
                     if( "b" in tablero[x+1][y+1] and tablero[x+2][y+2] == '-'):
                        dict2.update({(str(x+1)+str(y+1)+str(x+2+1)+str(y+2+1)) : 1 })
            #COMER 0 FICHAS
            if x>=0 and x<=6:
                #id15
                if y>=1 and y<=7:
                    if tablero[x+1][y-1] == '-':
                        dict2.update({(str(x+1)+str(y+1)+str(x+1+1)+str(y-1+1)) : 0 })
                #id16
                if y>=0 and y<=6:
                    if tablero[x+1][y+1] == '-':
                        dict2.update({(str(x+1)+str(y+1)+str(x+1+1)+str(y+1+1)) : 0 })
                
            
                        
        if len(dict2) == 0:
            dict2 = '-'
        return dict2
        
    def realizar_movimiento(self, tablero, movimiento):
    
        if len(movimiento) == 4:
            if(abs(int(movimiento[0]) - int(movimiento[2])) == 1 and abs(int(movimiento[1]) - int(movimiento[3])) == 1):
                aux = tablero[int(movimiento[0])-1][int(movimiento[1])-1]
                tablero[int(movimiento[0])-1][int(movimiento[1])-1] = '-'
                tablero[int(movimiento[2])-1][int(movimiento[3])-1] = aux
            else:
                aux = tablero[int(movimiento[0])-1][int(movimiento[1])-1]
                tablero[int(movimiento[0])-1][int(movimiento[1])-1] = '-'
                tablero[int(movimiento[2])-1][int(movimiento[3])-1] = aux
                x = abs((int(movimiento[0])+int(movimiento[2]))//2)
                y = abs((int(movimiento[1])+int(movimiento[3]))//2)
                tablero[x-1, y-1] = '-'
                
        elif len(movimiento) == 6:
            
            aux = tablero[int(movimiento[0])-1][int(movimiento[1])-1]
            tablero[int(movimiento[0])-1][int(movimiento[1])-1] = '-'
            tablero[int(movimiento[4])-1][int(movimiento[5])-1] = aux
            x = abs((int(movimiento[0])+int(movimiento[2]))//2)
            y = abs((int(movimiento[1])+int(movimiento[3]))//2)
            x1 = abs((int(movimiento[2])+int(movimiento[4]))//2)
            y1 = abs((int(movimiento[3])+int(movimiento[5]))//2)
            tablero[x-1, y-1] = '-'
            tablero[x1-1, y1-1] = '-'
            
        else:    
            aux = tablero[int(movimiento[0])-1][int(movimiento[1])-1]
            tablero[int(movimiento[0])-1][int(movimiento[1])-1] = '-'
            tablero[int(movimiento[6])-1][int(movimiento[7])-1] = aux
            
            x = abs((int(movimiento[0])+int(movimiento[2]))//2)
            y = abs((int(movimiento[1])+int(movimiento[3]))//2)
            x1 = abs((int(movimiento[2])+int(movimiento[4]))//2)
            y1 = abs((int(movimiento[3])+int(movimiento[5]))//2)
            x2 = abs((int(movimiento[4])+int(movimiento[6]))//2)
            y2 = abs((int(movimiento[5])+int(movimiento[7]))//2)
            tablero[x-1, y-1] = '-'
            tablero[x1-1, y1-1] = '-'
            tablero[x2-1, y2-1] = '-'
            
        return tablero
    
    def posibles_movimientos(self, tablero, dict_movimientos, jugador):
        
        lista = []
        if jugador == 'b':
            lista = ["b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9","b10", "b11", "b12"]
        else:
            lista = ["n1", "n2", "n3", "n4", "n5", "n6", "n7", "n8", "n9","n10", "n11", "n12"]
        
        for ficha in lista:
            if ficha in dict_movimientos.keys():
                for x in range(len(tablero)):
                    for y in range(len(tablero)):
                        dict2 = {}
                        if tablero[x][y] == ficha:
                            dict2 = self.comprobar_movimiento(tablero, x, y, ficha)
                            dict_movimientos.update({ficha: dict2})
                
        return dict_movimientos
    
    def fichas_comidas(self, move):
        
        if len(move) == 4:
            if(abs(int(move[0]) - int(move[2])) == 1 and abs(int(move[1]) - int(move[3])) == 1):
                fichas_comidas = ""
            else:
                x = abs((int(move[0])+int(move[2]))//2)
                y = abs((int(move[1])+int(move[3]))//2)
                string = str(x) + str(y)
                fichas_comidas = string
                
        elif len(move) == 6:
            x = abs((int(move[0])+int(move[2]))//2)
            y = abs((int(move[1])+int(move[3]))//2)
            x1 = abs((int(move[2])+int(move[4]))//2)
            y1 = abs((int(move[3])+int(move[5]))//2)
            string = str(x) + str(y) + str(x1) + str(y1)
            fichas_comidas = string 
            
        else:    
            x = abs((int(move[0])+int(move[2]))//2)
            y = abs((int(move[1])+int(move[3]))//2)
            x1 = abs((int(move[2])+int(move[4]))//2)
            y1 = abs((int(move[3])+int(move[5]))//2)
            x2 = abs((int(move[4])+int(move[6]))//2)
            y2 = abs((int(move[5])+int(move[7]))//2)
            string = str(x) + str(y) + str(x1) + str(y1) + str(x2) + str(y2)
            fichas_comidas = string
        
        return fichas_comidas
