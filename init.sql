-- ============================================================
-- KARDEX AGRICOLA - Hoja Fresca
-- Base de datos: db_kardex
-- ============================================================

CREATE DATABASE IF NOT EXISTS db_kardex CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE db_kardex;

-- ============================================================
-- TABLA: usuarios (module/auth)
-- Usuarios del sistema para iniciar sesion
-- ============================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(50)  NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(100) NOT NULL,
    rol             ENUM('admin', 'operador', 'consulta') NOT NULL DEFAULT 'operador',
    activo          BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLA: cosecheros (module/supliers)
-- Personas que realizan la cosecha
-- Ej: Hermenegildo Copa, David Cala Vilca, Tania Quiroz
-- ============================================================
CREATE TABLE IF NOT EXISTS cosecheros (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    nombre     VARCHAR(100) NOT NULL,
    ci         VARCHAR(20)  NULL,
    telefono   VARCHAR(20)  NULL,
    activo     BOOLEAN NOT NULL DEFAULT TRUE,
    creado_en  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- TABLA: fincas (module/inventory)
-- Ej: Finca N.º 1, Finca N.º 2
-- ============================================================
CREATE TABLE IF NOT EXISTS fincas (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    numero    INT NOT NULL UNIQUE,
    nombre    VARCHAR(100) NULL,
    ubicacion VARCHAR(150) NULL,
    activo    BOOLEAN NOT NULL DEFAULT TRUE
);

-- ============================================================
-- TABLA: parcelas (module/inventory)
-- Parcelas dentro de cada finca, con superficie en hectareas
-- ============================================================
CREATE TABLE IF NOT EXISTS parcelas (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    finca_id       INT NOT NULL,
    numero         INT NOT NULL,
    superficie_ha  DECIMAL(10,2) NULL,
    activo         BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE KEY uq_parcela (finca_id, numero),
    FOREIGN KEY (finca_id) REFERENCES fincas(id)
);

-- ============================================================
-- TABLA: lotes (module/inventory)
-- Lotes de ingreso al almacen
-- Ej: TVH194E, TVH195E, TVH196E
-- ============================================================
CREATE TABLE IF NOT EXISTS lotes (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    codigo        VARCHAR(30) NOT NULL UNIQUE,
    finca_id      INT NULL,
    fecha_ingreso DATE NOT NULL,
    detalle       VARCHAR(150) NULL,
    creado_en     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (finca_id) REFERENCES fincas(id)
);

-- ============================================================
-- TABLA: cosechas (module/kardex)
-- Planilla de cosechas: fecha, cosechero, finca, kg, monto Bs.
-- Ejemplo: 02/01/2020 | Hermenegildo Copa | Finca 2 | 215,9 kg
-- ============================================================
CREATE TABLE IF NOT EXISTS cosechas (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    fecha         DATE NOT NULL,
    cosechero_id  INT NOT NULL,
    finca_id      INT NOT NULL,
    parcela_id    INT NULL,
    tipo_cosecha  VARCHAR(50) NOT NULL DEFAULT 'HOJA FRESCA',
    kg            DECIMAL(12,3) NOT NULL,
    monto_bs      DECIMAL(12,2) NOT NULL DEFAULT 0,
    observacion   VARCHAR(200) NULL,
    FOREIGN KEY (cosechero_id) REFERENCES cosecheros(id),
    FOREIGN KEY (finca_id)     REFERENCES fincas(id),
    FOREIGN KEY (parcela_id)   REFERENCES parcelas(id)
);

-- ============================================================
-- TABLA: kardex_movimientos (module/kardex)
-- Libro kardex del almacen: ENTRADA / SALIDA / SALDO
-- Ej: 3/1/2020 | Ingreso Almacen Chimore | TVH194E | Finca | entrada 20,18
-- ============================================================
CREATE TABLE IF NOT EXISTS kardex_movimientos (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    fecha       DATE NOT NULL,
    detalle     VARCHAR(150) NOT NULL,
    doc         VARCHAR(30) NULL,
    lote_id     INT NULL,
    finca_id    INT NULL,
    entrada_kg  DECIMAL(12,3) NOT NULL DEFAULT 0,
    salida_kg   DECIMAL(12,3) NOT NULL DEFAULT 0,
    saldo_kg    DECIMAL(12,3) NOT NULL DEFAULT 0,
    observacion VARCHAR(200) NULL,
    FOREIGN KEY (lote_id)  REFERENCES lotes(id),
    FOREIGN KEY (finca_id) REFERENCES fincas(id)
);

-- ============================================================
-- INDICES para busquedas frecuentes por fecha y finca
-- ============================================================
CREATE INDEX idx_cosechas_fecha      ON cosechas(fecha);
CREATE INDEX idx_cosechas_finca      ON cosechas(finca_id);
CREATE INDEX idx_cosechas_cosechero  ON cosechas(cosechero_id);
CREATE INDEX idx_kardex_fecha        ON kardex_movimientos(fecha);
CREATE INDEX idx_kardex_lote         ON kardex_movimientos(lote_id);
