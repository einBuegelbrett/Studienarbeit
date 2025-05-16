import asyncio
import uuid
from datetime import datetime
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from bleak import BleakClient, BleakScanner

CHARACTERISTIC_UUID = "00002a56-0000-1000-8000-00805f9b34fb"

cluster = Cluster(['cassandra-service'], port=9042)
session = cluster.connect("bewegung")

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
    devices = await BleakScanner.discover()
    arduino = next((d for d in devices if "Arduino" in d.name), None)

    if not arduino:
        print("Kein Arduino gefunden.")
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
                        datetime.utcnow(),
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
