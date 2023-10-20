import paho.mqtt.client as mqtt
import os

# ensure that ip address is updated in env file
BROKER_IP = os.getenv("PI_IP_ADDRESS")
print("broker: ",BROKER_IP)
# BROKER_IP = os.getenv("PI_IP_ADDRESS")
VIBRATION_OUTPUT_FILE = "../fine_tuning/data/vibration_raw_data.txt"
LIGHT_OUTPUT_FILE = "../fine_tuning/data/light_raw_data.txt"
ROBOT_OUTPUT_FILE = "../robot/data/robot_raw_data.txt"

LIGHT_TOPIC = "light"
VIBRAITON_TOPIC = "vibration"
ROBOT_TOPIC = "robot"

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
    # light 
    print("payload: ",message.payload)

    """
    light_file = open(LIGHT_OUTPUT_FILE,"a")
    vibration_file = open(VIBRATION_OUTPUT_FILE,"a")
    print("Received message on /topic {}: {}".format(message.topic, message.payload))
    if message.topic==LIGHT_TOPIC:
        light_file.write(message.payload.decode('utf-8'))
    elif message.topic==VIBRAITON_TOPIC:
        vibration_file.write(message.payload.decode('utf-8'))
    """

    robot_file = open(ROBOT_OUTPUT_FILE,"a")
    if message.topic==ROBOT_TOPIC:
        robot_file.write(message.payload.decode('utf-8'))

    file.close()

# configuring connection
broker = BROKER_IP
client = mqtt.Client("sub")
client.username_pw_set("pi","123456")

# Subscribe to topic
# topic = "test/status"

# Set callback functions
client.on_message = on_message
client.on_connect=on_connect
client.on_log=on_log

# starting 
print("Connecting to broker ", broker)
# file = open(LIGHT_OUTPUT_FILE,"w")
# file = open(VIBRATION_OUTPUT_FILE,"w")
file = open(ROBOT_OUTPUT_FILE,"w")

client.connect(broker)
# client.loop_start()

# client.subscribe(LIGHT_TOPIC)
# client.subscribe(VIBRAITON_TOPIC)
client.subscribe(ROBOT_TOPIC)

client.loop_forever()
# client.subscribe("non-ex")
# client.loop_stop()
