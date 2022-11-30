"""
# @Proj: socket_demo
# @Date: 2022/11/27
# @Author: BTMuli
# @Desc: The model of message
# @Update: 2022/11/27
"""
import json


class MessageModel:
    """
    The model of message
    """
    msg_origin: str  # 发送方
    origin_addr: tuple  # 发送方地址
    msg_target: str  # 接收方
    tar_addr: tuple  # 接收方地址
    msg_content: str  # 消息内容

    def __init__(self, origin: str, origin_addr: tuple):
        """
        初始化，默认采用用户的名字作为发送方

        :param origin: 发送方
        :param origin_addr: 发送方地址
        """
        self.msg_origin = origin
        self.origin_addr = origin_addr
        self.msg_target = ''
        self.target_addr = ('', 0)
        self.msg_content = ''

    def encode_msg(self) -> bytes:
        """
        消息编码，object -> bytes

        :return: bytes of message
        """
        msg = {
            'origin': self.msg_origin,
            'origin_addr': self.origin_addr,
            'target': self.msg_target,
            'target_addr': self.target_addr,
            'content': self.msg_content,
        }
        return json.dumps(msg).encode('utf-8')

    def decode_msg(self, msg: bytes) -> 'MessageModel':
        """
        消息解码，bytes -> object

        :param msg: bytes of message
        :return: None
        """
        msg = json.loads(msg.decode('utf-8'))
        self.msg_origin = msg['origin']
        self.origin_addr = msg['origin_addr']
        self.msg_target = msg['target']
        self.target_addr = msg['target_addr']
        self.msg_content = msg['content']
        return self

    def set_target(self, target: str, target_addr: tuple) -> None:
        """
        设置消息接收方

        :param target: 接收方
        :param target_addr: 接收方地址
        :return: None
        """
        self.msg_target = target
        self.target_addr = target_addr

    def set_content(self, content: str) -> None:
        """
        设置消息内容

        :param content: 消息内容
        :return: None
        """
        self.msg_content = content

    def get_origin(self) -> str:
        """
        获取消息发送方

        :return: 发送方
        """
        return self.msg_origin

    def get_origin_addr(self) -> tuple:
        """
        获取消息发送方地址

        :return: 发送方地址
        """
        return self.origin_addr

    def get_target(self) -> str:
        """
        获取消息接收方

        :return: 接收方
        """
        return self.msg_target

    def get_target_addr(self) -> tuple:
        """
        获取消息接收方地址

        :return: 接收方地址
        """
        return self.target_addr

    def get_content(self) -> str:
        """
        获取消息内容

        :return: 消息内容
        """
        return self.msg_content

    def to_msg(self):
        """
        将消息转换为字符串

        :return: 字符串
        """
        return f'From {self.msg_origin} to {self.msg_target}: {self.msg_content}'
