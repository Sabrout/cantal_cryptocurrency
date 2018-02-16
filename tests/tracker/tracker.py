import unittest
from src.tracker.tracker import Tracker
from src.network.peer import Peer
from tests.tracker.member_list import MemberListTest
from src.network.message import Message
import socket


class TrackerTest(unittest.TestCase):

    def test_list_request(self):
        # Tracker
        tracker = Tracker(9990)
        tracker.list = MemberListTest.populate(40)

        client1 = Peer(9991)

        # List Request Message
        request = Message()
        request.set_packet_type(Message.REQUEST)
        request.set_packet(Message.LIST)
        request.set_data(9991)

        client1.produce_response(socket.gethostname(), 9990, request)
        response = client1.consume_receive()[1]

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

    def test_list_error(self):
        # Tracker
        tracker = Tracker(9995)