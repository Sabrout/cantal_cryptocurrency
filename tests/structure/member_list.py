import unittest
import random
from src.member_list import MemberList


class MemberListTest(unittest.TestCase):

    def populate(self, size):
        list = MemberList()
        for i in range(size):
            ip = str(random.randint(1, 255)) + '.' + str(random.randint(1, 255)) + '.' \
                 + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255))
            port = '' + str(random.randint(1, 9999))
            list.add_member((ip, port))
        list.print_list()
        return list

    def test_add_member_pos(self):
        list = MemberList()
        list.add_member(('172.0.0.1', '8080'))
        self.assertEqual(list.is_member(('172.0.0.1', '8080')), True)

    def test_add_member_neg(self):
        list = MemberList()
        self.assertEqual(list.is_member(('172.0.0.1', '8080')), False)