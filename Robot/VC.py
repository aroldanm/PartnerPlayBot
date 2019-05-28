from PIL import Image
import numpy as np
import cv2

MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.15


# APLICACIoN:
# La imagen se transforma a un Core Image que es un modelo de datos para procesar
# imagenes en tiempo real. Haciendo uso de la libreria de vision se detectan cuantas 
from CameraController import CameraController

# caras hay en esa imagen y devuelve un valor.
class VCModule():

    def __init__(self):
        self.camera = CameraController()
        print("Creating histrogram...")
        self.valoresMinimos = 0
        self.valoresMaximos = 0
        
        
        #Rango de roojos en HSV
        self.rojo_bajos1 = np.array([150 ,65 ,75], dtype=np.uint8)
        self.rojo_altos1 = np.array([180, 255, 255], dtype=np.uint8)  
        self.rojo_bajos2 = np.array([240 ,65 ,75], dtype=np.uint8)
        self.rojo_altos2 = np.array([256, 255, 255], dtype=np.uint8)
        
        #Rango de verdes en HSV
        self.verdes_bajos = np.array([49 ,50 ,50], dtype=np.uint8)
        self.verdes_altos = np.array([107 ,255 ,255], dtype=np.uint8)
        
        #self.histograma=np.zeros((10, 256, 3))
        #Histograma y valores frontera inicializados
        
        self.llindar = 100
        self.getPhotosHistogram()
        self.crearHistograma()
    # Esta funcion devuelve una matriz con el tablero encontrado
    # Fases:
    #       1- Obtener foto
    #       2- Recortar y encuadrar la foto
    #       3- Comprobar que la foto contenga un tablero visible
    #       4- Transformacion de la foto a tablero en matriz
    def getTablero(self):
        imagenRuido = True
        while imagenRuido == True:
            imagen = self.getPhoto()
            imagen = self.cuadrarImagen(imagen, "histograma/lastPhoto.jpg")
            imagenRuido = self.comprobacionRuido(imagen)
        return self.deteccion_tablero(imagen)

#################################################################################
# 1- Obtener foto
#################################################################################

    def getPhotosHistogram(self):
        self.camera.getInitialPhotos()
        
    # Este metodo obtiene la foto del tablero
    def getPhoto(self):
        return self.camera.getPhoto()
        
#################################################################################
#2-  Recortar y encuadrar la foto
#################################################################################
    
    # Este metodo se encarga de coger una imagen, compararla con la muestra llamando
    # a alinear y guarda la foto nueva encuadrada y recortada
    def cuadrarImagen(self, im, outFilename):
        # Read reference image
        refFilename = "muestra.jpg"
        imReference = cv2.imread(refFilename, cv2.IMREAD_COLOR)
    
        # Registered image will be resotred in imReg.
        # The estimated homography will be stored in h.
        imReg, h = self.alignImages(im, imReference)
    
        # Write aligned image to disk.
        cv2.imwrite(outFilename, imReg)
        return imReg

    # Este metodo recibe dos imagenes, una muestra y la imagen a encuadrar, 
    # busca los puntos en comun entre ambas, elimina los puntos no comunes y
    # encuentra la homografia para hacer el transformado de la imagen final
    def alignImages(self, im1, im2):
        # Convert images to grayscale
        im1Gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        im2Gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    
        # Detect ORB features and compute descriptors.
        orb = cv2.ORB_create(MAX_FEATURES)
        keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
        keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)
        
        # Match features.
        matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        matches = matcher.match(descriptors1, descriptors2, None)
        
        # Sort matches by score
        matches.sort(key=lambda x: x.distance, reverse=False)
        
        # Remove not so good matches
        numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
        matches = matches[:numGoodMatches]
        
        # Draw top matches
        imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
        cv2.imwrite("histograma/matches.jpg", imMatches)
        
        # Extract location of good matches
        points1 = np.zeros((len(matches), 2), dtype=np.float32)
        points2 = np.zeros((len(matches), 2), dtype=np.float32)
        
        for i, match in enumerate(matches):
            points1[i, :] = keypoints1[match.queryIdx].pt
            points2[i, :] = keypoints2[match.trainIdx].pt
        
        # Find homography
        h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

        # Use homography
        height, width, channels = im2.shape
        im1Reg = cv2.warpPerspective(im1, h, (width, height))

        return im1Reg, h

