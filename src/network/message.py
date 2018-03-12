from src.structure.cheese import Cheese
from src.structure.transaction import Transaction


class Message():
    """
    The message represents all possible
    message of the protocol
    """
    # Packet
    NOTHING = -1
    LIST = 0
    MEMBER = 1
    TRANSACTION = 2
    CHEESE = 3
    PING = 4

    # Packet Type
    RESPONSE = 5
    REQUEST = 6
    BROADCAST = 7
    REPORT = 8
    ERROR = 9

    def __init__(self):
        """
        The constructor will set
        initialize the message
        """
        self.packet = Message.NOTHING
        self.packet_type = Message.NOTHING
        self.data = None

    def create(packet, packet_type, data):
        """
        The function will create a message
        """
        message = Message()
        message.set_packet(packet)
        message.set_packet_type(packet_type)
        message.set_data(data)
        return message

    def set_packet(self, packet):
        """
        Set the packet and verify the
        informations
        """
        if(packet == Message.LIST
           or packet == Message.PING
           or packet == Message.MEMBER
           or packet == Message.TRANSACTION
           or packet == Message.CHEESE):

            self.packet = packet
        else:
            self.packet = Message.NOTHING

    def get_packet(self):
        """
        Get the packet
        """
        return self.packet

    def set_packet_type(self, packet_type):
        """
        Set the packet type and verify the
        informations
        """
        if(packet_type == Message.RESPONSE
           or packet_type == Message.REQUEST
           or packet_type == Message.BROADCAST
           or packet_type == Message.REPORT
           or packet_type == Message.ERROR):

            self.packet_type = packet_type
        else:
            self.packet = Message.NOTHING

    def get_packet_type(self):
        """
        Get the packet type
        """
        return self.packet_type

    def set_data(self, data):
        """
        Set the data
        """
        if(isinstance(data, Cheese)):
            self.data = self.format_cheese(data)
        elif(isinstance(data, Transaction)):
            self.data = self.format_transaction(data)
        else:
            self.data = data

    def get_data(self):
        """
        Get the data
        """
        return self.data

    def format_transaction(self, transaction):
        """
        We convert an object Transaction to a Message
        """
        format_transaction = {}
        format_transaction["input"] = transaction.list_input
        format_transaction["wallet"] = transaction.list_wallet
        format_transaction["amount"] = transaction.list_amount
        format_transaction["signature"] = transaction.list_sign
        return format_transaction

    def format_list_transaction(self, list_transaction):
        """
        We convert an object Transaction List to a Message
        """
        format_transactions = []
        for transaction in list_transaction:
            format_transaction = self.format_transaction(transaction)
            format_transactions.append(format_transaction)
        return format_transactions

    def format_cheese(self, cheese):
        """
        We convert an object Cheese List to a Message
        """
        format_cheese = {}
        data = cheese.data
        format_cheese["transactions"] = self.format_list_transaction(data)
        format_cheese["nonce"] = cheese.nonce
        format_cheese["hash"] = cheese.smell
