#include "bluetoothHandler.h"

BLEService sensorService("180C");
BLECharacteristic sensorCharacteristic("2A56", BLERead | BLENotify, 120);

void setupBLE() {
    if (!BLE.begin()) {
        Serial.println("BLE konnte nicht gestartet werden!");
        while (1);
    }

    BLE.setLocalName("Bewegungstracker");
    BLE.setAdvertisedService(sensorService);

    sensorService.addCharacteristic(sensorCharacteristic);
    BLE.addService(sensorService);

    sensorCharacteristic.writeValue("Init");

    BLE.advertise();
    Serial.println("BLE aktiv – warte auf Verbindung...");
}

void sendSensorData(const char* data) {
    BLEDevice central = BLE.central();

    if (central && central.connected()) {
        sensorCharacteristic.writeValue(data);
    }
}

bool isBLEConnected() {
  return BLE.connected();
}