#################################################################################
# 3- Comprobar que la foto contenga un tablero visible
#################################################################################

    # Este metodo se encarga de crear un histograma a partir de N imagenes el cual
    # servira para obtener los valores frontera.
    def crearHistograma(self):
        print("please wait during calibration...")
        
        count = self.camera.num_histo_photos
        histograma = np.zeros((count, 256 ,3))
        for z in range(count):
            porciento = int((z/(count-1))*100)
            print(str(porciento)+"%")
            contador = 0
            imgName = "histograma/" + str(z) + ".jpg"
            img  = cv2.imread(imgName)
            img = self.cuadrarImagen(img, imgName)
            color = ('b' ,'g' ,'r')
            for i, c in enumerate(color):
                hist = cv2.calcHist([img], [i], None, [256], [0, 256])
                for j in range(256):
                    histograma[z][j][contador] = hist[j][0]
                contador += 1
                
        self.valoresMinimos = histograma.min(axis=0)
        self.valoresMaximos = histograma.max(axis=0)

        
    # Los valores frontera se utilizaran en este metodo para determinar si la
    # foto obtenida es valida. Sera valida cuando el histograma de la nueva 
    # imagen este comprendida entre los valores frontera.
    def comprobacionRuido(self, image):
        #calculo del nuevo hisograma
        histograma = np.zeros((256 ,3))
        color = ('b' ,'g' ,'r')
        contador = 0
        for i, c in enumerate(color):
            hist = cv2.calcHist([image], [i], None, [256], [0, 256])
            for j in range(256):
                histograma[j][contador] = hist[j][0]
            contador += 1
        
        #calculo del numero de diferencias
        return self.comprobarDiferencias(histograma) > 200
    
    #Metodo para contabilizar el numero de valores fuera de los valores frontera
    def comprobarDiferencias(self, h):
        final = np.zeros((256 ,3))
        for j in range(3):
            for i in range(256):
                
                if ((h[i][j] >self.valoresMaximos[i][j] + self.llindar)
                    or (h[i][j] < self.valoresMinimos[i][j] - self.llindar)):
                    final[i][j] = 1
        return final.sum()

#################################################################################
# 4- Transformacion de la foto a tablero en matriz
#################################################################################
        
    # Metodo para crear una mascara que detecte el color rojo
    def detector_rojo(self, hsv):
        mascara_rojo1 = cv2.inRange(hsv, self.rojo_bajos1, self.rojo_altos1)
        mascara_rojo2 = cv2.inRange(hsv, self.rojo_bajos2, self.rojo_altos2)
        return cv2.add(mascara_rojo1, mascara_rojo2)
    
    def detector_verde(self, hsv):
        mascara_verde = cv2.inRange(hsv, self.verdes_bajos, self.verdes_altos)
        return cv2.add(mascara_verde, mascara_verde)
    
    # Metdo para obtener la imagen en HSV
    def RGBtoHSV(self, imagen):
        return cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    
    # Este metodo transforma la imagen a matriz 
    # Fases:
    #       1- Obtener la imagen en HSV
    #       2- Crear la mascara verde y roja para la deteccion de colores
    #       3- Division de las mascaras en porciones segun el tablero
    #       4- Por cada porcion miramos la cantidad de color detectado y si es 
    #       mayor a la tolerancia establecida. se considera que hay una ficha.
    #       5- Transformar las fichas detectadas a matriz de caracteres    
    def deteccion_tablero(self, imagen):
        tablero = np.zeros((8,8), dtype=(np.unicode_ , 2))
        
        imagen = self.RGBtoHSV(imagen)
        mask_verde = self.detector_verde(imagen)
        mask_rojo = self.detector_rojo(imagen)
            
        valor_blancas = False
        valor_negras = False
        contador_n = 1
        contador_b = 1
        pos_x = 0
            
        suma_x = int(imagen.shape[0]/ 8)
        suma_y = int(imagen.shape[1]/ 8)
            
        for i in range(8):
            pos_y = 0
            for j in range(8):
                aux_negras = mask_verde[pos_x:pos_x + suma_x, pos_y:pos_y + suma_y]
                aux_blancas = mask_rojo[pos_x:pos_x + suma_x, pos_y:pos_y + suma_y]
                valor_negras = self.encontrarFichaEnCasilla(aux_negras)
                valor_blancas = self.encontrarFichaEnCasilla(aux_blancas)
                if (valor_negras == True):
                    numero = 'n' + str(contador_n)
                    contador_n = contador_n + 1
                    tablero[i][j] = numero
                elif (valor_blancas == True):
                    numero_b = 'b' + str(contador_b)
                    contador_b = contador_b + 1
                    tablero[i][j] = numero_b
                else:
                    tablero[i][j] = '-'
                pos_y = pos_y + suma_y
            pos_x = pos_x + suma_x
        print(tablero)
        return tablero

    # Metodo que comprueba si hay pieza en una casilla
    def encontrarFichaEnCasilla(self, block):
        valor = False
        contador = 0
        total_pixeles = block.shape[0] * block.shape[1]
        contador = np.count_nonzero(block)
        if contador / total_pixeles > 0.075:
            valor = True
        return valor
    

    
    

