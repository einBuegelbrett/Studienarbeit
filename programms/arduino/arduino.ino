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

            float totalAcc = sqrt(ax * ax + ay * ay + az * az);
            float totalGyro = sqrt(gx * gx + gy * gy + gz * gz);
            float totalMag = sqrt(mx * mx + my * my + mz * mz);

            float accRate = IMU.accelerationSampleRate();
            float gyroRate = IMU.gyroscopeSampleRate();
            float magRate = IMU.magneticFieldSampleRate();

            String imuData = "ACC: X:" + String(ax, 2) + " Y:" + String(ay, 2) + " Z:" + String(az, 2) + " | G:" + String(totalAcc, 2) +
                             " | GYRO: X:" + String(gx, 2) + " Y:" + String(gy, 2) + " Z:" + String(gz, 2) + " | G:" + String(totalGyro, 2) +
                             " | MAG: X:" + String(mx, 2) + " Y:" + String(my, 2) + " Z:" + String(mz, 2) + " | G:" + String(totalMag, 2) +
                             " | Rates: A:" + String(accRate, 1) + "Hz G:" + String(gyroRate, 1) + "Hz M:" + String(magRate, 1) + "Hz";

            Serial.println(imuData); // Debug-Ausgabe

            // Nur senden, wenn verbunden
            if (isBLEConnected()) {
                sendSensorData(imuData);
            } else {
                Serial.println("Nicht verbunden – Daten werden übersprungen.");
            }

            lastSendTime = currentTime;
        }
    }
}