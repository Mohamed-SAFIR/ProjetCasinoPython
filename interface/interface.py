import datetime
from tkinter import *
import sqlite3

global label
global name_user
global mise
global solde
global max_mise
global commul_mise
global mise_btn
global nb_partie_coup
global nbrparga
global nb_partie

#FONCTION DE CONNEXION A LA BASE DONNE
def connect():
    label.config(text="je suis python quel, est ton pseudo ?")
    global entry
    entry = Entry(right_frame,text="entre ton pseudo", font=("Courrier", 20), width=30, bg='#1FBA49')
    entry.pack()
    global ok_btn
    ok_btn = Button(right_frame, text="ok", font=("courrier", 20), bg="white", command=lambda: verifie_pseudo())
    ok_btn.pack(fill=X)
    validate_btn.destroy()

#FONCTION QUI VERIFIE LE PSEUDO DU JOUEUR
def verifie_pseudo():
    name = entry.get()
    name_user = (name,)
    global connexion
    global cursor
    # Connexion a la base donnée
    connexion = sqlite3.connect("db-casino.db")
    cursor = connexion.cursor()
    cursor.execute('SELECT * FROM ca_user WHERE user_name =?', name_user)
    row = cursor.fetchone()
    ok_btn.destroy()
    #En champs de saisie
    # Test si le joueur existe déja dans la base donnée
    if row is not None:
        label.config(text=f"salut {name} choisie ton niveau de jeux")
        global niv1_btn
        niv1_btn = Button(right_frame, text="Niveau1", width=13, font=("courrier", 20), bg="#85e29a",
                          command=lambda: niveau1(name_user, name))
        niv1_btn.pack()
        global niv2_btn
        niv2_btn = Button(right_frame, text="Niveau2", width=21, font=("courrier", 20), bg="white",
                          command=lambda: niveau2())
        niv2_btn.pack()
        global niv3_btn
        niv3_btn = Button(right_frame, text="Niveau3", width=34, font=("courrier", 20), bg="white",
                          command=lambda: niveau3())
        niv3_btn.pack()
    else:
        myDatetime = datetime.datetime.now()
        date = myDatetime.strftime('%Y-%m-%d %H:%M:%S')
        # Ajout du nouveau joueur
        new_user = (name, 10, 1, date, 0.0, 0.0, 0)
        cursor.execute(
            'INSERT INTO ca_user (user_name,solde,max_level,last_date,max_gain,max_perte,nbr_partie) VALUES (?,?,?,?,?,?,?)',
            new_user)
        connexion.commit()
        label.config(
            text=f"Hello {name}, vous avez 10 €, Très bien ! Installez vous SVP à la table de pari\nSouhaitez vous connaitre les règle de jeu ?")
        global oui_btn
        oui_btn = Button(right_frame, text="Oui",width=20, font=("courrier", 20), bg="#ffc733", command=lambda: afficherRegle(name,name_user))
        oui_btn.pack()
        global non_btn
        non_btn = Button(right_frame, text="Non",width=20, font=("courrier", 20), bg="#ffc733")
        non_btn.pack()
        ok_btn.destroy()

    # connexion.close()

