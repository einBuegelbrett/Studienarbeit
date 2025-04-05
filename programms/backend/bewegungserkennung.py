from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from datetime import datetime

AUTH_PROVIDER = PlainTextAuthProvider("admin", "admin123") #Muss noch sicher gemacht werden über environment variables
cluster = Cluster(contact_points=['127.0.0.1'], port=9042) #localhost
# Verbindung zur Cassandra-Datenbank herstellen
session = cluster.connect()

session.execute("""
    CREATE KEYSPACE IF NOT EXISTS bewegungserkennung
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 3};  
""")
session.set_keyspace("bewegungserkennung")

# Verbindung schließen
cluster.shutdown()