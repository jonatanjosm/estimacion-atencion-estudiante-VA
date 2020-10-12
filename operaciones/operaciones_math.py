from scipy.spatial import distance as dist
import numpy as np
from operaciones.operaciones_math import *


class eye_aspect_ratio:
    def __init__(self,eyeR,eyeL):
        A = dist.euclidean(eyeR[1], eyeR[5])
        B = dist.euclidean(eyeR[2], eyeR[4])

        C = dist.euclidean(eyeR[0], eyeR[3])

        D = (A + B) / (2.0 * C)

        A = dist.euclidean(eyeL[1], eyeL[5])
        B = dist.euclidean(eyeL[2], eyeL[4])

        C = dist.euclidean(eyeL[0], eyeL[3])

        E = (A + B) / (2.0 * C)

        global EARG

        EARG = (D + E) / 2
