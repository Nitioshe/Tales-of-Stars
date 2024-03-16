import random
import time
import pygame
import json

ascii_art = """
 __ _  __  ____  __    ____  ____  _  _      ____  ____  ____  ____  ____  __ _  ____    _   
(  ( \(  )(_  _)(  )  (    \(  __)/ )( \    (  _ \(  _ \(  __)/ ___)(  __)(  ( \(_  _)  (_)  
/    / )(   )(   )(    ) D ( ) _) \ \/ /_    ) __/ )   / ) _) \___ \ ) _) /    /  )(     _   
\_)__)(__) (__) (__)  (____/(____) \__/(_)  (__)  (__\_)(____)(____/(____)\_)__) (__)   (_)  
"""
ascii_art2 = """
 ____  __   __    ____  ____     __  ____    ____  ____  __   ____  ____ 
(_  _)/ _\ (  )  (  __)/ ___)   /  \(  __)  / ___)(_  _)/ _\ (  _ \/ ___)
  )( /    \/ (_/\ ) _) \___ \  (  O )) _)   \___ \  )( /    \ )   /\___ \ 
 (__)\_/\_/\____/(____)(____/   \__/(__)    (____/ (__)\_/\_/(__\_)(____/
"""

class Player:
    def __init__(self, name, race, player_class):
        self.name = name
        self.race = race
        self.player_class = player_class
        self.level = 1
        self.health = 100
        self.attack = 10
        self.mana = 20 if player_class == "Mage" else 0
        self.agility = 2 if player_class == "Rogue" else 0
        self.dexterity = 2 if player_class == "Samuraï" else 0
        self.exp = 0
        self.exp_needed = 100

    def display_stats(self):
        print(f"{self.name} (Level {self.level}) - {self.race} {self.player_class}")
        print(f"Health: {self.health}, Attack: {self.attack}")
        if self.player_class == "Mage":
            print(f"Mana: {self.mana}")
        elif self.player_class == "Rogue":
            print(f"Agility: {self.agility}")
        elif self.player_class == "Samuraï":
            print(f"Dexterity: {self.dexterity}")
        print(f"Experience: {self.exp}/{self.exp_needed}")

    def level_up(self):
        while self.exp >= self.exp_needed and self.level < 90:  # Ajouter une limite de niveau à 90
            self.level += 1
            self.exp -= self.exp_needed
            self.exp_needed *= 2  # Exemple: exp_needed double 
            self.health += 20  # Bonus de santé 
            self.attack += 5  # Bonus d'attaque 
            if self.player_class == "Mage":
              if self.level==5 or self.level==12 or self.level==25 or self.level==35:
                self.mana +=10
            if self.player_class == "rogue":
              if self.level==5 or self.level==10 or self.level==20 or self.level==30 or self.level==40 or self.level==50 or self.level==15 or self.level==+30:
                self.agility +=1
            if self.player_class == "samurai":
              if self.level==10 or self.level==25 or self.level==70 or self.level==50:
                self.dexterity +=1
            jouer_bruit('Sound Effect\levelup-sound.mp3')
            print(f"{self.name} leveled up to level {self.level}!")
            assert self.exp_needed <=0, "Do not modify data save little fool !!"

        if self.level >= 90:
            print("Maximum level reached.")
        elif self.exp < self.exp_needed:
            print("Not enough experience to level up.")




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

def start_animation():
    jouer_bruit('Sound Effect\logo-sound.wav')
    print(ascii_art)  # Affichage de l'ASCII art
    time.sleep(1)
    print(ascii_art2)
    print("Starting game...", end="", flush=True)
    for _ in range(5):
        time.sleep(0.5)  # Pause de 0.5 seconde
        print(".", end="", flush=True)  # Imprime un point sans saut de ligne
    print("\n")  # Saut de ligne après l'animation

def load_game():
    try:
        with open("save.json", "r") as file:
            data = json.load(file)
        player = Player("", "", "")  #instance Player vide
        player.__dict__.update(data)  #joueur avec les données chargées
        print("Game loaded successfully.")
        print(f"{player.name}'s Current level: {player.level}, Experience: {player.exp}/{player.exp_needed}")
        return player
    except FileNotFoundError:
        print("No saved game found.")
        return None

def load_zone(zone_path):
    try:
        with open(zone_path, "r") as file:
            data = json.load(file)
        print("Zone loaded successfully.")
        print("-")
        print("Zone Name:", data["name"])
        print("Description:", data["description"])
        print("-")
        if "monsters" in data:
            print("Monsters:")
            for monster in data["monsters"]:

                print(f"    - {monster['name']}: Health - {monster['health']}, Attack - {monster['attack']}, Exp Reward - {monster['exp_reward']}")

        if "villagers" in data:
           print("Villagers") 
           for villagers in data["villagers"]:

                print(f"    - {villagers['name']}: {villagers['title']}")

        return data


    except FileNotFoundError:
        print(f"Error: Zone file '{zone_path}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Unable to decode JSON data in '{zone_path}'.")

