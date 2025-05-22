-- Keyspace für Sensordaten
CREATE KEYSPACE IF NOT EXISTS bewegung
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 2};

USE bewegung;

-- Tabelle für Sensordaten
CREATE TABLE IF NOT EXISTS sensordaten (
    id UUID PRIMARY KEY,
    timestamp TIMESTAMP,
    acc_x float,
    acc_y float,
    acc_z float,
    gyro_x float,
    gyro_y float,
    gyro_z float,
    mag_x float,
    mag_y float,
    mag_z float
);
