import bluetooth

def connect_to_arduino():
    # Replace with your Arduino's MAC address
    arduino_address = '<MAC_ADDRESS>'
    port = 1  # Usually port 1 for RFCOMM

    # Create a Bluetooth socket
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((arduino_address, port))

    try:
        while True:
            data = sock.recv(1024)
            if data:
                print(f"Received: {data.decode('utf-8')}")
    except KeyboardInterrupt:
        sock.close()