#AFFICHAGE DES REGLES DU JEUX
def afficherRegle(name,name_user):
            global window1
            window1 = Tk()
            window1.title("Regles du jeu")
            window1.geometry("600x600")
            window1.minsize(500, 600)
            window1.maxsize(500, 600)
            window1.config(background='#1FBA49')
            regle1 = Label(window1, text="Voici les règles à respecter :", font=("courrier", 14), bg='#1FBA49',
                           fg='#E2BA1A').grid(row=0, column=0)
            regle2 = Label(window1, text=" Vous misez sur un nombre compris: ", font=("courrier", 12), bg='#1FBA49',
                           fg='white').grid(row=3, column=0)
            regle3 = Label(window1, text="-Entre 1 et 10  si vous êtes dans le level 1 ", font=("courrier", 10),
                           bg='#1FBA49', fg='white').grid(row=4, column=0)
            regle4 = Label(window1, text="-Entre 1 et 20  si vous êtes dans le level 2  ", font=("courrier", 10),
                           bg='#1FBA49', fg='white').grid(row=5, column=0)
            regle5 = Label(window1, text=" -Entre 1 et 30 si vous êtes dans le level 3 ", font=("courrier", 10),
                           bg='#1FBA49', fg='white').grid(row=6, column=0)
            regle4 = Label(window1, text="vous avez le droit à :", font=("courrier", 12), bg='#1FBA49',
                           fg='white').grid(row=7, column=0)
            regle5 = Label(window1, text="-Trois essais au level 1 !", font=("courrier", 10), bg='#1FBA49',
                           fg='white').grid(row=8, column=0)
            regle6 = Label(window1, text="-Cinq essais au level 2 !", font=("courrier", 10), bg='#1FBA49',
                           fg='white').grid(row=9, column=0)
            regle7 = Label(window1, text="-Sept essais au level 3 !", font=("courrier", 10), bg='#1FBA49',
                           fg='white').grid(row=10, column=0)
            regle8 = Label(window1,
                           text=" Chaque essai ne durera pas plus de 10 secondes. Au-delà,vous perdez votre essai ",
                           font=("courrier", 10), bg='#1FBA49', fg='white').grid(row=11, column=0)
            regle9 = Label(window1,
                           text=" - Si vous devinez mon nombre dès le premier coup, vous gagnez le double de votre mise !",
                           font=("courrier", 10), bg='#1FBA49', fg='white').grid(row=12, column=0)
            regle10 = Label(window1, text="- Si vous le devinez au 2è coup, vous gagnez exactement votre mise ! ",
                            font=("courrier", 10), bg='#1FBA49', fg='white').grid(row=13, column=0)
            regle11 = Label(window1, text=" - Si vous le devinez au 3è coup, vous gagnez la moitiè votre mise !",
                            font=("courrier", 10), bg='#1FBA49', fg='white').grid(row=14, column=0)
            regle12 = Label(window1, text="  vous avez le droit :  ", font=("courrier", 12), bg='#1FBA49',
                            fg='white').grid(row=15, column=0)
            regle13 = Label(window1,
                            text=" -De retenter votre chance avec l'argent qu'il vous reste pour reconquérir le level perdu. ",
                            font=("courrier", 10), bg='#1FBA49', fg='white').grid(row=16, column=0)
            regle14 = Label(window1, text="-De quitter le jeu.", font=("courrier", 10), bg='#1FBA49', fg='white').grid(
                row=17, column=0)
            regle15 = Label(window1, text="Dès que vous devinez mon nombre :", font=("courrier", 12), bg='#1FBA49',
                            fg='white').grid(row=18, column=0)
            regle16 = Label(window1, text="-Vous avez le droit de quitter le jeu et de partir avec vos gains.",
                            font=("courrier", 10), bg='#1FBA49', fg='white').grid(row=18, column=0)
            regle17 = Label(window1, text=" OU ", font=("courrier", 12), bg='#1FBA49', fg='white').grid(row=19,
                                                                                                        column=0)
            regle18 = Label(window1, text="-De continuer le jeu en passant au level supérieur.", font=("courrier", 10),
                            bg='#1FBA49', fg='white').grid(row=20, column=0)
            regle19 = Label(window1, text="Attention!.", font=("courrier", 12), bg='#1FBA49', fg='red').grid(row=21,
                                                                                                             column=0)
            regle20 = Label(window1, text="Si vous perdez un level, vous rejouez le level précédent.",
                            font=("courrier", 10), bg='#1FBA49', fg='white').grid(row=22, column=0)
            regle21 = Label(window1,
                            text="Quand vous souhaitez quitter le jeu, un compteur de 10 secondes est mis en place",
                            font=("courrier", 10), bg='#1FBA49', fg='white').grid(row=23, column=0)
            regle22 = Label(window1, text=" En absence de validation de la décision, le jeu est terminé.",
                            font=("courrier", 10), bg='#1FBA49', fg='white').grid(row=24, column=0)
            Annuler = Button(window1, text="Lancer une partie", font=("courrier", 11), bg='#ffc733', fg='#F01111',
                             command=lambda: premiere_partie(name_user, name))
            Annuler.place(x=210, y=550)
            oui_btn.destroy()
            non_btn.destroy()

#FONCTION DU niveau 1 de jeux pour un nouveau joueur
def premiere_partie(name_user, name):
    window1.destroy()
    label.config(text="Le jeu commence, entrez votre mise: ?")
    global mise_btn
    mise_btn = Button(right_frame, text="miser", font=("courrier", 20), bg="white",
                      command=lambda: miser(0, 0, 10, 0, 0, 0, 0,0, name))
    mise_btn.pack(fill=X)
    ok_btn.destroy()

