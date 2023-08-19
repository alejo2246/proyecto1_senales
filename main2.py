import keyboard
import tkinter as tk
from tkinter import filedialog
import xml.etree.ElementTree as ET

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "Archivo no encontrado"
    except Exception as e:
        return f"Error: {e}"




def showStudentData():
    print('Juan Pablo Osuna de Leon')
    print('201503911')
    print('Introduccion a la Programacion y computacion 2 seccion A')
    print('Ingenieria en Ciencias y Sistemas')
    print('4to Semestre')
    
    








def main_menu():
    fileContent=''
    filePath=''
    while True:
        if keyboard.is_pressed('esc'):
            break
        print("Menú principal:")
        print("1. Cargar archivo")
        print("2. Procesar archivo")
        print('3. Escribir archivo salida')
        print('4. Mostrar datos del estudiante')
        print('5. Generar gráfica')
        print('6. Inicializar sistema')
        print('7. Salida')
        choice = int(input("--> "))

        if choice == '1':
            filePath= filedialog.askopenfilename(filetypes=[('XML Files', '*.xml')])
            fileContent = read_file(filePath)
            
        elif choice == '2':
            print("Exiting the program.")




     
        else:
            print("Esta opcion no es valida, seleccione nuevamente")

if __name__ == "__main__":
    main_menu()
