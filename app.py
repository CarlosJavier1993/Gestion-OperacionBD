import psycopg2

# Configura los parámetros de conexión
connection = psycopg2.connect(
    dsn="postgresql://carlos:ZdnCQhSnWqCMoktX6VfA8g@meadow-manatee-4740.jxf.gcp-us-east1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&sslrootcert=C:\\Users\\PC202\\AppData\\Roaming\\postgresql\\root.crt"
)

cursor = connection.cursor()

# Crear una tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS ejemplo (
    id SERIAL PRIMARY KEY,
    nombre TEXT,
    edad INT
)
""")
connection.commit()

# Insertar datos en la tabla
cursor.execute("INSERT INTO ejemplo (nombre, edad) VALUES (%s, %s)", ("SANTOFIMIO", 50))
connection.commit()

# Consultar datos en la tabla
cursor.execute("SELECT * FROM ejemplo")
result = cursor.fetchall()
print(result)

# Actualizar datos en la tabla
cursor.execute("UPDATE ejemplo SET nombre = %s, edad = %s WHERE id = %s", ("Juan", 30, 1))
connection.commit()

# Eliminar datos en la tabla
cursor.execute("DELETE FROM ejemplo WHERE id = %s", (1,))
connection.commit()

# Cierra la conexión
cursor.close()
connection.close()
