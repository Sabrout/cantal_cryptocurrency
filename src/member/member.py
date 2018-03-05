from src.network.peer import Peer
from src.tracker.member_list import MemberList
from src.structure.cheese_stack import CheeseStack
from src.structure.transaction import Transaction
from src.structure.transaction_list import TransactionList
from src.structure.ressource import Ressource
from src.network.message import Message
from src.member.ttl import TTL
from src.member.money_list import MoneyList
from threading import Thread
from threading import Event
import time


class Member(Peer):
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


        self.money_list = Ressource(MoneyList())

        self.ttl = TTL(ttl)
        self.ttl = Ressource(self.ttl)

    def process_message(self, tuple):
        (IP, socket, message) = tuple
        print(message.get_packet())
        print(message.get_packet_type())
        # Handling messages
        if(message.get_packet() == Message.LIST):
            if(message.get_packet_type() == Message.RESPONSE):
                print("tada")
                self.process_list_response(message)
        if(message.get_packet() == Message.TRANSACTION):
            if(message.get_packet_type() == Message.REQUEST):
                response = self.process_transaction_request()
                self.produce_response(socket=socket, message=response)
            if(message.get_packet_type() == Message.RESPONSE):
                self.process_transaction_response(message)
            if(message.get_packet_type() == Message.ERROR):
                self.process_transaction_error(message)
        if(message.get_packet() == Message.CHEESE):
            if(message.get_packet_type() == Message.REQUEST):
                response = self.process_cheese_request(message)
                print("sockettte: "+str(socket))
                self.produce_response(socket=socket, message=response)
            if(message.get_packet_type() == Message.RESPONSE):
                self.process_cheese_response(message)
                # Maybe we have to send back a message if the received cheese is bad
            if(message.get_packet_type() == Message.ERROR):
                self.process_cheese_error(message)

    def process_list_response(self, message):
        print("-----------------------")
        print("jean recoi un putain")
        for (ip, port) in message.get_data():
            member_list = self.member_list.ressource
            print((ip,port))
            self.member_list.write(member_list.add_member, (ip, port))
        print("I set the flag to true")
        self.event.set()
        print("I already set it to true")



    def process_transaction_error(self, message):
        print(message.data)

    def process_cheese_request(self, message):
        parent_smell = message.get_data()
        cheese_stack = self.cheese_stack.ressource
        cheese = self.cheese_stack.read(cheese_stack.__getitem__, parent_smell)
        print(cheese)
        if(cheese is not None):
            message = Message.create(Message.CHEESE, Message.RESPONSE, cheese)
        else:
            print("Une erreur")
            #  message = Message.create(Message.CHEESE, Message.ERROR, "Cheese not valid")

        return message

    def process_cheese_response(self, message):
        ttl = self.ttl.ressource
        self.ttl.write(ttl.reset)
        cheese = message.get_data()

        if(cheese.verify(cheese) is True):
            cheese_stack = self.cheese_stack.ressource
            self.cheese_stack.write(cheese_stack.add, cheese)
        else:
            self.procces_cheese_error(message)

    def process_cheese_error(self, message):
        ttl = self.ttl.ressource
        if(self.ttl.read(ttl.is_zero) is True):
            print(message.get_data())
        else:
            self.ttl.write(ttl.decrement)
            print("ttl : "+ str(self.ttl.read(ttl.get_ttl)))


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
            print("list_size")
            if size_member < size:
                print("I set the flag to false")
                self.event.clear()
                print("I already set it false")

                print("size: "+str(size_member))
                message = Message.create(Message.LIST, Message.REQUEST, self.port)
                self.produce_response(IP=self.ip_tracker, port=self.port_tracker, message=message)

            time.sleep(sleep)

            handle_thread()
        t = Thread(target=handle_thread)
        return t

    def process_member_list_ping(self, sleep):
        def handle_thread():
            member_list = self.member_list.ressource
            member = self.member_list.read(member_list.get_random)

            if member is not None:
                (ip, port) = member
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
                message = Message.create(Message.MEMBER, Message.REPORT, (ip, port))
                self.produce_response(IP=self.ip_tracker, port=self.port_tracker, message=message)

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

    def update_cheese_stack(self):
        def handle_thread():
            self.event.wait()
            member_list = self.member_list.ressource
            print("je wait")
            self.event.wait()
            print("j'ai fini de wait")
            if(self.member_list.read(member_list.__len__) != 0):
                ttl = self.ttl.ressource
                cheese_stack = self.cheese_stack.ressource
                while(self.ttl.read(ttl.is_zero) is False):
                    print("COUCOU")
                    last_cheese = self.cheese_stack.read(cheese_stack.last)
                    last_smell = last_cheese.smell
                    time.sleep(1)
                    message = Message.create(Message.CHEESE, Message.REQUEST, last_smell)
                    self.send(message)
                print("PAS COUCOU NORMAL")
            else:
                print("ELSE")
                handle_thread()
        t = Thread(target=handle_thread)
        return t

    def send(self, message):
        member_list = self.member_list.ressource
        (ip, port) = self.member_list.read(member_list.get_random)
        self.produce_response(IP=ip, port=port, message=message)

    def broadcast(self, message):
        member_list = self.member_list.ressource
        member_list = self.member_list.read(member_list.get_list)
        for (ip, port) in member_list:
            self.produce_response(IP=ip, port=port, message=message)

    def init(self):
        event = Event()
        self.process_member_list_size(1, 5).start()
        self.process_member_list_ping(5).start()
        self.process_member_list_pong().start()
        self.update_cheese_stack().start()

    def main(self):
        def handle_thread():
            print("je suis dans le main")
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


if __name__ == "__main__":
    port = 9001
    ip_tracker = "192.168.0.30"
    port_tracker = 9990
    try:
        member = Member(9001, ip_tracker, port_tracker)
        member.init()
        print("AVANT START")
        member.main().start()
        print("APRES MAIN START")
    except (KeyboardInterrupt, SystemExit):
        print("PUNTAIINNN MMAIS JE PETE DES CALBES")
        member.client.close()
        member.server.close()

    print("Debug: Member connected to "+str(ip_tracker)+":"+str(port_tracker))
