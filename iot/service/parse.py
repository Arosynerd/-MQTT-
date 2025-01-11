import json
from dao.sql import update_light_status


def parse_light_status(json_data):
    # 解析 JSON 数据
    data = json.loads(json_data)
    
    # 获取 LightSwitch 的值
    light_switch = data.get("params").get("LightSwitch")
    
    # 返回对应的状态
    if light_switch == 1:
        status =  1
    elif light_switch == 0:
        status =  0
    else:
        status =  -1
        
    if status >= 0:
        update_light_status(status)
    else:
        print("Error: Invalid status value")
    return status
        
    
    
    