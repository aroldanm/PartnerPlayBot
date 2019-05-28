import cv2
import picamera
from time import sleep

class CameraController():
    count = 0
    num_histo_photos = 10
    
    def __init__(self):
        print("init CameraController")
        self.camera = picamera.PiCamera()
    
    def getPhoto(self):
        name = "temporal/photo.jpg"
        #camera.start_preview()
        self.camera.capture(name)
        #camera.stop_preview()
        return cv2.imread(name)
    
    def getInitialPhotos(self):
        #Cambiar a 25
        for i in range(self.num_histo_photos):
            #camera.start_preview()
            self.camera.capture("histograma/" + str(i) + ".jpg")
            sleep(0.5)
        #self.camera.close()

