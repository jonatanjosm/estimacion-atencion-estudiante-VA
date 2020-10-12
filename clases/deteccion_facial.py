#!/usr/bin/env python
# -*-coding: utf8-*-
from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import datetime
import imutils
import cv2
import os
import dlib
import time
from imutils import face_utils
from scipy.spatial import distance as dist
import numpy as np
from subprocess import call
from tkinter import messagebox
from ffpyplayer.player import MediaPlayer
from imutils.video import FileVideoStream
from moviepy.editor import *
import pygame
import easygui as eg
import xlwt

class Facial_detection:

	def __init__(self,Video):


		self.Video = Video
		self.frame = None
		self.thread = None
		self.stopEvent = None
		self.loop = False

		self.Ventana = tki.Tk()
		self.panel = None
		self.Ventana.geometry('1400x800')
		self.Ventana.configure(background='#C1BCFA')

		self.Ear = tki.StringVar()
		self.Mar = tki.StringVar()
		self.Estado = tki.StringVar()
		self.Facultad = tki.StringVar()
		self.Tema = tki.StringVar()
		self.Empieza = 0
		self.next = 0

		self.salir = 0

		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.videoLoop, args=())
		self.thread.start()



		self.Ventana.title("TESIS SISTEMA INTERACTIVO")
		self.Ventana.protocol("WM_DELETE_WINDOW", self.Close)

		self.Inge = tki.Button(self.Ventana, text="INGENIERIAS", font=("Noto Sans Mono CJK TC Bold","15"),
			command=self.Ingeni, state='normal',borderwidth='10p')
		self.Inge.place(x=930, y=400)

		self.Arqui = tki.Button(self.Ventana, text="ARQUITECTURA", font=("Noto Sans Mono CJK TC Bold","15"),
			command=self.Arquitec, state='normal',borderwidth='10p')
		self.Arqui.place(x=1120, y=400)

		self.SAL= tki.Button(self.Ventana, text="SALIR", font=("Noto Sans Mono CJK TC Bold","15"),
			command=self.sal, state='normal',borderwidth='10p').place(x=1050, y=600)

		self.NEXT= tki.Button(self.Ventana, text="SIGUIENTE", font=("Noto Sans Mono CJK TC Bold","15"),
			command=self.siguiente, state='normal',borderwidth='10p')
		self.NEXT.place(x=1030, y=500)

		self.Titulo = tki.Label(self.Ventana, text="TESIS SISTEMA INTERACTIVO MEDIANTE VISION ARTIFICIAL\nPARA FINES DE PERCEPCION\nEnder Ortega",
			font=("Noto Sans Mono CJK JP Bold","15"),relief="groove", borderwidth=8,background="#66ccff")
		self.Titulo.place(x=300, y=3)


		self.FAC1 = tki.Label(self.Ventana, text="Facultad: ",foreground="black",
			font=("URW Bookman L","15"),relief="sunken", borderwidth=3)
		self.FAC1.place(x=1000,y=200)

		self.TEM1 = tki.Label(self.Ventana, text="Tema:      ",foreground="black",
			font=("URW Bookman L","15"),relief="sunken", borderwidth=3)
		self.TEM1.place(x=1000,y=240)

		self.EARL1 = tki.Label(self.Ventana, text="Ojos:       ",foreground="black",
			font=("URW Bookman L","15"),relief="sunken", borderwidth=3)
		self.EARL1.place(x=1000,y=320)

		self.MARL1 = tki.Label(self.Ventana, text="Boca:       ",foreground="black",
			font=("URW Bookman L","15"),relief="sunken", borderwidth=3)
		self.MARL1.place(x=1000,y=360)


		self.FACT = tki.Label(self.Ventana, textvariable=self.Facultad,foreground="black",
			background="white",font=("URW Bookman L","15"),relief="sunken", borderwidth=3)
		self.FACT.place(x=1100,y=200)

		self.TEM = tki.Label(self.Ventana, textvariable=self.Tema,foreground="black",
			background="white",font=("URW Bookman L","15"),relief="sunken", borderwidth=3)
		self.TEM.place(x=1100,y=240)

		self.EARL = tki.Label(self.Ventana, textvariable=self.Ear,foreground="black",
			background="white",font=("URW Bookman L","15"),relief="sunken", borderwidth=3)
		self.EARL.place(x=1100,y=320)

		self.MARL = tki.Label(self.Ventana, textvariable=self.Mar,foreground="black",
			background="white",font=("URW Bookman L","15"),relief="sunken", borderwidth=3)
		self.MARL.place(x=1100,y=360)

