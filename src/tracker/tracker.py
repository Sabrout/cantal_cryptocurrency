from src.tracker.member_list import MemberList
from src.network.peer import Peer
from src.network.message import Message


class Tracker(Peer):
    def __init__(self, IP, port):
        Peer.__init__(self, IP, port)
        self.list = MemberList()

    def process_message(self, tuple):
        (socket, message) = tuple
        ip = socket.getsockname()[0]
        # Handling Requests
        if message.packet_type == Message.REQUEST:
            # List REQUEST
            if message.packet == Message.LIST:
                # Creating a RESPONSE message
                response = Message()
                response.set_packet(Message.LIST)
                response.set_packet_type(Message.RESPONSE)
                response.set_data(self.list.get_sublist())
                # Adding member to list

                self.list.add_member((ip, int(message.data)))



print(int('a11'))