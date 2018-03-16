import random
import math


class MemberList():

    def __init__(self):
        self.list = {}

    def add_member(self, member):
        # Assuming that the member format is validated (ip, port)
        self.list[member] = 0

    def remove_member(self, member):
        try:
            del self.list[member]
        except ValueError:
            print('Debug: Member not found')
        except KeyError:
            print('Debug: Member not found')

    def is_member(self, member):
        if len(self.list) == 0 or self.list.get(member) is None:
            return False
        else:
            return True

    def print_list(self):
        for i in self.list.keys():
            (ip, port) = i
            print("Member: {}:{}".format(ip, port))

    def get_sublist(self, remove_ip_port=None):
        # Getting number of members to get a ratio for the sublist
        if len(self.list) < 1:
            # Base Case
            return {}
        if len(self.list) == 1:
            # Base Case
            return self.list
        # it depends on the function f(x)=4ln(x+2.5)-4
        num = math.floor((4 * math.log1p(len(self.list) + 2.5)) - 4)
        sublist = random.sample(list(self.list), num)

        if(remove_ip_port is not None):
            try:
                sublist.remove(remove_ip_port)
            except ValueError:
                return sublist
        return sublist

    def get_list(self):
        return list(self.list.keys())

    def __len__(self):
        return len(self.list)

    def __getitem__(self, item):
        member_list = list(self.list.keys())
        return member_list[item]

    def get_random(self):
        size = len(self)
        if size > 0:
            i = random.randint(0, size-1)
            return self[i]
        return None
