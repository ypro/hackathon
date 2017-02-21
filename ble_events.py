import dbus
import sys
from time import sleep
import dbus.mainloop.glib
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GObject

btn_a_state=0
btn_b_state=0

def btn_a_changed(charachteristic, changed_state, dummy):
    if 'Value' in changed_state:
        global btn_a_state
        btn_a_state = int(changed_state['Value'][0])
        print 'button A state ' + str(btn_a_state)
    if btn_a_state>0 and btn_b_state>0:
        loop.quit()

def btn_b_changed(charachteristic, changed_state, dummy):
    if 'Value' in changed_state:
        global btn_b_state
        btn_b_state = int(changed_state['Value'][0])
        print 'button B state ' + str(btn_b_state)
    if btn_a_state>0 and btn_b_state>0:
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
            if ifaces['org.bluez.GattCharacteristic1']['UUID'] == 'e95dda90-251d-470a-a062-fa1922dfa9a8':
                btn_a_path = obj
            if ifaces['org.bluez.GattCharacteristic1']['UUID'] == 'e95dda91-251d-470a-a062-fa1922dfa9a8':
                btn_b_path = obj

                
print btn_a_path
print btn_b_path

btn_a_obj=bus.get_object('org.bluez', btn_a_path)
btn_a_iface = dbus.Interface(bus.get_object('org.bluez', btn_a_path), 'org.bluez.GattCharacteristic1')
btn_a_prop = dbus.Interface(bus.get_object('org.bluez', btn_a_path), dbus.PROPERTIES_IFACE)
btn_a_prop.connect_to_signal('PropertiesChanged', btn_a_changed)
btn_a_obj.StartNotify(dbus_interface='org.bluez.GattCharacteristic1')

btn_b_obj=bus.get_object('org.bluez', btn_b_path)
btn_b_iface = dbus.Interface(bus.get_object('org.bluez', btn_b_path), 'org.bluez.GattCharacteristic1')
btn_b_prop = dbus.Interface(bus.get_object('org.bluez', btn_b_path), dbus.PROPERTIES_IFACE)
btn_b_prop.connect_to_signal('PropertiesChanged', btn_b_changed)
btn_b_obj.StartNotify(dbus_interface='org.bluez.GattCharacteristic1')


loop = GObject.MainLoop()
loop.run()

print 'Bye bye!!!'
remote_device_methods.Disconnect()
