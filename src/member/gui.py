import tkinter

class GUI():
    def __init__(self):
        self.window = tkinter.Tk()

        self.frame_information = tkinter.Frame(self.window)
        self.frame_information.pack(side=tkinter.TOP)

        self.frame_transaction = tkinter.Frame(self.window)
        self.frame_transaction.pack(side=tkinter.BOTTOM)

        self.frame_transaction_left = tkinter.Frame(self.frame_transaction)
        self.frame_transaction_left.pack(side=tkinter.LEFT)

        self.frame_transaction_right = tkinter.Frame(self.frame_transaction)
        self.frame_transaction_right.pack(side=tkinter.RIGHT)


        # Frame information
        self.amount_text = tkinter.StringVar()
        self.amount_text.set("90")

        self.wallet_text = tkinter.StringVar()
        self.wallet_text.set("APOJDOPJPZADOZAFEHFUIEHIFHEUIFPHAEFUIEHFEIUPAHFEIUFEFIUGAFIUGAGAEF")

        self.amount = tkinter.Label(self.frame_information, textvariable=self.amount_text)
        self.amount.pack(side=tkinter.TOP)

        self.wallet = tkinter.Label(self.frame_information, textvariable=self.wallet_text)
        self.wallet.pack(side=tkinter.BOTTOM)

        # Frame transaction
        self.entry_amount = tkinter.Entry(self.frame_transaction_left, bd=5)
        self.entry_amount.pack(side=tkinter.LEFT)

        self.to_text = tkinter.StringVar()
        self.to_text.set("to")
        self.to = tkinter.Label(self.frame_transaction_left, textvariable=self.to_text)
        self.to.pack(side=tkinter.RIGHT)

        self.entry_receiver = tkinter.Entry(self.frame_transaction_right, bd=5)
        self.entry_receiver.pack(side=tkinter.LEFT)

        self.apply = tkinter.Button(self.frame_transaction_right, text='apply')
        self.apply.pack(side=tkinter.RIGHT)

        print("coucouc")
        self.window.mainloop()

if __name__ == "__main__":
    GUI()
