from collections import deque


class MemberList():

    list = {}

    def __init__(self):
        self.list = {}

    def add_member(self, member):
        # Assuming that the member format is validated (ip, port)
        self.list[member] = 0

    def remove_member(self, member):
        try:
            self.list.__delitem__(member)
        except ValueError:
            raise Exception('MEMBER NOT FOUND ERROR')

    def print_list(self):
        for i in self.list.keys():
            (ip, port) = i
            print("Member: {}:{}".format(ip, port))


def main():
    list = MemberList()
    list.add_member(('172.0.0.1', '8080'))
    list.add_member(('172.0.0.2', '8081'))

    print("---------")
    list.print_list()

    list.remove_member(('172.0.0.2', '8081'))

    print("---------")
    list.print_list()


if __name__ == "__main__":
    main()