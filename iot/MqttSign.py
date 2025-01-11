import hmac
from hashlib import sha1

class AuthIfo:
    mqttClientId = 'k207iDLZRHX.website|securemode=2,signmethod=hmacsha256,timestamp=1736489183403|'
    mqttUsername = 'website&k207iDLZRHX'
    mqttPassword = '3d6dcaf88245016f1818f5ab4e7fc3ac6605f8751bc977c5f34045f5504d52dc'

    def calculate_sign_time(self, productKey, deviceName, deviceSecret, clientId, timeStamp):
        self.mqttClientId = clientId + "|securemode=2,signmethod=hmacsha1,timestamp=" + timeStamp + "|"
        self.mqttUsername = deviceName + "&" + productKey
        content = "clientId" + clientId + "deviceName" + deviceName + "productKey" + productKey + "timestamp" + timeStamp
        self.mqttPassword = hmac.new(deviceSecret.encode(), content.encode(), sha1).hexdigest()

    def calculate_sign(self, productKey, deviceName, deviceSecret, clientId):
        self.mqttClientId = clientId + "|securemode=2,signmethod=hmacsha1|"
        self.mqttUsername = deviceName + "&" + productKey
        content = "clientId" + clientId + "deviceName" + deviceName + "productKey" + productKey
        self.mqttPassword = hmac.new(deviceSecret.encode(), content.encode(), sha1).hexdigest()