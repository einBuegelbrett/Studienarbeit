#ifndef BLUETOOTH_HANDLER_H
#define BLUETOOTH_HANDLER_H

#include <ArduinoBLE.h>

// Wir "versprechen", dass es diese Funktionen gibt:
void setupBLE();
void sendSensorData(const String& data);

#endif
