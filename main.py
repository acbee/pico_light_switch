from acb import print_variable, mqtt_connect
from machine import Pin, reset, unique_id
from time import localtime, sleep
from mpy_env import load_env, get_env
from ubinascii import hexlify
import network

debug = 1
colon_position = 12
wlan_connection_retries = 10
mqtt_connection_retries = 10

# Load variables
load_env()
mqtt_srvr = get_env("mqtt_srvr")
mqtt_port = get_env("mqtt_port")
mqtt_user = get_env("mqtt_user")
mqtt_pass = get_env("mqtt_pass")
mqtt_item = get_env("mqtt_item")
wifi_ssid = get_env("wifi_ssid")
wifi_pass = get_env("wifi_pass")
if debug == 1: 
    print_variable("WLAN SSID", wifi_ssid, colon_position)
    print_variable("WLAN Secret", wifi_pass, colon_position)
    print_variable("MQTT Server", mqtt_srvr, colon_position)
    print_variable("MQTT Item", mqtt_item, colon_position)
    print()

# Setup LED
led = Pin("LED", Pin.OUT)
led.off()

# Connect to wireless network
if debug == 1: print("Connecting to WLAN %s ..." %wifi_ssid, end="")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_ssid, wifi_pass)
counter = 0
while True:
    led.on()
    wlan.connect(wifi_ssid, wifi_pass)
    sleep(1)
    if wlan.isconnected():
        if debug == 1: print(" Connected!")
        led.off()
        break;
    else:
        if debug == 1: print(".", end="")
        led.off()
        sleep(1)
        counter = counter + 1
        if counter > wlan_connection_retries:
            # reboot and try again
            if debug == 1: print("Unable to connect to WLAN. Restarting ... ")
            led.off()
            sleep(2)
            reset()

# MQTT
client_id = hexlify(unique_id())
if debug == 1: print("Connecting to MQTT %s ..." %mqtt_srvr, end="")
while True:
    led.on()
    try: 
        client = mqtt_connect(client_id, mqtt_srvr, mqtt_port, mqtt_user, mqtt_pass)
        if client:
            if debug == 1: print(" Connected!")
            led.off()
            break;
        else:
            counter = counter + 1
            print(".", end="")
            sleep(5)
    except: 
        print(".", end="")
        sleep(5)
        counter = counter + 1
    if counter > mqtt_connection_retries:
        # reboot and try again
        if debug == 1: print("Unable to connect to MQTT. Restarting ... ")
        led.off()
        sleep(2)
        reset()

print()

# Check switch value
counter = 0
mqtt_fail_count = 0
status_prv = 5 # not zero or one
while True:
    status_val = Pin(15, Pin.IN).value()

    # If we have a new value since the last loop
    if status_prv != status_val: 
        if status_val == 0: status_txt = "Off"
        if status_val == 1: status_txt = "On"
        if debug == 1: print("Status: " + status_txt)
        status_prv = status_val

        try:
            client.publish(mqtt_item, status_txt.lower())
        except OSError as e:
            mqtt_fail_count = mqtt_fail_count + 1
            print("MQTT Publish Error! Attempt " + str(mqtt_fail_count), end="")
            if mqtt_fail_count > mqtt_connection_retries:
                # reboot and try again
                print("Unable to connect to MQTT. Restarting ... ")
                led.off()
                sleep(2)
                reset()
