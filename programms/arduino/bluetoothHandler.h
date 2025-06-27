#ifndef BLUETOOTH_HANDLER_H
#define BLUETOOTH_HANDLER_H

#include <ArduinoBLE.h>

void setupBLE();
void sendSensorData(const char* data);
bool isBLEConnected();

#endif
