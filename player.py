from boat import Boat
import time

class Player:
    def __init__(self, name, deck, debug=False):
        self.name = name    # Propriété d'un joueur :
        self.deck = deck
        self.debug = debug
        self.boat_list = []
        self.grid = [["🌊"] * 10 for _ in range(10)]
        self.grid_vision = [["🌊"] * 10 for _ in range(10)]
        self.grid_sim = [["🌊"] * 10 for _ in range(10)]


    def grid_show(self, target, mode = "Default"):    # Fonction d'affichage de la grille de jeu. 
        #mode = "Default" => Tableau du joueur | "Visuel" => Visualisation du tableau de l'adversaire | "Personal" => Afficher le terrain du joueur concerner
        if mode == "Visuel":    
            print(f"\n- Visuel du terrain de l'adversaire -")
            
        elif mode == "Personal":
            print("\n        - Votre terrain -")

        elif mode == "Simulation":
            print(f"\n- Emplacement de votre bateau -\n- ❌ >>> Simulation du bateau -")

        else:
            print(f"\n        - Tableau de {self.name} -")

        print("   0 │1 │2 │3 │4 │5 │6 │7 │8 │9 ")
        time.sleep(0.1)
        print("  ┌──┼──┼──┼──┼──┼──┼──┼──┼──┼──┐")
        for i in range(len(target)):
            time.sleep(0.1)
            print(chr(97+i),"│", end="")
            for j in range(len(target[i])):

                print(target[i][j], end="│")
            print("")
        time.sleep(0.1)
        print("  └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘")
        time.sleep(0.1)
        print("  ┌─────────────────────────────┐")
        print("  │ 🌊 = Eau                    │\n  │ 🛥  = Bateau                 │\n  │ 💥 = Raté                   │\n  │ 🔥 = Touché                 │")
        print("  └─────────────────────────────┘\n\n")


    def boat_placement(self):   # Fonction de placement d'un bateau.
        for boat_type in range (len(self.deck)):

            while True: # Demande à l'utilisateur des coordonnées du bateau.

                while True: # Demande à l'utilisateur de la rotation du bateau.
                    self.grid_show(self.grid, "Personal")
                    rotate = input(">>> rotation du bateau : 0 = vertical, 1 = horizontal >>> ")
                    if rotate in ["0","1"]:
                        rotate = int(rotate)
                        break
                    else :
                        print("/!\ Le chiffre doit être 0 ou 1.")
                        time.sleep(2)

                reponse = input(">>> coordonnées de bateau sous forme chiffre/lettre (ex : 2c) >>> ")
                if len(reponse) == 2 and reponse[0] in ["0","1","2","3","4","5","6","7","8","9"] and reponse[1] in ["a","b","c","d","e","f","g","h","i","j","k"]:
                    coord_boat = [int(reponse[0])]
                    coord_boat.append(int(ord(reponse[1])-ord("a")))

                    # Calcul du future_body avant de créer le bateau afin de simuler si il y a une collision avec un bateau déjà existant.
                    future_body = []
                    boat_data = self.deck[boat_type]
                    if rotate == 0: # Simulation d'un bateau à la vertical
                        for i in range(boat_data["lenght"]):
                            for j in range(boat_data["width"]):
                                future_body.append([coord_boat[0]+j, coord_boat[1]+i])
                    else:  # Simulation d'un bateau à l'horizontale
                        for i in range(boat_data["lenght"]):
                            for j in range(boat_data["width"]):
                                future_body.append([coord_boat[0]+i, coord_boat[1]+j])
                    
                    if any(coord[0] < 0 or coord[0] > 9 or coord[1] < 0 or coord[1] > 9 for coord in future_body):  # Vérification que le bateau reste dans les limites de la grille (0-9 en x et y).
                        print("\n/!\ Le bateau dépasse les limites du tableau, choisissez d'autres coordonnées.\n")
                        time.sleep(2)
                        continue

                    if self.check_collision(future_body):   # Vérification de collision.
                        print("\n/!\ Collision avec un bateau déjà placé, choisissez d'autres coordonnées.\n")
                        time.sleep(2)
                        continue

                    # Copie profonde de grid dans grid_sim pour afficher les bateaux déjà placés + la simulation.
                    self.grid_sim = [row[:] for row in self.grid]
                    self.create_boat(boat_data["name"], boat_data["lenght"], boat_data["width"], rotate, coord_boat, self, True)
                    self.grid_show(self.grid_sim, "Simulation")
                    
                    confirmation = input("Voici où sera le bateau, écrivez > oui < pour confirmer le placement >>> ")
                    if confirmation == "oui":
                        self.grid_sim = [["🌊"] * 10 for _ in range(11)]
                        self.boat_list.pop()    # Retirer le bateau de simulation avant de créer le vrai.
                        self.create_boat(boat_data["name"], boat_data["lenght"], boat_data["width"], rotate, coord_boat, self, False)
                        break
                    else:
                        # Annuler : retirer le bateau fantôme et réinitialiser la grille de simulation.
                        self.boat_list.pop()
                        self.grid_sim = [["🌊"] * 10 for _ in range(11)]
                        continue

                else:
                    print("/!\ La valeur rentrée doit être en format chiffre/lettre (ex : 2c).")
                    time.sleep(2)


    def turn(self, player_target):  # Fonction du tour de jouer d'un joueur.
        verif = False   # Variable pour la boucle afin que le joueur entre une réponse correcte.
        while verif == False:
            self.grid_show(self.grid_vision, "Visuel")    # Affichage du terrain de l'adversaire.
            print("===================================")
            self.grid_show(self.grid, "Personal")   # Affichage du terrain du joueur.
            reponse = input(">>> entrez les coordonnées du tire (sous forme lettre/chiffre, ex : 2c) >>> ")
            if len(reponse) == 2 and reponse[0] in ["0","1","2","3","4","5","6","7","8","9"] and reponse[1] in ["a","b","c","d","e","f","g","h","i","j","k"]:   # Vérification d'une réponse valide.
                coord_fire = [int(reponse[0])]
                coord_fire.append(int(ord(reponse[1])-ord("a")))    # convertion de lettre à chiffre.
                verif = True
            else :
                print("/!\ La valeur rentrée doit être en format chiffre/lettre (ex : 2c).")
        detection_victoire = self.fire(player_target, coord_fire)   # Tire du joueur au coordonnée rentrer. Renvoie si le joueur à gagner ou non (si la liste des bateaux adverse est vide).
        return detection_victoire


    def fire(self, player_target, coord_fire):  # Fonction du tire d'un joueur.
        player_target.grid[coord_fire[1]][coord_fire[0]] = "💥"                                     # Affichage du tire du joueur sur la grille du joueur adverse.
        self.grid_vision[coord_fire[1]][coord_fire[0]] = "💥"                                       # Affichage du tire du joueur sur la grille d'affichage du joueur adverse.
        for boat in player_target.boat_list:                                                        # Vérification d'impact d'un tire avec un bateau pour chaque bateau présent dans la boat_list du joueur adverse.
            verif = boat.fire_verif(player_target, coord_fire)

            if verif[0] == True:                                                                    # Vérification si un bateau a été toucher
                player_target.grid[coord_fire[1]][coord_fire[0]] = "🔥"                             # Affichage du tire du joueur sur la grille du joueur adverse.
                self.grid_vision[coord_fire[1]][coord_fire[0]] = "🔥"                               # Affichage du tire du joueur sur la grille d'affichage du joueur adverse.

            if verif[1] == True:                                                                  # Vérification si le bateau est coulé
                if self.debug == True : print(f"boat list BEFORE : {player_target.boat_list}")
                player_target.boat_list.remove(boat)                                                # Supprimer le bateau de la boat_list de l'adversaire si le bateau est détruit (body vide).
                if self.debug == True : print(f"boat list AFTER : {player_target.boat_list}")
                if len(player_target.boat_list) == 0:                                               # Détection de victoire car liste de bateau vide 
                    return True                                                                     # Victoire
                
            return False    # Continuer la partie


    def check_collision(self, future_body): # Fonction de vérification de collision lors du placement d'un bateau entre future_body et les bateaux déjà présent.
        for boat in self.boat_list:
            for coord in future_body:
                if coord in boat.body:
                    return True
        return False


    def create_boat(self, name, length, width, rotate, coord, player, creation_sim):  # Fonction de création d'un bateau
        """Name, Length, Width, Rotate (0 = vertical, 1 = horizontal), coordonnée (y,x), tableau"""
        boat = Boat(name, length, width, rotate, coord, player, self.debug, creation_sim) # Création de l'instance de la class Boat.
        self.boat_list.append(boat) # Ajout du bateau dans la liste des bateaux du joueur (boat_list).