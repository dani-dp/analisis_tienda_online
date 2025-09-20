# Análisis de Ventas y Gestión de Stock para Tienda Online

![Dashboard de Ventas](https://i.imgur.com/MKvl7Lc.png) ## Descripción del Proyecto

Este proyecto realiza un análisis 360º sobre la actividad comercial de una tienda online ficticia. El objetivo es transformar datos brutos de ventas en información de valor que permitan optimizar la gestión de inventario e identificar patrones de compra de los clientes. El ciclo de vida del proyecto abarca desde el diseño de la BBDD en **MySQL**, pasando por un proceso de ETL con **Python (Pandas)**, hasta la creación de un dashboard interactivo en **Power BI**.

---
## Objetivos del Análisis
Este dashboard responde a preguntas de negocio clave:
* ¿Cuáles son los **productos más vendidos** por unidades?
* ¿Quiénes son los **clientes más recurrentes** por número de pedidos?
* ¿Cómo ha sido la **evolución de pedidos** a lo largo del tiempo?
* ¿Qué productos necesitan una **reposición de stock urgente**?

---
## Tecnologías Utilizadas
* **Base de Datos:** MySQL
* **ETL y Análisis:** Python (Pandas)
* **Visualización:** Power BI
* **Control de Versiones:** Git y GitHub

---
## Estructura del Proyecto
```
tienda-online-analisis/
├── data/
│   ├── raw/          # Datos originales exportados de SQL
│   └── processed/    # Datos limpios generados por el script de Python
├── scripts/
│   └── limpieza_y_analisis.py # Script principal de ETL y análisis
├── sql/
│   ├── 1_schema_creation.sql  # Script DDL para crear la estructura de la BBDD
│   ├── 2_data_insertion.sql   # Script DML para poblar la BBDD
│   └── tiendaonline_schema.mwb # Modelo visual de la BBDD (MySQL Workbench)
├── .gitignore
└── README.md
```

---
## ¿Cómo Empezar?

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/](https://github.com/)[TU_USUARIO_GITHUB]/[NOMBRE_DEL_REPOSITORIO].git
    ```
2.  **Monta la Base de Datos:**
    * Ejecuta el script `sql/1_schema_creation.sql` en tu gestor de MySQL para crear las tablas.
    * Ejecuta el script `sql/2_data_insertion.sql` para añadir los datos de ejemplo.

3.  **Prepara el Entorno de Python:**
    * Asegúrate de tener Python instalado.
    * Instala la librería necesaria:
        ```bash
        pip install pandas
        ```
4.  **Ejecuta el Script de Limpieza:**
    * Navega a la carpeta `scripts/` y ejecuta el script principal:
        ```bash
        python limpieza_y_analisis.py
        ```
    * Esto generará los ficheros limpios en la carpeta `data/processed/`.

5.  **Abre el Dashboard:**
    * Abre el fichero `.pbix` del proyecto con Power BI Desktop.
    * Si es necesario, actualiza las rutas de origen de los datos para que apunten a tu carpeta local `data/processed/`.

---
## Autor

* **Daniel Díaz** - [Perfil de Linkedin](https://www.linkedin.com/in/danieldiaz-data/) | [Portfolio en GitHub](https://github.com/dani-dp)
