# -MQTT-

这是一个简单的MTQQ+阿里云+esp8266的简单应用

基本功能
  在单片机按下按钮可以开关灯，数据上传阿里云
  在网页上可以远程控制灯的亮灭和查看灯的状态

文件介绍
  03STC是单片机控制灯亮灭逻辑和通过串口对esp8266发送AT指令，esp8266连接阿里云进行数据交互
  iot是用python flask框架写的前台，可以查看灯的状态和远程控制灯
