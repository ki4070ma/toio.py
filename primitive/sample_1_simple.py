#!/usr/bin/python
# -*- coding: utf-8 -*-
#toio BLE sample (with Adafruit_BluefruitLE)
#auther: mizumasa

import time
import uuid
import binascii
import Adafruit_BluefruitLE

SERVICE_UUID = uuid.UUID('10B20100-5B3B-4571-9508-CF3EFCD7BBAE')
MOTOR_UUID = uuid.UUID('10B20102-5B3B-4571-9508-CF3EFCD7BBAE')

def main():
    ble.clear_cached_data()
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))

    print('Disconnecting any connected devices...')
    ble.disconnect_devices([SERVICE_UUID])

    print('Searching device...')
    try:
        adapter.start_scan()

        device = ble.find_device(name="toio Core Cube")
        if device is None:
            raise RuntimeError('Failed to find device!')
        else:
            print('Found device name: {0}'.format(device.name))
    finally:
        # Make sure scanning is stopped before exiting.
        adapter.stop_scan()

    print('Connecting to device...')
    device.connect()
    
    try:
        print('Discovering services...')
        device.discover([SERVICE_UUID], [MOTOR_UUID])

        # Find the service and its characteristics.
        uart = device.find_service(SERVICE_UUID)
        chara = uart.find_characteristic(MOTOR_UUID)

        CommandStr = "01010164020164"
        print('Move forward: {0}'.format(CommandStr))
        chara.write_value(binascii.a2b_hex(CommandStr))
        time.sleep(1)

    finally:
        device.disconnect()

if __name__=='__main__':
    ble = Adafruit_BluefruitLE.get_provider()
    ble.initialize()
    ble.run_mainloop_with(main)

