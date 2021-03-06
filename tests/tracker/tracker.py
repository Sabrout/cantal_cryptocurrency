import unittest
from src.tracker.tracker import Tracker
from src.network.peer import Peer
from src.network.message import Message
import socket
import time

class TrackerTest(unittest.TestCase):

    # List Request test
    def test_list_request(self):
        # Tracker
        tracker = Tracker(9990)
        tracker.list = Tracker.populate(40)

        client1 = Peer(9991)

        # List Request Message
        request = Message()
        request.set_packet_type(Message.REQUEST)
        request.set_packet(Message.LIST)

        request.set_data(9991)

        client1.produce_response(IP=socket.gethostbyname(socket.gethostname()), port=9990, message=request)
        response = client1.consume_receive()[2]
        # Checking the sublist
        flag = True
        for i in response.get_data():
            if not tracker.list.is_member(i):
                flag = False

        client1.client.close()
        tracker.client.close()
        client1.server.close()
        tracker.server.close()

        self.assertEqual(flag, True)

    # List Error test (making sure that the error message is sent and not how it is generated)
    def test_list_error(self):
        # Tracker
        tracker = Tracker(9995)
        tracker.list = Tracker.populate(40)

        client1= Peer(9992)

        # List Error Message
        request = Message()
        request.set_packet_type(Message.ERROR)
        request.set_packet(Message.LIST)
        request.set_data(9992)

        client1.produce_response(IP=socket.gethostbyname(socket.gethostname()), port=9995, message=request)
        flag = True
        try:
            response = client1.consume_receive()[2]
        except Exception:
            flag = False

        client1.client.close()
        tracker.client.close()
        client1.server.close()
        tracker.server.close()

        self.assertEqual(flag, True)

    # Member Error test
    def test_member_error(self):
        # Tracker
        print('begin')
        tracker = Tracker(9996)
        print(tracker.client)
        print('end')
        tracker.list = Tracker.populate(5)
        print('beginC')
        client1 = Peer(9997)
        print('endC')
        print("step 1")
        # Add the client to Member List
        print(tracker.list.print_list())
        tracker.list.add_member((socket.gethostbyname(client1.server.host_name), client1.server.port))
        print("step 2")
        print(tracker.list.print_list())
        # List Request Message
        request = Message()
        request.set_packet_type(Message.REPORT)
        request.set_packet(Message.MEMBER)
        request.set_data((socket.gethostbyname(client1.server.host_name), client1.server.port))
        print("step 3")
        client1.produce_response(IP=socket.gethostbyname(socket.gethostname()), port=9996, message=request)
        print("step 4")
        # NOOOOOOOOOT FINISHEDDDDDDDDDDDDDD
        print("step 5")
        # Checking if Client is in Member List
        flag = tracker.list.is_member((socket.gethostbyname(client1.server.host_name), client1.server.port))
        print(flag)
        print("step 6")

        #time.sleep(2)
        print('Socket '+ str(client1.client.socket))
        client1.client.close()
        #tracker.client.close()
        client1.server.close()
        tracker.server.close()

        print("fini")
        self.assertEqual(flag, True)
