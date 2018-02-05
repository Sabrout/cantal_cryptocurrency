class Message():

    NOTHING = -1
    LIST = 0
    MEMBER = 1
    TRANSACTION = 2
    CHEESE = 3

    RESPONSE = 4
    REQUEST = 5
    REPORT = 6
    ERROR = 7

    def __init__(self):
        self.packet = Message.NOTHING
        self.packet_type = Message.NOTHING
        self.data = None

    def set_packet(self, packet):
        if(packet == Message.LIST
           or packet == Message.MEMBER
           or packet == Message.TRANSACTION
           or packet == Message.CHEESE):

            self.packet = packet

    def get_packet(self):
        return self.packet

    def set_packet_type(self, packet_type):
        if(packet_type == Message.RESPONSE
           or packet_type == Message.REQUEST
           or packet_type == Message.REPORT
           or packet_type == Message.ERROR):

            self.packet_type = packet_type

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data
