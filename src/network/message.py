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
    # Packet Type
    RESPONSE = 4
    REQUEST = 5
    BROADCAST = 6
    REPORT = 7
    ERROR = 8

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
        self.data = data

    def get_data(self):
        """
        Get the data
        """
        return self.data
