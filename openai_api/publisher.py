import paho.mqtt.client as mqtt
import sys
import time

BROKER_IP = "192.168.194.135"

def on_log(client,userdata,level,buf):
    print("log: "+buf)

def on_connect(client,userdata,flags,rc):
    if rc==0:
        print("connected OK")
    else:
        print("Bad connection, Code=",rc)

# message to be sent

broker = BROKER_IP
client = mqtt.Client("")
client.username_pw_set("pi","123456")

client.on_connect=on_connect
client.on_log=on_log
print("Connecting to broker ", broker)

client.connect(broker)
for i in range(1):
    message = str(time.time())+"rivals of mqtt???\n"
    client.publish("test/status","{}".format(message))
    client.loop_start()
    # time.sleep(1)
    client.loop_stop()
# client.disconnect

