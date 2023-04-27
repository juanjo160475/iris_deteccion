from buscarAnomalia import DeteccionIrirsAnomalias
import firebase_admin
from firebase_admin import credentials, firestore
import threading
import urllib.request
import os
import pandas as pd


cred = credentials.Certificate("deteccion\clave.json")
firebase_admin.initialize_app(cred)
db= firestore.client()

ruta_archivo_resultado = r'C:\proyecto_iris\deteccion\anomalias\detect\predict\labels\image0.txt'



def descargarImagen (url,ruta_archivo , nombre_archivo):
    ruta_completa= ruta_archivo + nombre_archivo + '.jpg'
    urllib.request.urlretrieve(url,ruta_completa)

#url='https://firebasestorage.googleapis.com/v0/b/proyecto-iris-723c2.appspot.com/o/fotos%2Fojos_260.jpg?alt=media&token=3e79645b-bdef-461f-8aef-91cf11bd5ebc'
#ruta='firebase-conexion\imagen'
#nombre = '\ojo'

def detectar_anomalia (ruta):

    iA= DeteccionIrirsAnomalias()
    iA.limpiarDirectorios()
    iA.convertirImagenAGris(ruta)
    iA.detectarIris()
    target=iA.detectarAnomalia()




def archivo_existe(ruta_archivo):
    return os.path.isfile(ruta_archivo)






def leer_txt_coordenada(ruta_archivo):
    
    if archivo_existe (ruta_archivo):
        fichero = open(ruta_archivo_resultado, 'r')
    
        try:
            linea= fichero.read()
            lista =linea.split()
            print (lista[1])
        finally:
            # Esta sección es siempre ejecutada
            fichero.close()
    else: 
            print('No se encontraron anomalias')

def borrar_imagen_resultado (ruta) :
    if archivo_existe(ruta):
        os.remove(ruta)


# Create an Event for notifying main thread.
callback_done = threading.Event()
ruta=''
# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(f'Received document snapshot: {doc.id}')
        datos = doc.to_dict()
        ruta =(datos.get("url"))
    if ruta != '':
        borrar_imagen_resultado('C:\proyecto_iris\deteccion\imagenes\descarga.jpg')
        descargarImagen(ruta,'deteccion\imagenes', '\descarga')
        detectar_anomalia('C:\proyecto_iris\deteccion\imagenes\descarga.jpg')    
        leer_txt_coordenada(ruta_archivo_resultado)   
      
   # callback_done.set()

doc_ref = db.collection(u'users').document(u'1')

# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)
callback_done.wait(60)



'''
    #limpiarDirectorios():
    #convertirImagenAGris('C:/Proyecto_iris/Deteccion/imagenes/ojos_264.jpg')
    #detectarIris() :
    #detectarAnomalia()
    
    
    Ekmplo descrga de imagen con barra de estado
    import urllib.request
from tqdm import tqdm

# URL del archivo que deseas descargar
url = "https://ejemplo.com/archivo.txt"

# Función para actualizar la barra de progreso
def progress_callback(block_num, block_size, total_size):
    downloaded = block_num * block_size
    progress = int(downloaded / total_size * 100)
    tqdm_instance.update(progress - tqdm_instance.n)

# Descargar el archivo con tqdm para mostrar la barra de progreso
    with tqdm(unit="B", unit_scale=True, miniters=1, desc=url.split('/')[-1]) as tqdm_instance:
    urllib.request.urlretrieve(url, reporthook=progress_callback)

print("Descarga completa.")

    '''

