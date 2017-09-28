
import sys
import sqlite3
import random


def main():

    # Open database and initialize location
    conn = sqlite3.connect("adventure.sqlite")
    c = conn.cursor()
    locid = 1

    # Create a list of weapon objects from weapon table
    c.execute('SELECT * FROM {tn}'.
              format(tn="Weapons"))
    rows = c.fetchall()
    weapons = []
    for w in rows:
        weapon = Weapon()
        weapon.store(w)
        weapons.append(weapon)

    # initialize player character
    player = Player()
    player.weapon_equipped = weapons[0]
    print("Hello", player.name)

    while True:

        # Fetch location row from database and create location object
        c.execute('SELECT * FROM {tn} WHERE {cn}=locid'.
                  format(tn="World", cn=locid))
        loc = Location()
        row = c.fetchone()
        loc.store(row)

        # Check for Encounter and create enemy (20% chance)
        if (random.randint(1, 100)) < 20:
            c.execute('SELECT * FROM {tn} ORDER BY RANDOM() LIMIT 1'.
                      format(tn="Enemy"))
            row = c.fetchone()
            enemy = Enemy()
            enemy.store(row)
            loc.enemies.append(enemy)
            print("Enemy :", loc.enemies[0].name)

        # Show world details and prompt for action
        print()
        print('Location:  You are in the', loc.name)
        print()
        print(loc.desc)
        if len(loc.enemies) > 0:
            print("Enemy encountered in this location!  You see a", loc.enemies[0].name)

        print()
        print("You have", player.hp, "health.")
        action = input("What next? ")
        action = action.lower()

        # Travel
        if action in ["north", "south", "east", "west"]:
            nextloc = getattr(loc, action)

            if nextloc > 0:
                locid = nextloc
            else:
                print()
                print("You can't go that way!")

            continue

        # Attack
        if action == "attack":
            Attack(player, loc.enemies[0])

        # User wants to quit
        if action == "q" or action == "quit":
            c.close()
            break


def Attack(player, enemy):

    while enemy.hp > 0 and player.hp > 0:

        # Player attacks
        hit_chance = random.randint(1, 20)

        # See if enemy AC is greater than hit chance (hit)
        if hit_chance < enemy.ac:
            damage = random.randint(1, player.weapon_equipped.damage)
            print(player.name, "has hit the", enemy.name, "for", damage, "damage!")
            enemy.hp -= damage
            print(enemy.name, "has", enemy.hp, "remaining.")
            print()

        # Enemy attacks
        hit_chance = random.randint(1, 20)

        # See if enemy AC is greater than hit chance (hit)
        if hit_chance < player.ac:
            damage = random.randint(1, enemy.damage)
            print(enemy.name, "has hit ", player.name, "for", damage, "damage!")
            player.hp -= damage
            print(player.name, "has", player.hp, "remaining.")
            print()


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
        self.items = []
        self.enemies = []

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
        self.weapons = [1]
        self.weapon_equipped = []


class Enemy:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.hp = 0
        self.ac = 0
        self.damage = 0
        self.inv = []
        self.CONST_ID = 0
        self.CONST_NAME = 1
        self.CONST_HP = 2
        self.CONST_AC = 3
        self.CONST_DAMAGE = 5

    def store(self, row):
        self.id = row[self.CONST_ID]
        self.name = row[self.CONST_NAME]
        self.hp = row[self.CONST_HP]
        self.ac = row[self.CONST_AC]
        self.damage = row[self.CONST_DAMAGE]

#    def spawn(self, c):
#        c.execute('SELECT * FROM {tn} ORDER BY RAND() LIMIT 1'.
#                  format(tn="Enemy"))
#        row = c.fetchone()
#        print("Enemy :", row)


class Weapon:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.damage = 0
        self.CONST_ID = 0
        self.CONST_NAME = 1
        self.CONST_DAMAGE = 2

    def store(self, row):
        self.id = row[self.CONST_ID]
        self.name = row[self.CONST_NAME]
        self.damage = row[self.CONST_DAMAGE]


if __name__ == '__main__':
    main()
