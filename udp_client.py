#!/usr/bin/python3
import argparse
import socket
import time

from utils import constants
from utils.ping_message import PingMessage, OperationType


def handle_ping(address, client_socket, ping_request, timeout):
    """
    send ping to destination and wait for reply
    :param address: address to send to
    :param client_socket: sockt to send on
    :param timeout: timeout in seconds
    :param ping_request: the ping request message
    :return: True if reply received, False otherwise
    """
    # send ping request
    try:
        client_socket.sendto(ping_request.to_bytes(), address)
    except socket.error as e:
        print(f"request timeout for icmp_seq {ping_request.sequence}")
        return False
    sent_time = time.time()

    # wait for reply
    try:
        # continue to receive until the correct packet is received, or until timeout
        while (time.time() - sent_time) < timeout:

            client_socket.settimeout(max(timeout - (time.time() - sent_time), 0.001))

            message, (agent_ip, agent_port) = client_socket.recvfrom(constants.BUFFER_SIZE)
            ping_reply = PingMessage.from_bytes(message)

            if not ping_request.validate_with_reply(ping_reply):
                continue
            else:
                print(f"{len(message)} bytes from {agent_ip}:"
                      f" seq={ping_request.sequence}"
                      f" rtt={time.time() - sent_time:.3f}ms")
                return True
    except socket.timeout:
        print(f"request timeout for icmp_seq {ping_request.sequence}")
    return False


def parse_arguments():
    parser = argparse.ArgumentParser(description='UDP Agent')
    parser.add_argument('ip', type=str, help='host to connect to')
    parser.add_argument('-p', dest='port', default=1337, type=int, help='host to connect to(default 1337)')
    parser.add_argument('-c', dest='count', default=10, type=int, help='num of messages to send(default 10)')
    parser.add_argument('-s', dest='size', default=100, type=int, help='data size to send(default 100)')
    parser.add_argument('-t', dest='timeout', default=1000, type=int, help='timeout in ms(default 1000)')
    return parser.parse_args()


def main():
    args = parse_arguments()

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        address = (args.ip, args.port)
        successful_pings = 0

        for seq_num in range(args.count):
            ping_request = PingMessage(OperationType.REQUEST, seq_num, b'0' * args.size)
            ping_result_successful = handle_ping(address, client_socket, ping_request, args.timeout / 1000)

            if ping_result_successful:
                successful_pings += 1

        success_rate = (successful_pings / args.count) * 100
        failure_rate = 100 - success_rate

        print(f"--- {args.ip} statistics ---")
        print(f"{args.count} packets transmitted, {successful_pings} packets received,"
              f" {failure_rate:.2f}% packet loss")


if __name__ == '__main__':
    main()
