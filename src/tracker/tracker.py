from src.tracker.member_list import MemberList
from src.network.peer import Peer
from src.network.message import Message
from threading import Thread
from src.structure.ressource import Ressource
import random
import time


class Tracker(Peer):
    def __init__(self, port):
        Peer.__init__(self, port)
        self.member_list = MemberList()
        self.member_list = Ressource(self.member_list)
        self.main().start()
        self.process_member_list_ping(5).start()
        self.process_member_list_pong().start()

    def process_message(self, tuple):
        (ip, socket, message) = tuple
        # Handling Messages
        if message.get_packet() == Message.LIST:
            # List REQUEST
            # Creating a RESPONSE message

            if message.get_packet_type() == Message.REQUEST:
                # Adding member to list
                port = int(message.get_data())

                member_list = self.member_list.ressource
                self.member_list.write(member_list.add_member, (ip, port))

                response = Message()
                response.set_packet(Message.LIST)
                response.set_packet_type(Message.RESPONSE)

                member_list = self.member_list.ressource
                sublist = self.member_list.read(member_list.get_sublist)
                response.set_data(sublist)
                self.produce_response(socket=socket, message=response, close=True)

            # List ERROR
            elif message.get_packet_type() == Message.ERROR:
                print(message.get_data())

        # Member REPORT
        elif (message.get_packet_type() == Message.REPORT and
            message.get_packet() == Message.MEMBER):
            try:
                ip_port = message.get_data()
            except ValueError:
                raise Exception('Error: Invalid IP Port')
            (ip, port) = ip_port
            self.produce_ping(ip, port)
        else:
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

    def process_member_list_ping(self, sleep):
        def handle_thread():
            member_list = self.member_list.ressource
            member = self.member_list.read(member_list.get_random)

            if member is not None:
                (ip, port) = member
                self.produce_ping(ip, port)

            time.sleep(sleep)

            handle_thread()

        t = Thread(target = handle_thread)
        return t

    def process_member_list_pong(self):
        def handle_thread():
            ip, port, pong = self.consume_pong()
            if(not(pong)):
                member_list = self.member_list.ressource
                self.member_list.write(member_list.remove_list, (ip, port))

            handle_thread()

        t = Thread(target = handle_thread)
        return t


if __name__ == "__main__":
    tracker = Tracker(9990)
    host = tracker.server.get_host_name()
    port = tracker.server.get_port()
    print("Debug: Tracker opened at "+str(host)+":"+str(port))
