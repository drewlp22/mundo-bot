import numpy as np
import datetime as dt

class CooldownError(Exception):
    pass

class Player:
    """user = ''
    balance = 0
    owned = []

    mining_cooldown = dt.datetime(dt.MINYEAR, 1, 1)
    minting_cooldown = dt.datetime(dt.MINYEAR, 1, 1)"""

    def __init__(self, name) -> None:
        self.user = name
        self.balance = 0
        self.owned = []
        self.mining_cooldown = dt.datetime(dt.MINYEAR, 1, 1)
        self.minting_cooldown = dt.datetime(dt.MINYEAR, 1, 1)
    """
    Constructs a Player object
    :param name: The player's name
    :return: Returns nothing
    """

    def to_string(self):
        return "User " + self.user + " has " + str(self.balance) + " mundocoins"

    def mine(self):
        if dt.datetime.now() > self.mining_cooldown:
            x_mined = np.random.normal(50, 20)
            self.balance += int(x_mined)
            self.mining_cooldown =  dt.datetime.now() + dt.timedelta(minutes=15)
            return x_mined
        else:
            raise CooldownError

    #For !?give, !?buy, and !?sell commands
    def add(self, count):
        self.balance += count

    def subtract(self, count):
        self.balance -= count

    def add_nft(self, nft, mint=False):
        current_time = dt.datetime.now()
        if mint and (current_time < self.minting_cooldown):
            raise CooldownError
        self.owned.append(nft)
        if mint:
            self.minting_cooldown = current_time + dt.timedelta(7)

    def remove_nft(self, nft):
        self.owned.remove(nft)
        #Throws ValueError

