from tkinter import * 
from PIL import ImageTk, Image
import csv
from pays import Pays
import random

# GLOBAL VALUES
width = 1230
height = 720
bg = "#698ADD"
button_bg = "#4872da"
num_current_question = 0 # score
counter_good_question = 0 # score

### IMPORTATINS / VARIABLES ###
# on importe les 4 indicateurs
liste_indicateurs = [] # liste des tout les indicateurs
with open("ressources/donnees/liste_indicateurs.txt", "r", encoding="utf-8") as fichier:
    for line in fichier.readlines()[:-1]:
        liste_indicateurs.append(line[:-1])

liste_indicateurs_choose = [] # liste des indicateurs choisis par l'utilisateur

dico_indics = { # dico pour les indicateurs et l'attribut indicateur de la classe Pays
    liste_indicateurs[0]:"esp",
    liste_indicateurs[1]:"com",
    liste_indicateurs[2]:"ide",
    liste_indicateurs[3]:"pib"}

# on importe la liste de tout les noms des pays, et leur position
liste_nom_pays = []
liste_positions = []
with open("ressources/donnees/liste_pays.txt", "r", encoding="utf-8") as fichier:
    for line in fichier.readlines()[:-1]:
        a = line.split(";")
        liste_nom_pays.append(a[0])
        t = []
        for elt in a[1].split(","):
            t.append(int(elt))
        liste_positions.append(tuple(t))

##### CHOOSE INDICATEURS ROOT #####
def check_indics():
    """ fonction de commande pour le check_button 'ok' """
    global var1, var2, var3, var4, c1, c2, c3, c4
    global check_button, liste_indicateurs, liste_indicateurs_choose, start_root

    # on regarde si les cases sont cochés
    # si oui on ajoute l'indicateur dans la liste des indicateurs choisis
    # si il l'utilisateur n'a rien choisis, ça fait crasher le programme (ce n'est pas dans son intérêt)
    if var1.get() == 1:
        liste_indicateurs_choose.append(liste_indicateurs[0])
    if var2.get() == 1:
        liste_indicateurs_choose.append(liste_indicateurs[1])
    if var3.get() == 1:
        liste_indicateurs_choose.append(liste_indicateurs[2])
    if var4.get() == 1:
        liste_indicateurs_choose.append(liste_indicateurs[3])
    # on désactive tout (il faut quitter la fenêtre pour continuer)
    check_button.configure(state=DISABLED)
    c1.configure(state=DISABLED)
    c2.configure(state=DISABLED)
    c3.configure(state=DISABLED)
    c4.configure(state=DISABLED)

# root
start_root = Tk()
start_root.title("Choisis ton/tes indicateur(s), clique sur ok, puis ferme cette fenêtre")
start_root.geometry(f"{width}x{height}")
start_root["bg"] = bg
start_root.resizable(width=False, height=False)
# checkbox (+ variables), check_button
var1, var2, var3, var4 = IntVar(), IntVar(), IntVar(), IntVar()
c1 = Checkbutton(start_root, text=liste_indicateurs[0], bg=bg, font=("Courrier", 22), variable=var1, onvalue=1, offvalue=0)
c2 = Checkbutton(start_root, text=liste_indicateurs[1], bg=bg, font=("Courrier", 22), variable=var2, onvalue=1, offvalue=0)
c3 = Checkbutton(start_root, text=liste_indicateurs[2], bg=bg, font=("Courrier", 22), variable=var3, onvalue=1, offvalue=0)
c4 = Checkbutton(start_root, text=liste_indicateurs[3], bg=bg, font=("Courrier", 22), variable=var4, onvalue=1, offvalue=0)
check_button = Button(start_root, text="ok", bg=button_bg, font=("Courrier", 22), width=10, command=check_indics)
c1.pack(expand=YES)
c2.pack(expand=YES)
c3.pack(expand=YES)
c4.pack(expand=YES)
check_button.pack(expand=YES, padx=50)

start_root.mainloop()
# end of choose indicateurs root (exit)




##### MAIN ROOT #####
root = Tk()
root.title("Hackathon JDB 2021")
root.geometry(f"{width}x{height}")
root["bg"] = bg
root.resizable(width=False, height=False)

