#include "bluetoothHandler.h"

BLEService sensorService("180C"); // eigene UUID oder Standard
BLECharacteristic sensorCharacteristic("2A56", BLERead | BLENotify, 50);

void setupBLE() {
    if (!BLE.begin()) {
        Serial.println("BLE konnte nicht gestartet werden!");
        while (1);
    }

    BLE.setLocalName("Bewegungstracker");
    BLE.setAdvertisedService(sensorService);

    sensorService.addCharacteristic(sensorCharacteristic);
    BLE.addService(sensorService);

    sensorCharacteristic.writeValue("Init");  // Optionaler Startwert

    BLE.advertise();
    Serial.println("BLE aktiv – warte auf Verbindung...");
}

void sendSensorData(const String& data) {
    BLEDevice central = BLE.central();  // Wer ist verbunden?

    if (central && central.connected()) {
        sensorCharacteristic.writeValue(data.c_str());
    }
}
