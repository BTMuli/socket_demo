"""
# @Proj: socket_demo
# @Date: 2022/11/27
# @Author: BTMuli
# @Desc: The common config
# @Update: 2022/11/27
"""


class Config:
    """
    The common config
    """
    # The host of server
    server_addr = '127.0.0.1'
    server_port = 8888
    # buffer size
    buffer_size = 1024
    # The max number of users
    SERVER_MAX_BACKLOG = 10
