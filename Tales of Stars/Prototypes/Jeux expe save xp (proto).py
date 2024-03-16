import random
import time
import pygame
import json

class Player:
    def __init__(self, name, race, player_class):
        self.name = name
        self.race = race
        self.player_class = player_class
        self.level = 1
        self.health = 100
        self.attack = 10
        self.mana = 50 if player_class == "Mage" else 0
        self.exp = 0
        self.exp_needed = 100

    def display_stats(self):
        print(f"{self.name} (Level {self.level}) - {self.race} {self.player_class}")
        print(f"Health: {self.health}, Attack: {self.attack}")
        if self.player_class == "Mage":
            print(f"Mana: {self.mana}")
        print(f"Experience: {self.exp}/{self.exp_needed}")

    def level_up(self):
        if self.exp >= self.exp_needed:
            self.level += 1
            self.exp -= self.exp_needed
            self.exp_needed *= 2  # Example: exp_needed doubles every level up
            print(f"{self.name} leveled up to level {self.level}!")

class Monster:
    def __init__(self, name, health, attack, exp):
        self.name = name
        self.health = health
        self.attack = attack
        self.exp = exp

    def display_stats(self):
        print(f"{self.name} - Health: {self.health}, Attack: {self.attack}")

def jouer_bruit(sound_path):
    pygame.mixer.init()
    son = pygame.mixer.Sound(sound_path)
    son.play()

def battle(player, monster):
    print("Battle Start!")
    while player.health > 0 and monster.health > 0:
        print("\nPlayer's Turn:")
        print("1. Physical Attack")
        if player.player_class == "Mage":
            print("2. Magic Attack")
            print("3. Heal")
        choice = input("Choose your action: ")
        if choice == "1":
            player.attack = random.randint(1, player.attack)
            monster.health -= player.attack
            time.sleep(2)
            jouer_bruit('Sound Effect\\attack-sound.mp3')
            print(f"{player.name} attacks {monster.name} for {player.attack} damage.")
        elif choice == "2" and player.player_class == "Mage":
            if player.mana >= 10:
                player.mana -= 10
                player.attack = random.randint(5, 15)  # Magic attack
                monster.health -= player.attack
                time.sleep(2)
                jouer_bruit('Sound Effect\\magic-sound.mp3')
                print(f"{player.name} casts a magic attack on {monster.name} for {player.attack} damage.")
            else:
                print("Not enough mana to cast a magic attack.")
        elif choice == "3" and player.player_class == "Mage":
            if player.mana >= 20:
                player.mana -= 20
                player.health += 20  # Healing
                time.sleep(2)
                print(f"{player.name} heals for 20 health points.")
            else:
                print("Not enough mana to cast a heal.")
        else:
            print("Invalid choice.")
            continue

        if monster.health <= 0:
            print(f"{monster.name} has been defeated!")
            player.exp += monster.exp
            player.level_up()
            break

        monster_attack = random.randint(1, monster.attack)
        player.health -= monster_attack
        jouer_bruit('Sound Effect\\attack-sound.mp3')
        print(f"{monster.name} attacks {player.name} for {monster_attack} damage.")
        if player.health <= 0:
            jouer_bruit('Sound Effect\\death-sound.mp3')
            print(f"{player.name} has been defeated!")
            print("Restarting the Game...")
            main()

    if player.health > 0:
        player.display_stats()

def save_game(player):
    with open("save.json", "w") as file:
        json.dump(player.__dict__, file)
    print("Game saved successfully.")

def load_game():
    try:
        with open("save.json", "r") as file:
            data = json.load(file)
        player = Player("", "", "")
        player.__dict__.update(data)
        print("Game loaded successfully.")
        return player
    except FileNotFoundError:
        print("No saved game found.")
        return None

def main():
    jouer_bruit('Sound Effect\\Start-Game.mp3')
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

    load_option = input("Do you want to load a saved game? (yes/no): ").lower()
    if load_option == "yes":
        player = load_game()
        if player is None:
            print("Starting a new game...")
            player = Player("", "", "")  # Assurez-vous d'assigner le nouvel objet Player à la variable player
    else:
        player = Player("", "", "")  # Assurez-vous d'assigner le nouvel objet Player à la variable player

    while True:  # Main game loop
        monsters = [
            Monster("Goblin", 20, 5, 50),
            Monster("Mimic", 30, 8, 100),
            Monster("Slime", 15, 3, 30)
        ]
        monster = random.choice(monsters)
        monster.display_stats()

        battle(player, monster)
        
        # Si le joueur a perdu, arrêter la boucle de combat
        if player.health <= 0:
            break

        save_option = input("Do you want to save the game? (yes/no): ").lower()
        if save_option == "yes":
            save_game(player)
        else:
            print("Game not saved.")

        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
