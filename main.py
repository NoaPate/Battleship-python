# Created the 03/17/2026, Python 3.7
from player import Player
import time

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- GAME =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


# --- Dictionnaire contenant les propriétés des différents types de bateaux.
torpilleur = {"name": "Torpilleur(s)", "lenght": 2, "width": 1}
croiseur = {"name": "Croiseur(s)", "lenght": 3, "width": 1}
cuirasse = {"name": "cuirassé(s)", "lenght": 4, "width": 1}
porte_avions = {"name": "Porte-avions", "lenght": 5, "width": 1}


# --- Les différents bateaux que possèdent les joueurs et peuvent placer au début de la partie.
deck = [torpilleur, croiseur, cuirasse, porte_avions]
debug = False


def deck_to_dict(deck):
    deck_dict = {}
    for boat in deck:
        if boat["name"] in deck_dict:
            deck_dict[boat["name"]] += 1
        else:
            deck_dict[boat["name"]] = 1
    return deck_dict


def skip(n):    # Fonction pour cacher les tours précédents (uniquement dans le mode de jeu dans la console).
    for i in range(n):
        print(f"--- TOUR DU JOUEUR SUIVANT DANS {n-i} SECONDES ! ---")
        time.sleep(1)
        print("\n" * 50)


def initialisation_joueur():    # Création des joueurs, de leurs instances dans la class Player et leurs propriétés.
    global debug
    pseudo = input(">>> Entrez le pseudo du joueur 1 >>> ")
    if pseudo == "debug":
        debug = True
        print("-----> Debug activé <-----")
    player1 = Player(pseudo, deck, debug)
    time.sleep(0.5)
    pseudo = input(">>> Entrez le pseudo du joueur 2 >>> ")
    player2 = Player(pseudo, deck, debug)
    time.sleep(0.5)
    return (player1,player2)


def game():
    deck_dict = deck_to_dict(deck)
    victoire_joueur1 = False
    victoire_joueur2 = False
    gameloop = True
    player1,player2 = initialisation_joueur()
    print(f"\n-----> {player1.name} place ses bateaux ! <-----\n")
    print("Votre deck comporte :")
    for key,value in deck_dict.items():
        print(value, key)
    player1.boat_placement()
    skip(5)
    print(f"\n-----> {player2.name} place ses bateaux ! <-----\n")
    print("Votre deck comporte :")
    for key,value in deck_dict.items():
        print(value, key)
    player2.boat_placement()

    while gameloop :
        if victoire_joueur1 == False:
            skip(5)
            print(f"-----> Tour de {player1.name} <-----\n")
            victoire_joueur1 = player1.turn(player2)

        if victoire_joueur1 == True:
            print(f"{player1.name} gagne")
            gameloop = False
            break

        if victoire_joueur2 == False:
            skip(5)
            print(f"-----> Tour de {player2.name} <-----\n")
            victoire_joueur2 = player2.turn(player1)
        
        if victoire_joueur2 == True:
            print(f"{player2.name} gagne")
            gameloop = False
            break
    
game()
