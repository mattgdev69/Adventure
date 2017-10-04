import sqlite3
import random
import time


def main():

    # Open database and initialize location
    conn = sqlite3.connect("adventure.sqlite")
    c = conn.cursor()
    # locid = 1

    # Create a list of weapon objects from weapon table
    c.execute('SELECT * FROM {tn}'.
              format(tn="Weapons"))
    rows = c.fetchall()
    weapons = []
    for w in rows:
        weapon = Weapon()
        weapon.store(w)
        weapons.append(weapon)

    # Create a list of location objects from location table
    # Set current_loc to first location
    c.execute('SELECT * FROM {tn}'.
              format(tn="World"))
    rows = c.fetchall()
    locations = []
    for l in rows:
        loc = Location()
        loc.store(l, weapons)
        locations.append(loc)
    current_loc = locations[0]

    # initialize player character
    player = Player(weapons)
    print("Hello", player.name)

    # Main loop
    while True:

        # There is a 20% chance an enemy will appear in the current area if
        # not already present
        if (random.randint(1, 100)) < 20 and len(current_loc.enemies) == 0:
            c.execute('SELECT * FROM {tn} ORDER BY RANDOM() LIMIT 1'.
                      format(tn="Enemy"))
            row = c.fetchone()
            enemy = Enemy()
            enemy.store(row)
            current_loc.enemies.append(enemy)

        # Show world details and prompt for action
        print()
        print('Location:  You are in the', current_loc.name)
        print()
        print(current_loc.desc)
        if len(current_loc.weapons) > 0:
            print("You see a", current_loc.weapons[0].name, "in this area.")
        if len(current_loc.enemies) > 0:
            print("Enemy encountered in this location!  You see a", current_loc.enemies[0].name)
        print()
        print("You have", player.hp, "health.")
        action = input("What next? ")
        action = action.lower()

        # Travel
        if action in ["north", "south", "east", "west"]:
            nextloc = getattr(current_loc, action)

            # Set current location to new location traveled
            if nextloc > 0:
                for l in locations:
                    if l.locid == nextloc:
                        current_loc = l
            else:
                print()
                print("You can't go that way!")
            continue

        # Get weapon.  Add it to player inventory and remove from location.
        if action[:3] == "get":
            weapon = action[4:]
            if current_loc.weapons[0].name.lower() == weapon:
                player.weapons.append(current_loc.weapons[0])
                del current_loc.weapons[0]
                print("You picked up the", weapon)
                print()
            else:
                print("You can't do that!")
                print()

        # Equip weapon in inventory
        if action[:5] == "equip":
            weapon = action[6:]
            player.equip(weapon)

        # List player inventory
        if action[:3] == "inv":
            player.inventory()

        # Attack
        if action == "attack":
            Attack(player, current_loc)
            if player.hp <= 0:
                action = "q"
                print(player.name, "has died!")

        # User wants to quit
        if action == "q" or action == "quit":
            c.close()
            break


# Combat routine
def Attack(player, loc):

    enemy = loc.enemies[0]
    while enemy.hp > 0 and player.hp > 0:

        # Player attacks
        hit_chance = random.randint(1, 20)

        # See if enemy AC is greater than hit chance (hit)
        if hit_chance < enemy.ac:
            # Damage is a random number between 1 and the player's max damage
            damage = random.randint(1, player.weapon_equipped.damage)
            print(player.name, "has hit the", enemy.name, "for", damage, "damage!")
            enemy.hp -= damage
            if enemy.hp > 0:
                print(enemy.name, "has", enemy.hp, "HP remaining.")
            else:
                print("The", enemy.name, "is dead!")
                del loc.enemies[0]
                break
            print()
        else:
            print(player.name, "has missed the", enemy.name)
            print()

        # Enemy attacks
        time.sleep(0.5)
        hit_chance = random.randint(1, 20)

        # See if player AC is greater than hit chance (hit)
        if hit_chance < player.ac:
            # Damage is a random number between 1 and the enemy's max damage
            damage = random.randint(1, enemy.damage)
            print(enemy.name, "has hit", player.name, "for", damage, "damage!")
            player.hp -= damage
            print(player.name, "has", player.hp, "HP remaining.")
            print()
        else:
            print(enemy.name, "has missed!")
            print()

        time.sleep(0.5)


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
        self.CONST_WEAPONS = 7
        self.weapons = []
        self.enemies = []

    def store(self, row, weapons):
        self.locid = row[self.CONST_LOCID]
        self.name = row[self.CONST_LOCATION]
        self.desc = row[self.CONST_DESC]
        self.north = row[self.CONST_NORTH]
        self.south = row[self.CONST_SOUTH]
        self.east = row[self.CONST_EAST]
        self.west = row[self.CONST_WEST]
        for w in weapons:
            if w.id == row[self.CONST_WEAPONS]:
                self.weapons.append(w)


class Player:
    def __init__(self, weapons):
        self.name = input("Enter your player's name: ")
        self.hp = 100
        self.ac = 20
        self.weapons = []
        for w in weapons:
            if w.id == 1:
                self.weapons.append(w)
        self.weapon_equipped = self.weapons[0]

    def equip(self, weapon):
        current_weapon = self.weapon_equipped
        for w in self.weapons:
            if w.name.lower() == weapon:
                self.weapon_equipped = w
                print (self.weapon_equipped.name, "equipped.")
                break
        if self.weapon_equipped == current_weapon:
            print("Weapon not in inventory!")
            print()

    def inventory(self):
        print("Weapons in inventory:")
        weapon = ""
        for w in self.weapons:
            if self.weapon_equipped.name == w.name:
                weapon = w.name + "*"
            else:
                weapon = w.name
            print(weapon)


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
