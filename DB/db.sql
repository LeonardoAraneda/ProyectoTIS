CREATE TABLE roles(
    id_rol INT PRIMARY KEY,
    nombre_rol VARCHAR(19)
);

CREATE TABLE telefonos(
    numero_telefonico VARCHAR(9) PRIMARY KEY
);

CREATE TABLE personal(
    id_personal VARCHAR(8) PRIMARY KEY,
    dv_personal VARCHAR(1),
    nombre_personal VARCHAR(100),
    mail_personal VARCHAR(100),
    pass VARCHAR(100),
    rol INT,
    FOREIGN KEY (rol) REFERENCES roles(id_rol) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE tel_personal(
    id_personal VARCHAR(8),
    numero_personal VARCHAR(9),
    prioridad INT,
    FOREIGN KEY (id_personal) REFERENCES personal(id_personal) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (numero_personal) REFERENCES telefonos(numero_telefonico) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (id_personal, numero)
);

CREATE TABLE cliente(
    id_cliente VARCHAR(8) PRIMARY KEY,
    dv_cliente VARCHAR(1),
    nombre_cliente VARCHAR(100),
    mail_cliente VARCHAR(100),
);

CREATE TABLE tel_cliente(
    id_cliente VARCHAR(8),
    numero_cliente VARCHAR(9),
    prioridad INT,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (numero_cliente) REFERENCES telefonos(numero_telefonico) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (id_cliente, numero_cliente)
);

CREATE TABLE tipo_cancha(
    id_tipo INT PRIMARY KEY,
    nombre_tipo VARCHAR(15)
);

CREATE TABLE canchas(
    id_cancha INT,
    tipo_cancha INT,
    FOREIGN KEY (tipo_cancha) REFERENCES tipo_cancha(id_tipo) ON DELETE CASCADE ON UPDATE CASCADE,
    PRIMARY KEY (id_tipo, tipo_cancha)
);

CREATE TABLE bloques(
    id_bloque INT PRIMARY KEY,
    id_cancha INT,
    dia VARCHAR(11),
    hora VARCHAR(10),
    FOREIGN KEY (id_cancha) REFERENCES canchas(id_cancha) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE tipo_pago(
    id_pago INT PRIMARY KEY,
    nombre_pago VARCHAR(8)
);

CREATE TABLE reserva(
    id_reserva INT PRIMARY KEY,
    fecha_ingreso VARCHAR(21),
    cliente VARCHAR(8),
    a_cargo VARCHAR(8),
    tipo_pago INT,
    numero_pago INT,
    cancha INT,
    dia VARCHAR(10),
    hora VARCHAR(10),
    FOREIGN KEY (cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (a_cargo) REFERENCES personal(id_personal) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (tipo_pago) REFERENCES tipo_pago(id_pago) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (cancha) REFERENCES canchas(id_cancha) ON DELETE CASCADE ON UPDATE CASCADE
);