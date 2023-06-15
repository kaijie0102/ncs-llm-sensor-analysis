import paho.mqtt.client as mqtt

# callback to output log
def on_log(client,userdata,level,buf):
    print("log: "+buf)

# callback to confirm connection
def on_connect(client,userdata,flags,rc):
    if rc==0:
        print("connected OK")
    else:
        print("Bad connection, Code=",rc)

# callback to output message received by client
def on_message(client, userdata, message):
    # print("im in here")
    print("Received message on topic {}: {}".format(message.topic, message.payload))
    file = open("mqtt_message.txt","w")
    file.write(message.payload.decode('utf-8'))
    file.close()

# configuring connection
broker = "192.168.88.209"
client = mqtt.Client("sub")
client.username_pw_set("pi","123456")

# Subscribe to topic
topic = "test/status"

# Set callback functions
client.on_message = on_message
client.on_connect=on_connect
client.on_log=on_log

# starting 
print("Connecting to broker ", broker)
client.connect(broker)
client.loop_start()
client.subscribe(topic)
client.loop_forever()
# client.loop_stop()
