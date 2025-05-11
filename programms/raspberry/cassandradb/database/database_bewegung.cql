-- Keyspace für Sensordaten
CREATE KEYSPACE IF NOT EXISTS bewegung
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 2};

USE bewegung;

-- Tabelle für Sensordaten


