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
        # Handling Messages

        if message.get_packet() == Message.LIST:

            # List REQUEST
            # Creating a RESPONSE message
            response = Message()
            response.set_packet(Message.LIST)
            response.set_packet_type(Message.RESPONSE)
            response.set_data(self.list.get_sublist())
            if message.get_packet_type() == Message.REQUEST:
                # Adding member to list
                try:
                    port = int(message.get_data())
                except ValueError:
                    raise Exception('Error: Invalid Port')
                self.list.add_member((ip, port))
                Peer.produce_response(self, socket, response)

            # List ERROR
            if message.get_packet_type() == Message.ERROR:
                Peer.produce_response(self, socket, response)

        # Member REPORT
        if message.get_packet_type() == Message.REPORT and message.get_packet() == Message.MEMBER:
            # Removing member
            try:
                port = int(message.get_data())
            except ValueError:
                raise Exception('Error: Invalid Port')
            self.list.remove_member((ip, port))