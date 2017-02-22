import dbus
import sys
from time import sleep

name = sys.argv[1]
bus = dbus.SystemBus()
bluez = bus.get_object('org.bluez','/')
bluez_iface = dbus.Interface(bluez, 'org.freedesktop.DBus.ObjectManager')
objects = bluez_iface.GetManagedObjects()

for obj, ifaces in objects.items():
    if 'org.bluez.Device1' in ifaces.keys():
        if 'Name' in ifaces['org.bluez.Device1']:
            if name in ifaces['org.bluez.Device1']['Name']:
                print "Name match with", name
                device_path = obj

print device_path

remote_device_obj = bus.get_object('org.bluez', device_path)
remote_device_methods = dbus.Interface(remote_device_obj, 'org.bluez.Device1')
remote_device_props = dbus.Interface(remote_device_obj, dbus.PROPERTIES_IFACE)

remote_device_methods.Connect()

while not remote_device_props.Get('org.bluez.Device1','ServicesResolved'):
    sleep(0.25)

for obj, ifaces in objects.items():
    if 'org.bluez.GattCharacteristic1' in ifaces.keys():
        if obj.startswith(device_path):
            if ifaces['org.bluez.GattCharacteristic1']['UUID'] == 'e95dda90-251d-470a-a062-fa1922dfa9a8':
                btn_a_path = obj
            if ifaces['org.bluez.GattCharacteristic1']['UUID'] == 'e95dda91-251d-470a-a062-fa1922dfa9a8':
                btn_b_path = obj
            if ifaces['org.bluez.GattCharacteristic1']['UUID'] == 'e95d93ee-251d-470a-a062-fa1922dfa9a8':
                led_path = obj
            if ifaces['org.bluez.GattCharacteristic1']['UUID'] == '6e400003-b5a3-f393-e0a9-e50e24dcca9e':
                uart_path = obj

                
print btn_a_path
print btn_b_path
print led_path
print uart_path

btn_a_iface = dbus.Interface(bus.get_object('org.bluez', btn_a_path), 'org.bluez.GattCharacteristic1')
btn_b_iface = dbus.Interface(bus.get_object('org.bluez', btn_b_path), 'org.bluez.GattCharacteristic1')
led_iface = dbus.Interface(bus.get_object('org.bluez', led_path), 'org.bluez.GattCharacteristic1')
uart_iface = dbus.Interface(bus.get_object('org.bluez', uart_path), 'org.bluez.GattCharacteristic1')

print btn_a_iface

sense_buttons = True

while sense_buttons:
    btn_val = btn_a_iface.ReadValue(dbus.Array())
    btn_a = int(btn_val[0])
    btn_val = btn_b_iface.ReadValue(dbus.Array())
    btn_b = int(btn_val[0])
    if btn_a > 0 and btn_b < 1:
        led_iface.WriteValue([ord('A')], ())
        print('Button A')        
    elif btn_a < 1 and btn_b > 0:
        print('Button B')
        led_iface.WriteValue([ord('B')], ())
    elif btn_a > 0 and btn_b > 0:
        message = 'Quit.'
        val = []
        for c in message:
            val.append(ord(c))
        uart_iface.WriteValue(val, ())
        sense_buttons = False
        print('Bye bye!!!')
    if not remote_device_props.Get('org.bluez.Device1', 'Connected'):  
        sense_buttons = False
    sleep(0.02)

remote_device_methods.Disconnect()
