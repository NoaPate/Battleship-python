class Boat:
    def __init__(self, name, length, width, rotate, coord, player, debug=False, creation_sim=False):
        self.debug = debug
        self.creation_sim = creation_sim
        self.name = name        # Propriété d'un bateau :
        self.length = length
        self.width = width
        self.rotate = rotate
        self.coord = coord
        self.body = []          # Corps d'un bateau, pour les détéctions de tire et de bateau détruit. (liste vide = badeau coulé.)
        if creation_sim == True:
            if self.rotate == 0:    # Rotation du bateau à placer. (verticale)
                for i in range (self.length):
                    for j in range (self.width):
                        self.body.append([self.coord[0]+j,self.coord[1]+i])
                        player.grid_sim[self.coord[1]+i][self.coord[0]+j] = "❌"   # Affichage du bateau dans la grille de jeu.

            if self.rotate == 1:    # Rotation du bateau à placer. (horizontale)
                for i in range (self.length):
                    for j in range (self.width):
                        self.body.append([self.coord[0]+i,self.coord[1]+j])
                        player.grid_sim[self.coord[1]+j][self.coord[0]+i] = "❌"
            if self.debug == True : print(self.body)

        else :
            if self.rotate == 0:    # Rotation du bateau à placer. (verticale)
                for i in range (self.length):
                    for j in range (self.width):
                        self.body.append([self.coord[0]+j,self.coord[1]+i])
                        player.grid[self.coord[1]+i][self.coord[0]+j] = "🛥 "   # Affichage du bateau dans la grille de jeu.

            if self.rotate == 1:    # Rotation du bateau à placer. (horizontale)
                for i in range (self.length):
                    for j in range (self.width):
                        self.body.append([self.coord[0]+i,self.coord[1]+j])
                        player.grid[self.coord[1]+j][self.coord[0]+i] = "🛥 "
            if self.debug == True : print(self.body)
        

    def fire_verif(self, player_target, coord_tire): # Fonction de vérification des impacts d'un tire. 
        verif = [False,False]
        for coords in self.body:
            if coord_tire == coords:
                if self.debug == True:
                    print(f"{self.body} boat body BEFORE")
                    print(f"{coords} fire coord")

                self.body.remove(coords)    # Supprimer la partie du bateau toucher
                verif[0] = True

                if self.debug == True : print(f"{self.body} boat body AFTER")

                if len(self.body) == 0: 
                    verif[1] = True # Le bateau est coulé.
                    return verif 
        return verif  # Le bateau n'est pas encore coulé.