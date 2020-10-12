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

        def videoLoop(self):

		try:

			EARG = 0
			MARG = 0

			print("[INFO] Cargando paquete predictor...")
			detector = dlib.get_frontal_face_detector()
			predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

			time.sleep(1.0)

			(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
			(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
			(mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

			#Variables auxiliares
			cont = 0
			contaux = 0
			SumaE = 0
			contp = 0
			i = 0
			contM = 0
			contMAu = 0
			conpat = 1

			#Variables para tiempos
			t_ojos_cerrados = 0
			t_ini_ojos_cerrados = 0
			con_t_ojos = 0
			con_gene = 0

			contador_general_distraccion = 0

			t_boca_abierta = 0
			t_ini_boca_abierta = 0
			con_t_boca = 0

			t_distraccion = 0
			self.t_global = 0

			self.Facul = 0
			self.Pro = 0
			#Variables para Video

			Cont_video = 1

			self.Estado.set("ESPERANDO...")
			self.Facultad.set("ESPERANDO...")
			self.Tema.set("ESPERANDO...")

			nombre = eg.enterbox(msg='Ingrese su nombre COMPLETO:',
                                title='Nombre del Usuario',
                                strip=True,
                                image=None)
			id = eg.enterbox(msg='Ingrese su numero de Identificacion:',
                                title='Identificacion del Usuario',
                                strip=True,
                                image=None)

			Lista_tiempo = []
			Lista_boca = []
			Lista_ojos = []
			Lista_tema = []
			Lista_estado = []

			self.Estado_lista = "CONCENTRADO"


			#Bucle principal para la obtencion de datos
			messagebox.showinfo('Aviso', 'Calibracion de valores...')
			while not self.stopEvent.is_set() and self.salir ==  0:

				self.Imprimir()

				if contaux == 0:
					print("\033[1;36m"+"[INFO] Calibrando data para ojos abiertos..."+'\033[0;m')
					messagebox.showinfo('Aviso', 'Por favor, mantenga los ojos ABIERTOS durante 3 segundos')
					t_inicial = time.monotonic()

				elif contaux == 1:
					print("\033[1;36m"+"[INFO] Calibrando data para ojos cerrados..."+'\033[0;m')
					messagebox.showinfo('Aviso', 'Por favor, mantenga los ojos CERRADOS durante 3 segundos')
					t_inicial = time.monotonic()

				elif contaux == 2:
					print("\033[1;36m"+"[INFO] Calibrando data para boca cerrada..."+'\033[0;m')
					messagebox.showinfo('Aviso', 'Por favor, mantenga la boca CERRADA durante 3 segundos')
					t_inicial = time.monotonic()

				elif contaux == 3:
					print("\033[1;36m"+"[INFO] Calibrando data para boca abierta..."+'\033[0;m')
					messagebox.showinfo('Aviso', 'Por favor, mantenga la boca ABIERTA durante 3 segundos')
					t_inicial = time.monotonic()

				self.frame = self.Video.read()
				self.frame = imutils.resize(self.frame, width=830)


				gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
				rects = detector(gray, 0)


				for rect in rects:

					shape = predictor(gray, rect)
					shape = face_utils.shape_to_np(shape)

					leftEye = shape[lStart:lEnd]
					rightEye = shape[rStart:rEnd]

					Mouth = shape[mStart:mEnd]

					EARG = round(self.eye_aspect_ratio(rightEye, leftEye),4)
					MARG = round(self.mouth_aspect_ratio(Mouth),4)

					if self.Empieza < 1:

						self.Ear.set(str(round(EARG,3)))
						self.Mar.set(str(round(MARG,3)))
					else:
						self.Ear.set("")
						self.Mar.set("")

################################################################################################
				if cont == 4 and self.Empieza == 1:
					if con_gene == 0:
						self.t_global = time.monotonic()
						con_gene = 1

					self.Inge.place_forget()

					self.Arqui.place_forget()
					self.EARL.place_forget()
					self.EARL1.place_forget()
					self.MARL.place_forget()
					self.MARL1.place_forget()
					self.Titulo.place_forget()

					##############################################
					##############################################
					if EARG <= Umbral_ojos or MARG >= Umbral_boca:

						self.Estado_lista = "POCA ATENCIÓN"
						t_boca_abierta = time.monotonic() - t_ini_boca_abierta
						t_ojos_cerrados = time.monotonic() - t_ini_ojos_cerrados


						if t_boca_abierta >= t_ojos_cerrados:
							t_distraccion = t_boca_abierta
						else:
							t_distraccion = t_ojos_cerrados

					else:
						self.Estado_lista = "CONCENTRADO"
					##############################################
					##############################################

					if EARG <= Umbral_ojos and con_t_ojos == 0:

						t_ini_ojos_cerrados = time.monotonic()
						con_t_ojos = 1

						#if (time.monotonic() - t_ini_ojos_cerrados) >=2:
					#		self.Estado_lista = "POCA ATENCIÓN"

					elif EARG > Umbral_ojos and con_t_ojos == 1:
						t_ojos_cerrados = time.monotonic() - t_ini_ojos_cerrados

						con_t_ojos = 0

						if t_ojos_cerrados >= 3:

							contador_general_distraccion += 1
							#self.Estado_lista = "CONCENTRADO"
						t_ojos_cerrados = 0;

					if MARG >= Umbral_boca and con_t_boca == 0:

						t_ini_boca_abierta = time.monotonic()
						con_t_boca = 1

						#if time.monotonic() - t_ini_boca_abierta >=2:
						#	self.Estado_lista = "POCA ATENCIÓN"

					elif MARG < Umbral_boca and con_t_boca == 1:

						t_boca_abierta = time.monotonic() - t_ini_boca_abierta
						con_t_boca = 0

						if t_boca_abierta > 3:
							t_distraccion = t_distraccion + t_boca_abierta
							contador_general_distraccion += 1
							#self.Estado_lista = "CONCENTRADO"

					#########################################################
					self.Imprimir()
					t_actual_lista = round((time.monotonic() - self.t_global),4)

					Lista_tiempo.append(t_actual_lista)
					Lista_boca.append(MARG)
					Lista_ojos.append(EARG)
					Lista_tema.append(self.Tema_lista)
					Lista_estado.append(self.Estado_lista)

					###########################################################
					###########################################################
					if self.next==1:
						self.next = 0
						self.Estado_lista = "CAMBIO DE TEMA"

						t_actual_lista = round((time.monotonic() - self.t_global),4)

						Lista_tiempo.append(t_actual_lista)
						Lista_boca.append(MARG)
						Lista_ojos.append(EARG)
						Lista_tema.append(self.Tema_lista)
						Lista_estado.append(self.Estado_lista)


						if Cont_video < 4:
							self.Pro+=1
							Cap = 1
							self.video_clase.release()
							self.video_clase = self.Video_Path(self.Facul, self.Pro, Cap)
							grabbed, frame=self.video_clase.read()
							frame = imutils.resize(frame, width=950)
							contador_general_distraccion = 0
							Cont_video+=1
						else:
							messagebox.showinfo('Aviso', 'Fin de la sesion.')
							break;

					if contador_general_distraccion >= 7:
						self.Estado_lista = "UMBRAL DISTRACCIONES SUPERADO"
						Op = messagebox.askyesno("Aviso!","Se detecto poco interes, ¿Desea cambiar de tema?")
						if Op:
							if Cont_video < 4:
								self.Pro+=1
								Cap = 1
								self.video_clase.release()
								self.video_clase = self.Video_Path(self.Facul, self.Pro, Cap)
								grabbed, frame=self.video_clase.read()
								frame = imutils.resize(frame, width=950)
								contador_general_distraccion = 0
								Cont_video+=1
							else:
								messagebox.showinfo('Aviso', 'Fin de la sesion.')
								break;

						else:
							contador_general_distraccion = 0



					grabbed, frame=self.video_clase.read()
					self.panel.place(x=10, y=10)
					frame = imutils.resize(frame, width=950)
					if not grabbed:

						if Cont_video < 4:
							if contador_general_distraccion >= 4:
								self.Pro+=1
								Cap = 1
							else:
								Cap+=1

							self.video_clase.release()
							self.video_clase = self.Video_Path(self.Facul, self.Pro, Cap)
							grabbed, frame=self.video_clase.read()
							frame = imutils.resize(frame, width=830)
							contador_general_distraccion = 0
							Cont_video+=1
						else:
							messagebox.showinfo('Aviso', 'Fin de la sesion.')
							break;

					else:

						#image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
						image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
						image = Image.fromarray(image)
						image = ImageTk.PhotoImage(image)
#######################################################################################################
				else:
					for (x, y) in shape:
						cv2.circle(self.frame, (x, y), 1, (0, 0, 255), -1)

					image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
					image = Image.fromarray(image)
					image = ImageTk.PhotoImage(image)


				if self.panel is None:
					self.panel = tki.Label(image=image,relief="sunken", borderwidth=3)
					self.panel.image = image
					self.panel.place(x=80, y=115)

				else:
					self.panel.configure(image=image,relief="sunken", borderwidth=3)
					self.panel.image = image

				t_act = time.monotonic() - t_inicial
#########################################################################################################
				#Etapa inicial para determinar los valores para ojos y boca
				#Ojos Abiertos
				if cont == 0:

					contaux = -1
					SumaE = SumaE + EARG
					contp = contp + 1


					if t_act >= 3:

						promEarAbi = SumaE / contp
						print("[INFO] Valor de Eye Aspect Ratio (EAR) para ojos abiertos: ",promEarAbi)
						cont = 1
						contaux = 1
						contp = 0
						SumaE = 0

				#Ojos Cerrados
				elif cont == 1:

					contaux = -1
					SumaE = SumaE + EARG
					contp = contp + 1

					if t_act >= 3:

						promEarCe = SumaE / contp
						print("[INFO] Valor de Eye Aspect Ratio (EAR) para ojos cerrados: ",promEarCe)
						cont = 2
						contaux = 2
						contp = 0
						SumaE = 0

				


		except RuntimeError:
			print("\033[1;31m"+"[ERROR] Error en RunTime " +'\033[0;m')

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

#####################################################################################################
###################################################################################################
	def Video_Path(self,Facul,Pro,Cap):

		Path = "Facul_" + str(Facul) + "_Pro_" + str(Pro) + "_Cap_" + str(Cap) + ".mp4"
		video_clase=cv2.VideoCapture(Path)
		return video_clase