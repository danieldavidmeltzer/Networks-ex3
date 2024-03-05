#!/usr/bin/python3
import argparse
import socket

from utils import constants
from utils.ping_message import PingMessage, OperationType


def main():
    args = parse_arguments()

    # receive pings from client
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as agent_socket:
        agent_socket.bind((args.ip, args.port))
        while True:
            message, address = agent_socket.recvfrom(constants.BUFFER_SIZE)
            ping_message = PingMessage.from_bytes(message)
            ping_message.operation_type = OperationType.REPLY
            agent_socket.sendto(ping_message.to_bytes(), address)


def parse_arguments():
    parser = argparse.ArgumentParser(description='UDP Agent')
    parser.add_argument('ip', type=str, help='host to connect to')
    parser.add_argument('-p', dest='port', default=1337, type=int, help='port to bind to(default 1337)')
    return parser.parse_args()


if __name__ == '__main__':
    main()
