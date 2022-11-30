"""
# @Proj: socket_demo
# @Date: 2022/11/27
# @Author: BTMuli
# @Desc: The model of user
# @Update: 2022/11/27
"""
import socket
import threading

from backend.config.config import Config
from backend.model.message import MessageModel


class UserModel:
    """
    The model of user
    """
    user_socket: socket  # 用户socket
    user_name: str  # 用户名作为唯一标识
    user_addr: tuple  # 用户地址
    user_msg: MessageModel  # 用户消息

    def __init__(self, name: str):
        """
        初始化用户

        :param name: 用户名
        """
        print('用户初始化')
        self.user_socket: socket = None
        self.user_name: str = name
        self.user_addr: tuple = ('', 0)
        self.user_msg: MessageModel = MessageModel(name, self.user_addr)

    def set_socket(self, _socket: socket) -> None:
        """
        设置用户socket

        :param _socket: socket
        :return: None
        """
        print('设置用户socket')
        self.user_socket = _socket

    def set_msg(self, msg: MessageModel) -> None:
        """
        设置用户消息

        :param msg: 用户消息
        :return: None
        """
        print(f'设置用户消息:{msg}')
        self.user_msg = msg

    def get_socket(self) -> object:
        """
        获取用户socket

        :return: socket
        """
        print(f'获取用户socket:{self.user_socket}')
        return self.user_socket

    def get_msg(self) -> object:
        """
        获取用户消息

        :return: 用户消息
        """
        print(f'获取用户消息:{self.user_msg}')
        return self.user_msg

    def get_name(self) -> str:
        """
        获取用户名

        :return: 用户名
        """
        print(f'获取用户名:{self.user_name}')
        return self.user_name

    def send_msg(self, msg: MessageModel) -> None:
        """
        发送消息

        :param msg: 消息
        :return: None
        """
        print(f'发送消息')
        send_msg = msg.encode_msg()
        print(f'消息编码:{send_msg}')
        self.user_socket.send(send_msg)

    def recv_msg(self, msg: bytes) -> None:
        """
        接收消息

        :return: 消息
        """
        self.user_msg.decode_msg(msg)
        print(f'接收到来自{self.user_msg.get_origin()}的消息:{self.user_msg.get_content()}')

    def set_addr(self, user_addr):
        """
        设置用户地址

        :param user_addr: 用户地址
        :return: None
        """
        print(f'设置用户地址:{user_addr}')
        self.user_addr = user_addr

    def get_addr(self):
        """
        获取用户地址

        :return: 用户地址
        """
        print(f'获取用户地址:{self.user_addr}')
        return self.user_addr


class User(UserModel):
    """
    The user base on user_model
    """

    def __init__(self, name: str):
        """
        初始化用户

        :param name: 用户名
        """
        super().__init__(name)
        self.user_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user_name = name
        self.user_addr = ('', 0)
        self.user_msg = MessageModel(name, ('', 0))

    def start(self, ip: str, port: int) -> None:
        """
        连接服务器，连接成功后，会自动发送用户名，等待服务器回复

        :param ip: 服务器ip
        :param port: 服务器端口
        :return: None
        """
        print(f'连接服务器:{ip}:{port}')
        self.user_socket.connect((ip, port))
        # 发送用户名
        print(f'发送用户名:{self.user_name}')
        self.user_msg.set_target('server', (Config.server_addr, Config.server_port))
        self.user_msg.set_content(self.user_name)
        self.send_msg(self.user_msg)
        # 接收服务器回复
        print('接收服务器回复')
        msg = self.user_socket.recv(Config.buffer_size)
        self.recv_msg(msg)
        # 设置用户地址
        self.parse_addr()
        print(f'用户地址:{self.user_addr}')
        # 创建线程
        thread_recv = threading.Thread(target=self.recv_thread)
        thread_send = threading.Thread(target=self.parse_cmd)
        # 启动线程
        thread_recv.start()
        thread_send.start()
        # 等待线程结束
        thread_recv.join()
        thread_send.join()

    def parse_addr(self) -> None:
        """
        解析用户地址

        :return: None
        """
        print(f'解析用户地址:{self.user_msg.get_target_addr()}')
        self.user_addr = tuple(self.user_msg.get_target_addr())
        self.user_msg = MessageModel(self.user_name, self.user_addr)

    def recv_thread(self) -> None:
        """
        接收消息线程

        :return: None
        """
        print('接收消息线程启动')
        while True:
            msg = self.user_socket.recv(Config.buffer_size)
            self.recv_msg(msg)
            print(f'接收消息:{self.user_msg.to_msg()}')

    def parse_cmd(self) -> None:
        """
        解析命令线程

        :return: None
        """
        while True:
            cmd = input()
            if cmd == 'exit':
                break
            elif cmd == 'send':
                target = input('请输入目标:')
                content = input('请输入内容:')
                self.user_msg.set_target(target, ('', 0))
                self.user_msg.set_content(content)
                self.send_msg(self.user_msg)
            else:
                print('命令错误')

    def send_thread(self) -> None:
        """
        发送消息线程

        :return: None
        """
        print('发送消息线程启动')
        while True:
            msg = input()
            self.user_msg.set_content(msg)
            self.send_msg(self.user_msg)

    def close(self) -> None:
        """
        关闭连接

        :return: None
        """
        self.user_socket.close()
