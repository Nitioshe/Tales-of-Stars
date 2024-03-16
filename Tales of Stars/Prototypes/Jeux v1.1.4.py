import random
import time
import pygame
import json

player_zone = ""
self = ""

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
    self.max_health = 100
    self.health = self.max_health
    self.attack = 10
    self.mana = 20 if player_class == "Mage" else 0
    self.maxmana = 20 if player_class == "Mage" else 0
    self.agility = 2 if player_class == "Rogue" else 0
    self.maxagility = 2 if player_class == "Rogue" else 0
    self.dexterity = 2 if player_class == "Samuraï" else 0
    self.maxdexterity = 2 if player_class == "Samuraï" else 0
    self.exp = 0
    self.exp_needed = 100
    self.inventory = Inventory

  def display_stats(self):
    print(
        f"{self.name} (Level {self.level}) - {self.race} {self.player_class}")
    print(f"Health: {self.health}, Attack: {self.attack}")
    if self.player_class == "Mage":
      print(f"Mana: {self.mana}")
    elif self.player_class == "Rogue":
      print(f"Agility: {self.agility}")
    elif self.player_class == "Samuraï":
      print(f"Dexterity: {self.dexterity}")
    print(f"Experience: {self.exp}/{self.exp_needed}")
  
  def display_inventory(self):
        print("-")
        print(f"{self.name}'s Inventory:")
        if not self.inventory:
            print("Empty")
        else:
            for item, quantity in self.inventory.items():
                print(f" - {item}: {quantity}")

  def level_up(self):
    while self.exp >= self.exp_needed and self.level < 90:  # Ajouter une limite de niveau à 90
      self.level += 1
      self.exp -= self.exp_needed
      self.exp_needed *= 2  # Exemple: exp_needed double
      self.health += 20
      self.max_health += 20  # Bonus de santé
      self.attack += 5  # Bonus d'attaque
      if self.player_class == "Mage":
        if self.level == 5 or self.level == 12 or self.level == 25 or self.level == 35:
          self.mana += 10
          self.maxmana += 10
      if self.player_class == "Rogue":
        if self.level == 5 or self.level == 10 or self.level == 20 or self.level == 30 or self.level == 40 or self.level == 50 or self.level == 15 or self.level == +30:
          self.agility += 1
          self.maxagility += 1
      if self.player_class == "Samuraï":
        if self.level == 10 or self.level == 25 or self.level == 70 or self.level == 50:
          self.dexterity += 1
          self.maxdexterity += 1
      jouer_bruit('Sound Effect\levelup-sound.mp3')
      print(f"{self.name} leveled up to level {self.level}!")
      assert self.exp_needed < 0, "Do not modify data save little fool !!"

    if self.level >= 90:
      print("Maximum level reached.")
    elif self.exp < self.exp_needed:
      print("Not enough experience to level up.")


class Monster:

  def __init__(self, name, health, attack, exp_reward, drop):
    self.name = name
    self.health = health
    self.attack = attack
    self.exp_reward = exp_reward
    self.drop = drop

  def display_stats(self):
    print(f"{self.name} - Health: {self.health}, Attack: {self.attack}")


def monster_drop(monster, data):
  if "monsters" in data and monster.name in data["monsters"]:
    drop_table = data["monsters"][monster.name].get("drop", {})
    dropped_items = []
    for item, chance in drop_table.items():
      if random.random() < chance:
        dropped_items.append(item)
    print(f"The {monster.name} dropped: {', '.join(dropped_items)}")


class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item_name, quantity):
        item_name = item_name.lower()
        if item_name in self.items:
            self.items[item_name] += quantity
        else:
            self.items[item_name] = quantity

    def remove_item(self, item_name, item_quantity):
        if item_name in self.items:
            self.items[item_name] -= item_quantity
            if self.items[item_name] <= 0:
                del self.items[item_name]

    def display_inventory(self):
        print("Player's Inventory:")
        for item, quantity in self.items.items():
                print(f"{item}: {quantity}")
        else:
          if not self.items:
            print("Empty")
            

    def save_inventory(self):
        with open('Saves\\Inventory.json', 'w') as file:
            json.dump(self.items, file)

    def load_inventory(self):
        try:
            with open('Saves\\Inventory.json', 'r') as file:
                self.items = json.load(file)
        except FileNotFoundError:
            self.items = {}
            print("Inventory file not found. Starting with an empty inventory.")



