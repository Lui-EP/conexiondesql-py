import tkinter as tk
from tkinter import messagebox
import re
import csv
import mysql.connector

def insertarRegistro(nombre, apellidos, edad, estatura, telefono, genero):
    try:
        conexion = mysql.connector.connect(
            host="localhost", 
            port="3306", 
            user="root",
            password="pERSONAL04",
            database="programacionavanzada"
        )
        cursor = conexion.cursor()
        query = "INSERT INTO registros (Nombre, Apellidos, Edad, Estatura, Telefono, Genero) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (nombre, apellidos, edad, estatura, telefono, genero)

        print(f"Intentando insertar: {valores}")  # Imprimir los valores que se intentan insertar

        cursor.execute(query, valores)
        conexion.commit()
        print("Datos insertados correctamente")  # Confirmar inserción
        messagebox.showinfo("Información", "Datos guardados en la base de datos con éxito")  # Mover esto aquí
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al insertar los datos: {err}")
        print(f"Error: {err}")  # Imprimir el error en consola
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

def mostrar_datos(nombre, apellidos, edad, estatura, telefono, genero):
    datos = f"Nombres: {nombre}\nApellidos: {apellidos}\nEdad: {edad} años\nEstatura: {estatura} m\nTeléfono: {telefono}\nGénero: {genero}\n"
    messagebox.showinfo("Datos Insertados", datos)  # Mostrar los datos en una ventana

def limpiar_campos():
    tbNombre.delete(0, tk.END)
    tbApellidos.delete(0, tk.END)
    tbEdad.delete(0, tk.END)
    tbEstatura.delete(0, tk.END)
    tbTelefono.delete(0, tk.END)
    var_genero.set(0)  

def borrar_fun():
    limpiar_campos()

def validar_telefono(valor):
    return valor.isdigit() and len(valor) == 10

def validar_texto(valor):
    return bool(re.match("^[a-zA-Z\s]+$", valor))

def validar_altura(valor):
    try:
        return 0.5 <= float(valor) <= 2.5
    except ValueError:
        return False

def validar_edad(valor):
    return valor.isdigit() and 1 <= int(valor) <= 120 

def guardar_valores():
    nombre = tbNombre.get()  # Cambié "nombres" a "nombre"
    apellidos = tbApellidos.get()
    edad = tbEdad.get()
    estatura = tbEstatura.get()
    telefono = tbTelefono.get()
   
    if not validar_texto(nombre):
        messagebox.showerror("Error", "Nombre inválido")
        return
    if not validar_texto(apellidos):
        messagebox.showerror("Error", "Apellido inválido")
        return
    if not validar_telefono(telefono):
        messagebox.showerror("Error", "Teléfono inválido")
        return
    if not validar_edad(edad):
        messagebox.showerror("Error", "Edad inválida")
        return
    if not validar_altura(estatura):
        messagebox.showerror("Error", "Altura inválida (en metros)")
        return
    
    genero = ""
    if var_genero.get() == 1:
        genero = "Hombre"
    elif var_genero.get() == 2:
        genero = "Mujer"
    
    # Verificar que todos los datos son válidos antes de insertar
    if (validar_edad(edad) and validar_altura(estatura) and validar_telefono(telefono) and validar_texto(nombre) and validar_texto(apellidos)):
        datos = f"Nombres: {nombre}\nApellidos: {apellidos}\nEdad: {edad} años\nEstatura: {estatura}\nTeléfono: {telefono}\nGénero: {genero}\n"

        # Guardar en archivo CSV
        nombre_archivo = "Datos_Registro.csv"
        with open(nombre_archivo, mode="a", newline='') as archivo_csv:
            escritor_csv = csv.writer(archivo_csv)
            escritor_csv.writerow([nombre, apellidos, telefono, estatura, edad, genero])
        
        # Guardar en archivo de texto
        with open("Datos.txt", "a") as archivo:
            archivo.write(datos + "\n\n")
        
        # Llamar a la función para insertar los datos en la base de datos
        insertarRegistro(nombre, apellidos, edad, estatura, telefono, genero)
        
        # Mostrar los datos insertados
        mostrar_datos(nombre, apellidos, edad, estatura, telefono, genero)
        
        limpiar_campos()

ventana = tk.Tk()
ventana.geometry("520x500")
ventana.title("Formulario Vr.01")

var_genero = tk.IntVar()

lbNombre = tk.Label(ventana, text="Nombres:")
lbNombre.pack()
tbNombre = tk.Entry(ventana)
tbNombre.pack()

lbApellidos = tk.Label(ventana, text="Apellidos:")
lbApellidos.pack()
tbApellidos = tk.Entry(ventana)
tbApellidos.pack()

lbTelefono = tk.Label(ventana, text="Teléfono:")
lbTelefono.pack()
tbTelefono = tk.Entry(ventana)
tbTelefono.pack()

lbEdad = tk.Label(ventana, text="Edad:")
lbEdad.pack()
tbEdad = tk.Entry(ventana)
tbEdad.pack()

lbEstatura = tk.Label(ventana, text="Estatura:")
lbEstatura.pack()
tbEstatura = tk.Entry(ventana)
tbEstatura.pack()

lbGenero = tk.Label(ventana, text="Género")
lbGenero.pack()

rbHombre = tk.Radiobutton(ventana, text="Hombre", variable=var_genero, value=1)
rbHombre.pack()

rbMujer = tk.Radiobutton(ventana, text="Mujer", variable=var_genero, value=2)
rbMujer.pack()

btnBorrar = tk.Button(ventana, text="Borrar valores", command=borrar_fun)
btnBorrar.pack()

btnGuardar = tk.Button(ventana, text="Guardar", command=guardar_valores)
btnGuardar.pack()

ventana.mainloop()