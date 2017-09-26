
import sys
import sqlite3


def main():

    # initialize character
    player = Player()
    print("Hello", player.name)

    # Open database and initialize location
    conn = sqlite3.connect("adventure.sqlite")
    c = conn.cursor()
    locid = 1

    while True:

        # Fetch location row from database and create location object
        c.execute('SELECT * FROM {tn} WHERE {cn}=locid'.
                  format(tn="World", cn=locid))
        loc = Location()
        row = c.fetchone()
        loc.store(row)

        # Show world details and prompt for action
        print()
        print('Location:  You are in the', loc.name)
        print()
        print(loc.desc)
        print()
        action = input("What next? ")

        # Travel
        if action.upper() in ["NORTH", "SOUTH", "EAST", "WEST"]:
            nav_action = action.lower()
            nextloc = getattr(loc, nav_action)

            if nextloc > 0:
                locid = nextloc
            else:
                print()
                print("You can't go that way!")

            continue

        # User wants to quit
        if action.upper() == "Q" or action.upper() == "QUIT":
            c.close()
            break


class Location:
    def __init__(self):
        self.locid = 0
        self.name = ""
        self.desc = ""
        self.north = 0
        self.south = 0
        self.east = 0
        self.west = 0
        self.CONST_LOCID = 0
        self.CONST_LOCATION = 1
        self.CONST_DESC = 2
        self.CONST_NORTH = 3
        self.CONST_SOUTH = 4
        self.CONST_EAST = 5
        self.CONST_WEST = 6
        self.weapons = []

    def store(self, row):
        self.locid = row[self.CONST_LOCID]
        self.name = row[self.CONST_LOCATION]
        self.desc = row[self.CONST_DESC]
        self.north = row[self.CONST_NORTH]
        self.south = row[self.CONST_SOUTH]
        self.east = row[self.CONST_EAST]
        self.west = row[self.CONST_WEST]


class Player:
    def __init__(self):
        self.name = input("Enter your player's name: ")
        self.hp = 100
        self.ac = 20
        self.inv = []
        self.weapons = []


class Enemy:
    def __init__(self):
        self.name = ""
        self.hp = 0
        self.ac = 0
        self.inv = []


class Weapon:
    def __init__(self):
        self.wid = 0
        self.name = ""
        self.damage = 0


if __name__ == '__main__':
    main()