#FONCTION DE NIVEAU 1 POUR UN JOEUR Déja inscrit
def niveau1(name_user,name):
    niv1_btn.destroy()
    niv2_btn.destroy()
    niv3_btn.destroy()
    # On récupère le solde dans la base de données
    cursor.execute('SELECT solde FROM ca_user WHERE user_name =?', name_user)
    row = cursor.fetchone()
    solde = row[0]
    # On vérifie si le solde n'est pas nul pour pouvoir continuer à jouer, s'il est nul on affiche un message et arrête le jeu
    if (solde == 0):
        partie_continue = False
        label.config(text="Désolé votre solde est nul !!!")
    else:
        partie_continue = True
    if (partie_continue):
        # On récupère le nombres de partie 'nbr_partie' dans la base de données
        cursor.execute('SELECT nbr_partie FROM ca_user WHERE user_name =?', name_user)
        row = cursor.fetchone()
        nb_partie = row[0]
        nb_partie = nb_partie + 1  # On incrémente le nombre de partie à chaque fois l'utilisateur joue
        # On récupère le gain maximum 'max_gain' dans la base de données
        cursor.execute('SELECT max_gain FROM ca_user WHERE user_name =?', name_user)
        row = cursor.fetchone()
        global gain
        gain = row[0]
        # On récupère le nombre de partie gangnée 'nbr_partie_ga' dans la base de données
        cursor.execute('SELECT nbr_partie_ga FROM ca_user WHERE user_name =?', name_user)
        row = cursor.fetchone()
        global nbrparga
        nbrparga = row[0]
        # On récupère la mise maximale 'max_mise' dans la base de données
        cursor.execute('SELECT max_mise FROM ca_user WHERE user_name =?', name_user)
        row = cursor.fetchone()
        mise_max = row[0]
        # On récupère le nombre de partie gagnéé sur le premier coup 'nbr_premier_coup' dans la base de données
        cursor.execute('SELECT nbr_premier_coup FROM ca_user WHERE user_name =?', name_user)
        row = cursor.fetchone()
        nb_partie_coup = row[0]
        # On récupère le cumule de la mise 'commul_mise' dans la base de données
        cursor.execute('SELECT commul_mise FROM ca_user WHERE user_name =?', name_user)
        row = cursor.fetchone()
        commul_mise = row[0]
        # On récupère le nombre de tentative ( tout les coups ) 'nbr_tentative' dans la base de données
        cursor.execute('SELECT nbr_tentative FROM ca_user WHERE user_name =?', name_user)
        row = cursor.fetchone()
        nb_tentative = row[0]
        # On récupère la perte maximale 'max_perte' dans la base de données
        cursor.execute('SELECT max_perte FROM ca_user WHERE user_name =?', name_user)
        row = cursor.fetchone()
        perte = row[0]
        # On récupère le nombre de partie perdue 'nbr_partie_pe' dans la base de données
        cursor.execute('SELECT nbr_partie_pe FROM ca_user WHERE user_name =?', name_user)
        row = cursor.fetchone()
        nbrparpe = row[0]
        # On récupère le niveau maximum atteint 'max_level' dans la base de données
        cursor.execute('SELECT max_level FROM ca_user WHERE user_name =?', name_user)
        row = cursor.fetchone()
        level = row[0]
        task = (level, nb_partie, name)
        # mise à jour de la base de donné pour la ligne de l'utilisateur avec le nouveau level et le nombre de partie
        cursor.execute('UPDATE ca_user SET max_level=?,nbr_partie=?WHERE user_name=?', task)
        connexion.commit()
        label.config(text="Le jeu commence, entrez votre mise: ?")
        global mise_btn
        mise_btn = Button(right_frame, text="miser", font=("courrier", 20), bg="white", command=lambda: miser(mise_max, commul_mise,solde,nbrparga,gain,perte,nb_tentative,nb_partie_coup,name))
        mise_btn.pack(fill=X)
        ok_btn.destroy()

#Fonction effectuer les mises
def miser(mise_max, commul_mise,solde,nbrparga,gain,perte,nb_tentative,nb_partie_coup,name):
   # while partie_continue:
        try:

            mise = float(entry.get())
            while (mise > solde) or (mise <= 0):  # si la mise est inférieur à 0 ou supérieur au solde du joueur
                label.config(text="Le montant saisi n'est pas valide. Entrer SVP un montant entre 1 et {} € :  ?".format(solde))
                mise_btn.destroy()
                mise_btn = Button(right_frame, text="miser", font=("courrier", 20), bg="#ffc733",command=lambda: miser(mise_max, commul_mise, solde))
                mise_btn.pack(fill=X)

            if (mise > 0) and (mise <= solde):  # la saisie de la mise est correcte
                partie_continue = False
                # Mise à jour du cumule de la mise sur la base de données
                commul_mise =commul_mise +  mise
                task = (commul_mise, "said")
                cursor.execute('UPDATE ca_user SET commul_mise=? WHERE user_name=?', task)
                connexion.commit()
                if (mise > mise_max):
                    mise_max = mise
        except ValueError:
            label.config(text="Veuillez entrer un NOMBRE SVP !")
        jouer(mise_max, commul_mise,solde,nbrparga,gain,perte,nb_tentative,nb_partie_coup,name)

