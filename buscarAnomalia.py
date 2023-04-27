# **YOLOV8 Deteccion de iris y anomalia**

"""## Carga Yolo V8"""
from ultralytics import YOLO
from IPython.display import Image
import os
import shutil
import cv2

class DeteccionIrirsAnomalias:
	# https://www.geeksforgeeks.org/python-move-and-overwrite-files-and-folders/

	
		

	"""##  Elimina directorios de trabajo antes de predecir"""

	def limpiarDirectorios(self):
		
		os.chdir('C:/Proyecto_Iris/Deteccion')

		# elimina runs
		path = 'C:/Proyecto_Iris/Deteccion/runs' 

		# Controla si el directorio existe
		if os.path.isdir(path):
				shutil.rmtree(path)
			
		# elimina prediccion de anomalias
		path = 'C:/Proyecto_iris/Deteccion/iris/detect' 

		# Controla si el directorio existe
		if os.path.isdir(path):
				shutil.rmtree(path)
		
		# elimina prediccion de anomalias
		path = 'C:/Proyecto_iris/Deteccion/anomalias/detect' 

		# Controla si el directorio existe
		if os.path.isdir(path):
				shutil.rmtree(path)
		##########################
	

	"""###  Pasa a escala de grises las fotos a color"""
	def convertirImagenAGris(self, ruta_imagen_para_analizar):
		
		img = cv2.imread(ruta_imagen_para_analizar)

		gris = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY) # imagen gris
		#cv2.imshow(gris)
		cv2.imwrite('C:/Proyecto_iris/deteccion/imagenes/gimagen.jpg',gris)
	########################################################
	

	"""## Predice iris con una imagen"""
	def detectarIris(self) :
		#yolo task=detect mode=predict model='C:/Proyecto_iris/Deteccion/iris/weights/pupila_iris_100_epochs.pt' source='C:/Proyecto_iris/Deteccion/imagenes/gimagen.jpg' conf=0.8 save_crop=True save=True
		model = YOLO('C:/Proyecto_Iris/Deteccion/iris/weights/pupila_iris_100_epochs.pt')
		img = cv2.imread('C:/Proyecto_Iris/Deteccion/imagenes/gimagen.jpg')
		results = model.predict(source=img, conf=0.8, save=True, save_crop=True)
		"""## Muevo los directorios con los resultados de la prediccion"""

		original = r'C:/Proyecto_iris/Deteccion/runs/detect'
		target = r'C:/Proyecto_iris/Deteccion/iris/detect'

		# Controla si el directorio existe
		if os.path.isdir(target):
				shutil.rmtree(target)

		shutil.move(original, target)
	###############################################################

	### Predice anomalias en base al crop del iris
	#El formato que devuelve el txt es: 
	#0 para el iris 1 para la pupila, 
	#x sup izq, 
	#y sup izq, 
	#ancho, 
	#alto.
	def detectarAnomalia (self):
		model = YOLO('C:/Proyecto_Iris/Deteccion/anomalias/weights/anomalias_iris_epochs=100_imgsz=800_batch=10_Grayscale.pt')
		img = cv2.imread('C:/Proyecto_Iris/Deteccion/iris/detect/predict/crops/iris/image0.jpg')
		results = model.predict(source=img, conf=0.8, save=True, save_txt=True, show_labels=False ,imgsz=800)
		"""## Muevo los directorios con los resultados de la prediccion"""

		original = r'C:/Proyecto_iris/Deteccion/runs/detect'
		target = r'C:/Proyecto_iris/Deteccion/anomalias/detect'

		# Controla si el directorio existe
		if os.path.isdir(target):
				shutil.rmtree(target)

		shutil.move(original, target)
		return results
		

	