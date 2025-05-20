import time
from cassandra.cluster import Cluster
from cassandra.policies import ExponentialReconnectionPolicy
import os

MAX_RETRIES = 10
for attempt in range(MAX_RETRIES):
    try:
        cluster = Cluster(['cassandra-service'], port=9042, reconnection_policy=ExponentialReconnectionPolicy(base_delay=2, max_delay=120))
        session = cluster.connect()
        print("Verbindung zu Cassandra erfolgreich.")
        break
    except Exception as e:
        print(f"Versuch {attempt + 1} fehlgeschlagen (initial): {e}")
        time.sleep(5)
else:
    raise Exception("Verbindung zu Cassandra konnte nach mehreren initialen Versuchen nicht aufgebaut werden.")

cql_file_path = 'database/database_bewegung.cql'

if not os.path.exists(cql_file_path):
    print(f"Fehler: Die CQL-Datei wurde nicht gefunden unter: {cql_file_path}")
    raise FileNotFoundError(f"CQL-Datei nicht gefunden: {cql_file_path}")

with open(cql_file_path, 'r') as f:
    commands = f.read().split(';')

for cmd in commands:
    if cmd.strip():
        try:
            session.execute(cmd.strip())
            print("Cassandra-Befehl erfolgreich ausgeführt.")
        except Exception as e:
            print(f"Fehler beim Ausführen des Befehls: {cmd.strip()} - {e}")
            raise

print("Cassandra-Initialisierung abgeschlossen.")
cluster.shutdown()



