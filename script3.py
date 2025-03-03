import firebase_admin 
from firebase_admin import credentials, db
import tkinter as tk
from tkinter import ttk, messagebox
import math
import matplotlib.pyplot as plt
import numpy as np
import time

# Inicializar Firebase
cred = credentials.Certificate("C:/Users/celes/OneDrive/Escritorio/script3-35624-firebase-adminsdk-fbsvc-d2b33dcbe6.json")
firebase_admin.initialize_app(cred, {'databaseURL': 'https://script3-35624-default-rtdb.firebaseio.com/'})
ref = db.reference('/historial')

def guardar_operacion(operacion, resultado):
    ref.push({'operacion': operacion, 'resultado': resultado, 'timestamp': int(time.time() * 1000)})

def crear_ventana(titulo, tamaño="300x400"):
    ventana = tk.Toplevel(root)
    ventana.title(titulo)
    ventana.geometry(tamaño)
    return ventana
def abrir_calculadora(tipo):
    ventana = crear_ventana(f"Calculadora {tipo}")
    entrada, resultado_var = tk.StringVar(), tk.StringVar()
    tk.Entry(ventana, textvariable=entrada, font=("Arial", 18), width=20, justify="right").pack(pady=10)
    tk.Label(ventana, textvariable=resultado_var, font=("Arial", 18), bg="lightgray", width=20).pack(pady=5)
    
    # Diccionario con funciones matemáticas permitidas
    funciones_permitidas = {
        "sin": math.sin, "cos": math.cos, "tan": math.tan,
        "log": math.log10, "sqrt": math.sqrt, "exp": math.exp,
        "pi": math.pi, "e": math.e, "pow": pow
    }

    def calcular():
        try:
            expresion = entrada.get().replace("^", "**")  # Reemplazar ^ por **
            resultado = eval(expresion, {"__builtins__": None}, funciones_permitidas)
            resultado_var.set(resultado)
            guardar_operacion(expresion, resultado)
        except Exception as e:
            messagebox.showerror("Error", f"Operación no válida: {e}")

    botones_basicos = [
        ('7', '8', '9', '/'), ('4', '5', '6', '*'),
        ('1', '2', '3', '-'), ('0', '.', '+', '=')
    ]
    funciones_cientificas = ['sin', 'cos', 'tan', 'log', 'sqrt', 'exp', 'pi', 'e']

    # Botones de la calculadora básica
    for fila in botones_basicos:
        frame = tk.Frame(ventana)
        frame.pack()
        for text in fila:
            tk.Button(frame, text=text, font=("Arial", 14), width=5, height=2,
                      command=lambda t=text: entrada.set(entrada.get() + t) if t != "=" else calcular()).pack(side=tk.LEFT)

    # Botones de la calculadora científica
    if tipo == "Científica":
       frame = tk.Frame(ventana)
       frame.pack()
       for func in funciones_cientificas:
           tk.Button(frame, text=func, font=("Arial", 12), width=5,
                     command=lambda f=func: entrada.set(entrada.get() + f)).pack(side=tk.LEFT)


def abrir_calculadora_grafica():
    ventana = crear_ventana("Calculadora Gráfica")
    entrada = tk.StringVar()
    tk.Label(ventana, text="Ingrese una función de x:").pack(pady=5)
    tk.Entry(ventana, textvariable=entrada, font=("Arial", 14), width=20).pack(pady=5)

    def graficar():
        try:
            expresion = entrada.get().replace("^", "**")
            x = np.linspace(-10, 10, 400)
            funciones = {
                "x": x, "sin": np.sin, "cos": np.cos, "tan": np.tan,
                "sqrt": np.sqrt, "log": np.log10, "exp": np.exp,
                "abs": np.abs, "pi": np.pi, "e": np.e
            }
            y = eval(expresion, {"__builtins__": None}, funciones)

            plt.figure()
            plt.plot(x, y, label=f"y = {expresion}")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.title("Gráfica de la función")
            plt.legend()
            plt.grid()
            plt.show()

            guardar_operacion(f"y={expresion}", "Gráfica generada")
        except Exception as e:
            messagebox.showerror("Error", f"Expresión no válida: {e}")

    tk.Button(ventana, text="Graficar", font=("Arial", 14), command=graficar).pack(pady=10)

def mostrar_historial():
    ventana = crear_ventana("Historial de Operaciones", "400x300")
    historial = ref.order_by_child('timestamp').limit_to_last(10).get()

    # Si historial es None, mostrar mensaje de error
    if not historial:
        texto_historial = "No hay historial disponible."
    else:
        # Asegurar que cada valor en historial no sea None
        texto_historial = "\n".join(
            f"{v.get('operacion', 'Desconocida')} = {v.get('resultado', 'Error')}"
            for v in historial.values() if v
        )

    tk.Label(ventana, text=texto_historial, font=("Arial", 12), justify="left").pack(pady=10, padx=10)

# INTERFAZ PRINCIPAL
root = tk.Tk()
root.title("Calculadoras con Firebase")
root.geometry("300x400")

botones = [
    ("Calculadora Básica", lambda: abrir_calculadora("Básica")),
    ("Calculadora Científica", lambda: abrir_calculadora("Científica")),
    ("Calculadora Gráfica", abrir_calculadora_grafica),
    ("Ver Historial", mostrar_historial)
]

for text, command in botones:
    ttk.Button(root, text=text, command=command).pack(pady=10)

root.mainloop()


