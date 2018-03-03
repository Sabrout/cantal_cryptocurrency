from src.tracker.member_list import MemberList
from src.network.peer import Peer
from src.network.message import Message
from threading import Thread
import random


class Tracker(Peer):
    def __init__(self, port):
        Peer.__init__(self, port)
        self.list = MemberList()
        self.main().start()

    def process_message(self, tuple):
        (ip, socket, message) = tuple
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
                self.produce_response(IP=ip, port=port, message=response)

            # List ERROR
            if message.get_packet_type() == Message.ERROR:
                try:
                    port = int(message.get_data())
                except ValueError:
                    raise Exception('Error: Invalid Port')
                self.produce_response(IP=ip, port=port, message=response)
            return

        # Member REPORT
        if (message.get_packet_type() == Message.REPORT and
            message.get_packet() == Message.MEMBER):
            # NOOOOTTTTT FINISHEEEDDDD
            # Removing member
            print('sstep 1')
            try:
                ip_port = message.get_data()
                print('sstep 2')
            except ValueError:
                raise Exception('Error: Invalid Port')
            self.list.remove_member(ip_port)
            print(self.list.print_list())
            print('sstep 3')
            return

        print('Error: No Message Type Detected\n')

    def main(self):
        """
        We create a thread where we accept the connection
        """
        def handle_thread():
            self.process_message(self.consume_receive())
            handle_thread()

        t = Thread(target=handle_thread)
        return t

    @staticmethod
    def populate(size):
        list = MemberList()
        for i in range(size):
            ip = str(random.randint(1, 255)) + '.'\
                 + str(random.randint(1, 255)) + '.'\
                 + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255))
            port = random.randint(1, 9999)
            list.add_member((ip, port))
        return list

# if __name__ == "__main__":
#     tracker = Tracker(9990)
#     host = tracker.server.get_host_name()
#     port = tracker.server.get_port()
#     print("Debug: Tracker opened at "+str(host)+":"+str(port))
