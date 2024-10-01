import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO


# This is the GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12, GPIO.OUT)


# This is the MQTT Connection Settings
host = "mqtt.beebotte.com"
port = 1883
password = ""
username = "token_FZCQ6qBS2L4G0zDm"
channel = "CPE4040"
resource = "sensor"
defStr = "Temperature"
topic = channel + "/" + resource


def on_connect(client, userdata, flags, rc, properties):
    print("Connected with result code" + str(rc))
    client.subscribe(topic, 1)



def on_message(client, userdata, msg):
    if defStr in str(msg.payload.decode()):
        print("Message Received:", str(msg.payload.decode()))
    elif "ledON" in str(msg.payload.decode()):
        print("LED ON!")
        GPIO.output(12, GPIO.HIGH)
    elif "ledOFF" in str(msg.payload.decode()):
        print("LED OFF!")
        GPIO.output(12, GPIO.LOW)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(username)
client.connect(host,port,60)
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()
