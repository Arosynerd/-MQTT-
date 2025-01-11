#include "Config.h"
#include "GPIO.h"
#include "UART.h"
#include "NVIC.h"
#include "Delay.h"
#define KEY P24
#define LED P40
#define Comand_Lenth 8
void GPIO_config(void)
{
	GPIO_InitTypeDef GPIO_InitStructure;
	GPIO_InitTypeDef GPIO_InitStructure1;
	GPIO_InitStructure.Pin = GPIO_Pin_0 | GPIO_Pin_1;
	GPIO_InitStructure.Mode = GPIO_PullUp;
	GPIO_Inilize(GPIO_P3, &GPIO_InitStructure);
	// P4.0 For LED
	GPIO_Inilize(GPIO_P4, &GPIO_InitStructure);
	// P2.4 For Key

	GPIO_InitStructure1.Pin = GPIO_Pin_4;
	GPIO_InitStructure1.Mode = GPIO_PullUp;
	GPIO_Inilize(GPIO_P2, &GPIO_InitStructure1);
}

void UART_config(void)
{
	COMx_InitDefine COMx_InitStructure;

	COMx_InitStructure.UART_Mode = UART_8bit_BRTx;
	COMx_InitStructure.UART_BRT_Use = BRT_Timer1;
	COMx_InitStructure.UART_BaudRate = 115200ul;
	COMx_InitStructure.UART_RxEnable = ENABLE;
	COMx_InitStructure.BaudRateDouble = DISABLE;
	UART_Configuration(UART1, &COMx_InitStructure);
	NVIC_UART1_Init(ENABLE, Priority_1);

	// UART1_SW(UART1_SW_P30_P31);		//UART1_SW_P30_P31,UART1_SW_P36_P37,UART1_SW_P16_P17,UART1_SW_P43_P44
}
void on_uart_recv()
{
	u8 i;
	for (i = 0; i < COM1.RX_Cnt; i++)
	{
		u8 dat = RX1_Buffer[i];
		TX1_write2buff(dat);
	}
}
void MQTT_publish(char *command, char *payload)
{
	u8 j;
	PrintString1(command);
	for (j = 0; j < 16; j++)
		delay_ms(200);
	PrintString1(payload);
}
void MQTT_connect(char *atCommands[])
{
	u8 j;
	u8 i;
	for (i = 0; i < Comand_Lenth; i++)
	{
		PrintString1(atCommands[i]);
		for (j = 0; j < 8; j++)
			delay_ms(200);
	}
}
void main(void)
{
	static char *atCommands[] = {
		"AT+RST\r\n",
		"ATE0\r\n",
		"AT+CWMODE=3\r\n",
		"AT+CWJAP=\"huawei123\",\"111222333\"\r\n",
		"AT+MQTTUSERCFG=0,1,\"NULL\",\"test&k207iDLZRHX\",\"554aabac8df975d9dd4fee00341af1c60807ae11a1b924cd7fe6b98378b3e7fc\",0,0,\"\"\r\n",
		"AT+MQTTCLIENTID=0,\"k207iDLZRHX.test|securemode=2\\,signmethod=hmacsha256\\,timestamp=1736345621897|\"\r\n",
		"AT+MQTTCONN=0,\"iot-06z00bb9fyfyeq7.mqtt.iothub.aliyuncs.com\",1883,1\r\n",
		"AT+MQTTSUB=0,\"/k207iDLZRHX/test/user/led\",1\r\n",
	};
	u8 temp = 0xFF;
	u8 cmp = 0x00;
	char *publish = "AT+MQTTPUBRAW=0,\"/k207iDLZRHX/test/user/led\",28,1,0\r\n";
	char payload[40];
	GPIO_config();
	UART_config();
	ES = 1;
	EA = 1;
	KEY = 1;
	LED = 1;
	PrintString1("hello world");
	MQTT_connect(atCommands);
	while (1)
	{
		temp = func();
		if (temp != 0xFF)
		{
			if (temp == '0')
				LED = 0;
			else
				LED = 1;
		}

		if (!KEY)
		{
			int i = 1;
			LED = !LED;
			if (LED)
				i = 0;
			delay_ms(250);
			sprintf(payload, "{\"params\":{\"LightSwitch\":%d}}", i);
			// PrintString1(payload);
			MQTT_publish(publish, payload);
		}
	}
}