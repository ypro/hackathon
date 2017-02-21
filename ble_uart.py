import dbus
import sys
from time import sleep
import dbus.mainloop.glib
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GObject

def uart_read(charachteristic, changed_state, dummy):
    if 'Value' in changed_state:
        value = int(changed_state['Value'][0]) - ord('0')
        if value == 1:
            print 'button A'
        if value == 2:
            print 'button B'
        if value == 3:
            print 'Bye bye!!!'
            loop.quit()
    
address = sys.argv[1]

DBusGMainLoop(set_as_default=True)
bus = dbus.SystemBus()
bluez = bus.get_object('org.bluez','/')
bluez_iface = dbus.Interface(bluez, 'org.freedesktop.DBus.ObjectManager')
objects = bluez_iface.GetManagedObjects()

for obj, ifaces in objects.items():
    if 'org.bluez.Device1' in ifaces.keys():
        if 'Address' in ifaces['org.bluez.Device1']:
            if address in ifaces['org.bluez.Device1']['Address']:
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
            if ifaces['org.bluez.GattCharacteristic1']['UUID'] == '6e400002-b5a3-f393-e0a9-e50e24dcca9e':
                uart_path = obj

uart_obj=bus.get_object('org.bluez', uart_path)
uart_iface = dbus.Interface(bus.get_object('org.bluez', uart_path), 'org.bluez.GattCharacteristic1')
uart_prop = dbus.Interface(bus.get_object('org.bluez', uart_path), dbus.PROPERTIES_IFACE)
uart_prop.connect_to_signal('PropertiesChanged', uart_read)
uart_obj.StartNotify(dbus_interface='org.bluez.GattCharacteristic1')

print 'starting'

loop = GObject.MainLoop()
loop.run()

print 'Bye bye!!!'
remote_device_methods.Disconnect()
