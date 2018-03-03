from src.tracker.member_list import MemberList
from src.network.peer import Peer
from src.network.message import Message
from threading import Thread


class Tracker(Peer):
    def __init__(self, port):
        Peer.__init__(self, port)

        self.main().start()

    def process_message(self, tuple):
        (ip, message) = tuple

        # Handling Messages
        if message.get_packet() == Message.LIST:

            # List REQUEST
            # Creating a RESPONSE message
            response = Message()
            response.set_packet(Message.LIST)
            response.set_packet_type(Message.RESPONSE)
            response.set_data(self.member_list.get_sublist())
            if message.get_packet_type() == Message.REQUEST:
                # Adding member to list
                try:
                    port = int(message.get_data())
                except ValueError:
                    raise Exception('Error: Invalid Port')
                self.member_list.add_member((ip, port))
                self.produce_response(ip, port, response)

            # List ERROR
            if message.get_packet_type() == Message.ERROR:
                try:
                    port = int(message.get_data())
                except ValueError:
                    raise Exception('Error: Invalid Port')
                self.produce_response(ip, port, response)

        # Member REPORT
        if (message.get_packet_type() == Message.REPORT and
            message.get_packet() == Message.MEMBER):
            # NOOOOTTTTT FINISHEEEDDDD
            # Removing member
            try:
                port = int(message.get_data())
            except ValueError:
                raise Exception('Error: Invalid Port')
            self.member_list.remove_member((ip, port))

    def main(self):
        """
        We create a thread where we accept the connection
        """
        def handle_thread():
            self.process_message(self.consume_receive())
            handle_thread()

        t = Thread(target=handle_thread)
        return t


if __name__ == "__main__":
    tracker = Tracker(9990)
    host = tracker.server.get_host_name()
    port = tracker.server.get_port()
    print("Debug: Tracker opened at "+str(host)+":"+str(port))
