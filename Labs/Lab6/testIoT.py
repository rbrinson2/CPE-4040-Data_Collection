from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
import json

import max30102
import hrcalc

m = max30102.MAX30102()

host = "a1s0215me7aosd-ats.iot.us-east-2.amazonaws.com"
certPath = "/home/rbrin/Documents/connect_device_package/"
clientId = "pi4"
topic = "sensor"
# topic = "$aws/things/myRPi/shadow/update"


# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(
    "{}root-CA.crt".format(certPath),
    "{}CPE4040_HRM.private.key".format(certPath),
    "{}CPE4040_HRM.cert.pem".format(certPath),
)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(
    -1
)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.connect()

# Publish to the same topic in a loop forever
dataHR = []
while True:
    red, ir = m.read_sequential()

    hr, hr_valid, spo2, spo2_valid = hrcalc.calc_hr_and_spo2(
        ir[:100], red[:100]
    )  # Calculating heart rate and SpO2 values from raw data.

    messageJson = json.dumps(
        {"HRvalue": hr, "HRvalid": hr_valid, "SpO2value": spo2, "SpO2valid": spo2_valid}
    )
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    print("Published topic %s: %s\n" % (topic, messageJson))
#    time.sleep(1)
myAWSIoTMQTTClient.disconnect()
