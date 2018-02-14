import unittest
import random
from src.tracker.member_list import MemberList


class MemberListTest(unittest.TestCase):

    @staticmethod
    def populate(size):
        list = MemberList()
        for i in range(size):
            ip = str(random.randint(1, 255)) + '.'\
                 + str(random.randint(1, 255)) + '.'\
                 + str(random.randint(1, 255)) + '.' + str(random.randint(1, 255))
            port = '' + str(random.randint(1, 9999))
            list.add_member((ip, port))
        return list

    def test_add_member_pos(self):
        list = MemberList()
        list.add_member(('172.0.0.1', '8080'))
        self.assertEqual(list.is_member(('172.0.0.1', '8080')), True)

    def test_add_member_neg(self):
        list = MemberList()
        self.assertEqual(list.is_member(('172.0.0.1', '8080')), False)

    def test_remove_member_pos(self):
        list = MemberList()
        list.add_member(('172.0.0.1', '8080'))
        # Removing from an existing list
        list.remove_member(('172.0.0.1', '8080'))
        self.assertEqual(list.is_member(('172.0.0.1', '8080')), False)

    def test_get_sublist(self):
        sublist_size = 0
        is_sublist_flag = True
        for i in range(1, 500, 5):
            list = MemberListTest.populate(i)
            sublist = list.get_sublist()
            # Updating the size of the sublist
            sublist_size = max(sublist_size, len(sublist))
            # Checking if all elements of sublist are elements of list
            for j in sublist:
                if not list.is_member(j):
                    is_sublist_flag = False
        self.assertEqual((sublist_size <= 20), True)
        self.assertEqual(is_sublist_flag, True)
