import pandas as pd
from sqlalchemy import create_engine
import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Configuración de la conexión a la base de datos MySQL
usuario = "root"
contraseña = ""
host = "localhost"
puerto = "3306"
nombre_base_de_datos = "sakila"

# Crear la cadena de conexión para MySQL
cadena_conexion = f"mysql+pymysql://{usuario}:{contraseña}@{host}:{puerto}/{nombre_base_de_datos}"

# Crear el motor de SQLAlchemy
engine = create_engine(cadena_conexion)

# Consultas SQL

query_inner_join = """
SELECT 
    c.customer_id, 
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name, 
    r.rental_id, 
    r.rental_date, 
    i.inventory_id, 
    f.film_id, 
    f.title, 
    fc.category_id
FROM customer c
INNER JOIN rental r ON c.customer_id = r.customer_id
INNER JOIN inventory i ON r.inventory_id = i.inventory_id
INNER JOIN film f ON i.film_id = f.film_id
INNER JOIN film_category fc ON f.film_id = fc.film_id
WHERE r.rental_date BETWEEN '2005-06-01' AND '2005-07-01';
"""

query_left_join = """
SELECT 
    c.customer_id, 
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name, 
    r.rental_id, 
    r.rental_date, 
    i.inventory_id
FROM customer c
LEFT JOIN rental r ON c.customer_id = r.customer_id
LEFT JOIN inventory i ON r.inventory_id = i.inventory_id
WHERE c.active = 1;
"""

query_right_join = """
SELECT 
    s.staff_id, 
    CONCAT(s.first_name, ' ', s.last_name) AS staff_name, 
    i.inventory_id, 
    f.film_id, 
    f.title
FROM staff s
RIGHT JOIN inventory i ON s.store_id = i.store_id
RIGHT JOIN film f ON i.film_id = f.film_id
WHERE f.rental_rate > 2.99;
"""

query_full_outer_join = """
SELECT 
    c.customer_id, 
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name, 
    r.rental_id, 
    r.rental_date, 
    s.staff_id, 
    CONCAT(s.first_name, ' ', s.last_name) AS staff_name, 
    i.inventory_id
FROM customer c
LEFT JOIN rental r ON c.customer_id = r.customer_id
LEFT JOIN inventory i ON r.inventory_id = i.inventory_id
LEFT JOIN staff s ON r.staff_id = s.staff_id
WHERE r.rental_date IS NULL OR s.staff_id IS NULL OR i.inventory_id IS NULL
UNION
SELECT 
    c.customer_id, 
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name, 
    r.rental_id, 
    r.rental_date, 
    s.staff_id, 
    CONCAT(s.first_name, ' ', s.last_name) AS staff_name, 
    i.inventory_id
FROM customer c
RIGHT JOIN rental r ON c.customer_id = r.customer_id
RIGHT JOIN inventory i ON r.inventory_id = i.inventory_id
RIGHT JOIN staff s ON r.staff_id = s.staff_id
WHERE r.rental_date IS NULL OR s.staff_id IS NULL OR i.inventory_id IS NULL;
"""

query_cross_join = """
SELECT 
    c.customer_id, 
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name, 
    f.film_id, 
    f.title
FROM customer c
CROSS JOIN film f
WHERE c.customer_id < 10;
"""

# Función para ejecutar las consultas SQL
def ejecutar_consulta(query):
    df = pd.read_sql(query, engine)
    return df

# Función para guardar los resultados en PDF
def guardar_pdf(df, nombre_pdf):
    c = canvas.Canvas(nombre_pdf, pagesize=letter)
    c.setFont("Helvetica", 10)
    
    x_start = 30
    column_width = 130
    
    # Títulos de las columnas
    for i, column in enumerate(df.columns):
        c.drawString(x_start + (i * column_width), 750, column)
    
    # Filas de datos
    for row_index, row in df.iterrows():
        for col_index, value in enumerate(row):
            c.drawString(x_start + (col_index * column_width), 730 - (row_index * 20), str(value))
    
    c.save()


