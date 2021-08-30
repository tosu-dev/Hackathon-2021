from tkinter import *
from PIL import ImageTk, Image


class Pays():

    def __init__(self, nom, indicateurs, position, root):
        self.nom = nom

        indicateurs = self.transforme_indicateurs(indicateurs)
        self.indicateurs = {"esp":float(indicateurs[0]), "com":float(indicateurs[1]), "ide":float(indicateurs[2]), "pib":float(indicateurs[3])}
        
        self.position = position

        self.root = root
        image = Image.open(f"ressources/images/drapeaux/{nom}.png")
        image = image.resize((30, 25))
        self.drapeau = ImageTk.PhotoImage(image)


    def transforme_indicateurs(self, indicateurs):
        """ transforme les valeurs des indicateurs pour les convertir en float """
        for i in range(len(indicateurs)):
            txt = ""
            for c in indicateurs[i]:
                # on change les ',' en '.'
                if c == ",":
                    txt += "."
                else:
                    txt += c
            # si il n'y a pas de valeur, on met une valeur infini
            if txt == "..":
                txt = '-inf'
            indicateurs[i] = txt
        return indicateurs