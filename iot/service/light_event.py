import json
from iot import IoTDevice
from dao.sql import update_light_status, get_light_status


class Service:
    def __init__(self):
        self.productKey = "k207iDLZRHX"
        self.deviceName = "website"
        self.deviceSecret = "4713662d6aeb2cf7cdd90d86b5def150"
        self.iotdevice = IoTDevice(self.productKey, self.deviceName, self.deviceSecret)
        # Bind callback methods
        
    def light_event(self,status):
        data ={"params": {"LightSwitch": 0}}
        if "params" in data and "LightSwitch" in data["params"]:
            data["params"]["LightSwitch"] = status
        print(data)
        message = json.dumps(data)
        self.iotdevice.publish_light_events(message)

    def light_event_sql(self,status):
        update_light_status(status)
        
    def light_event_get(self):
        return get_light_status()
        