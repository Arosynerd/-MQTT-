from flask import Flask, render_template, jsonify, request
from service.light_event import Service

def create_app():
    app = Flask(__name__)

    service = Service()
    service.iotdevice.start()

    # 控制器：主页
    @app.route('/')
    def index():
        # 从数据库获取灯泡状态
       
        status = service.light_event_get()
        status_text = "ON" if status == 1 else "OFF"
        return render_template('index.html', status=status_text)

    # 控制器：切换灯泡状态
    @app.route('/toggle', methods=['POST'])
    def toggle():
        # 获取当前状态
        current_status = service.light_event_get()
        
        # 切换灯泡状态
        new_status = 0 if current_status == 1 else 1
        
        # 更新数据库中的灯泡状态
        service.light_event_sql(new_status)
        
        #发送MQTT
        service.light_event(new_status)
        
        return jsonify({'status': "ON" if new_status == 1 else "OFF"})

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