class CraftingSystem:

  def __init__(self):
    self.recipes = {
        "Health Potion": {
            "Slime Gall": 1,
            "Water": 1,
            "Bottle": 1
        },
        "Mana Potion": {
            "Magic Essence": 1,
            "Water": 1,
            "Bottle": 1
        },
        "Stamina Potion": {
            "Energy Extract": 1,
            "Water": 1,
            "Bottle": 1
        },
    }
    pass

  def craft(self, recipe_name, inventory):
    if recipe_name in self.recipes:
      recipe = self.recipes[recipe_name]
      ingredients_available = True
      for ingredient, quantity in recipe.items():
        if ingredient.lower() not in map(
            str.lower, inventory) or inventory[ingredient] < quantity:
          print(f"You don't have enough {ingredient} to craft {recipe_name}.")
          ingredients_available = False
          break
      if ingredients_available:
        for ingredient, quantity in recipe.items():
          inventory[ingredient] -= quantity
        print(f"You have crafted {recipe_name}!")
        player_inventory = Inventory()
        player_inventory.add_item(f"{recipe_name}", 1)
    else:
      print("Invalid recipe name.")

  def list_possible_craft(self, inventory):
    possible_crafts = []
    for recipe_name, recipe in self.recipes.items():
      craft_possible = True
      for ingredient, quantity in recipe.items():
        if ingredient.lower() not in map(
            str.lower, inventory) or inventory[ingredient.lower()] < quantity:
          craft_possible = False
          break
      if craft_possible:
        possible_crafts.append(recipe_name)
    return possible_crafts


def jouer_bruit(sound_path):
  pygame.mixer.init()
  son = pygame.mixer.Sound(sound_path)
  son.play()

def NotAvailable(player, inventory):
      print("This part of the story is not yet available, please come back later.")
      return Tettno_main(self, player, inventory, CraftingSystem, player_zone)

def start_animation():
  jouer_bruit('Sound Effect\\logo-sound.wav')
  print(ascii_art)  # Affichage de l'ASCII art
  time.sleep(1)
  print(ascii_art2)
  print("Starting game...", end="", flush=True)
  for _ in range(5):
    time.sleep(0.5)  # Pause de 0.5 seconde
    print(".", end="", flush=True)  # Imprime un point sans saut de ligne
  print("\n")  # Saut de ligne après l'animation


def save_game(player):
  data = {
      "player": player.__dict__,
  }
  with open("Saves\\save.json", "w") as file:
    json.dump(data, file)
  print("Game saved successfully.")


def load_game(self):
  try:
    with open("Saves\\save.json", "r") as file:
      data = json.load(file)
    for i in data:
      self[i] = data[i]
    print("Game loaded successfully.")
    return self

  except FileNotFoundError:
    print("No saved game found.")
    return None, None, None


def load_zone(zone_path):
  try:
    with open(zone_path, "r") as file:
      data = json.load(file)
    time.sleep(1)
    print("Zone loaded successfully.")
    global player_zone
    player_zone = zone_path
    print("-")
    print("Zone Name:", data["name"])
    time.sleep(2)
    print("Description:", data["description"])
    print("-")
    time.sleep(2)
    if "monsters" in data:
      print("Monsters:")
      for monster in data["monsters"]:

        print(f"    - {monster['name']}: Health - {monster['health']}, Attack - {monster['attack']}, ")

    if "villagers" in data:
      print("Villagers:")
      for villagers in data["villagers"]:

        print(f"    - {villagers['name']}: {villagers['title']}")

    return data

  except FileNotFoundError:
    print(f"Error: Zone file '{zone_path}' not found.")
  except json.JSONDecodeError:
    print(f"Error: Unable to decode JSON data in '{zone_path}'.")


def mars(player):
  print(f"{player.name} you have commited an horrible mistake ")
  incantation = input(
      "in order to leave you must say the divine incantation: Ostie de câlice de tabarnak "
  )
  if incantation == "Ostie de câlice de tabarnak":
    return load_zone('Zones\Tettno.json')

