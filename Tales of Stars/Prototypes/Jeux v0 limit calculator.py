import random
import time

class Player:
    def __init__(self, name, race, player_class):
        self.name = name
        self.race = race
        self.player_class = player_class
        self.level = 1
        self.health = 100
        self.attack = 10

    def display_stats(self):
        print("{} (Level {}) - {} {}".format(self.name, self.level, self.race, self.player_class))
        print("Health: {}, Attack: {}".format(self.health, self.attack))

class Monster:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def display_stats(self):
        print("{} - Health: {}, Attack: {}".format(self.name, self.health, self.attack))

def battle(player, monster):
    print("Battle Start!")
    while player.health > 0 and monster.health > 0:
        # Player
        player_attack = random.randint(1, player.attack)
        monster.health -= player_attack
        time.sleep(2)

        print("{} attacks {} for {} damage.".format(player.name, monster.name, player_attack))
        if monster.health <= 0:
            print("{} has been defeated!".format(monster.name))
            break

        # Monster
        monster_attack = random.randint(1, monster.attack)
        player.health -= monster_attack

        print("{} attacks {} for {} damage.".format(monster.name, player.name, monster_attack))
        if player.health <= 0:
            print("{} has been defeated!".format(player.name))
            print("Restarting the Game...")
            main()

        print("")

def main():
    print("Welcome to the Adventure Game!")
    time.sleep(2)
    
    name = "Player"  # You can use an alternative method to get user input on NumWorks
    
    time.sleep(1)
    races = ["Human", "Elf", "Dwarf"]
    player_race = "Elf"  # You can use an alternative method to get user input on NumWorks
    while player_race not in races:
        print("Invalid race. Please choose from Human, Elf, or Dwarf.")
        player_race = "Elf"  # You can use an alternative method to get user input on NumWorks

    time.sleep(1)
    classes = ["Warrior", "Mage", "Rogue"]
    player_class = "Warrior"  # You can use an alternative method to get user input on NumWorks
    while player_class not in classes:
        print("Invalid class. Please choose from Warrior, Mage, or Rogue.")
        player_class = "Warrior"  # You can use an alternative method to get user input on NumWorks

    time.sleep(2)
    player = Player(name, player_race, player_class)
    player.display_stats()

    monster = Monster("Goblin", 20, 5)
    monster.display_stats()

    battle(player, monster)

if __name__ == "__main__":
    main()
