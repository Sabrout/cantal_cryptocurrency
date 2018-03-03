from src.network.peer import Peer

class Member(Peer):
    def __init__(self, port):
        Peer.__init__(self, port)
        self.member_list = None
        self.transaction_list = None
        self.monney_list = None
        self.blockchain = None

    def set_member_list(self, member_l):
        self.member_list = member_l

    def set_transaction_list(self, transaction_l):
        self.transaction_list = transaction_l

    def set_monney_list(self, monney_l):
        self.monney_list = monney_l

    def set_blockchain(self, blockchain):
        self.blockchain = blockchain