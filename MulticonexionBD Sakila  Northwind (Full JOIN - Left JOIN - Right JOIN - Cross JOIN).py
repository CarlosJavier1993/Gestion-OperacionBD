from sqlalchemy import create_engine
import pandas as pd

# 📌 conexiones con SQLAlchemy
engine_pg = create_engine("postgresql+psycopg2://postgres:JR1234@localhost/123")
engine_mysql = create_engine("mysql+mysqlconnector://root:@localhost/Sakila")

# 📌 Obtener datos de PostgreSQL (customers de Northwind)
query_pg = "SELECT customer_id, company_name, contact_name FROM customers"
df_pg = pd.read_sql(query_pg, engine_pg)

# 📌 Obtener datos de MySQL (actor de Sakila)
query_mysql = "SELECT actor_id, first_name, last_name FROM actor"
df_mysql = pd.read_sql(query_mysql, engine_mysql)

# 📌 Tablas por separado 1 Postgres y otra de MySQL
print("🔹 Datos de PostgreSQL (Northwind - Customers)")
print(df_pg)

print("\n🔹 Datos de MySQL (Sakila - Actor)")
print(df_mysql)

# 📌LEFT JOIN (todos los de PostgreSQL y solo coincidentes de MySQL)
left_join = pd.merge(df_pg, df_mysql, how="left", left_on="contact_name", right_on="first_name")

# 📌 RIGHT JOIN (todos los de MySQL y solo coincidentes de PostgreSQL)
right_join = pd.merge(df_pg, df_mysql, how="right", left_on="contact_name", right_on="first_name")

# 📌 UNION de ambos resultados (simulando FULL JOIN)
df_full_join = pd.concat([left_join, right_join]).drop_duplicates()

# 📌 Mostrar el resultado incluyendo datos vacios.
print(df_full_join)

# Mostrar todas las combinaciones posibles sin datos vacios.
df_pg["key"] = 1
df_mysql["key"] = 1

df_cross_join = pd.merge(df_pg, df_mysql, on="key").drop(columns=["key"])
print(df_cross_join)