### IMPORTATIONS / VARIABLES ###
# on importe les informations des indicateurs choisis des pays choisis avec le fichier csv
liste_pays = [] # liste pays avec la classe Pays()
with open("ressources/donnees/donnees_pays_csv.csv", "r", encoding="utf-8") as fichier:
    lecteur = csv.reader(fichier, delimiter="\t")
    indics = lecteur.__next__()
    indicateurs_index = [i for i in range(len(indics)) if indics[i] in liste_indicateurs]
    for ligne in lecteur:
        if ligne[0] in liste_nom_pays:
            l = []
            for i in indicateurs_index:
                l.append(ligne[i])
            pays = Pays(ligne[0], [info for info in l], liste_positions[liste_nom_pays.index(ligne[0])], root)
            liste_pays.append(pays)

# on répartie les pays dans les 3 catégories
liste_pays_tresconnus = []
liste_pays_connus = []
liste_pays_peuconnus = []
with open("ressources/donnees/liste_classement_pays.txt", "r", encoding="utf-8") as fichier:
    l1, l2, l3 = fichier.readlines()[:-1]
    l1 = l1.split(";")[:-1]
    l2 = l2.split(";")[:-1]
    l3 = l3.split(';')[:-1]
for pays in liste_pays:
    if pays.nom in l1:
        liste_pays_tresconnus.append(pays)
    elif pays.nom in l2:
        liste_pays_connus.append(pays)
    else:
        liste_pays_peuconnus.append(pays)

# pourcentages de chance de tirer un pays selon ça catégorie
chance_pays_tresconnus = 100
chance_pays_connus = 0
chance_pays_peuconnus = 0

# dictionnaire des couples déjà faits dico[pays.nom] = [pays1.nom, pays2.nom, ...]
dico_couples = {} 
for pays in liste_pays:
    dico_couples[pays.nom] = []


### FUNCTIONS ###
# buttons enable/disable
def enable_next_button():
    """ désactive les boutons réponses et active le bouton 'next' """
    global button_next, button1, button2
    button_next.configure(state=NORMAL, cursor="hand2")
    button1.configure(state=DISABLED, cursor="X_cursor")
    button2.configure(state=DISABLED, cursor="X_cursor")

def disable_next_button():
    """ active les boutons réponses et désactive le bouton 'next' """
    global button_next, button1, button2
    button_next.configure(state=DISABLED, cursor="X_cursor")
    button1.configure(state=NORMAL, cursor="hand2")
    button2.configure(state=NORMAL, cursor="hand2")

# chance
def set_chances(a, b, c):
    """ 
    change la chances de pioche des catégories 
    :param a,b,c: int, repectivement tres_connus, connus, peu_connus
    """
    global chance_pays_tresconnus, chance_pays_connus, chance_pays_peuconnus
    chance_pays_tresconnus = a
    chance_pays_connus = b
    chance_pays_peuconnus = c

def change_chances():
    """ change les chances de pioche des catégories selon le nombre de question déjà fait """
    global num_current_question, chance_pays_connus, chance_pays_peuconnus, chance_pays_tresconnus

    if 0 <= num_current_question <= 10:
        set_chances(100, 0, 0)
    elif 11 <= num_current_question <= 20:
        set_chances(0, 100, 0)
    elif 21 <= num_current_question <= 30:
        set_chances(0, 0, 100)
    elif 31 <= num_current_question <= 50           :
        set_chances(33, 33, 34)

    else: # à la fin, full random
        set_chances(-1, -1, -1)

def random_categorie():
    """ 
    chosis aléatoirement une catégorie de pays et retourn 1, 2 ou 3
    1 = tres connus, 2 = connus, 3 = peu connus
    """
    global chance_pays_peuconnus, chance_pays_connus, chance_pays_tresconnus

    if chance_pays_peuconnus == -1 or chance_pays_connus == -1 or chance_pays_tresconnus == -1:
        return 0

    a = random.randint(1, 100)
    if 0 <= a <= chance_pays_tresconnus:
        return 1
    elif chance_pays_tresconnus < a <= chance_pays_tresconnus+chance_pays_connus:
        return 2
    elif chance_pays_tresconnus+chance_pays_connus < a <= 100:
        return 3

