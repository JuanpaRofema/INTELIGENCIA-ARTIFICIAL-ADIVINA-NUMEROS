import cv2
import numpy as np
from tkinter import simpledialog
from tkinter import messagebox
import os as os
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier

messagebox.showinfo(
    "Bienvenido - Reconocedor de Números IA", 
    "Instrucciones de uso:\n\n"
    "1. Dibujá un número del 1 al 9 en el CENTRO del lienzo.\n"
    "2. Presioná la tecla 'P' para que la IA prediga tu número.\n"
    "3. Presioná la tecla 'L' para limpiar el lienzo y borrar el dibujo.\n"
    "4. Presioná la tecla 'Q' para salir.\n\n"
    "⚠️ Nota: Al ser un prototipo, el modelo puede cometer errores en la predicción."
)
N, M = 200, 200
canvas = np.zeros((N, M), dtype="uint8")


def de_cero_a_uno(dato):
    if(dato == 255):
        return 1
    else:
        return 0
def entrenamiento_modelo():
    df = pd.read_csv("dibujos.csv")
    df_y = df["y"]
    df_x = df.drop(columns=['y'])
    df_x = df_x.map(de_cero_a_uno)

    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(df_x, df_y)
    print("¡Súper Pitágoras ha sido entrenado con éxito!")
    return knn
def recorrer_imagen(n):
    if(n==1):
        lista_de_pixeles = []
        for fila in range(N):
            for columna in range(M):
                dato =  canvas[fila,columna]
                lista_de_pixeles.append(dato)
        return lista_de_pixeles
    elif(n==2):
        lista_de_pixeles = []
        for fila in range(N):
            for columna in range(M):
                dato =  f"f{fila}c{columna}"
                lista_de_pixeles.append(dato)
        return lista_de_pixeles


def pincel(event, x, y, flags, param):
    global presionado 

  
    if event == cv2.EVENT_LBUTTONDOWN:
        presionado = True
        canvas[y, x] = 255

    elif event == cv2.EVENT_MOUSEMOVE:
        if presionado:
            
            cv2.circle(canvas, (x, y), 5, (255), -1)

    
    elif event == cv2.EVENT_LBUTTONUP:
        presionado = False


modelo_knn = entrenamiento_modelo()
if((not os.path.exists("dibujos.csv"))or (os.stat("dibujos.csv").st_size < 10)):
    nombres_columnas = recorrer_imagen(2)
    nombres_columnas.append("y")
    with open("dibujos.csv","a" ) as archivo:
        for nombre in nombres_columnas: 
            if(nombre != "y"):
                archivo.write(f"{nombre},")
            else:
                archivo.write("y")
        archivo.write("\n")
    archivo.close()



# --- NUESTRO ESTADO ---
# Empezamos en False porque el mouse no está apretado al inicio
presionado = False 


# Configuración de la ventana (El "addEventListener")
cv2.namedWindow("Pincel Pro")
cv2.setMouseCallback("Pincel Pro", pincel)

print("Mantené el click para dibujar. Presioná 'q' para salir.")

while True:

    cv2.imshow("Pincel Pro", canvas)


    key = cv2.waitKey(1) 

    if key == ord('q'):
        print("Saliendo...")
        break
    elif key == ord('l'):
        canvas[:] = 0
    elif key == ord('g'):
        
        with open("dibujos.csv","a" ) as archivo:
            respuesta = simpledialog.askstring("Entrada de datos", "¿Qué número dibujaste?")
            imagen = recorrer_imagen(1)  
            imagen.append(int(respuesta))
            
            for pixel in imagen:
                if(not pixel in [1,2,3,4,5,6,7,8,9]):
                    archivo.write(f"{pixel},")
                else:
                    archivo.write(str(pixel)) 
                
            archivo.write("\n")
            archivo.close()
            print("se añadio un registro!")
            canvas[:] = 0

    elif key == ord('p'):
        imagen = recorrer_imagen(1)  
        df_imagen = pd.DataFrame([imagen])
        df_normalizado = df_imagen.map(de_cero_a_uno)
        prediccion = modelo_knn.predict(df_normalizado)
        print("¡Procesando con Súper Pitágoras!")
        messagebox.showinfo("Resultado de la IA", f"Súper Pitágoras dice que es un: {prediccion[0]}")
        canvas[:] = 0

        
    elif key == ord('c'):
        # Desafío: ¿Cómo hacés que 'canvas' vuelva a ser negro?
        # Pista: Es la misma línea que usaste al principio del script
        print("Lienzo limpio")