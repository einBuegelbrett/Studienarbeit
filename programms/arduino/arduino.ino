#include <Arduino_BMI270_BMM150.h>

void setup() {
    Serial.begin(115200);
    while (!Serial);

    if (!IMU.begin()) {
        Serial.println("IMU-Sensor nicht gefunden!");
        while (1);
    }
    Serial.println("IMU-Sensor bereit!");
}

void loop() {
    float x, y, z;

    if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(x, y, z);

        float totalAcceleration = sqrt(x * x + y * y + z * z);

        Serial.print("X: "); Serial.print(x);
        Serial.print(" Y: "); Serial.print(y);
        Serial.print(" Z: "); Serial.print(z);
        Serial.print(" | Gesamt: "); Serial.println(totalAcceleration);

        if (totalAcceleration > 2.5) {  // Schwellenwert anpassen
            Serial.println("⚡ Schütteln erkannt! ⚡");
            exit(0);
        }
    }

    delay(1000);
}
