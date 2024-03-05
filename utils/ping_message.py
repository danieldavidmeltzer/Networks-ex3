import struct


class OperationType:
    REQUEST = 0
    REPLY = 1


class PingMessage:
    # 1 bytes for type + 4 for id
    HEADER_SIZE = 5

    def __init__(self, operation_type, sequence_number, data):
        """
        initialize a pin message
        :param operation_type: the operation type, `OperationType.REQUEST` or `OperationType.REPLY`
        :param sequence_number: the id of the message, should increment each new message
        :param data: data to send with packet
        """
        self.operation_type = operation_type
        self.sequence = sequence_number
        self.data = data

    def to_bytes(self):
        encoded = struct.pack(f'!BI{len(self.data)}s', self.operation_type, self.sequence, self.data)
        return encoded

    @staticmethod
    def from_bytes(encoded):
        operation_type, sequence, data = struct.unpack(f'!BI{len(encoded) - PingMessage.HEADER_SIZE}s', encoded)
        return PingMessage(operation_type, sequence, data)

    def validate_with_reply(self, reply):
        """
        validate that the reply is a valid reply to this message
        :param reply: the reply message
        :return: True if the reply is valid, False otherwise
        """
        return self.sequence == reply.sequence and self.data == reply.data and reply.operation_type == OperationType.REPLY

