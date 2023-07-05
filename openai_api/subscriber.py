import paho.mqtt.client as mqtt

BROKER_IP = "192.168.194.135"
OUTPUT_FILE = "../fine_tuning/raw_data.txt"

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
    # print("Received message on /topic {}: {}".format(message.topic, message.payload))
    file = open(OUTPUT_FILE,"a")
    print("payload: ",message.payload)
    file.write(message.payload.decode('utf-8'))
    # file.write("\n")
    file.close()

# configuring connection
broker = BROKER_IP
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
file = open(OUTPUT_FILE,"w")
client.connect(broker)
# client.loop_start()
client.subscribe("test/status")
client.loop_forever()
# client.subscribe("non-ex")
# client.loop_stop()
