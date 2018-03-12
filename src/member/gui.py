import tkinter
from threading import Thread
from src.structure.transaction import Transaction
from src.network.message import Message
import time


class GUI():
    def __init__(self, member):
        """
        We initialize the GUI
        """

        # We set the member
        self.member = member
        # We set the money
        (self.amount, _) = member.money_list.compute_money()
        # We set the public key
        self.public_key = self.member.crypto.get_public()

        # We initialize the GUI
        self.window = tkinter.Tk()

        # We create the frame for the general information
        self.frame_information = tkinter.Frame(self.window)
        self.frame_information.pack(side=tkinter.TOP)

        # We create a frame which will contain the transaction
        self.frame_transaction = tkinter.Frame(self.window)
        self.frame_transaction.pack(side=tkinter.BOTTOM)

        # We create a sub frame for the transactions
        self.frame_transaction_left = tkinter.Frame(self.frame_transaction)
        self.frame_transaction_left.pack(side=tkinter.LEFT)

        # We create the second sub frame for the transactions
        self.frame_transaction_right = tkinter.Frame(self.frame_transaction)
        self.frame_transaction_right.pack(side=tkinter.RIGHT)

        # We set the amount
        self.amount_text = tkinter.StringVar()
        self.amount_text.set(self.amount)
        self.amount = tkinter.Label(self.frame_information,
                                    textvariable=self.amount_text)
        self.amount.pack(side=tkinter.TOP)

        # We set the wallet public key
        self.wallet_text = tkinter.StringVar()
        self.wallet_text.set(self.public_key)
        self.wallet = tkinter.Label(self.frame_information,
                                    textvariable=self.wallet_text)
        self.wallet.pack(side=tkinter.BOTTOM)

        # We create an entry for the amount
        self.entry_amount = tkinter.Entry(self.frame_transaction_left, bd=5)
        self.entry_amount.pack(side=tkinter.LEFT)

        # We create a text
        self.to_text = tkinter.StringVar()
        self.to_text.set("CantalCoin to")
        self.to = tkinter.Label(self.frame_transaction_left,
                                textvariable=self.to_text)
        self.to.pack(side=tkinter.RIGHT)

        # We create an entry for the receiver
        self.entry_receiver = tkinter.Entry(self.frame_transaction_right, bd=5)
        self.entry_receiver.pack(side=tkinter.LEFT)

        # We create the button Apply
        self.apply = tkinter.Button(self.frame_transaction_right,
                                    text='Apply',
                                    command=self.create_transaction)
        self.apply.pack(side=tkinter.RIGHT)

    def create_transaction(self):
        """
        We will create a transaction after pushing the button
        """
        # We get the amount
        amount = int(self.entry_amount.get())
        # We create the transaction
        transaction_user = Transaction.create_user(self.member.money_list,
                                                   amount,
                                                   self.entry_receiver.get())
        # We add it to the transactions list
        transaction_list = self.member.transaction_list.ressource
        self.member.transaction_list.write(transaction_list.add,
                                           transaction_user)

        # We broadcast the transaction
        message = Message.create(Message.TRANSACTION,
                                 Message.BROADCAST,
                                 transaction_user)
        self.member.broadcast(message)

        self.entry_amount.delete(0, 'end')
        self.entry_receiver.delete(0, 'end')

    def update_money(self, sleep):
        def handle_thread():
            while(not(self.member.event_halt.is_set())):
                (self.amount, _) = self.member.money_list.compute_money()
                self.amount_text.set(self.amount)
                time.sleep(sleep)
        t = Thread(target=handle_thread)
        return t

    def mainloop(self):
        """
        This is the function which will launch the mainloop
        """
        self.member.list_thread.append(self.update_money(3))
        self.member.list_thread[-1].start()
        self.window.mainloop()
