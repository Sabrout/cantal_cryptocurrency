from src.network.peer import Peer
from src.tracker.member_list import MemberList
from src.structure.cheese_stack import CheeseStack
from src.structure.transaction import Transaction
from src.structure.transaction_list import TransactionList
from src.structure.ressource import Ressource
from src.network.message import Message
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

        self.monney_list = Ressource(list())

    def process_message(self):
        def handle_thread():
            print()
        t = Thread(target=handle_thread)
        return t

    def process_transaction_request(self):
        last = self.transaction_list.read(self.transaction_list.ressource.get_last)

        message = Message()
        message.set_packet(Message.TRANSACTION)
        message.set_packet_type(Message.RESPONSE)
        data = {"input": last.list_input, "wallet": last.list_wallet,
                "amount": last.list_amount, "signature": last.list_sign}
        message.set_data(data)
        return message

    def process_transaction_response(self, message):
        data = message.get_data()
        transaction = Transaction(data["input"], data["wallet"], data["amount"])

        transaction.compute_hash()
        transaction.set_list_sign(data["signature"])
        if(not(transaction.verify())):
            return None
        self.transaction_list.write(self.transaction_list.ressource.add, transaction)

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