def Bank(self, player, inventory, CraftingSystem, player_zone):
  load_zone('Zones\\bank.json')
  print("What do you want to do ?\n1-Go somewhere else\n2-Deposit\n3-Withdraw\n4-See your inventory")
  choice = input("Enter your choice: ")
  if choice == "1":
    return Tettno_main(self, player, inventory, CraftingSystem, player_zone)
  elif choice == "2":
    return NotAvailable(player, inventory)    #En Mise à jour
    return  deposit
  elif choice == "3":
    return NotAvailable(player, inventory)    #En Mise à jour
    return  #withdraw
  elif choice == "4":
    inventory.display_inventory()
    return Bank(self, player, inventory, CraftingSystem, player_zone)

def Adventurers_guild(self, player, inventory, CraftingSystem, player_zone):
  load_zone('Zones\\adventurer_guild.json')
  print("What do you want to do ?\n1-Speak to someone\n2-See your inventory\n3-Go Somewhere else\n4-Craft Somthing")
  choice = input("Enter your choice: ")
  if choice == "1":
    print("who do you want to speak to ?\n1-Katheryne\n2-Diluc\n3-Kafka")
    choice2 = input("Enter your choice: ")
    if choice2 == 1:
      return NotAvailable(player, inventory)    #En Mise à jour
      return  #Katheryne(player, inventory, CraftingSystem,player_zone)

    elif choice2 == 2:
      return NotAvailable(player, inventory)    #En Mise à jour
      return  #Diluc(player, inventory, CraftingSystem,player_zone)

    elif choice2 == 3:
      with open("Saves\\progress.json", "r") as file:
        add = json.load(file)
      kafka = add.get("Kafka", 0)
      kafka += 1
      data = {"Kafka": kafka}
      add.update(data)
      with open("Saves\\progress.json", "w") as file:
        json.dump(add, file)
      if kafka == 1:
        print(f"Kafka : Hello Babygirl, are you new around here ?")
        jouer_bruit('Sound Effect\\Kafka.mp3')
        time.sleep(5)
        print(
            f"Me : Yes, I'm {player.name}, I am the new adventurer endorsded by Sir Bertram Veridius."
        )
        print(f"Kafka : Ah, it's you i've heard of you")
        print(
            f"Kafka : I have a question for you.\ndo you prefer [1] eating fish & chip's or [2] chating with me ?"
        )
        choice3 = input("Enter your choice: ")
        print(f"Kafka : I see")
        return Adventurers_guild(player, inventory, CraftingSystem, player_zone)
      else:
        return Adventurers_guild(player, inventory, CraftingSystem, player_zone)
  elif choice == "2":
    player.display_inventory()
    return Adventurers_guild(player, inventory, CraftingSystem, player_zone)

  elif choice == "3":
    print(f"Where do you want to go ?\n1-Tettno")
    choice2 = input("Enter your choice: ")
    if choice == 1:
      return Tettno_main(self, player, inventory, CraftingSystem, player_zone)
    else:
      return Adventurers_guild(player, inventory, CraftingSystem, player_zone)

  elif choice == "4":
    crafting_system = CraftingSystem()
    inventory = {"Slime Gall": 4, "Water": 4, "Bottle": 4}
    possible_crafts = crafting_system.list_possible_craft(inventory)

    print("Possible Crafts:")
    for craft in possible_crafts:
      print(possible_crafts)
      print("Enter the name of the craft you want to perform, or 'back' to go back:")
      craft_choice = input()
      if craft_choice == "back":
        return Adventurers_guild(player, inventory, CraftingSystem, player_zone)

    print("Current Inventory:")
    for item, quantity in inventory.items():
      print(f"{item}: {quantity}")

    recipe_name = "Health Potion"
    print(f"\nAttempting to craft {recipe_name}...")
    crafting_system.craft(recipe_name, inventory)

    print("\nUpdated Inventory:")
    for item, quantity in inventory.items():
      print(f"{item}: {quantity}")

  else:
    return Adventurers_guild(self, player, inventory, CraftingSystem, player_zone)

