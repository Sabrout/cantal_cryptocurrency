from src.tracker.member_list import MemberList
from src.network.peer import Peer


class Tracker(Peer):
    def __init__(self, IP, port):
        Peer.__init__(self, IP, port)
        self.list = MemberList()

    def add_member(self, new_member):
        self.list.add_member(new_member)

    def remove_member(self, member):
        self.list.remove_member(member)

    def get_sublist(self):
        return self.get_sublist()