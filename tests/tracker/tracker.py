import unittest
from src.tracker.tracker import Tracker
from src.network.peer import Peer
from tests.tracker.member_list import MemberListTest
from src.network.message import Message


class TrackerTest(unittest.TestCase):

    def test_list_request(self):
        # Tracker
        tracker = Tracker('127.0.0.1', 1111)
        tracker.list = MemberListTest.populate(40)

        client1 = Peer('127.0.0.1', 1111)
        # List Request Message
        request = Message()
        request.set_packet_type(Message.REQUEST)
        request.set_packet(Message.LIST)
        request.set_data(1111)

        client1.produce_response(tracker.client.socket, request)
        tracker.process_message(tracker.consume_receive())
        response = client1.consume_receive()[1]

        # Checking the sublist
        flag = True
        for i in response.get_data():
            if not tracker.list.is_member(i):
                flag = False

        client1.client.socket.close()
        tracker.client.socket.close()
        self.assertEqual(flag, True)