def Forest(self, player, inventory, CraftingSystem, player_zone):
  zone_data = load_zone('Zones\\Forest.json')
  time.sleep(2)
  if zone_data is None:
    print("Failed to load the zone. Exiting the game.")
    return

  combat_count = 0  # Compteur de combats
  max_combats = 2  # Limite de 2 combats

  while combat_count < max_combats:  # Boucle pour les combats successifs
    monsters_data = zone_data.get("monsters", [])
    if not monsters_data:
      print("No monsters found in the zone. Exiting the game.")
      break

    monsters = [
        Monster(monster_data["name"], monster_data["health"],
                monster_data["attack"], monster_data["exp_reward"],
                monster_data["drops"]) for monster_data in monsters_data
    ]
    monster = random.choice(monsters)
    monster.display_stats()

    result = battle(player, monster, player_zone, inventory)
    combat_count = combat_count + 1

    if not result:
      break  # Si le joueur a perdu, arrêter la boucle de combat

    save_option = input("Do you want to save the game? (yes/no): ").lower()
    if save_option == "yes":
      jouer_bruit('Sound Effect\\save-sound.wav')
      save_game(player)
    else:
      print("Game not saved.")

    quit_option = input("Do you want to quit the game? (yes/no): ").lower()
    if quit_option == "yes":
      jouer_bruit('Sound Effect\\game-cut-sound.mp3')
      print("Thanks for playing!")
      return

    if combat_count == max_combats:
      print(f"\n\nMe: This forest sure has a lot of monsters, i'm gonna  get back to Tettno.")
      return Tettno_main(self, player, inventory, CraftingSystem, player_zone)



