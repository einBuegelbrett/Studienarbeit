#include <Arduino_BMI270_BMM150.h>
#include "bluetoothHandler.h"

unsigned long startTime;
const unsigned long duration = 125000; // 125 Sekunden in Millisekunden
const unsigned long interval = 500;    // Daten alle 500 ms
unsigned long lastSendTime = 0;
bool messungAktiv = false;

void setup() {
    Serial.begin(115200);

    if (!IMU.begin()) {
        Serial.println("IMU-Sensor nicht gefunden!");
        while (1);
    }

    Serial.println("IMU-Sensor bereit!");
    setupBLE();

    // Warten bis Bluetooth verbunden ist
    Serial.println("Warte auf Bluetooth-Verbindung...");
    while (!isBLEConnected()) {
        delay(500);
    }

    Serial.println("Bluetooth verbunden – Messung startet");
        // Eingebaute LED 2x blinken als Startsignal
    for (int i = 0; i < 10; i++) {
        digitalWrite(LED_BUILTIN, HIGH);
        delay(200);
        digitalWrite(LED_BUILTIN, LOW);
        delay(200);
    }
    startTime = millis();
    messungAktiv = true;
}

void loop() {
    unsigned long currentTime = millis();

    // Prüfen ob Messzeit abgelaufen ist
    if (messungAktiv && (currentTime - startTime >= duration)) {
        Serial.println("ENDZEIT ERREICHT");
        sendSensorData("ENDZEIT");
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

            String imuData = String(ax, 2) + ";" + String(ay, 2) + ";" + String(az, 2) + ";" + 
                             String(gx, 2) + ";" + String(gy, 2) + ";" + String(gz, 2) + ";" +
                             String(mx, 2) + ";" + String(my, 2) + ";" + String(mz, 2);

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