######################################################################################################
##########################################################################################################
	def Exportar(self, nombre, id, Lista_boca, Lista_ojos, Lista_tema, Lista_estado, Lista_tiempo, porcentaje, porce_2, promEarAbi, promEarCe, promMarCe, promMarAbi, Umbral_ojos, Umbral_boca,t_distraccion):

		libro = xlwt.Workbook()
		libro1 = libro.add_sheet("Prueba")


		Ojos_ab = "Valor de Ojos ABIERTOS: "+ str(promEarAbi)
		Ojos_ce = "Valor de Ojos CERRADOS: "+ str(promEarCe)

		Boca_ab = "Valor de Boca ABIERTA: "+ str(promMarAbi)
		Boca_ce = "Valor de Boca CERRADA: "+ str(promMarCe)

		Umbral_o = "Umbral para OJOS: "+ str(Umbral_ojos)
		Umbral_b = "Umbral para BOCA: "+ str(Umbral_boca)

		Porcen_dis = "Porcentaje de DISTRACCION: "+str(porcentaje)+"%"
		Porcen_aten = "Porcentaje de ATENCION: "+str(porce_2)+"%"

		t_distraccion = round(t_distraccion,4)
		self.t_global = round(self.t_global,4)

		T_dist = "Tiempo de Distraccion: "+ str(t_distraccion) + "seg"
		T_total = "Tiempo Total: "+ str(self.t_global) + "seg"

		N = "Nombre: "+ nombre
		I = "Identificacion: "+ id
		F = "Facultad: "+ self.Facultad_lista

		libro1.write(0,0,N)
		libro1.write(1,0,I)
		libro1.write(2,0,F)
		libro1.write(3,0,Ojos_ab)
		libro1.write(4,0,Ojos_ce)
		libro1.write(5,0,Umbral_o)
		libro1.write(6,0,Boca_ab)
		libro1.write(7,0,Boca_ce)
		libro1.write(8,0,Umbral_b)

		libro1.write(9,0,T_total)
		libro1.write(10,0,T_dist)
		libro1.write(11,0,Porcen_dis)
		libro1.write(12,0,Porcen_aten)

		libro1.write(0,1,"TIEMPO (Segundos)")
		libro1.write(0,2,"OJOS")
		libro1.write(0,3,"BOCA")
		libro1.write(0,4,"TEMA")
		libro1.write(0,5,"ESTADO")

		i=1
		for n in Lista_tiempo:
			libro1.write(i,1,n)
			i += 1
		i=1
		for n in Lista_ojos:
			libro1.write(i,2,n)
			i += 1
		i=1
		for n in Lista_boca:
			libro1.write(i,3,n)
			i += 1
		i=1
		for n in Lista_tema:
			libro1.write(i,4,n)
			i += 1
		i=1
		for n in Lista_estado:
			libro1.write(i,5,n)
			i += 1

		N2 = nombre.replace(" ","-")
		Fecha = time.strftime("%d-%m-%y %H:%M:%S")
		path = "Exportes/Exporte-" + N2 + " " + Fecha + ".xls"
		print("[INFO] Exporte generado: "+path)
		libro.save(path)

######################################################################################################
##########################################################################################################
	def sal(self):
		self.salir = 1
######################################################################################################
##########################################################################################################
	def siguiente(self):
		self.next = 1
####################################################################################################
#####################################################################################################
	def Close(self):
		print("\033[1;36m"+"[INFO] Cerrando..."+'\033[0;m')
		self.stopEvent.set()
		self.Video.stop()
		self.loop = True
		self.Ventana.quit()

####################################################################################################
#####################################################################################################
	def Ingeni(self):

		self.Empieza = 1
		self.Facul = 1
		print("\033[1;33m"+"[INFO] Sistema interactivo ACTIVADO..."+'\033[0;m')
		print("\033[1;36m"+"[INFO] Facultad de Ingenieria seleccionada..."+'\033[0;m')
		self.Estado.set("CONCENTRADO")
		self.Pro = 1
		Cap = 1
		self.video_clase = self.Video_Path(self.Facul,self.Pro,Cap)

#####################################################################################################
###################################################################################################
	def Arquitec(self):

		self.Empieza = 1
		self.Facul = 2
		print("\033[1;33m"+"[INFO] Sistema interactivo ACTIVADO..."+'\033[0;m')
		print("\033[1;36m"+"[INFO] Facultad de Arquitectura seleccionada..."+'\033[0;m')
		self.Estado.set("CONCENTRADO")
		self.Pro = 1
		Cap = 1
		self.video_clase = self.Video_Path(self.Facul,self.Pro,Cap)


#####################################################################################################
###################################################################################################
	def Imprimir(self):
		if self.Facul == 1:
			self.Facultad_lista = "Ingenieria"
			self.Facultad.set("INGENIERIAS")
			if self.Pro == 1:
				self.Tema_lista = "Mecatronica"
				self.Tema.set("Mecatrónica")
			elif self.Pro == 2:
				self.Tema_lista = "Mecanica"
				self.Tema.set("Mecanica")
			elif self.Pro == 3:
				self.Tema_lista = "Electronica"
				self.Tema.set("Electrica")
			elif self.Pro == 4:
				self.Tema_lista = "Industrial"
				self.Tema.set("Industrial")

		elif self.Facul == 2:
			self.Facultad_lista = "Arquitectura"
			self.Facultad.set("ARQUITECTURA")
			if self.Pro == 1:
				self.Tema_lista = "Arquitectonica"
				self.Tema.set("Arquitectonica")
			elif self.Pro == 2:
				self.Tema_lista = "Arq. Contemporanea"
				self.Tema.set("Arq. Contemporanea")
			elif self.Pro == 3:
				self.Tema_lista = "Geometria"
				self.Tema.set("Geometria")
			elif self.Pro == 4:
				self.Tema_lista = "Liberalismo"
				self.Tema.set("Liberalismo")

#####################################################################################################
###################################################################################################
	def eye_aspect_ratio(self,eyeR,eyeL):

		A = dist.euclidean(eyeR[1], eyeR[5])
		B = dist.euclidean(eyeR[2], eyeR[4])

		C = dist.euclidean(eyeR[0], eyeR[3])

		D = (A + B) / (2.0 * C)

		A = dist.euclidean(eyeL[1], eyeL[5])
		B = dist.euclidean(eyeL[2], eyeL[4])

		C = dist.euclidean(eyeL[0], eyeL[3])

		E = (A + B) / (2.0 * C)

		F = (D + E) / 2

		return F

#####################################################################################################
###################################################################################################

	def mouth_aspect_ratio(self,mouth):

		A = dist.euclidean(mouth[13], mouth[19])
		B = dist.euclidean(mouth[14], mouth[18])
		C = dist.euclidean(mouth[15], mouth[17])

		D = dist.euclidean(mouth[12], mouth[16])

		mar = (A + B + C) / (3.0 * D)

		return mar