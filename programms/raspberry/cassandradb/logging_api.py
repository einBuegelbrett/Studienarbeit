from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from datetime import datetime

# 🔒 Sichere Verbindung mit Benutzer & Passwort
AUTH_PROVIDER = PlainTextAuthProvider("admin", "admin123")
cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
session = cluster.connect()

# 🔹 Keyspace erstellen (falls nicht vorhanden)
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS logging
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 2};
""")
session.set_keyspace("logging")

# 🔹 Log-Tabelle mit Zeitpartitionierung erstellen
session.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        time_bucket int,      -- Partition Key (z. B. `HOUR % 12`)
        timestamp timestamp,  -- Clustering Key für Sortierung
        server_id int,        -- Server-ID
        message text,         -- Log-Nachricht
        PRIMARY KEY (time_bucket, timestamp)
    );
""")

# 🔹 Funktion zum Einfügen von Logs
def insert_log(timestamp, server_id, message):
    time_bucket = timestamp.hour % 12  # Berechnung des Partition Keys
    session.execute("""
        INSERT INTO logs (time_bucket, timestamp, server_id, message)
        VALUES (%s, %s, %s, %s)
    """, (time_bucket, timestamp, server_id, message))
    print(f"✅ Log gespeichert: [{timestamp}] {message}")

# 🔹 Beispiel-Logs speichern
insert_log(datetime(2025, 4, 4, 1, 0), 1, "Log-Eintrag um 01:00 Uhr")
insert_log(datetime(2025, 4, 4, 13, 0), 1, "Log-Eintrag um 13:00 Uhr")

# 🔹 Alle Logs anzeigen
rows = session.execute("SELECT * FROM logs")
for row in rows:
    print(f"📝 Log: {row.timestamp} | Server {row.server_id} | {row.message}")

# Verbindung schließen
cluster.shutdown()