# Funciones para ejecutar cada consulta y mostrar resultados
def mostrar_inner_join():
    df = ejecutar_consulta(query_inner_join)
    print(df)
    guardar_pdf(df, "inner_join_result.pdf")
    messagebox.showinfo("Éxito", "PDF generado con éxito!")

def mostrar_left_join():
    df = ejecutar_consulta(query_left_join)
    print(df)
    guardar_pdf(df, "left_join_result.pdf")
    messagebox.showinfo("Éxito", "PDF generado con éxito!")

def mostrar_right_join():
    df = ejecutar_consulta(query_right_join)
    print(df)
    guardar_pdf(df, "right_join_result.pdf")
    messagebox.showinfo("Éxito", "PDF generado con éxito!")

def mostrar_full_outer_join():
    df = ejecutar_consulta(query_full_outer_join)
    print(df)
    guardar_pdf(df, "full_outer_join_result.pdf")
    messagebox.showinfo("Éxito", "PDF generado con éxito!")

def mostrar_cross_join():
    df = ejecutar_consulta(query_cross_join)
    print(df)
    guardar_pdf(df, "cross_join_result.pdf")
    messagebox.showinfo("Éxito", "PDF generado con éxito!")

# Crear la interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Consultas SQL y Generación de PDF")

# Cambiar color de fondo de la ventana
root.configure(bg="#f0f8ff")  # Color de fondo suave (aliceblue)

# Establecer el tamaño de la ventana
root.geometry("400x450")

# Título con fuente personalizada
title_label = tk.Label(root, text="Consultas SQL", font=("Arial", 16, "bold"), fg="#4b0082", bg="#f0f8ff")
title_label.pack(pady=20)

# Función para mejorar los botones (agregar color, efectos hover)
def button_hover(event):
    event.widget.config(bg="#8a2be2")

def button_leave(event):
    event.widget.config(bg="#4b0082")

# Crear botones para cada consulta
button_inner_join = tk.Button(root, text="Mostrar INNER JOIN", font=("Arial", 12), bg="#4b0082", fg="white", width=20, height=2)
button_inner_join.pack(pady=10)
button_inner_join.bind("<Enter>", button_hover)
button_inner_join.bind("<Leave>", button_leave)
button_inner_join.config(command=mostrar_inner_join)

button_left_join = tk.Button(root, text="Mostrar LEFT JOIN", font=("Arial", 12), bg="#4b0082", fg="white", width=20, height=2)
button_left_join.pack(pady=10)
button_left_join.bind("<Enter>", button_hover)
button_left_join.bind("<Leave>", button_leave)
button_left_join.config(command=mostrar_left_join)

button_right_join = tk.Button(root, text="Mostrar RIGHT JOIN", font=("Arial", 12), bg="#4b0082", fg="white", width=20, height=2)
button_right_join.pack(pady=10)
button_right_join.bind("<Enter>", button_hover)
button_right_join.bind("<Leave>", button_leave)
button_right_join.config(command=mostrar_right_join)

button_full_outer_join = tk.Button(root, text="Mostrar FULL OUTER JOIN", font=("Arial", 12), bg="#4b0082", fg="white", width=20, height=2)
button_full_outer_join.pack(pady=10)
button_full_outer_join.bind("<Enter>", button_hover)
button_full_outer_join.bind("<Leave>", button_leave)
button_full_outer_join.config(command=mostrar_full_outer_join)

button_cross_join = tk.Button(root, text="Mostrar CROSS JOIN", font=("Arial", 12), bg="#4b0082", fg="white", width=20, height=2)
button_cross_join.pack(pady=10)
button_cross_join.bind("<Enter>", button_hover)
button_cross_join.bind("<Leave>", button_leave)
button_cross_join.config(command=mostrar_cross_join)

# Ejecutar la interfaz gráfica
root.mainloop()
