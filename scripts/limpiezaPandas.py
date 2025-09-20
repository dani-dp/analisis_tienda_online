"""
==============================================================================
                    ANÁLISIS DE VENTAS - TIENDA ONLINE
==============================================================================
Autor: Daniel Díaz
Fecha: 20 de septiembre de 2025
Descripción: 
Este script realiza el proceso de limpieza, transformación y análisis
exploratorio de los datos de ventas exportados desde la base de datos MySQL 
'TiendaOnline'. 
El objetivo es preparar los datos para su posterior visualización en Power BI
y extraer insights iniciales sobre el comportamiento de los clientes y la 
gestión de stock.

Ficheros de entrada: 
- clientes.csv
- pedidos.csv
- productos.csv
- stock.csv
- producto_dep_ventotales.csv

Ficheros de salida:
- altas_por_mes_año_limpio.csv
- clientes_compras_limpio.csv
- ventas_totales_ordenado_limpio.csv
==============================================================================
"""
import pandas as pd
import os

# Declaramos funciones
def comprobar_datos(csv, nombre):
    if not csv.empty:
        print(f"\n{nombre}: Información cargada correctamente ✅")  # Añadimos nombre del csv
        print(f"Filas: {csv.shape[0]}, Columnas: {csv.shape[1]}")   # Comprobamos filas y columnas
        print(f"Valores nulos:\n{csv.isnull().sum()}")              # Comprovamos valores nulos
    else:
        print(f"\n{nombre}: El archivo está vacío ⚠️")



# Diccionario con archivos
archivos = {
    "Clientes":         r"../data/raw/clientes.csv",
    "Pedidos":          r"../data/raw/pedidos.csv",
    "Productos":        r"../data/raw/productos.csv",
    "Stock":            r"../data/raw/stock.csv",
    "Ventas Totales":   r"../data/raw/producto_dep_ventotales.csv"
    }

# Bucle para cargar y comprobar
dataframes = {}  # aquí guardamos cada DF
for nombre, ruta in archivos.items():
    try:
        df = pd.read_csv(ruta)
        comprobar_datos(df, nombre)
        dataframes[nombre] = df  # lo guardamos por si luego quieres acceder
    except FileNotFoundError:
        print(f"\n{nombre}: archivo no encontrado ❌")
        dataframes[nombre] = None
    
"""
RANGO DE MESES TOP DE CAPTACIONES EN CLIENTES
"""
# Rango de meses top de captaciones en clientes
dataframes['Clientes']['fecha_alta'] = pd.to_datetime(dataframes['Clientes']['fecha_alta']) # Aseguramos el tipo de dato
dataframes['Clientes']['año_alta'] = dataframes['Clientes']['fecha_alta'].dt.year   # Añadimos columna año
dataframes['Clientes']['mes_alta'] = dataframes['Clientes']['fecha_alta'].dt.month  # Añadimos columna mes
dataframes['Clientes']['nombre_mes'] = dataframes['Clientes']['fecha_alta'].dt.month_name() # Añadimos nombre del mes

# Análisis de Pandas
altas_por_mes_año = dataframes['Clientes'].groupby(['año_alta', 'mes_alta'])['cliente_id'].count().sort_index() # Uso un ID de cliente, es más explícito
altas_por_mes_año.to_csv("../data/processed/altas_por_mes_año_limpio.csv", index=False)

"""
COUNT DE GROUPBY DE PRODUCTOS Y ANALIZARLO JUNTO CON LAS COMPRAS, PARA DETECTAR SI TENEMOS QUE TRAER MAS PRODUCTOS DE UNA RAMA EN CONCRETO
(GRÁFICO POWERBI)
"""
# Al estar ya ordenado por MySQL, vamos a ordenar las ventas totales
dataframes["Ventas Totales"] = dataframes["Ventas Totales"].sort_values(by="Ventas Totales", ascending=False)
dataframes["Ventas Totales"].to_csv("../data/processed/ventas_totales_ordenado_limpio.csv", index=False)

"""
CLIENTES CON CERO COMPRAS
"""
# Unimos con .merge() la tabla 'Clientes' con la tabla 'Pedidos' 
df_conjunto = dataframes['Clientes'].merge(right=dataframes['Pedidos'], how ='left' , on='cliente_id')
# print(df_conjunto.sort_values(by='pedido_id', ascending=True))

# Para saber si hay null, eso nos daría clientes que no han hecho pedidos
clientes_sin_compras = df_conjunto[df_conjunto['pedido_id'].isnull()]
print(f"\nClientes sin compras: {clientes_sin_compras}") # Nos devuelve una lista vacía ya que no hay ningún valor null, por que todos los clientes han comprado

df_conjunto.to_csv("../data/processed/clientes_compras_limpio.csv", index=False)


"""
STOCK A CERO Y VER SU FECHA DE ENTRADA: SI LA FECHA DE ENTRADA ES ANTES QUE LA DE HOY, TENEMOS QUE VOVLER A PEDIR Y QUE SALTE UN AVISO
"""
# Queremos todos los productos que tienen el stock 0
stock_cero_conjunto = dataframes['Stock'][dataframes['Stock']['cantidad_s'] == 0].merge(right=dataframes['Productos'], how='left', on='producto_id')

# Comenzamos con las fechas:
dataframes['Stock']['fecha_entrada'] = pd.to_datetime(dataframes['Stock']['fecha_entrada']) # Aseguramos el tipo de dato
hoy = pd.Timestamp.now().normalize()

# 1. Preparamos las listas para guardar los mensajes
articulos_pedir = []
articulos_en_camino = []

# 2. UN ÚNICO BUCLE para clasificar
for indice, fila in stock_cero_conjunto.iterrows():
    fecha_del_producto = pd.to_datetime(fila['fecha_entrada']).normalize()
    
    if fecha_del_producto < hoy:
        mensaje = f"El artículo {fila['producto_id']}: {fila['designacion_x']}. Última entrada {fecha_del_producto.strftime('%Y-%m-%d')}"
        articulos_pedir.append(mensaje)
    else: # Si no es menor, es que es hoy o en el futuro
        mensaje = f"El artículo {fila['producto_id']}: {fila['designacion_x']} llega el día {fecha_del_producto.strftime('%Y-%m-%d')}"
        articulos_en_camino.append(mensaje)

# 3. Imprimimos los resultados DESPUÉS del bucle
print("\n----- Artículos sin stock y que NECESITAN PEDIDO -----")
if articulos_pedir:
    for item in articulos_pedir:
        print(item)
else:
    print("¡No hay que pedir! Todas las reposiciones están en camino.")

print("\n----- Artículos sin stock pero CON REPOSICIÓN EN CAMINO -----")
if articulos_en_camino:
    for item in articulos_en_camino:
        print(item)
else:
    print("No hay ninguna reposición programada.")

