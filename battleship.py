# Created the 03/17/2026, Python 3.7


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- BOAT =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-



class Boat:
    def __init__(self, name, length, width, rotate, coord, target):
        self.name = name        # Propriété d'un bateau :
        self.length = length
        self.width = width
        self.rotate = rotate
        self.coord = coord
        self.body = []          # Corps d'un bateau, pour les détéctions de tire et de bateau détruit. (liste vide = badeau coulé.)
        if self.rotate == 0:    # Rotation du bateau à placer. (verticale)
            for i in range (self.length):
                for j in range (self.width):
                    self.body.append([self.coord[0]+j,self.coord[1]+i])
                    target.grid[self.coord[1]+i][self.coord[0]+j] = "🛥 "   # Affichage du bateau dans la grille de jeu.

        if self.rotate == 1:    # Rotation du bateau à placer. (horizontale)
            for i in range (self.length):
                for j in range (self.width):
                    self.body.append([self.coord[0]+i,self.coord[1]+j])
                    target.grid[self.coord[1]+j][self.coord[0]+i] = "🛥 "
        if debug == True : print(self.body)

    def fire_verif(self, player_target, coord_tire): # Fonction de vérification des impacts d'un tire. 
        verif = [False,False]
        for coords in self.body:
            if coord_tire == coords:
                if debug == True:
                    print(f"{self.body} boat body BEFORE")
                    print(f"{coords} fire coord")

                self.body.remove(coords)    # Supprimer la partie du bateau toucher
                verif[0] = True

                if debug == True : print(f"{self.body} boat body AFTER")

                if len(self.body) == 0: 
                    verif[1] = True # Le bateau est coulé.
                    return verif 
        return verif  # Le bateau n'est pas encore coulé.



# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- PLAYER =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-



class Player:
    def __init__(self, name, deck):
        self.name = name    # Propriété d'un joueur :
        self.deck = deck
        self.boat_list = []
        self.grid = [["🌊"] * 10 for _ in range(11)]
        self.grid_vision = [["🌊"] * 10 for _ in range(11)]

    def grid_show(self, target, mode = "Default"):    # Fonction d'affichage de la grille de jeu. 
        #mode = "Default" => Tableau du joueur | "Visuel" => Visualisation du tableau de l'adversaire | "Personal" => Afficher le terrain du joueur concerner
        if mode == "Visuel":    
            print(f"\n- Visuel du terrain de l'adversaire -")
        elif mode == "Personal":
            print("\n          - Votre terrain -")
        else:
            print(f"\n        - Tableau de {self.name} -")
        print("   0 │1 │2 │3 │4 │5 │6 │7 │8 │9 ")
        print("  ┌──┼──┼──┼──┼──┼──┼──┼──┼──┼──┐")
        for i in range(len(target)):
            print(chr(97+i),"│", end="")
            for j in range(len(target[i])):

                print(target[i][j], end="│")
            print("")
        print("  └──┴──┴──┴──┴──┴──┴──┴──┴──┴──┘\n")

    def boat_placement(self):   # Fonction de placement d'un bateau.
        for boat_type in range (len(self.deck)):
            while True: # Demande à l'utilisateur de la rotation du bateau.
                self.grid_show(self.grid)
                rotate = input(">>> rotation du bateau : 0 = vertical, 1 = horizontal >>> \n")
                if rotate in ["0","1"]:
                    rotate = int(rotate)
                    break
                else :
                    print("/!\ Le chiffre doit être 0 ou 1.")

            while True: # Demande à l'utilisateur des coordonnées du bateau.
                reponse = input(">>> coordonnées de bateau sous forme chiffre/lettre (ex : 2c) >>> \n")
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
                        continue

                    if self.check_collision(future_body):   # Vérification de collision.
                        print("\n/!\ Collision avec un bateau déjà placé, choisissez d'autres coordonnées.\n")
                        continue

                    self.create_boat(boat_data["name"], boat_data["lenght"], boat_data["width"], rotate, coord_boat, self)
                    self.grid_show(self.grid)
                    break

                print("/!\ La valeur rentrée doit être en format chiffre/lettre (ex : 2c).")    

    def turn(self, player_target):  # Fonction du tour de jouer d'un joueur.
        verif = False   # Variable pour la boucle afin que le joueur entre une réponse correcte.
        while verif == False:
            self.grid_show(self.grid_vision, "Visuel")    # Affichage du terrain de l'adversaire.
            print("===================================")
            self.grid_show(self.grid, "Personal")   # Affichage du terrain du joueur.
            reponse = input(">>> entrez les coordonnées du tire (sous forme lettre/chiffre, ex : 2c) >>> \n")
            if len(reponse) == 2 and reponse[0] in ["0","1","2","3","4","5","6","7","8","9"] and reponse[1] in ["a","b","c","d","e","f","g","h","i","j","k"]:   # Vérification d'une réponse valide.
                coord_fire = [int(reponse[0])]
                coord_fire.append(int(ord(reponse[1])-ord("a")))    # convertion de lettre à chiffre.
                verif = True
            else :
                print("/!\ La valeur rentrée doit être en format chiffre/lettre (ex : 2c).")
        detection_victoire = self.fire(player_target, coord_fire)   # Tire du joueur au coordonnée rentrer. Renvoie si le joueur à gagner ou non (si la liste des bateaux adverse est vide).
        return detection_victoire

    def fire(self, player_target, coord_fire):  # Fonction du tire d'un joueur.
        global debug
        player_target.grid[coord_fire[1]][coord_fire[0]] = "💥"                                     # Affichage du tire du joueur sur la grille du joueur adverse.
        self.grid_vision[coord_fire[1]][coord_fire[0]] = "💥"                                       # Affichage du tire du joueur sur la grille d'affichage du joueur adverse.
        for boat in player_target.boat_list:                                                        # Vérification d'impact d'un tire avec un bateau pour chaque bateau présent dans la boat_list du joueur adverse.
            verif = boat.fire_verif(player_target, coord_fire)

            if verif[0] == True:                                                                    # Vérification si un bateau a été toucher
                player_target.grid[coord_fire[1]][coord_fire[0]] = "🔥"                             # Affichage du tire du joueur sur la grille du joueur adverse.
                self.grid_vision[coord_fire[1]][coord_fire[0]] = "🔥"                               # Affichage du tire du joueur sur la grille d'affichage du joueur adverse.

            if verif[1] == True:                                                                  # Vérification si le bateau est coulé
                if debug == True : print(f"boat list BEFORE : {player_target.boat_list}")
                player_target.boat_list.remove(boat)                                                # Supprimer le bateau de la boat_list de l'adversaire si le bateau est détruit (body vide).
                if debug == True : print(f"boat list AFTER : {player_target.boat_list}")
                if len(player_target.boat_list) == 0:                                               # Détection de victoire car liste de bateau vide 
                    return True                                                                     # Victoire
                
            return False    # Continuer la partie

    def check_collision(self, future_body): # Fonction de vérification de collision lors du placement d'un bateau entre future_body et les bateaux déjà présent.
        for boat in self.boat_list:
            for coord in future_body:
                if coord in boat.body:
                    return True
        return False

    def create_boat(self, name, length, width, rotate, coord, target):  # Fonction de création d'un bateau
        """Name, Length, Width, Rotate (0 = vertical, 1 = horizontal), coordonnée (y,x), tableau"""
        boat = Boat(name, length, width, rotate, coord, target) # Création de l'instance de la class Boat.
        self.boat_list.append(boat) # Ajout du bateau dans la liste des bateaux du joueur (boat_list).



# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- GAME =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


# --- Dictionnaire contenant les propriétés des différents types de bateaux.
peniche = {"name": "Peniche", "lenght": 2, "width": 1}
destroyer = {"name": "Destroyer", "lenght": 5, "width": 2}
# --- Les différents bateaux que possèdent les joueurs et peuvent placer au début de la partie.
deck = [destroyer]
debug = False

def skip(n):    # Fonction pour cacher les tours précédents (uniquement dans le mode de jeu dans la console).
    print("\n" * n)

def initialisation_joueur():    # Création des joueurs, de leurs instances dans la class Player et leurs propriétés.
    global debug
    pseudo = input(">>> Entrez le pseudo du joueur 1 >>> \n")
    if pseudo == "debug":
        debug = True
        print("-----> Debug activé <-----")
    player1 = Player(pseudo, deck)
    pseudo = input(">>> Entrez le pseudo du joueur 2 >>> \n")
    player2 = Player(pseudo, deck)
    return (player1,player2)


def game():
    victoire_joueur1 = False
    victoire_joueur2 = False
    gameloop = True
    player1,player2 = initialisation_joueur()
    print(f"\n-----> {player1.name} place ses bateaux ! <-----")
    player1.boat_placement()
    skip(100)
    print(f"\n-----> {player2.name} place ses bateaux ! <-----")
    player2.boat_placement()
    skip(100)
    while gameloop :
        if victoire_joueur1 == False:
            skip(100)
            print(f"-----> Tour de {player1.name} <-----\n")
            victoire_joueur1 = player1.turn(player2)

        if victoire_joueur1 == True:
            print(f"{player1.name} gagne")
            gameloop = False
            break

        if victoire_joueur2 == False:
            skip(100)
            print(f"-----> Tour de {player2.name} <-----\n")
            victoire_joueur2 = player2.turn(player1)
        
        if victoire_joueur2 == True:
            print(f"{player2.name} gagne")
            gameloop = False
            break
    
game()
