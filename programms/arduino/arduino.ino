#include <Arduino_BMI270_BMM150.h>
#include "bluetoothHandler.h"

unsigned long startTime;
const unsigned long duration = 125000; // 125 Sekunden in Millisekunden
const unsigned long interval = 500;    // Daten alle 500 ms
unsigned long lastSendTime = 0;
bool messungAktiv = false;
int packetCounter = 0;

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
        digitalWrite(LED_BUILTIN, HIGH); // LED einschalten um zu zeigen, dass Daten gesendet werden
        delay(100);
        digitalWrite(LED_BUILTIN, LOW);
        delay(100);
        if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable() && IMU.magneticFieldAvailable()) {
            float ax, ay, az;
            float gx, gy, gz;
            float mx, my, mz;

            IMU.readAcceleration(ax, ay, az);
            IMU.readGyroscope(gx, gy, gz);
            IMU.readMagneticField(mx, my, mz);

           char imuData[120];
           snprintf(imuData, sizeof(imuData), "%d;%.2f;%.2f;%.2f;%.2f;%.2f;%.2f;%.2f;%.2f;%.2f", packetCounter, ax, ay, az, gx, gy, gz, mx, my, mz);
            if (isBLEConnected()) {
                sendSensorData(imuData);
                packetCounter++;

            } else {
                Serial.println("Nicht verbunden – Daten werden übersprungen.");
            }
            lastSendTime = currentTime;
        }
    }
}