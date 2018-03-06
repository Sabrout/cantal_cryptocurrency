from src.network.peer import Peer
from src.tracker.member_list import MemberList
from src.structure.cheese_stack import CheeseStack
from src.structure.transaction import Transaction
from src.structure.transaction_list import TransactionList
from src.structure.ressource import Ressource
from src.structure.crypto import Crypto
from src.network.message import Message
from src.member.ttl import TTL
from src.member.money_list import MoneyList
from src.member.gui import GUI
from threading import Thread
from threading import Event
import time


class Member(Peer):
    """
    Member is the class which represent the member
    """
    def __init__(self, port, ip_tracker, port_tracker, ttl=5):
        self.event = Event()
        Peer.__init__(self, port)
        self.port = port
        self.ip_tracker = ip_tracker
        self.port_tracker = port_tracker

        self.member_list = MemberList()
        self.cheese_stack = CheeseStack.load()
        self.member_list = Ressource(self.member_list)
        self.cheese_stack = Ressource(self.cheese_stack)

        self.transaction_list = TransactionList()
        self.transaction_list = Ressource(self.transaction_list)

        self.money_list = MoneyList(self.cheese_stack)

        self.crypto = Crypto()

        self.ttl = TTL(ttl)
        self.ttl = Ressource(self.ttl)

        self.gui = GUI(self)

    def process_message(self, tuple):
        """
        We will process the data
        """
        (IP, socket, message) = tuple

        # Handling messages
        if(message.get_packet() == Message.LIST):
            if(message.get_packet_type() == Message.RESPONSE):
                # If we have a LIST RESPONSE, we can update the list of members
                self.process_list_response(message)
        if(message.get_packet() == Message.TRANSACTION):
            if(message.get_packet_type() == Message.REQUEST):
                # If we have a transaction request, we can send the last
                # request we receive
                response = self.process_transaction_request()
                self.produce_response(socket=socket, message=response)
            if(message.get_packet_type() == Message.RESPONSE):
                # If we have a transaction response, we store the transaction
                self.process_transaction_response(message)
            if(message.get_packet_type() == Message.ERROR):
                # We can ignore the message
                self.process_transaction_error(message)
        if(message.get_packet() == Message.CHEESE):
            if(message.get_packet_type() == Message.REQUEST):
                # We want to request a cheese
                response = self.process_cheese_request(message)
                self.produce_response(socket=socket, message=response)
            if(message.get_packet_type() == Message.RESPONSE):
                # We want to store the new cheese if we can
                self.process_cheese_response(message)
            if(message.get_packet_type() == Message.ERROR):
                # If we have a cheese error, it means that there is no
                # cheese after
                self.process_cheese_error(message)

    def process_list_response(self, message):
        """
        We process the message LIST RESPONSE
        """
        # For each (ip, port),
        for (ip, port) in message.get_data():
            # we will add the member
            member_list = self.member_list.ressource
            self.member_list.write(member_list.add_member, (ip, port))
        self.event.set()

    def process_transaction_error(self, message):
        """
        We will processe the message TRANSACTION ERROR
        """
        print(message.data)

    def process_cheese_request(self, message):
        """
        We process the message CHEESE REQUEST
        """
        # We get the parent smell
        parent_smell = message.get_data()
        # We get the cheese stak
        cheese_stack = self.cheese_stack.ressource
        # We get the requested cheese
        cheese = self.cheese_stack.read(cheese_stack.__getitem__, parent_smell)
        # If we have the requested cheese,
        if(cheese is not None):
            # we return the response
            message = Message.create(Message.CHEESE, Message.RESPONSE, cheese)
        else:
            # otherwise, we get the cheese error
            message = Message.create(Message.CHEESE, Message.ERROR, None)
        return message

    def process_cheese_response(self, message):
        """
        We process the message CHEESE RESPONSE
        """
        # We get a Time to Live to ask for a cheese
        ttl = self.ttl.ressource
        # If we receive a new cheese, we can reset the cheese
        self.ttl.write(ttl.reset)
        # We get the cheese
        cheese = message.get_data()

        # If the cheese is verified
        if(cheese.verify(cheese)):
            # We add it to the cheese stack
            cheese_stack = self.cheese_stack.ressource
            self.cheese_stack.write(cheese_stack.add, cheese)
        else:
            # Otherwise we process an error
            self.procces_cheese_error(message)

    def process_cheese_error(self, message):
        """
        We process a CHEESE ERROR
        """
        # We get the TTL
        ttl = self.ttl.ressource
        # If the time to live is ... not dead,
        if(not(self.ttl.read(ttl.is_zero))):
            self.ttl.write(ttl.decrement)

    def process_transaction_request(self):
        """
        We process a TRANSACTION REQUEST
        """
        # We get a list of transactions
        transaction_list = self.transaction_list.ressource
        # We get the last transaction
        last = self.transaction_list.read(transaction_list.get_last)

        # We send back the response
        message = Message()
        message.set_packet(Message.TRANSACTION)
        message.set_packet_type(Message.RESPONSE)
        message.set_data(last)
        return message

    def process_transaction_response(self, message):
        # Get the transaction and set the transaction
        data = message.get_data()
        transaction = Transaction(data["input"],
                                  data["wallet"],
                                  data["amount"])

        # We compute the hash
        transaction.compute_hash()
        # We verify it
        transaction.set_list_sign(data["signature"])
        if(not(transaction.verify())):
            # If it's not verify we can ignore the message
            return None

        # We get a list of transactions
        transaction_list = self.transaction_list.ressource
        # We add the transaction in the list
        self.transaction_list.write(transaction_list.ressource.add,
                                    transaction)

    def process_member_list_size(self, size, sleep):
        """
        We will ask a new list of members
        """
        def handle_thread():
            member_list = self.member_list.ressource
            size_member = self.member_list.read(member_list.__len__)
            if size_member < size:
                self.event.clear()

                # We create a message to send to the tracker
                message = Message.create(Message.LIST,
                                         Message.REQUEST,
                                         self.port)
                # and we send it
                self.produce_response(IP=self.ip_tracker,
                                      port=self.port_tracker,
                                      message=message)

            # We ask test the list every sleep seconds
            time.sleep(sleep)

            handle_thread()
        t = Thread(target=handle_thread)
        return t

    def process_member_list_ping(self, sleep):
        """
        We will ping the peers
        """
        def handle_thread():
            # We get the member list
            member_list = self.member_list.ressource
            # We get a member randomly
            member = self.member_list.read(member_list.get_random)

            # We ping the member
            if member is not None:
                (ip, port) = member
                self.produce_ping(ip, port)

            # and we do this operation every sleep seconds
            time.sleep(sleep)

            handle_thread()
        t = Thread(target=handle_thread)
        return t

    def process_member_list_pong(self):
        """
        We receive the response of the ping (i.e the pong)
        """
        def handle_thread():
            # We get the response of a pong
            ip, port, pong = self.consume_pong()
            if(not(pong)):
                # We get the member list
                member_list = self.member_list.ressource
                # We remove the member from our list
                self.member_list.write(member_list.remove_list, (ip, port))
                # and we report to the tracker that a member is not connected
                message = Message.create(Message.MEMBER,
                                         Message.REPORT,
                                         (ip, port))
                self.produce_response(IP=self.ip_tracker,
                                      port=self.port_tracker,
                                      message=message)

            handle_thread()
        t = Thread(target=handle_thread)
        return t

    def update_cheese_stack(self):
        """
        We update the cheese stack
        """
        def handle_thread():
            # Get the member list
            self.event.wait()
            member_list = self.member_list.ressource
            self.event.wait()
            # If the member list is not empty then
            if(self.member_list.read(member_list.__len__) != 0):
                ttl = self.ttl.ressource
                cheese_stack = self.cheese_stack.ressource
                # If the ttl is not dead,
                while(not(self.ttl.read(ttl.is_zero))):
                    # We get the last cheese
                    last_cheese = self.cheese_stack.read(cheese_stack.last)
                    last_smell = last_cheese.smell
                    # and we will ask if there is a new cheese
                    message = Message.create(Message.CHEESE,
                                             Message.REQUEST,
                                             last_smell)
                    self.send(message)
            else:
                handle_thread()
        t = Thread(target=handle_thread)
        return t

    def send(self, message):
        """
        We send a message to a random member
        """
        member_list = self.member_list.ressource
        (ip, port) = self.member_list.read(member_list.get_random)
        self.produce_response(IP=ip, port=port, message=message)

    def broadcast(self, message):
        """
        We send the same message to the peers
        """
        member_list = self.member_list.ressource
        member_list = self.member_list.read(member_list.get_list)
        for (ip, port) in member_list:
            self.produce_response(IP=ip, port=port, message=message)

    def init(self):
        """
        We initialize the threads
        """
        self.process_member_list_size(1, 5).start()
        self.process_member_list_ping(5).start()
        self.process_member_list_pong().start()
        self.update_cheese_stack().start()

    def main(self):
        """
        We process the messages
        """
        def handle_thread():
            self.process_message(self.consume_receive())
            handle_thread()
        t = Thread(target=handle_thread)
        return t

    def mine(self, ntimes):
        """
        We mine the cheese
        """
        def handle_thread():
            self.create_temp_cheese.mine(ntimes)
            handle_thread()
        t = Thread(target=handle_thread)
        return t

    def create(port, ip_tracker, port_tracker):
        # We create the member
        try:
            member = Member(port, ip_tracker, port_tracker)
            member.init()
            member.main().start()
            member.gui.mainloop()
        except (KeyboardInterrupt, SystemExit):
            member.client.close()
            member.server.close()

    def add_money_to_list(self, money):
        money_list = self.money_list.ressource
        self.money_list.write(money_list.add_money, money)


if __name__ == "__main__":
    port = 9001
    ip_tracker = "192.168.1.48"
    port_tracker = 9990
    Member.create(port, ip_tracker, port_tracker)

    print("Debug: Member connected to "+str(ip_tracker)+":"+str(port_tracker))