# choose lands/indics
def choose_lands():
    """ Choisis 2 pays au hasard qui n'ont pas déjà été ensemble et les retournes """

    # on change la chance des choix des pays si besoin
    change_chances()

    # on choisis le pays1
    categorie_pays1 = random_categorie()
    if categorie_pays1 == 0:
        i = random.randrange(0, len(liste_pays))
        pays1 = liste_pays[i]      
    elif categorie_pays1 == 1:
        i = random.randrange(0, len(liste_pays_tresconnus))
        pays1 = liste_pays_tresconnus[i]
    elif categorie_pays1 == 2:
        i = random.randrange(0, len(liste_pays_connus))
        pays1 = liste_pays_connus[i]
    else:
        i = random.randrange(0, len(liste_pays_peuconnus))
        pays1 = liste_pays_peuconnus[i]

    # puis le pays 2
    categorie_pays2 = random_categorie()
    j = -1
    while j < 0:
        if categorie_pays2 == 0:
            j = random.randrange(0, len(liste_pays))
            pays2 = liste_pays[j]   
        elif categorie_pays2 == 1:
            j = random.randrange(0, len(liste_pays_tresconnus))
            pays2 = liste_pays_tresconnus[j]
        elif categorie_pays2 == 2:
            j = random.randrange(0, len(liste_pays_connus))
            pays2 = liste_pays_connus[j]
        else:
            j = random.randrange(0, len(liste_pays_peuconnus))
            pays2 = liste_pays_peuconnus[j]
        # si ce sont les mêmes pays ou que le couples à déjà été fait, on recommence
        if pays1.nom == pays2.nom or pays2.nom in dico_couples[pays1.nom]:
            j = -1

    return pays1, pays2

def choose_indic():
    """ Choisis un indicateur au hasard parmis les indicateurs choisis par l'utilisateur et le retourne """
    i = random.randrange(0, len(liste_indicateurs_choose))
    return liste_indicateurs_choose[i]

# buttons commands
def button1_command():
    """ fonction pour la commande du bouton 1 'plus petit que' """
    global pays1, pays2, indic, label_top, reponse, num_current_question, counter_good_question, label_score

    enable_next_button() # switch les boutons
    # check si la réponse est bonne ou pas et on créer le texte de la réponse
    # si oui on rajoute 1 au score
    ind = dico_indics[indic]
    if pays1.indicateurs[ind] == float("-inf") or pays2.indicateurs[ind] == float("-inf"):
        reponse = f"Manques de données!\n'{pays1.nom}':{pays1.indicateurs[ind]} // '{pays2.nom}':{pays2.indicateurs[ind]}\n{indic}"
        counter_good_question += 1
    elif pays1.indicateurs[ind] <= pays2.indicateurs[ind]:
        reponse = f"CORRECT !\n'{pays1.nom}': {pays1.indicateurs[ind]} < '{pays2.nom}':{pays2.indicateurs[ind]}\n{indic}"
        counter_good_question += 1
    else:
        reponse = f"INCORRECT !\n'{pays1.nom}':{pays1.indicateurs[ind]} > '{pays2.nom}':{pays2.indicateurs[ind]}\n{indic}"
    # affiche la réponse et le nouveau score
    num_current_question += 1
    label_top.configure(text=reponse)
    label_score.configure(text=f"{counter_good_question}/{num_current_question} questions")

def button2_command():
    """ fonction pour la commande du bouton 2 'plus grand que' """
    global pays1, pays2, indic, label_top, reponse, num_current_question, counter_good_question, label_score
    
    enable_next_button() # switch les boutons
    # check si la réponse est bonne et on créer le texte de la réponse
    # si oui on rajoute 1 au score
    ind = dico_indics[indic]
    if pays1.indicateurs[ind] == float("-inf") or pays2.indicateurs[ind] == float("-inf"):
        reponse = f"Manques de données !\n'{pays1.nom}':{pays1.indicateurs[ind]} // '{pays2.nom}':{pays2.indicateurs[ind]}\n{indic}"
        counter_good_question += 1
    elif pays1.indicateurs[ind] >= pays2.indicateurs[ind] :
        reponse = f"CORRECT !\n'{pays1.nom}': {pays1.indicateurs[ind]} > '{pays2.nom}':{pays2.indicateurs[ind]}\n{indic}"
        counter_good_question += 1
    else:
        reponse = f"INCORRECT !\n'{pays1.nom}':{pays1.indicateurs[ind]} < '{pays2.nom}':{pays2.indicateurs[ind]}\n{indic}"
    # affiche la réponse et le nouveau score
    num_current_question += 1
    label_top.configure(text=reponse)
    label_score.configure(text=f"{counter_good_question}/{num_current_question} questions")

