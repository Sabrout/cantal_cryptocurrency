import os


class MoneyList():
    hash_size = 64

    def __init__(self):
        self.list = list()
        path = os.path.normpath(os.path.join(os.getcwd(), "money.list"))
        if not(os.path.exists(path)):
            writer = open('money.list', 'w')
            writer.close()
        else:
            self.read_money()

    def verify(self, money):
        (hash, output) = money
        if len(hash) != self.hash_size:
            raise Exception('Error: Invalid Hash Size')
        if not (int(output) == 0 or int(output) == 1):
            raise Exception('Error: Invalid Output Number')
        return money

    def add_money(self, money):
        money = self.verify(money)
        self.list.append(money)
        writer = open('money.list', 'a')
        writer.write(str(money)+'\n')
        writer.close()

    def remove_money(self, money):
        money = self.verify(money)
        self.list.remove(money)
        writer = open('money.list', 'w')
        for i in self.list:
            writer.write(str(i) + '\n')
        writer.close()

    def save_money(self):
        writer = open('money.list', 'w')
        for i in self.list:
            writer.write(str(i) + '\n')
        writer.close()

    def read_money(self):
        path = os.path.normpath(os.path.join(os.getcwd(), "money.list"))
        if not(os.path.exists(path)):
            raise Exception('Error: File Not Found')
        reader = open('money.list', 'r')
        lines = reader.readlines()
        reader.close()
        for i in lines:
            if i == '' or i == '\n': continue
            output = i[-3]
            hash = i[2:(2 + self.hash_size)]
            self.verify((hash, output))
            self.list.append((hash, int(output)))


# if __name__ == "__main__":
#     money_list = MoneyList()
#     # money_list.add_money(('1234', 0))
#     # money_list.add_money(('4562', 1))
#     # money_list.add_money(('1234', 1))
#     # money_list.add_money(('1235', 0))
#
#     # print(len(money_list.list))
#     for i in money_list.list:
#         print(i)


