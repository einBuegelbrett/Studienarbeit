#include <Arduino_BMI270_BMM150.h>
#include "bluetoothHandler.h"

void setup() {
    Serial.begin(115200);
    while (!Serial);

    if (!IMU.begin()) {
        Serial.println("IMU-Sensor nicht gefunden!");
        while (1);
    }
    Serial.println("IMU-Sensor bereit!");
    setupBLE();
}

void loop() {
    float x, y, z;

    if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(x, y, z);

        float totalAcceleration = sqrt(x * x + y * y + z * z);

        String imuData = "X: " + String(x, 2) +
                         " Y: " + String(y, 2) +
                         " Z: " + String(z, 2) +
                         " | Gesamt: " + String(totalAcceleration, 2);

        Serial.println(imuData);           // Debug über USB
        sendSensorData(imuData);           // Senden über BLE
    }

    delay(1000);
}

