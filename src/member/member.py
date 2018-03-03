from src.network.peer import Peer
from src.tracker.member_list import MemberList
from src.structure.cheese_stack import CheeseStack
from src.structure.ressource import Ressource
from src.member.money_list import MoneyList
from src.structure.transaction_list import TransactionList
from threading import Thread


class Member(Peer):
    def __init__(self, port):
        Peer.__init__(self, port)
        self.member_list = MemberList()
        self.cheese_stack = CheeseStack()
        self.member_list = Ressource(self.member_list)
        self.cheese_stack = Ressource(self.cheese_stack)

        self.transaction_list = TransactionList()
        self.transaction_list = Ressource(self.transaction_list)

        self.money_list = Ressource(MoneyList())

    def process_message(self):
        def handle_thread():
            print()
        t = Thread(target=handle_thread)
        return t

    def process_transaction_request(self):
        print()

    def process_member_list(self):
        def handle_thread():
            return "Don't care"
        t = Thread(target=handle_thread)
        return t

    def process_cheese_stack(self):
        def handle_thread():
            return "Don't care"
        t = Thread(target=handle_thread)
        return t

