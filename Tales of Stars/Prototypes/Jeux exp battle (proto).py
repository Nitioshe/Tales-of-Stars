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
            self.exp_needed *= 2  # Exemple: exp_needed double à chaque passage de niveau
            self.health += 20  # Bonus de santé à chaque passage de niveau
            self.attack += 5  # Bonus d'attaque à chaque passage de niveau
            print(f"{self.name} leveled up to level {self.level}!")


class Monster:
    def __init__(self, name, health, attack, exp_reward):
        self.name = name
        self.health = health
        self.attack = attack
        self.exp_reward = exp_reward

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
                player.attack = random.randint(5, 15)  # Attaque magique
                monster.health -= player.attack
                time.sleep(2)
                jouer_bruit('Sound Effect\\magic-sound.mp3')
                print(f"{player.name} casts a magic attack on {monster.name} for {player.attack} damage.")
            else:
                print("Not enough mana to cast a magic attack.")
        elif choice == "3" and player.player_class == "Mage":
            if player.mana >= 20:
                player.mana -= 20
                player.health += 20  # Soins
                time.sleep(2)
                jouer_bruit('Sound Effect\\heal-sound.mp3')
                print(f"{player.name} heals for 20 health points.")
            else:
                print("Not enough mana to cast a heal.")
        else:
            print("Invalid choice.")
            continue

        if monster.health <= 0:
            print(f"{monster.name} has been defeated!")
            exp_gained = monster.exp_reward
            player.exp += exp_gained
            player.level_up()
            print(f"You gained {exp_gained} experience!")
            print(f"{player.name}'s Current level: {player.level}, Experience: {player.exp}/{player.exp_needed}")
            return True

        monster_attack = random.randint(1, monster.attack)
        player.health -= monster_attack
        jouer_bruit('Sound Effect\\attack-sound.mp3')
        print(f"{monster.name} attacks {player.name} for {monster_attack} damage.")
        if player.health <= 0:
            jouer_bruit('Sound Effect\\death-sound.mp3')
            print(f"{player.name} has been defeated!")
            print("Restarting the Game...")
            return False

    if player.health > 0:
        player.display_stats()


def main():
    jouer_bruit('Sound Effect\\Start-Game.mp3')
    print("Welcome to the Adventure Game!")
    time.sleep(1)

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

    while True:  # Boucle pour gérer les combats successifs
        monsters = [
            Monster("Goblin", 20, 5, 50),
            Monster("Mimic", 30, 8, 100),
            Monster("Slime", 15, 3, 30)
        ]
        monster = random.choice(monsters)
        monster.display_stats()

        result = battle(player, monster)
        if not result:
            break  # Si le joueur a perdu, arrêter la boucle de combat


if __name__ == "__main__":
    main()
