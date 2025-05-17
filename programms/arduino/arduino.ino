#include <Arduino_BMI270_BMM150.h>
#include "bluetoothHandler.h"

unsigned long startTime;
const unsigned long duration = 125000; // 125 Sekunden in Millisekunden
const unsigned long interval = 500;    // Daten alle 500 ms
unsigned long lastSendTime = 0;
bool messungAktiv = true;

void setup() {
    Serial.begin(115200);
    while (!Serial);

    if (!IMU.begin()) {
        Serial.println("IMU-Sensor nicht gefunden!");
        while (1);
    }

    Serial.println("IMU-Sensor bereit!");
    setupBLE();
    delay(10000); // Wartezeit für die Verbindung
    startTime = millis();
}

void loop() {
    unsigned long currentTime = millis();

    // Prüfen ob Messzeit abgelaufen ist
    if (messungAktiv && (currentTime - startTime >= duration)) {
        Serial.println("ENDZEIT ERREICHT");
        messungAktiv = false;  // weitere Messungen stoppen
        return;
    }

    // Nur weitermachen, wenn Messung noch aktiv
    if (messungAktiv && (currentTime - lastSendTime >= interval)) {
        if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable() && IMU.magneticFieldAvailable()) {
            float ax, ay, az;
            float gx, gy, gz;
            float mx, my, mz;

            IMU.readAcceleration(ax, ay, az);
            IMU.readGyroscope(gx, gy, gz);
            IMU.readMagneticField(mx, my, mz);

            String imuData = "Acc: X:" + String(ax, 2) + " Y:" + String(ay, 2) + " Z:" + String(az, 2) +
                 " | Gyro: X:" + String(gx, 2) + " Y:" + String(gy, 2) + " Z:" + String(gz, 2) +
                 " | Mag: X:" + String(mx, 2) + " Y:" + String(my, 2) + " Z:" + String(mz, 2);

            Serial.println(imuData);

            if (isBLEConnected()) {
                sendSensorData(imuData);
            } else {
                Serial.println("Nicht verbunden – Daten werden übersprungen.");
            }

            lastSendTime = currentTime;
        }
    }
}