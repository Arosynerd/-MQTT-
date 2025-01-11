


# 模拟灯泡状态
light_status = False

# 获取灯泡状态
def get_light_status():
    return 'ON' if light_status else 'OFF'

# 切换灯泡状态
def toggle_light():
    global light_status
    light_status = not light_status
    return 'ON' if light_status else 'OFF'