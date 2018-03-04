from src.network.peer import Peer
from src.tracker.member_list import MemberList
from src.structure.cheese_stack import CheeseStack
from src.structure.transaction import Transaction
from src.structure.transaction_list import TransactionList
from src.structure.ressource import Ressource
from src.network.message import Message
from src.member.money_list import MoneyList
from threading import Thread
import random
import time


class Member(Peer):
    def __init__(self, port, ip_tracker, port_tracker):
        Peer.__init__(self, port)
        self.port = port
        self.ip_tracker = ip_tracker
        self.port_tracker = port_tracker

        self.member_list = MemberList()
        self.cheese_stack = CheeseStack()
        self.member_list = Ressource(self.member_list)
        self.cheese_stack = Ressource(self.cheese_stack)

        self.transaction_list = TransactionList()
        self.transaction_list = Ressource(self.transaction_list)


        self.money_list = Ressource(MoneyList())


    def process_message(self, tuple):
        (IP, socket, message) = tuple

        # Handling messages
        if(message.get_packet() == Message.TRANSACTION):
            if(message.get_packet_type() == Message.REQUEST):
                response = self.process_transaction_request()
                self.produce_response(socket=socket, close=True, message=response)
            if(message.get_packet_type() == Message.RESPONSE):
                self.process_transaction_response(message)
            if(message.get_packet_type() == Message.ERROR):
                self.process_transaction_error(message)
        if(message.get_packet() == Message.CHEESE):
            if(message.get_packet_type() == Message.REQUEST):
                response = self.process_cheese_request(message)
                self.produce_response(socket, close=True, message=response)
            if(message.get_packet_type() == Message.RESPONSE):
                self.process_cheese_response(message)
                # Maybe we have to send back a message if the received cheese is bad
            if(message.get_packet_type() == Message.ERROR):
                self.process_cheese_error(message)

    def process_transaction_error(self, message):
        print(message.data)

    def process_cheese_request(self, message):
        parent_smell = message.get_data()
        cheese = self.cheese_stack[parent_smell]

        if(cheese is not None):
            message = Message.create(Message.CHEESE, Message.RESPONSE, cheese)
        else:
            message = Message.create(Message.CHEESE, Message.ERROR, "Cheese not valid")

        return Message

    def process_cheese_response(self, message):
        cheese = message.get_data()

        if(cheese.verify(cheese) is True):
            self.cheese_stack.add(cheese)
        else:
            return None

    def process_cheese_error(self, message):
        print(message.get_data())

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

    def process_member_list_size(self, size, sleep):
        def handle_thread():
            size_member = self.member_list.read(self.member_list.ressource.__len__)
            if size_member < size:
                message = Message(Message.LIST, Message.REQUEST, self.port)
                self.produce_response(ip=self.ip_tracker, port=self.port_tracker, message=message)

            time.sleep(sleep)

            handle_thread()
        t = Thread(target=handle_thread)
        return t

    def process_member_list_ping(self, sleep):
        def handle_thread():
            member_list = self.member_list.ressource
            (ip, port) = self.member_list.read(member_list.get_random)

            self.produce_ping(ip, port)

            time.sleep(sleep)

            handle_thread()
        t = Thread(target=handle_thread)
        return t

    def process_member_list_pong(self):
        def handle_thread():
            ip, port, pong = self.consume_pong()
            if(not(pong)):
                member_list = self.member_list.ressource
                self.member_list.write(member_list.remove_list, (ip, port))
                message = Message(Message.MEMBER, Message.REPORT, (ip, port))
                self.produce_response(ip=self.ip_tracker, port=self.port_tracker, message=message)

            handle_thread()
        t = Thread(target=handle_thread)
        return t

    def process_transaction_list(self, sleep):
        def handle_thread():
            message = Message()
            message.set_packet(Message.TRANSACTION)
            message.set_packet_type(Message.REQUEST)

            self.send(message)

            time.sleep(sleep)
            handle_thread()
        t = Thread(target=handle_thread)
        return t

    def send(self, message):
        member_list = self.member_list.ressource
        (ip, port) = self.member_list.read(member_list.get_random)
        self.produce_response(ip=ip, port=port, message=message)

    def broadcast(self, message):
        member_list = self.member_list.ressource
        member_list = self.member_list.read(member_list.get_list)
        for (ip, port) in member_list:
            self.produce_response(ip=ip, port=port, message=message)

    def main(self):
        def handle_thread():
            self.process_message(self.consume_receive())
            handle_thread()
        t = Thread(target=handle_thread)
        return t

    def mine(self, ntimes):
        def handle_thread():
            self.create_temp_cheese.mine(ntimes)
            handle_thread()
        t = Thread(target=handle_thread)
        return t