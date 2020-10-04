#!/usr/bin/python
from clases.deteccion_facial import Facial_detection
from imutils.video import VideoStream
import time
from operaciones.operaciones_math import *

print("\033[1;35m"+"[INFO] Tesis de interacción social mediante vision artificial"+'\033[0;m')
time.sleep(2.0)
print("[INFO] Inicializando cámara...")

try:

    Video = VideoStream(0).start()
    time.sleep(2.0)
    Inter = Facial_detection(Video)
    Inter.Ventana.mainloop()


except Exception as e:
    print("\033[1;31m"+"[ERROR] Error al iniciar la camara..." +'\033[0;m')
    print(e)