def next_button_command():
    """ fonction pour la commande du bouton 'next' """
    global question, label_top, pays1, pays2, cercle_pays1, cercle_pays2, canvas_map, indic

    disable_next_button() # switch les boutons
    # on enlève les 2 drapeaux des 2 anciens pays sur la carte
    canvas_map.delete(cercle_pays1)
    canvas_map.delete(cercle_pays2)

    # on choisis un nouvel indicateur, 2 pays
    indic = choose_indic()
    pays1, pays2 = choose_lands()
    # on les rajoutes dans les couples déjà faits
    dico_couples[pays1.nom].append(pays2.nom)
    dico_couples[pays2.nom].append(pays1.nom)
    # on affiche les drapeaux sur la carte
    cercle_pays1 = canvas_map.create_image(pays1.position[0], pays1.position[1], image=pays1.drapeau)
    cercle_pays2 =  canvas_map.create_image(pays2.position[0], pays2.position[1], image=pays2.drapeau)
    # on change et affiche la question
    question = f"Le pays \"{pays1.nom}\" à un(e) \"{indic}\" plus petit ou plus grand que le pays \"{pays2.nom}\" ?"
    label_top.configure(text=question)


### APPLICATION GRAPHICS ###
# FRAMES
frame_top = Frame(root, width=width, height=height//3, bg=bg)
frame_bot = Frame(root, width=width, height=height-(height//3), bg=bg)
frame_bot_left = Frame(frame_bot, width=width-(width//3), height=height-(height//3), bg=bg)
frame_bot_right = Frame(frame_bot, width=width//3, height=height-(height//3), bg=bg)
frame_top.pack()
frame_top.pack_propagate(0)
frame_bot.pack()
frame_bot.pack_propagate(0)
frame_bot_left.pack(side=LEFT)
frame_bot_left.pack_propagate(0)
frame_bot_right.pack(side=RIGHT)
frame_bot_right.pack_propagate(0)

# label_top
indic = choose_indic()
pays1, pays2 = choose_lands()
question = f"Le pays \"{pays1.nom}\" à un(e) \"{indic}\" plus petit ou plus grand que le pays \"{pays2.nom}\" ?"
reponse = ""
dico_couples[pays1.nom].append(pays2.nom)
dico_couples[pays2.nom].append(pays1.nom)
label_top = Label(frame_top, text=question, font=("Courrier", 28), bg=bg, fg="white", wraplength=1100, relief=GROOVE, bd=10, padx=50, pady=20)
label_top.pack(expand=YES)

# buttons
button1 = Button(frame_bot_right, text="plus petit", font=("Courrier", 24), bg=button_bg, fg="white", width=200, bd=3, cursor="hand2", command=button1_command)
button2 = Button(frame_bot_right, text="plus grand", font=("Courrier", 24), bg=button_bg, fg="white", width=200, bd=3, cursor="hand2", command=button2_command)
button_next = Button(frame_bot_right, text="next", font=("Courrier", 24), bg=button_bg, fg="white", width=200, bd=3, state=DISABLED, cursor="X_cursor", command=next_button_command)
button1.pack(padx=50, pady=20)
button2.pack(padx=50, pady=20)
button_next.pack(padx=50, pady=20)

# score
label_score = Label(frame_bot_right, text=f"{counter_good_question}/{num_current_question} questions", font=("Courrier", 22), bg=bg, fg="white", padx=50, pady=20)
label_score.pack()

# map
image = Image.open("ressources/images/earth_map.png")
image = image.resize((width-(width//3), height-(height//3)))
image_map = ImageTk.PhotoImage(image)

# canvas map
canvas_map = Canvas(frame_bot_left, width=width-(width//3), height=height-(height//3), bg=bg, highlightthickness=0)
canvas_map.create_image( (width-(width//3))//2, (height-(height//3))//2, image=image_map)
cercle_pays1 = canvas_map.create_image(pays1.position[0], pays1.position[1], image=pays1.drapeau)
cercle_pays2 =  canvas_map.create_image(pays2.position[0], pays2.position[1], image=pays2.drapeau)
canvas_map.place(relx=0, rely=0)


root.mainloop()