def mars(player):
  print(f"{player.name} you have commited an horrible mistake ")
  incantation = input("in order to leave you must say the divine incantation: Ostie de câlice de tabarnak ")
  if incantation == "Ostie de câlice de tabarnak":
    return load_zone('Zones\Tettno.json')

def save_game(player):
    data = player.__dict__
    with open("save.json", "w") as file:
        json.dump(data, file)
    print("Game saved successfully.")

def battle(player, monster):
    poison=0
    print("Battle Start!")
    while player.health > 0 and monster.health > 0:
        print("\nPlayer's Turn:")
        print("1. Physical Attack")
        if player.player_class == "Mage":
            print("2. Magic Attack")
            print("3. Heal")
        elif player.player_class == "Rogue":
            print("2. Assault")
            print("3. Fast Kill")
        elif player.player_class == "Samuraï":
            print("2. Meiyō's Technique")
            print("3. Iaijutsu's Technique")
        choice = input("Choose your action: ")
        if choice == "1":
          crit=random.randint(0,100)
          if crit >= 75:
              player_attack=random.randint(player.attack*1.5,player.attack*3)
              monster.health -= player_attack
              time.sleep(2)
              jouer_bruit('Sound Effect\\attack-sound.mp3')
              print(f"CRITICAL HIT !!!\n{player.name} attacks {monster.name} for {player_attack} damage.")
          else:
              player_attack=random.randint(player.attack/2,player.attack)
              monster.health -= player_attack
              time.sleep(2)
              jouer_bruit('Sound Effect\\attack-sound.mp3')
              print(f"{player.name} attacks {monster.name} for {player_attack} damage.")
        elif choice == "2" and player.player_class == "Mage":
            if player.mana >= 10:
                player.mana -= 10
                crit=random.randint(0,100) 
                if crit >= 90:
                  player_attack = random.randint(player.attack*3,player.attack*5)  # Attaque magique
                  monster.health -= player_attack
                  time.sleep(2)
                  jouer_bruit('Sound Effect\\magic-sound.mp3')
                  print(f"CRITICAL HIT !!!\n{player.name} casts a magic attack on {monster.name} for {player_attack} damage.")
                else:
                  player_attack = random.randint(player.attack,player.attack*1.5)  # Attaque magique
                  monster.health -= player_attack
                  time.sleep(2)
                  jouer_bruit('Sound Effect\\magic-sound.mp3')
                  print(f"{player.name} casts a magic attack on {monster.name} for {player_attack} damage.")
            else:
                print("Not enough mana to cast a magic attack.")
        elif choice == "2" and player.player_class == "Rogue":
            if player.agility >= 1:
                player.agility -= 1
                player_attack = random.randint(player.attack/10,player.attack/2)  # Attaque "Assault"
                monster.health -= player_attack
                poison+=1
                time.sleep(2)
                jouer_bruit('Sound Effect\Strike5.wav')
                print(f"{player.name} assault on {monster.name} for {player_attack} damage.")
            else:
                print("Not enough agility point to poison the opponent.")
        elif choice == "2" and player.player_class == "Samuraï":
            if player.dexterity >= 10:
                player.dexterity -= 10
                player_attack = random.randint(15, 25)  # Attaque "Meiyō"
                monster.health -= player_attack
                time.sleep(2)
                jouer_bruit('Sound Effect\Sword1.wav')
                print(f"{player.name} use meiyō's technique on {monster.name} for {player_attack} damage.")
            else:
                print("Not enough dexterity to use meiyō's technique.")
        elif choice == "3" and player.player_class == "Mage":
            if player.mana >= 20:
                player.mana -= 20
                player.health += 20  # Soins
                time.sleep(2)
                jouer_bruit('Sound Effect\heal-sound.wav')
                print(f"{player.name} heals for 20 health points.")
                error=random.randint(0,10000)
                if error==1:
                  jouer_bruit('Sound Effect\\teleport.mp3')
                  load_zone('Zones/mars.json')
                  return mars(player)
            else:
                print("Not enough mana to cast a heal.")
        elif choice == "3" and player.player_class == "Rogue":
            if player.agility >= 20:
                player.agility -= 20
                player_attack = random.randint(20, 30)   # "Fast kill"
                monster.health -= player_attack
                time.sleep(2)
                jouer_bruit('Sound Effect\\assasin-sound.wav')
                print(f"{player.name} fast kill {monster.name} for {player_attack} damage.")
            else:
                print("Not enough agility to fast kill.")
        elif choice == "3" and player.player_class == "Samuraï":
            if player.dexterity >= 10:
                player.dexterity -= 10
                player_attack = random.randint(15, 25)  # Attaque "Iaijutsu"
                monster.health -= player_attack
                time.sleep(2)
                jouer_bruit('Sound Effect\Sword1.wav')
                print(f"{player.name} use iaijutsu's technique on {monster.name} for {player_attack} damage.")
            else:
                print("Not enough dexterity to use iaijutsu's technique.")
        else:
            print("Invalid choice.")
            continue
        if poison>=1:
            player_attack=player_attack/3
            monster.health-=random.randint(player_attack*poison/poison, player.attack*poison)
        if monster.health <= 0:
            print(f"{monster.name} has been defeated!")
            exp_gained = monster.exp_reward
            player.exp += exp_gained
            player.level_up()
            print(f"You gained {exp_gained} experience!")
            print(f"{player.name}'s Current level: {player.level}, Experience: {player.exp}/{player.exp_needed}")
            print("-")
            time.sleep(1)
            player.display_stats()
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
        
        print(f"{player.name}'s Health: {player.health}")
        if player.player_class == "Mage":
          print(f"{player.name}'s Mana: {player.mana}")
        elif player.player_class == "Rogue":
          print(f"{player.name}'s left agility point: {player.agility}")
        elif player.player_class == "Samuraï":
          print(f"{player.name}'s left dexterity point: {player.dexterity}")
        print(f"{monster.name}'s Health: {monster.health}")


