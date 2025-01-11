import mysql.connector
from mysql.connector import Error

# 连接到数据库的函数
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",  # 数据库主机
        user="root",       # 数据库用户名
        password="1234",  # 数据库密码
        database="iot_db"  # 数据库名称
    )

# 获取当前灯泡状态
def get_light_status():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # 获取灯泡状态
        cursor.execute("SELECT status FROM light_status ORDER BY updated_at DESC LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            return result['status']
        else:
            return 0  # 默认灯泡关闭
        
    except Error as e:
        print(f"Error: {e}")
        return 0
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# 修改灯泡状态
def update_light_status(status):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # 更新灯泡状态
        cursor.execute("INSERT INTO light_status (status) VALUES (%s)", (status,))
        connection.commit()
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