def battle(self, player, monster, player_zone, inventory):
  poison = 0
  stun = 0
  print("Battle Start!")
  while player.health > 0 and monster.health > 0:
    print("\nPlayer's Turn:")
    print("1. Physical Attack")
    if player.player_class == "Mage":
      print("2. Magic Attack")
      print("3. Heal")
    elif player.player_class == "Rogue" and player.level >= 10:
      print("2. Assault")
      print("3. Fast Kill")
    elif player.player_class == "Rogue":
      print("2. Assault")
    elif player.player_class == "Samuraï":
      print("2. Meiyō's Technique")
      print("3. Iaijutsu's Technique")
    choice = input("Choose your action: ")
    if choice == "1":
      crit = random.randint(0, 100)
      if crit >= 75:
        player.attack = random.randint(player.attack, player.attack * 2)
        monster.health -= player.attack
        time.sleep(2)
        jouer_bruit('Sound Effect\\attack-sound.mp3')
        print(
            f"CRITICAL HIT !!!\n{player.name} attacks {monster.name} for {player.attack} damage."
        )
      else:
        player.attack = random.randint(player.attack // 2, player.attack) # ici
        monster.health -= player.attack

        time.sleep(2)
        jouer_bruit('Sound Effect\\attack-sound.mp3')
        print(
            f"{player.name} attacks {monster.name} for {player.attack} damage."
        )
    elif choice == "2" and player.player_class == "Mage":
      if player.mana >= 10:
        player.mana -= 10
        crit = random.randint(0, 100)
        if crit >= 90:
          player.attack = random.randint(player.attack * 3, player.attack * 5)  # Attaque magique
          monster.health -= player.attack
          time.sleep(2)
          jouer_bruit('Sound Effect\\magic-sound.mp3')
          print(f"CRITICAL HIT !!!\n{player.name} casts a magic attack on {monster.name} for {player.attack} damage.")
        else:
          player.attack = random.randint(player.attack, player.attack * 2)  # Attaque magique
          monster.health -= player.attack
          time.sleep(2)
          jouer_bruit('Sound Effect\\magic-sound.mp3')
          print(f"{player.name} casts a magic attack on {monster.name} for {player.attack} damage.")
      else:
        print("Not enough mana to cast a magic attack.")
    elif choice == "2" and player.player_class == "Rogue":
      if player.agility >= 1:
        player.agility -= 1
        player.attack = random.randint(player.attack % 10, player.attack % 2)  # Attaque "Assault"
        monster.health -= player.attack
        poison += 1
        time.sleep(2)
        jouer_bruit('Sound Effect\Strike5.wav')
        print(
            f"{player.name} assault on {monster.name} for {player.attack} damage."
        )
      else:
        print("Not enough agility point to poison the opponent.")
    elif choice == "2" and player.player_class == "Samuraï":
      if player.dexterity >= 2:
        player.dexterity -= 2
        crit = random.randint(0, 100)
        if crit >= 95:
          player.attack = random.randint(player.attack * 3, player.attack * 6)  # Attaque "Meiyō" crit
          monster.health -= player.attack
          time.sleep(2)
          jouer_bruit('Sound Effect\Sword1.wav')
          print(
              f"CRITICAL HIT !!!\n{player.name} use meiyō's technique on {monster.name} for {player.attack} damage."
          )
        else:
          player.attack = random.randint(player.attack, player.attack * 2)  # Attaque "Meiyō"
          monster.health -= player.attack
          time.sleep(2)
          jouer_bruit('Sound Effect\Sword1.wav')
          print(
              f"{player.name} use meiyō's technique on {monster.name} for {player.attack} damage."
          )
      else:
        print("Not enough dexterity to use meiyō's technique.")
    elif choice == "3" and player.player_class == "Mage":
      if player.mana >= 20:
        player.mana -= 20
        player.health += 20  # Soins
        time.sleep(2)
        jouer_bruit('Sound Effect\heal-sound.wav')
        print(f"{player.name} heals for 20 health points.")
        error = random.randint(0, 10000)
        if error == 1:
          jouer_bruit('Sound Effect\\teleport.mp3')
          load_zone('Zones/mars.json')
          return mars(player)
      else:
        print("Not enough mana to cast a heal.")
    elif choice == "3" and player.player_class == "Rogue":
      if player.agility >= 4:
        player.agility -= 4
        kill = random.randint(0, 5)
        if kill == 2:
          time.sleep(2)
          jouer_bruit('Sound Effect\Strike5.wav')
          monster.health = 0
        else:
          crit = random.randint(0, 100)
          if crit >= 75:
            player.attack = random.randint(player.attack * 2, player.attack * 3)
            monster.health -= player.attack
            time.sleep(2)
            jouer_bruit('Sound Effect\\attack-sound.mp3')
            print(f"CRITICAL HIT !!!\n{player.name} attacks {monster.name} for {player.attack} damage.")
          else:
            player.attack = random.randint(player.attack % 2, player.attack)
            monster.health -= player.attack
            time.sleep(2)
            jouer_bruit('Sound Effect\\attack-sound.mp3')
            print(f"{player.name} attacks {monster.name} for {player.attack} damage.")
      else:
        print("Not enough agility to fast kill.")
    elif choice == "3" and player.player_class == "Samuraï":
      if player.dexterity >= 1:
        player.dexterity -= 1
        stun += 2
        time.sleep(2)
        jouer_bruit('Sound Effect\Sword1.wav')
        print(
            f"{player.name} use iaijutsu's technique to stun {monster.name} ")
      else:
        print("Not enough dexterity to use iaijutsu's technique.")
    else:
      print("Invalid choice.")
      continue
    if poison >= 1:
      player.attack = int(player.attack % 3)
      monster.health -= random.randint(player.attack * poison, player.attack * poison)
    if monster.health <= 0:
      print(f"{monster.name} has been defeated!")
      exp_gained = monster.exp_reward
      drop = monster.drop
      for i in drop:
        print(f"the {monster} dropped {i}")
        inventory.add_item(i, drop[i])
      player.exp += exp_gained
      player.level_up()
      print(f"You gained {exp_gained} experience!")
      print(f"{player.name}'s Current level: {player.level}, Experience: {player.exp}/{player.exp_needed}")
      print("-")
      time.sleep(1)
      player.display_stats()
      return True

    monster.attack = random.randint(monster.attack % 2, monster.attack)
    if stun >= 1:
      if random.randint(0, 5) >= 4:
        player.health -= monster.attack
        jouer_bruit('Sound Effect\\attack-sound.mp3')
        print(f"{monster.name} attacks {player.name} for {monster.attack} damage.")
      else:
        print(f"{monster.name} is stuned and can't attack")
    else:
      player.health -= monster.attack
      jouer_bruit('Sound Effect\\attack-sound.mp3')
      print(f"{monster.name} attacks {player.name} for {monster.attack} damage.")

    if player.health <= 0:
      jouer_bruit('Sound Effect\\death-sound.mp3')
      print(f"{player.name} has been defeated!")
      print("Restarting the Game...")
      return False

    print(f"\n{player.name}'s Health: {player.health}")
    if player.player_class == "Mage":
      print(f"{player.name}'s Mana: {player.mana}")
    elif player.player_class == "Rogue":
      print(f"{player.name}'s left agility point: {player.agility}")
    elif player.player_class == "Samuraï":
      print(f"{player.name}'s left dexterity point: {player.dexterity}")
    print(f"{monster.name}'s Health: {monster.health}")


def main(player_zone, self):
  start_animation()
  jouer_bruit('Sound Effect\\Start-Game.mp3')
  print("Welcome to the Adventure Game!")
  time.sleep(1)

  player_inventory = Inventory()
  player_inventory.load_inventory()
  player_inventory.add_item("Potion", 1)
  player_inventory.save_inventory()

  load_option = input("Do you want to load a saved game? (yes/no): ").lower()
  if load_option == "yes":
    player = {}
    player = load_game(player)
    with open("Saves\\progress.json", "r") as file:
      data = json.load(file)
    intro_flag = data.get("intro_flag")
    training_flag = data.get("training_flag")
    forest_flag = data.get("forest_flag")

  else:
    player = create_character()

    intro_flag = 0
    training_flag = 0
    forest_flag = 0

  if intro_flag == 0:
    intro_flag = 1
    data = {"intro_flag": 1}
    with open("Saves\\progress.json", "w") as file:
      json.dump(data, file)

    print("-")
    time.sleep(3)
    print("??? : Hello adventurer and welcome to the continent, a land of mystery and conflict.")
    time.sleep(5)
    print("??? : It's also a cursed land that awaits its final hour.")
    time.sleep(5)
    print("??? : Dear adventurer, you won't be asked to save this world, but explore it while it still exists!")
    time.sleep(5)
    print("??? : May the stars bless your journey and who knows? maybe we'll meet again...")

  if training_flag == 0:
    training_flag = 1
    data = {"training_flag": 1}
    with open("Saves\\progress.json", "r") as file:
      add = json.load(file)
    add.update(data)
    with open("Saves\\progress.json", "w") as file:
      json.dump(add, file)
    time.sleep(5)
    zone_data = load_zone(
        'Zones\\Tettno.json')  # Charger les données de la zone
    if zone_data is None:
      print("Failed to load the zone. Exiting the game.")
      return
    time.sleep(5)
    print("Stout man : HOHO! Are you the new adventurer?")
    time.sleep(5)
    print(f"Me : Yes, my name is {player.name}, I'm a {player.player_class}.")
    time.sleep(5)
    print("Sir Bertram Veridius : And i'm Sir Bertram Veridius, Commander of the Tettno Fortress !")
    time.sleep(5)
    print("Sir Bertram Veridius : Good! Now let's get started on your training!")
    time.sleep(5)
    monster = Monster("Puppet", 15, 0, 10, {"none": 1})
    monster.display_stats()
    time.sleep(3)
    battle(player, monster, player_zone, player_inventory)
    time.sleep(3)
    print("Sir Bertram Veridius : HOHO! Now you can explore the world !")
    time.sleep(5)

  if forest_flag == 0:
    forest_flag = 1
    data = {"forest_flag": 1}
    with open("Saves\\progress.json", "r") as file:
      add = json.load(file)
    add.update(data)
    with open("Saves\\progress.json", "w") as file:
      json.dump(add, file)
    zone_data = load_zone(
        "Zones\\Forest.json")  # Charger les données de la zone
    time.sleep(2)
    if zone_data is None:
      print("Failed to load the zone. Exiting the game.")
      return

    combat_count = 0  # Compteur de combats
    max_combats = 2  # Limite de 4 combats

    while combat_count < max_combats:  # Boucle pour les combats successifs
      with open('Zones\\Forest.json', "r") as file:
        data = json.load(file)
        monsters_data = data.get("monsters", [])

      monsters = [
          Monster(monster_data["name"], monster_data["health"],
                  monster_data["attack"], monster_data["exp_reward"],
                  monster_data["drop"]) for monster_data in monsters_data
      ]
      monster = random.choice(monsters)
      monster.display_stats()

      result = battle(player, monster, player_zone, player_inventory)
      combat_count = combat_count + 1

      if not result:
        break  # Si le joueur a perdu, arrêter la boucle de combat

      save_option = input("Do you want to save the game? (yes/no): ").lower()
      if save_option == "yes":
        jouer_bruit('Sound Effect\\save-sound.wav')
        save_game(player)
      else:
        print("Game not saved.")

      quit_option = input("Do you want to quit the game? (yes/no): ").lower()
      if quit_option == "yes":
        jouer_bruit('Sound Effect\\game-cut-sound.mp3')
        print("Thanks for playing!")
        return

      if combat_count == max_combats:
        print(
            f"\n\nMe: This forest sure has a lot of monsters, i'm gonna  get back to Tettno."
        )
        return Tettno_main(self, player, player_inventory, CraftingSystem, player_zone)

  else:
    return Tettno_main(self, player, player_inventory, CraftingSystem, player_zone)


def create_character():
  name = input("Enter your name: ")
  time.sleep(1)
  races = ["Human", "Elf", "Dwarf"]
  player_race = input("Choose your race (Human, Elf, Dwarf): ").capitalize()
  while player_race not in races:
    print("Invalid race. Please choose from Human, Elf or Dwarf.")
    player_race = input("Choose your race (Human, Elf, Dwarf): ").capitalize()

  time.sleep(1)
  classes = ["Mage", "Samuraï", "Rogue"]
  player_class = input(
      "Choose your class (Mage, Samuraï, Rogue): ").capitalize()
  while player_class not in classes:
    print("Invalid class. Please choose from Mage, Samuraï or Rogue.")
    player_class = input(
        "Choose your class (Mage, Samuraï, Rogue): ").capitalize()

  time.sleep(2)
  print("-")
  player = Player(name, player_race, player_class)
  player.display_stats()
  return Player(name, player_race, player_class)


def Tettno_main(self, player, inventory, CraftingSystem, player_zone):
  load_zone('Zones\\Tettno.json')
  time.sleep(2)
  print(f"What do you want to do ?\n1-Speak to Sir Bertram Veridius\n2-See your inventory\n3-Craft something\n4-Go somewhere else")
  choice = input("Enter your choice: ")
  if choice == "1":
    #return  #storypart2()
    return NotAvailable(player, inventory)
  
  elif choice == "2":
    with open('Saves\\Inventory.json', 'r') as file:
      data = json.load(file)
      inventory_data = data.get("inventory", {})
      inventory = Inventory()
    player = Player('name', 'race', 'player_class')
    player_inventory = player.inventory
    player_inventory.display_inventory()
    return Tettno_main(self, player, inventory, CraftingSystem, player_zone)
  
  elif choice == "3":
    return NotAvailable(player, inventory)
    crafting_system = CraftingSystem()
    inventory = {"Slime Gall": 4, "Water": 4, "Bottle": 4}
    possible_crafts = crafting_system.list_possible_craft(inventory)

    print("Possible Crafts:")
    for craft in possible_crafts:
      print(possible_crafts)
      print("Enter the name of the craft you want to perform, or 'back' to go back:")
      craft_choice = input()
      
      if craft_choice == "back":
        return Tettno_main(self, player, inventory, CraftingSystem, player_zone)

    print("Current Inventory:")
    for item, quantity in inventory.items():
      print(f"{item}: {quantity}")

    recipe_name = "Health Potion"
    print(f"\nAttempting to craft {recipe_name}...")
    crafting_system.craft(recipe_name, inventory)

    print("\nUpdated Inventory:")
    for item, quantity in inventory.items():
      print(f"{item}: {quantity}")
      craft_choice = input()

      if craft_choice == "back":
        return Tettno_main(self, player, inventory, CraftingSystem, player_zone)
      else:
        crafting_system.craft(craft_choice, inventory)
        return Tettno_main(self, player, inventory, CraftingSystem, player_zone)

  elif choice == "4":
    print(f"Where do you want to go ?\n1-Bank\n2-Forest\n3-Adventurer's guild")
    choice2 = input("Enter your choice: ")
    if choice2 == "1":
      return Bank(self, player, inventory, CraftingSystem, player_zone)
    elif choice2 == "2":
      return Forest(self, player, inventory, CraftingSystem, player_zone)
    elif choice2 == "3":
      return Adventurers_guild(self, player, inventory, CraftingSystem, player_zone)
  else:
    return Tettno_main(self, player, inventory, CraftingSystem, player_zone)


main(player_zone, self)