def main():
        start_animation()
        jouer_bruit('Sound Effect\\Start-Game.mp3')
        print("Welcome to the Adventure Game!")
        time.sleep(1)

        load_option = input("Do you want to load a saved game? (yes/no): ").lower()
        if load_option == "yes":
            player = load_game()
            if player is None:
                print("Starting a new game...")
                player = create_character()
        else:
            player = create_character()

        print("-")
        time.sleep(5)
        print("??? : Hello adventurer and welcome to the continent, a land of mystery and conflict.")
        time.sleep(5)
        print("??? : It's also a cursed land that awaits its final hour.")
        time.sleep(5)
        print("??? : Dear adventurer, you won't be asked to save this world, but explore it while it still exists!")
        time.sleep(5)
        print("??? : May the stars bless your journey and who knows? maybe we'll meet again...")

        time.sleep(5)
        zone_data = load_zone('Zones\Tettno.json')  # Charger les données de la zone
        if zone_data is None:
            print("Failed to load the zone. Exiting the game.")
            return
        time.sleep(5)
        print("Stout man : HOHO! Are you the new adventurer?")
        time.sleep(5)
        print(f"Me : Yes, my name is {player.name} ")
        time.sleep(5)
        print("Sir Bertram Veridius : And i'm Sir Bertram Veridius, Commander of the Tettno Fortress !")
        time.sleep(5)
        print("Sir Bertram Veridius : Good! Now let's get started on your training!")
        time.sleep(5)
        monster = Monster("Slime", 15, 3, 30)
        monster.display_stats()
        time.sleep(3)
        battle(player, monster)
        time.sleep(3)
        print("Sir Bertram Veridius : HOHO! Now you can explore the world !")
        time.sleep(5)


        zone_data = load_zone('Zones\Forest.json')  # Charger les données de la zone
        if zone_data is None:
            print("Failed to load the zone. Exiting the game.")
            return

        combat_count = 0  # Compteur de combats
        max_combats = 4  # Limite de 4 combats

        while combat_count < max_combats:  # Boucle pour les combats successifs
            monsters_data = zone_data.get("monsters", [])
            if not monsters_data:
                print("No monsters found in the zone. Exiting the game.")
                break

            monsters = [Monster(monster_data["name"], monster_data["health"], monster_data["attack"], monster_data["exp_reward"]) for monster_data in monsters_data]
            monster = random.choice(monsters)
            monster.display_stats()

            result = battle(player, monster)
            combat_count += 1

            if not result:
                break  # Si le joueur a perdu, arrêter la boucle de combat

            save_option = input("Do you want to save the game? (yes/no): ").lower()
            if save_option == "yes":
                jouer_bruit('Sound Effect\save-sound.wav')
                save_game(player)
            else:
                print("Game not saved.")

            quit_option = input("Do you want to quit the game? (yes/no): ").lower()
            if quit_option == "yes":
                jouer_bruit('Sound Effect\game-cut-sound.mp3')
                print("Thanks for playing!")
                break

        if combat_count == max_combats:
            print("You have reached the maximum number of allowed combats.")


def create_character():
    name = input("Enter your name: ")
    time.sleep(1)
    races = ["Human", "Elf", "Dwarf"]
    player_race = input("Choose your race (Human, Elf, Dwarf): ").capitalize()
    while player_race not in races:
        print("Invalid race. Please choose from Human, Elf, or Dwarf.")
        player_race = input("Choose your race (Human, Elf, Dwarf): ").capitalize()

    time.sleep(1)
    classes = ["Warrior", "Mage","Samuraï", "Rogue"]
    player_class = input("Choose your class (Warrior, Mage, Samuraï, Rogue): ").capitalize()
    while player_class not in classes:
        print("Invalid class. Please choose from Warrior, Mage, Samuraï, or Rogue.")
        player_class = input("Choose your class (Warrior, Mage, Samuraï, Rogue): ").capitalize()

    time.sleep(2)
    player = Player(name, player_race, player_class)
    player.display_stats()
    return Player(name, player_race, player_class)



main()



