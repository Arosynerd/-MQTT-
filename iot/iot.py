import json
import time
import paho.mqtt.client as mqtt
from MqttSign import AuthIfo
from service.parse import parse_light_status

class IoTDevice:
    def __init__(self, product_key, device_name, device_secret):
        self.product_key = product_key
        self.device_name = device_name
        self.device_secret = device_secret
        self.client_id = device_name
        self.timestamp = str(int(round(time.time() * 1000)))
        self.sub_topic = f"/{product_key}/{device_name}/user/led"
        self.pub_topic = f"/{product_key}/{device_name}/user/led"
        self.host = f"{product_key}.iot-as-mqtt.cn-shanghai.aliyuncs.com"
        self.port = 1883
        self.tls_crt = "root.crt"
        self.keep_alive = 300
        
        # Calculate and set the MQTT authentication information
        self.auth_info = AuthIfo()
        self.auth_info.calculate_sign_time(product_key, device_name, device_secret, self.client_id, self.timestamp)
        
        self.client = mqtt.Client(self.auth_info.mqttClientId)
        self.client.username_pw_set(username=self.auth_info.mqttUsername, password=self.auth_info.mqttPassword)
        self.client.tls_set(self.tls_crt)
        
        # Bind callback methods
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            print(f"Connection failed with error code: {rc}")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        print(f"Received message on topic: {topic}")
        print(f"Message payload: {payload}")
        statu = parse_light_status(payload)
        if(statu >= 0):
            print("update datas success")
        else:
            print("update datas fail")

        if "thing/service/property/set" in topic:
            self.on_thing_prop_changed(client, topic, payload)

    def on_thing_prop_changed(self, client, topic, payload):
        post_topic = topic.replace("service", "event").replace("set", "post")
        msg = json.loads(payload)
        params = msg['params']
        post_payload = json.dumps({"params": params})
        print(f"Received property_set command, posting to topic: {post_topic}")
        print(f"Post payload: {post_payload}")
        client.publish(post_topic, post_payload)

    def connect(self):
        self.client.connect(self.host, self.port, self.keep_alive)
        self.client.loop_start()

    def subscribe(self):
        self.client.subscribe(self.sub_topic)
        print(f"Subscribed to topic: {self.sub_topic}")

    def publish_message(self, message, delay=2, count=5):
        for i in range(count):
            print(f"Publishing message {i+1}/{count}: {message}")
            self.client.publish(self.pub_topic, message)
            time.sleep(delay)
    def publish_light_events(self, message):
        print(f"Publishing message : {message}")
        self.client.publish(self.pub_topic, message)
        
        

    def start(self):
        self.connect()
        time.sleep(2)
        # self.subscribe()
        # self.publish_light_events(message)
    
    
# if __name__ == "__main__":
#     productKey = "k207iDLZRHX"
#     deviceName = "website"
#     deviceSecret = "4713662d6aeb2cf7cdd90d86b5def150"
    
#     device = IoTDevice(productKey, deviceName, deviceSecret)
#     device.start("{\"params\": {\"LightSwitch\": 0}}")
    
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("Exiting...")
