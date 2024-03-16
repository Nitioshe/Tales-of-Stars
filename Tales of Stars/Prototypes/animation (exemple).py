import time

# ASCII art pour "Starting Game" https://patorjk.com/software/taag/#p=display&f=Graceful&t=Tales%20of%20Stars  osti d'caliss ! tabarnak de saint ciboire !

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

def start_animation():
    print(ascii_art)  # Affichage de l'ASCII art
    print(ascii_art2)
    print("Starting game...", end="", flush=True)
    for _ in range(5):
        time.sleep(0.5)  # Pause de 0.5 seconde
        print(".", end="", flush=True)  # Imprime un point sans saut de ligne
    print("\n")  # Saut de ligne après l'animation

def main():
    start_animation()
    # Autres opérations de démarrage du jeu ici

if __name__ == "__main__":
    main()
