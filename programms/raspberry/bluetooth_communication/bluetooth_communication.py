import asyncio
import uuid
from datetime import datetime
from cassandra.cluster import Cluster
from cassandra.policies import ExponentialReconnectionPolicy
import time
from bleak import BleakClient, BleakScanner

CHARACTERISTIC_UUID = "00002a56-0000-1000-8000-00805f9b34fb"

MAX_RETRIES = 10
for attempt in range(MAX_RETRIES):
    try:
        cluster = Cluster(['localhost'], port=9042, reconnection_policy=ExponentialReconnectionPolicy(base_delay=2, max_delay=120))
        session = cluster.connect("bewegung")
        print("Verbindung zu Cassandra erfolgreich.")
        break
    except Exception as e:
        print(f"Versuch {attempt + 1} fehlgeschlagen (initial): {e}")
        time.sleep(5)
else:
    raise Exception("Verbindung zu Cassandra konnte nach mehreren initialen Versuchen nicht aufgebaut werden.")

insert_stmt = session.prepare("""
    INSERT INTO sensordaten (id, timestamp, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""")

def parse_imu_data(raw_data):
    try:
        parts = raw_data.split(" | ")
        acc = [float(p.split(":")[1]) for p in parts[0].split()[1:]]
        gyro = [float(p.split(":")[1]) for p in parts[2].split()[1:]]
        mag = [float(p.split+(":")[1]) for p in parts[4].split()[1:]]

        return {
            "acc": acc,
            "gyro": gyro,
            "mag": mag
        }
    except Exception as e:
        print("Parsing error:", e)
        return None

async def main():
    max_versuche = 5  # Anzahl der Versuche
    arduino = None

    for versuch in range(1, max_versuche + 1):
        print(f"Versuch {versuch} von {max_versuche}...")
        devices = await BleakScanner.discover()
        arduino = next((d for d in devices if d.name and "Bewegungstracker" in d.name), None)

        if arduino:
            print(f"Arduino gefunden: {arduino.name} ({arduino.address})")
            break

        print("Kein Arduino gefunden. Warte 5 Sekunden...")
        await asyncio.sleep(5)

    if not arduino:
        print("Arduino nach mehreren Versuchen nicht gefunden.")
        return

    async with BleakClient(arduino.address) as client:
        print("Verbunden mit:", arduino.name)

        def handle_notification(_, data):
            decoded = data.decode("utf-8").strip()
            if "ENDZEIT" in decoded:
                print("[INFO] Übertragung beendet.")
                return

            parsed = parse_imu_data(decoded)
            if parsed:
                session.execute(
                    insert_stmt,
                    (
                        uuid.uuid4(),
                        datetime.now(),
                        *parsed["acc"],
                        *parsed["gyro"],
                        *parsed["mag"]
                    )
                )
                print("Gespeichert:", decoded)

        await client.start_notify(CHARACTERISTIC_UUID, handle_notification)

        print("Starte Datenempfang für 125 Sekunden...")
        await asyncio.sleep(125)

        await client.stop_notify(CHARACTERISTIC_UUID)
        print("Verbindung beendet.")

if __name__ == "__main__":
    asyncio.run(main())
