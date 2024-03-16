
import random
import time
import pygame


class Player:
    def __init__(self, name, race, player_class):
        self.name = name
        self.race = race
        self.player_class = player_class
        self.level = 1
        self.health = 100
        self.attack = 10

    def display_stats(self):
        print(f"{self.name} (Level {self.level}) - {self.race} {self.player_class}")
        print(f"Health: {self.health}, Attack: {self.attack}")

class Monster:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def display_stats(self):
        print(f"{self.name} - Health: {self.health}, Attack: {self.attack}")


def jouer_bruit(sound_path):
    pygame.mixer.init()
    son = pygame.mixer.Sound(sound_path)  
    son.play()


def battle(player, monster):
    print("Battle Start!")
    while player.health > 0 and monster.health > 0:
        # Player
        player_attack = random.randint(1, player.attack)
        monster.health -= player_attack
        time.sleep(2)
        jouer_bruit('Sound Effect\\attack-sound.mp3')
        print(f"{player.name} attacks {monster.name} for {player_attack} damage.")
        if monster.health <= 0:
            print(f"{monster.name} has been defeated!")
            break

        # Monster
        monster_attack = random.randint(1, monster.attack)
        player.health -= monster_attack
        jouer_bruit('Sound Effect\\attack-sound.mp3')
        print(f"{monster.name} attacks {player.name} for {monster_attack} damage.")
        if player.health <= 0:
            jouer_bruit('Sound Effect\death-sound.mp3')
            print(f"{player.name} has been defeated!")
            print("Restarting the Game...")
            main()
        
        print("")


def main():
    
    jouer_bruit('Sound Effect\Start-Game.mp3')
    print("Welcome to the Adventure Game!")
    time.sleep(2)
    
    name = input("Enter your name: ")

    time.sleep(1)
    races = ["Human", "Elf", "Dwarf"]
    player_race = input("Choose your race (Human, Elf, Dwarf): ").capitalize()
    while player_race not in races:
        print("Invalid race. Please choose from Human, Elf, or Dwarf.")
        player_race = input("Choose your race (Human, Elf, Dwarf): ").capitalize()

    time.sleep(1)
    classes = ["Warrior", "Mage", "Rogue"]
    player_class = input("Choose your class (Warrior, Mage, Rogue): ").capitalize()
    while player_class not in classes:
        print("Invalid class. Please choose from Warrior, Mage, or Rogue.")
        player_class = input("Choose your class (Warrior, Mage, Rogue): ").capitalize()

    time.sleep(2)
    player = Player(name, player_race, player_class)
    player.display_stats()


    monster = Monster("Goblin", 20, 5)
    monster.display_stats()


    battle(player, monster)

if __name__ == "__main__":
    main()

