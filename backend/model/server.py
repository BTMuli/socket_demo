"""
# @Proj: socket_demo
# @Date: 2022/11/27
# @Author: BTMuli
# @Desc: The model of server
# @Update: 2022/11/27
"""
import socket
import threading
from typing import List

from backend.config.config import Config
from backend.model.message import MessageModel
from backend.model.user import UserModel


class ServerModel:
    """
    The model of server
    """
    server_socket: socket  # 服务器socket
    server_addr: tuple  # 服务器地址
    server_msg: MessageModel  # 服务器消息
    user_list: List[UserModel]  # 用户列表

    def __init__(self, name: str):
        """
        初始化服务器

        :param name: 服务器名
        """
        print('服务器初始化')
        self.server_socket: socket = None
        self.server_addr: tuple = (Config.server_addr, Config.server_port)
        self.server_msg: MessageModel = MessageModel(name, self.server_addr)
        self.user_list: List[UserModel] = []

    def start(self) -> None:
        """
        启动服务器

        :return: None
        """
        print('启动服务器')
        # 创建socket对象
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定端口
        self.server_socket.bind(self.server_addr)
        # 监听
        self.server_socket.listen(Config.SERVER_MAX_BACKLOG)
        print('服务器启动成功')
        # 创建线程
        thread_accept = threading.Thread(target=self.accept_user)  # 接收用户
        thread_send = threading.Thread(target=self.parse_cmd)  # 解析命令
        # 启动线程
        thread_accept.start()
        thread_send.start()
        # 等待线程结束
        thread_accept.join()
        thread_send.join()

    def recv_msg(self, user_socket: socket, user_addr: tuple) -> None:
        """
        接收消息

        :param user_socket: 用户socket
        :param user_addr: 用户地址
        :return: None
        """
        while True:
            # 接收消息
            msg: bytes = user_socket.recv(Config.buffer_size)
            print(f'接收消息:{msg}')
            # 解析消息
            msg_trans = self.parse_msg(msg)
            # 处理消息
            print(f'处理消息:{msg_trans.to_msg()}')
            if msg_trans.get_target() == 'server':
                self.server_msg.set_target(msg_trans.get_origin(), msg_trans.get_origin_addr())
                self.server_msg.set_content('receive')
                self.send_msg(self.server_msg, 'server')
            else:
                # 转发消息
                print(f'转发消息:{msg_trans.to_msg()}')
                self.trans_msg(msg_trans)

    def parse_msg(self, msg: bytes) -> MessageModel:
        """
        解析消息

        :param msg: 消息
        :return: None
        """
        # 解析消息
        msg = self.server_msg.decode_msg(msg)
        return msg

    def send_msg(self, msg: MessageModel, user_name: str) -> None:
        """
        发送消息

        :param msg: 消息
        :param user_name: 用户名
        :return: None
        """
        # 获取用户
        user = self.get_user(user_name)
        if user is None:
            print('用户不存在')
            return
        # 发送消息
        print(f'发送消息:{msg.to_msg()}')
        user.send_msg(msg)

    def trans_msg(self, msg: MessageModel) -> None:
        """
        消息转发

        :param msg:
        :return:
        """
        # 获取目标用户
        user = self.get_user(msg.get_target())
        if user is None:
            print('用户不存在')
            return
        # 转发消息
        user.send_msg(msg)

    def get_user(self, name: str) -> UserModel | None:
        """
        获取用户

        :param name: 用户名
        :return: 用户
        """
        for user in self.user_list:
            if user.user_name == name:
                return user
        return None

    def parse_cmd(self, cmd=None) -> None:
        """
        解析消息

        :param cmd: 消息
        :return: None
        """
        while True:
            if cmd is None:
                cmd = input()
            if cmd == 'exit':
                self.server_socket.close()
                break
            else:
                print('命令错误')
                cmd = None

    def accept_user(self) -> None:
        """
        接收端口，用户连接→发送消息→接收消息→关闭连接

        :return: None
        """
        while True:
            # 接收用户
            user_socket, user_addr = self.server_socket.accept()
            print(f'接收用户:{user_addr}')
            # 接收消息
            msg = user_socket.recv(Config.buffer_size)
            print(f'接收消息:{msg}')
            # 解析消息
            msg_trans = self.parse_msg(msg)
            # 创建用户
            user = UserModel(msg_trans.get_origin())
            # 设置用户socket
            user.set_socket(user_socket)
            # 设置用户地址
            user.set_addr(user_addr)
            # 添加用户
            self.user_list.append(user)
            # 回复该消息的来源地址
            print('回复该消息的来源地址')
            self.server_msg.set_content(f'{user_addr}')
            self.server_msg.set_target(user.user_name, user_addr)
            self.send_msg(self.server_msg, user.user_name)
            # 创建线程
            thread_recv = threading.Thread(target=self.recv_msg, args=(user_socket, user_addr))  # 接收消息
            # 启动线程
            thread_recv.start()


class Server(ServerModel):
    """
    The server base on server_model
    """

    def __init__(self, name: str):
        super().__init__(name)

    def start(self) -> None:
        super().start()

    def parse_cmd(self, cmd=None) -> None:
        super().parse_cmd(cmd)
