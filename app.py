"""
# @Proj: socket_demo
# @Date: 2022/11/27
# @Author: BTMuli
# @Desc: The main function
# @Update: 2022/11/27
"""
from backend.config.config import Config
from backend.model.server import Server
from backend.model.user import User

if __name__ == '__main__':
    print("请选择服务器或用户")
    choice = input("server or user: ")
    if choice == 'server':
        server = Server('server')
        server.start()
    elif choice == 'user':
        user_name = input("请输入用户名: ")
        user = User(user_name)
        user.start(Config.server_addr, Config.server_port)
