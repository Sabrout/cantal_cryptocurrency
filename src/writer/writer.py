from src.network.message import Message

class Writer():

    def __init__(self, message):
        self.message = message
        self.write()

    def write(self):
        if(self.message.packet == Message.LIST
           and self.message.packet_type == Message.REQUEST):
            return self.write_list_request()
        elif (self.message.packet == Message.LIST
           and self.message.packet_type == Message.RESPONSE):
            return self.write_list_response()
        elif (self.message.packet == Message.LIST
           and self.message.packet_type == Message.ERROR):
            return self.write_list_error()

        elif (self.message.packet == Message.MEMBER
           and self.message.packet_type == Message.REPORT):
            return self.write_member_report()

        elif (self.message.packet == Message.TRANSACTION
           and self.message.packet_type == Message.REQUEST):
            return self.write_transaction_request()
        elif (self.message.packet == Message.TRANSACTION
           and self.message.packet_type == Message.RESPONSE):
            return self.write_transaction_response()
        elif (self.message.packet == Message.TRANSACTION
           and self.message.packet_type == Message.ERROR):
            return self.write_transaction_error()

        elif (self.message.packet == Message.CHEESE
           and self.message.packet_type == Message.REQUEST):
            return self.write_cheese_request()
        elif (self.message.packet == Message.CHEESE
           and self.message.packet_type == Message.RESPONSE):
            return self.write_cheese_response()
        elif (self.message.packet == Message.CHEESE
           and self.message.packet_type == Message.ERROR):
            return self.write_cheese_error()

    def write_list_request(self):
        port = self.message.get_data()
        string = "LIST REQUEST "+str(port)+"\r\n"
        return string

    def write_list_response(self):
        string = "LIST RESPONSE"

        list_ip_port = self.message.get_data()
        for (ip, port) in list_ip_port:
            string += " "+ip+" "+str(port)

        string += "\r\n"
        return string

    def write_list_error(self):
        string = "LIST ERROR\r\n"
        return string

    def write_member_report(self):
        (ip, port) = self.message.get_data()
        string = "MEMBER REPORT "+ip+" "+str(port)+"\r\n"
        return string

    def write_transaction_request(self):
        return "TRANSACTION REQUEST\r\n"

    def write_transaction_response(self):
        string = "TRANSACTION RESPONSE"
        string = self.write_transaction(string)+"\r\n"
        return string

    def write_transaction_error(self):
        string = "TRANSACTION ERROR\r\n"
        return string

    def write_cheese_request(self):
        smell = self.message.get_data()
        return "CHEESE REQUEST "+str(smell)+"\r\n"

    def write_cheese_response(self):
        string = "CHEESE RESPONSE"
        data = self.message.get_data()
        string = self.write_transaction_list(string)
        string += " "+str(data["nonce"])+"\r\n"
        return string

    def write_cheese_error(self):
        string = "CHEESE ERROR\r\n"
        return string

    def write_transaction_list(self, string):
        original_data = self.message.get_data()
        transaction_list = original_data["transactions"]
        for transaction in transaction_list:
            self.message.set_data(transaction)
            string = self.write_transaction(string)

        self.message.set_data(original_data)
        return string

    def write_transaction(self, string):
        string = self.write_input_list(string)
        string = self.write_wallet_list(string)
        string = self.write_amount_list(string)
        string = self.write_signature_list(string)
        return string

    def write_input_list(self, string):
        input_list = self.message.get_data()["input"]

        for (hash, output) in input_list:
            string += " "+hash+" "+str(output)

        return string

    def write_wallet_list(self, string):
        wallet_list = self.message.get_data()["wallet"]

        for wallet in wallet_list:
            string += " "+wallet

        return string

    def write_amount_list(self, string):
        amount_list = self.message.get_data()["amount"]

        for amount in amount_list:
            string += " "+str(amount)

        return string

    def write_signature_list(self, string):
        signature_list = self.message.get_data()["signature"]

        for signature in signature_list:
            string += " "+signature

        return string
