from src.network.peer import Peer

class Member(Peer):
    def __init__(self, port):
        Peer.__init__(self, port)
        self.member_list = MemberList()
        self.cheese_stack = CheeseStack()
        self.member_list = Ressource(self.member_list)
        self.cheese_stack = Ressource(self.cheese_stack)

        self.transaction_list = None
        self.monney_list = None

    def process_message(self, tuple):
        (IP, socket, message) = tuple

        # Handling messages
        if(message.get_packet() == Message.TRANSACTION):
            if(message.get_packet_type() == REQUEST):
                response = self.process_transaction_request()
                self.produce_response(socket, close=True, response)
            if(message.get_packet_type() == RESPONSE):
                self.process_transaction_response(message)
            if(message.get_packet_type() == ERROR):
                self.process_transaction_error(message)
        if(message.get_packet() == Message.CHEESE):
            if(message.get_packet_type() == REQUEST):
                response = self.process_cheese_request(message)
                self.produce_response(socket, close=True, response)
            if(message.get_packet_type() == RESPONSE):
                self.process_cheese_response(message)
                # Maybe we have to send back a message if the received cheese is bad
            if(message.get_packet_type() == ERROR):
                self.process_cheese_error(message)

    def process_transaction_error(self, message):
        print(message.data)
        
    def process_cheese_request(self, message):
        parent_smell = message.get_data()
        cheese = self.cheese_stack[parent_smell]
        
        if(cheese is not None):
            message = Message.create(CHEESE, RESPONSE, cheese)
        else:
            message = Message.create(CHEESE, ERROR, "Cheese not valid")

        return Message

    def process_cheese_response(self, message):
        cheese = message.get_data()

        if(cheese.verify(cheese) is True):
            self.cheese_stack.add(cheese)
        else:
            return None

    def process_cheese_error(self, message):
        print(message.get_data())

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

    def main(self):
        def handle_thread():
            self.process_message(self.consume_receive())
            handle_thread()

        t = Thread(target=handle_thread)
        return t 