#fonction pour jouer
def jouer(mise_max, commul_mise,solde,nbrparga,gain,perte,nb_tentative,nb_partie_coup,name):
    def choix_nombre(nb_python,nb_coup):
        nb_user = int(entry.get())

        while (nb_coup < 3):
            try:
                if (nb_user < 1) or (nb_user > 10):  # Si le nombre saisie est inférieur à 0 ou supérieur à 10
                    label.config(text="Je ne comprends pas ! Entrer SVP un nombre entre 1 et 10 :  ?")
                    choix_btn.destroy()
                    choix1 =Button(right_frame, text="valider choix", font=("courrier", 20), bg="white", command=lambda: choix_nombre(nb_python))
                    choix1.pack()
                    break

                if nb_user == nb_python:  # Si le nombre saisie est égal au random,
                    label.config(text=f"Bingo ! Vous avez gagné en {nb_coup} coup(s) !")
                    import winsound
                    winsound.PlaySound('son.wav', winsound.SND_FILENAME | winsound.SND_ASYNC)
                    choix1.destroy()
                    choix_btn.destroy()
                    choix2 = Button(right_frame, text="valider choix", font=("courrier", 20), bg="white",command=lambda: choix_nombre(nb_python,(nb_coup+1)))
                    choix2.pack()
                    break
                if nb_user > nb_python:  # Si le nombre saisie est supérieur au random
                    label.config(text="Votre nbre est trop grand'")
                    choix_btn.destroy()
                    choix = Button(right_frame, text="valider choix", font=("courrier", 20), bg="white",
                                   command=lambda: choix_nombre(nb_python,(nb_coup+1)))
                    choix.pack()
                    break

                if nb_user < nb_python:  # Si le nombre saisie est inférieur au random
                    label.config(text="Votre nbre est trop petit")
                    choix_btn.destroy()
                    choix = Button(right_frame, text="valider choix", font=("courrier", 20), bg="white",
                                   command=lambda: choix_nombre(nb_python,(nb_coup+1)))
                    choix.pack()
                    break

            except ValueError:
                    label.config(text="Veuillez entrer un NOMBRE SVP !")
     # Tant que le nombre saisie est différent du random, et le nombre de coups ne dépasse pas 3 :
    nb_coup=1
    from random import randrange
    nb_python = randrange(1, 11, 1)  # Un random de 1 à 10
    label.config(text="Alors, mon nombre est : ?\n")
    mise_btn.destroy()
    global choix_btn
    choix_btn=Button(right_frame, text="valider choix", font=("courrier", 20), bg="white", command=lambda: choix_nombre(nb_python,nb_coup))
    choix_btn.pack()


# Fenetre principal
window = Tk()
# personnalisation de la fenetre
window.title("Casino")
window.geometry("1600x900")
window.iconbitmap('logo.ico')
window.config(background='#1FBA49')
# Creer la frame principale
frame = Frame(window, bg='#1FBA49')
# Création d'image
width = 500
height = 600
image = PhotoImage(file="image.png")
canvas = Canvas(frame, width=width, height=height, bg='#1FBA49', bd=0, highlightthickness=0)
canvas.create_image(250, 300, image=image)
canvas.grid(row=0, column=0, sticky=W)
# creersous boite
right_frame = Frame(frame, bg='#1FBA60')
left_frame = Frame(frame, bg='WHITE')
# Creer un titre
label_title = Label(window, text="Bienvenue au Casino", font=("Courrier", 30), bg='#1FBA49')
label_title.pack()

global validate_btn
validate_btn = Button(right_frame, text="Commencer", font=("courrier", 20), bg="#ffc733",command=lambda :connect())
validate_btn.pack(fill=X)

label = Label(right_frame, text="Appuyer sur commencer pour jouer", font=("courrier", 20), bg='#8cf26a', fg='#231903')
label.pack()

# creer boutton quite
exit_button = Button(window, text="quitter", font=("courrier", 20), bg="#ffc733", command=window.quit)
exit_button.place(x=970,y=660)

# on place la sous boite à droite de la frame principale
right_frame.grid(row=0, column=2, sticky=W)
left_frame.grid(row=0, column=1, sticky=W)
# afficher le frame
frame.pack(expand=YES)
# affichage
window.mainloop()


