
import tkinter as tk
import random

class Morpion:
    def __init__(self):
        self.boutons = []
        self.joueur_actuel = 'X'
        self.partie_gagnee = False
        self.taille_grille = 5
        self.alignement_victoire = 5
        self.label_message = None

    def afficher_message(self, message):
        if self.label_message is not None:
            self.label_message.destroy()
        self.label_message = tk.Label(root, text=message, font=("Arial", 12))
        self.label_message.grid(row=self.taille_grille + 1, columnspan=self.taille_grille)

    def afficher_gagnant(self):
        if not self.partie_gagnee:
            self.partie_gagnee = True
            self.afficher_message(f"Le joueur {self.joueur_actuel} remporte la partie")

    def changer_joueur(self):
        self.joueur_actuel = 'O' if self.joueur_actuel == 'X' else 'X'

    def verifier_victoire(self, row, col):
        # Vérification de la victoire horizontale
        if any(all(self.boutons[i][row]['text'] == self.joueur_actuel for i in range(col, col + self.alignement_victoire))
               for col in range(self.taille_grille - self.alignement_victoire + 1)):
            self.afficher_gagnant()

        # Vérification de la victoire verticale
        if any(all(self.boutons[col][i]['text'] == self.joueur_actuel for i in range(row, row + self.alignement_victoire))
               for row in range(self.taille_grille - self.alignement_victoire + 1)):
            self.afficher_gagnant()

        # Vérification de la victoire diagonale
        if any(all(self.boutons[col + i][row + i]['text'] == self.joueur_actuel for i in range(self.alignement_victoire))
               for col in range(self.taille_grille - self.alignement_victoire + 1)
               for row in range(self.taille_grille - self.alignement_victoire + 1)):
            self.afficher_gagnant()

        # Vérification de la victoire diagonale inversée
        if any(all(self.boutons[col - i][row + i]['text'] == self.joueur_actuel for i in range(self.alignement_victoire))
               for col in range(self.alignement_victoire - 1, self.taille_grille)
               for row in range(self.taille_grille - self.alignement_victoire + 1)):
            self.afficher_gagnant()

        # Vérification de l'égalité
        if not self.partie_gagnee and all(self.boutons[col][row]['text'] in ['X', 'O']
                                           for col in range(self.taille_grille)
                                           for row in range(self.taille_grille)):
            self.afficher_message("Match nul")

    def placer_symbole(self, row, col):
        bouton = self.boutons[col][row]
        if bouton['text'] == "" and not self.partie_gagnee:
            bouton.config(text=self.joueur_actuel)
            couleur = 'red' if self.joueur_actuel == 'X' else 'blue'
            bouton.config(fg=couleur)
            self.verifier_victoire(row, col)
            self.changer_joueur()
            # Vérifie si c'est le tour de l'IA
            if self.joueur_actuel == 'O':
                self.jouer_ia()


    def jouer_ia(self):
        if not self.partie_gagnee:
            cases_disponibles = [(row, col) for col in range(self.taille_grille) for row in range(self.taille_grille) if self.boutons[col][row]['text'] == ""]
            if cases_disponibles:
                choix = random.choice(cases_disponibles)
                self.placer_symbole(choix[0], choix[1])

    def creer_grille(self):
        for col in range(self.taille_grille):
            boutons_col = []
            for row in range(self.taille_grille):
                bouton = tk.Button(
                    root, font=("Arial", 15),
                    width=4, height=2,
                    command=lambda r=row, c=col: jeu.placer_symbole(r, c)
                )
                bouton.grid(row=row, column=col)
                boutons_col.append(bouton)
            self.boutons.append(boutons_col)

    def reinitialiser_partie(self):
        for col in self.boutons:
            for bouton in col:
                bouton.destroy()
        if self.label_message is not None:
            self.label_message.destroy()
        self.boutons = []
        self.joueur_actuel = 'X'
        self.partie_gagnee = False
        self.creer_grille()

if __name__ == "__main__":
    jeu = Morpion()

    root = tk.Tk()
    root.title("Morpion")
    root.minsize(400, 400)

    bouton_reset = tk.Button(root, text="Réinitialiser", command=jeu.reinitialiser_partie)
    bouton_reset.grid(row=5, column=0, columnspan=5)

    jeu.creer_grille()

    root.mainloop()