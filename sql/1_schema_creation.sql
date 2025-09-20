-- Base de datos para cliente de su tienda online
CREATE DATABASE IF NOT EXISTS TiendaOnline;

USE tiendaonline;

CREATE TABLE IF NOT EXISTS Clientes (
	cliente_id INT AUTO_INCREMENT PRIMARY KEY, 
    nombre VARCHAR(255) NOT NULL, 
    apellido VARCHAR(255),
    telefono INT,
    correo_elec VARCHAR(255),
    fecha_alta DATE,
    rango_cliente VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Productos (
	producto_id INT AUTO_INCREMENT PRIMARY KEY, 
    designacion VARCHAR(255) NOT NULL, 
    departamento VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Pedidos (
	pedido_id INT AUTO_INCREMENT PRIMARY KEY, 
    cliente_id INT, 
    producto_id INT, 
    cantidad_p INT,
    FOREIGN KEY (cliente_id) REFERENCES Clientes(cliente_id) ON DELETE CASCADE,			-- Si se borra en Clientes, se borran sus pedidos
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id)
    ON DELETE SET NULL 
);

CREATE TABLE IF NOT EXISTS Stock (
	stock_id INT AUTO_INCREMENT PRIMARY KEY, 
    producto_id INT, 
    cantidad_s INT,
    fecha_entrada DATE, 
    FOREIGN KEY (producto_id) REFERENCES Productos(producto_id)
    ON DELETE SET NULL
);
