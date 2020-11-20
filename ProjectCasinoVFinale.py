import datetime
import sqlite3
import time
from inputimeout import inputimeout, TimeoutOccurred


# Connexion a notre base de donnée
connexion = sqlite3.connect("db-casino.db")
cursor = connexion.cursor()



# Cette fonction nous permets d'appeler les fonctions level en fonction du nombre de niveau saisie par l'utilisateur
def appel_level(name_user,level,name):
    if (level==1):
        nb_level_1(name_user,name)
    if (level==2):
        nb_level_2(name_user,name)
    if (level==3):
        nb_level_3(name_user,name)


# La fonction level, elle demande a l'utilisateur de donner son pseudo, et verifie s'il existe dans la base de données
# si oui il lui demande de choisir un level, sinon il ajoute l'utilisateur à la base de données et lui affecte le level 1
def level():
    # initilialisation du niveau
    level = 1
    print('\t\t\tJe suis Python. Quel est votre pseudo ?\n')
    name = input()
    name_user = (name,)
    # verification si l'utilisateur existe dans base donnée
    cursor.execute('SELECT * FROM ca_user WHERE user_name =?',name_user)
    row = cursor.fetchone()
    print ("\n\t\t\tHello",name +".\nTrès bien ! Installez vous SVP à la table de pari.\n")
    print("\t\t\tSouhaitez-vous connaitre les règles du jeu ? (o/n)\n")
    regle = input ()
    while(regle!='o') and (regle!='O') and (regle!='n') and (regle!='N'):
        regle=input("\t\t\tJe ne comprends pas votre réponse. Veuillez répondre par (O/N) ?")
    if(regle=='n') or (regle=='N'):
        print("\n\t\t\tDaccord ! On continue sans afficher les règles du jeu Alors !\n")
    else:
        print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————")
        print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n")
        print ("Vous misez sur un nombre comprit:\n \t\t-Entre 1 et 10 € si vous êtes dans le niveau 1 \n \t\t-Entre 1 et 20 € si vous êtes dans le niveau 2 \n \t\t-Entre 1 et 30 € si vous êtes dans le niveau 3 ")
        print("\nVous avez le droit à : \n \t\t-Trois essais au niveau 1 ! \n \t\t-Cinq essais au niveau 2 ! \n \t\t-Sept essais au niveau 3 ! \n ")
        print("\nChaque essai ne durera pas plus de 10 secondes. Au-delà,vous perdez votre essai")
        print("\t\t- Si vous devinez mon nombre dès le premier coup, vous gagnez le double de votre mise !")
        print("\t\t- Si vous le devinez au 2è coup, vous gagnez exactement votre mise !")
        print("\t\t- Si vous le devinez au 3è coup, vous gagnez la moitiè votre mise !")
        print("\t\t- Si vous ne le devinez pas au 3è coup, vous perdez votre mise et vous avez le droit :")
        print("\t\t\t\t-de retenter votre chance avec l'argent qu'il vous reste pour reconquérir le niveau perdu.")
        print("\t\t\t\t-de quitter le jeu.\n")    
        print("-Dès que vous devinez mon nombre :\n  \t\tvous avez le droit de quitter le jeu et de partir avec vos gains OU de continuer le jeu en passant au niveau supérieur.")
        print("\n Attention!")
        print("\t\tSi vous perdez un niveau, vous rejouez le niveau précédent.Quand vous souhaitez quitter le jeu, un compteur de 10 secondes est mis en place.\n \t\tEn absence de validation de la décision, le jeu est terminé")
        print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————")
        print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n\n")



    if row is not None: # Si l'utilisateur existe dans la base de données
        cursor.execute('SELECT max_level FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        max_level=row[0] # On récupère le dernier level de ce user
        stat(name)
        print("\n\n\t\t\t POUVEZ VOUS FAIRE MEIUX !!!! \n\n")
        print('\t\t\tchoisissez un niveau de jeux')
        while True:
            level = input()
            try:
                levelChoice = int(level)
                if (levelChoice >= 1) and (levelChoice <= max_level):
                    level = levelChoice
                    break
                else:
                    print('\t\t\tEntrez un niveau entre 1 et {}'.format(max_level))
            except ValueError:
                print("\t\t\tEntrez un niveau de 1 à {}".format(max_level))
        appel_level(name_user,level,name)
    else: # Si l'utilisateur n'existe pas 
        myDatetime = datetime.datetime.now()
        date = myDatetime.strftime('%Y-%m-%d %H:%M:%S')
        new_user = (name, 10, 1, date, 0.0, 0.0, 0,0,0,0.0,0,0.0,0)
        cursor.execute('INSERT INTO ca_user (user_name,solde,max_level,last_date,max_gain,max_perte,nbr_partie,nbr_partie_ga,nbr_partie_pe,max_mise,nbr_premier_coup,commul_mise,nbr_tentative) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',new_user)
        connexion.commit()
        appel_level(name_user,level,name)



# la fonction nb_level_3, permet de jouer quand le joeuer passe au level 3
def nb_level_3(name_user,name):
    # On récupère le solde dans la base de données
    cursor.execute('SELECT solde FROM ca_user WHERE user_name =?', name_user)
    row=cursor.fetchone()
    solde=row[0]
    # On vérifie si le solde n'est pas nul pour pouvoir continuer à jouer, s'il est nul on affiche un message et arrête le jeu
    if(solde==0):
        partie_continue=False
        print("\t\t\tOups !!! Vous n'avez plus de solde!\n")
    else:
        partie_continue=True
    if(partie_continue):
        # On récupère le nombres de partie 'nbr_partie' dans la base de données
        cursor.execute('SELECT nbr_partie FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        nb_partie=row[0]
        nb_partie=nb_partie+1  # On incrémente le nombre de partie à chaque fois l'utilisateur joue
        # On récupère le gain maximum 'max_gain' dans la base de données
        cursor.execute('SELECT max_gain FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        gain=row[0]
        # On récupère le nombre de partie gangnée 'nbr_partie_ga' dans la base de données
        cursor.execute('SELECT nbr_partie_ga FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        nbrparga=row[0]
        # On récupère la mise maximale 'max_mise' dans la base de données
        cursor.execute('SELECT max_mise FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        mise_max=row[0]
        # On récupère le nombre de partie gagnéé sur le premier coup 'nbr_premier_coup' dans la base de données
        cursor.execute('SELECT nbr_premier_coup FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        nb_partie_coup=row[0]
        # On récupère le cumule de la mise 'commul_mise' dans la base de données
        cursor.execute('SELECT commul_mise FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        commul_mise=row[0]
        # On récupère le nombre de tentative ( tout les coups ) 'nbr_tentative' dans la base de données
        cursor.execute('SELECT nbr_tentative FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        nb_tentative=row[0]
        # On récupère le nombre de tentative ( tout les coups ) 'nbr_tentative' dans la base de données
        cursor.execute('SELECT max_perte FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        perte=row[0]
        # On récupère le nombre de partie perdue 'nbr_partie_pe' dans la base de données
        cursor.execute('SELECT nbr_partie_pe FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        nbrparpe=row[0]
        # On récupère le niveau maximum atteint 'max_level' dans la base de données
        cursor.execute('SELECT max_level FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        level=row[0]
        if(level>3):
            level=level
        else:
            level=3
        # mise à jour de la base de donné pour la ligne de l'utilisateur avec le nouveau level et le nombre de partie
        task=(level,nb_partie,name)
        cursor.execute('UPDATE ca_user SET max_level=?,nbr_partie=? WHERE user_name=?',task)
        connexion.commit()
        print("\n\t\t\tVotre solde est : {} ***".format(round(solde,2)))
        print("\n\t\t\tRappelez vous, le principe est le même sauf que mon nombre est maintenant entre 1 et 30 et vous avez le droit à 7 essais !")
        partie_continue=True
        while partie_continue:
            try:
                mise=float(input("\t\t\tEntrez votre mise: ?")) 
                if (mise<0) or (mise>solde): # si la mise est supérieur au solde et inférieur à 0
                    print("\t\t\tOups!!! votre mise est supérieur à votre solde.")
                    print("\t\t\tEntrer une mise inférieure ou égale à {} € : ?".format(round(solde,2)))
                if (mise>0) and (mise<=solde): #la saisie est correcte
                    partie_continue=False
                    # Mise à jour du cumule de la mise sur la base de données
                    commul_mise=mise+commul_mise
                    task=(commul_mise,name)
                    cursor.execute('UPDATE ca_user SET commul_mise=? WHERE user_name=?',task)
                    connexion.commit()
                    if(mise>mise_max):
                        mise_max=mise  
            except ValueError:
                print("\n\t\t\t Veuillez entrez un NOMBRE SVP !")
        from random import randrange
        nb_python = randrange(1, 31, 1) # un random de 1 à 30
        nb_user = -1
        nb_coup = 0
        gainA=0
        # Tant que le nombre saisie est différent du random, et le nombre de coups ne dépasse pas 7 :
        while (nb_python != nb_user) and (nb_coup<7) :
            try:  
                # nb_user = int(input("\n\t\t\tAlors, mon nombre est : ?\n"))
                nb_user = int(inputimeout("\n\t\t\tAlors, mon nombre est : ?\n", timeout=10))
                if (nb_user<1) or (nb_user>30): # Si le nombre saisie est inférieur à 0 ou supérieur à 30
                    print("\t\t\tJe ne comprends pas ! Entrez SVP un nombre entre 1 et 30 :  ?")
                if nb_user > nb_python : # Si le nombre est supérieur au random
                    print ('\n\t\t\tVotre nombre est trop grand')
                elif nb_user < nb_python : # Si le nombre est inférieur au random
                    print ('\n\t\t\tVotre nombre est trop petit')
                nb_coup += 1 # On incrémentele nombre de coups
                # Avertissement lorsque il nous reste une chance
                if(nb_coup==6):
                    print("\n\t\t\tIl vous reste une chance !")
                if(nb_python == nb_user): # si le nombre saisie égale le random
                    trouver=True
                else:
                    trouver=False
            except ValueError:
                print("\n\t\t\tVeuillez entrer un NOMBRE SVP !")
        if (trouver):
            print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————")
            print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n")
            print("\n\n\t\t\t\tBingo ! Vous avez gagné en {} coup(s) !".format(nb_coup))
            nbrparga=nbrparga+1 # Incrémentation de nombre de partie gagnée
            nb_coup_total=nb_tentative+nb_coup # Mise à jour du nombre de tentatives
            # Vérification à quel coup le joueur à réussi, affectation des gains
            if(nb_coup==1):
                newSolde=(2*mise)+solde
                gainA=(2*mise)
                nb_partie_coup=nb_partie_coup+1
            if(nb_coup==2):
                newSolde=mise+solde
                gainA=(mise)
            if(nb_coup==3):
                newSolde=(0.5*mise)+solde
                gainA=(0.5*mise)
            if(nb_coup==4):
                newSolde=(mise*0.25)+solde
                gainA=(0.25*mise)
            if(nb_coup==5):
                newSolde=(mise*0.2)+solde
                gainA=(0.2*mise)
            if(nb_coup==6):
                newSolde=(mise*0.17)+solde
                gainA=(0.17*mise)
            if(nb_coup==7):
                newSolde=(mise*0.14)+solde
                gainA=(0.14*mise)
            # Mise à jour des champs : solde, le gain maximum, le nombre de partie gagnée, la mise maximale, le nombre de tentative de la base de données
            if(gainA>gain):
                gain=gainA
            task=(newSolde,gain,nbrparga,mise_max,nb_partie_coup,nb_coup_total,name)
            cursor.execute('UPDATE ca_user SET solde = ? ,max_gain=?,nbr_partie_ga=?,max_mise=?,nbr_premier_coup=? ,nbr_tentative=? WHERE user_name = ?',task)
            connexion.commit()
            print("\n\t\t\tBravo, vous avez gagné ! Les statistiques de la partie en cours sont les suivantes : ")
            # Demande au joueur s'il peut faire mieux, ou quitter
            print("\n\t\t\tLes statistiques du niveau 3 sont les suivantes :\n")
            stat_niveau(gainA,nb_coup,3,mise,1)
            print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————")
            print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n")
            contin=input("\n\t\t\tPouvez-vous faire mieux (O/N) ?")
            while(contin!='o') and (contin!='O') and (contin!='n') and (contin!='N'):
                contin=input("\t\t\tJe ne comprends pas votre réponse. Veuillez répondre par (O/N) ?")
            if(contin=='n') or (contin=='N'):
                print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n")
                print("\t\t\tAu revoir ! Vous finissez la partie avec {} €.".format(round(newSolde,2)))
                stat(name)
            else: # Possibilité de rejouer les niveaux actuel et inférieurs
                print("\t\t\tSuper ! Allons-y !")
                while True:
                    rep=int(input("\t\t\tChoisissez un niveau entre 1 et 3 !"))
                    try:
                        if (rep==1):
                            nb_level_1(name_user,name)
                            break
                        if (rep==2):
                            nb_level_2(name_user,name)
                            break
                        if (rep==3):
                            nb_level_3(name_user,name)
                            break
                        print("\t\t\tEntrer un niveau entre 1 et 3 !!! ")
                    except ValueError:
                        print("\t\t\tEntrer un niveau entre 1 et 3 !!! ")
        else:
            print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————")
            print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n")
            print("\n\n\t\t\t\tVous avez perdu ! Mon nombre est: {} !".format(nb_python))
            print("\n\t\t\tLes statistiques du niveau 3 sont les suivantes :\n")
            stat_niveau(gainA,nb_coup,3,mise,0)
            nbrparpe=nbrparpe+1 # Incrémentation du nombre de partie perdue
            # Mise à jour des champs : solde, la perte maximale, le nombre de partie perdue, la mise maximale, le nombre de tentative de la base de données
            newSolde=solde-mise
            if(perte<mise):
                perte=mise
            nb_tentative=nb_tentative+7
            if(mise>mise_max):
                mise_max=mise
            task=(newSolde,perte,nbrparpe,mise_max,nb_tentative,name)
            cursor.execute('UPDATE ca_user SET solde=?, max_perte=?, nbr_partie_pe=?, max_mise=?, nbr_tentative=? WHERE user_name=?',task)
            connexion.commit()
            # Demande au joueur la possibilté de retenter sa chance avec le reste de son solde
            if(newSolde!=0):
                contin=input("\n\t\t\tRetentez votre chance avec {} € qui vous reste (O/N) ?".format(round(newSolde,2)))
                while(contin!='o') and (contin!='O') and (contin!='n') and (contin!='N'):
                    contin=input("\t\t\tJe ne comprends pas votre réponse. Veuillez répondre par (O/N) ?")
                if(contin=='n') or (contin=='N'):
                    print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n")
                    print("\t\t\tAu revoir ! Vous finissez la partie avec {} €.".format(round(newSolde,2)))
                    stat(name)
                else:  # Possibilité de rejouer les niveaux actuel et inférieurs
                    print("\t\t\tSuper ! Aloons-y ! ")
                    while True:
                        rep=int(input("\t\t\tChoisissez un niveau entre 1 et {} !".format(level)))
                        try:
                            if (rep==1):
                                nb_level_1(name_user,name)
                                break
                            if (rep==2):
                                nb_level_2(name_user,name)
                                break
                            if (rep==3):
                                nb_level_3(name_user,name)
                                break
                            print("\t\t\tEntrer un niveau entre 1 et {} !!! ".format(level))
                        except ValueError:
                            print("\t\t\tEntrer un niveau entre 1 et {} !!! ".format(level))
            else:
                print("\n\n\t\t\tOups !!! Vous n'avez plus de solde. Vous ne pouvez pas continuer !\n\n")


# la fonction nb_level_2, permet de jouer quand le joeuer passe au level 2
def nb_level_2(name_user,name):
    # On récupère le solde dans la base de données
    cursor.execute('SELECT solde FROM ca_user WHERE user_name =?', name_user)
    row=cursor.fetchone()
    solde=row[0]
    # On vérifie si le solde n'est pas nul pour pouvoir continuer à jouer, s'il est nul on affiche un message et arrête le jeu
    if(solde==0):
        partie_continue=False
        print("\t\t\tOups !!! Vous n'avez plus de solde!\n")
    else:
        partie_continue=True
    if(partie_continue):
        # On récupère le nombres de partie 'nbr_partie' dans la base de données
        cursor.execute('SELECT nbr_partie FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        nb_partie=row[0]
        nb_partie=nb_partie+1 # On incrémente le nombre de partie à chaque fois l'utilisateur joue
        # On récupère le gain maximum 'max_gain' dans la base de données
        cursor.execute('SELECT max_gain FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        gain=row[0]
        # On récupère le nombre de partie gangnée 'nbr_partie_ga' dans la base de données
        cursor.execute('SELECT nbr_partie_ga FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        nbrparga=row[0]
        # On récupère la mise maximale 'max_mise' dans la base de données
        cursor.execute('SELECT max_mise FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        mise_max=row[0]
        # On récupère le nombre de partie gagnéé sur le premier coup 'nbr_premier_coup' dans la base de données
        cursor.execute('SELECT nbr_premier_coup FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        nb_partie_coup=row[0]
        # On récupère le cumule de la mise 'commul_mise' dans la base de données
        cursor.execute('SELECT commul_mise FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        commul_mise=row[0]
        # On récupère le nombre de tentative ( tout les coups ) 'nbr_tentative' dans la base de données
        cursor.execute('SELECT nbr_tentative FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        nb_tentative=row[0]
        # On récupère la perte maximale 'max_perte' dans la base de données
        cursor.execute('SELECT max_perte FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        perte=row[0]
        # On récupère le nombre de partie perdue 'nbr_partie_pe' dans la base de données
        cursor.execute('SELECT nbr_partie_pe FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        nbrparpe=row[0]
        # On récupère le niveau maximum atteint 'max_level' dans la base de données
        cursor.execute('SELECT max_level FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        level=row[0]
        if(level>2):
            level=level
        else:
            level=2
        # mise à jour de la base de donné pour la ligne de l'utilisateur avec le nouveau level et le nombre de partie
        task=(level,nb_partie,name)
        cursor.execute('UPDATE ca_user SET max_level=?,nbr_partie=? WHERE user_name=?',task)
        connexion.commit()
        print("\n\t\t\tVotre solde est de : {} ".format(round(solde,2)))
        print("\n\t\t\tRappelez vous, le principe est le même sauf que mon nombre est maintenant entre 1 et 20 et vous avez le droit à 5 essais !")
        partie_continue=True
        while partie_continue:
            try:
                mise=float(input("\t\t\t-Entrez votre mise: ?")) 
                if (mise<0) or (mise>solde): # si la mise est supérieur au solde ou inférieur à 0
                    print("\t\t\tOups!!! Votre mise est supérieure à votre solde.")
                    print("\t\t\tEntrez une mise inférieure ou égale à {} € : ?".format(round(solde,2)))
                if (mise>0) and (mise<=solde): #la saisie est correcte
                    partie_continue=False 
                    # Mise à jour du cumule de la mise sur la base de données
                    commul_mise=mise+commul_mise
                    task=(commul_mise,name)
                    cursor.execute('UPDATE ca_user SET commul_mise=? WHERE user_name=?',task)
                    connexion.commit()
                    if(mise>mise_max):
                        mise_max=mise 
            except ValueError:
                print("\n\t\t\tVeuillez entrez un NOMBRE SVP !")
        from random import randrange
        nb_python = randrange(1, 21, 1) # un random de 1 à 20
        nb_user = -1
        nb_coup = 0
        gainA=0
        # Tant que le nombre saisie est différent du random, et le nombre de coups ne dépasse pas 5 :
        while (nb_python != nb_user) and (nb_coup<5) :
            try:  
                # nb_user = int(input("\n\t\t\tAlors, mon nombre est : ?\n"))
                nb_user = int(inputimeout("\n\t\t\tAlors, mon nombre est : ?\n", timeout=10))
                if (nb_user<1) or (nb_user>20): # Si le nombre saisie est inférieur à 0 ou supérieur à 20 
                    print("\t\t\tJe ne comprends pas ! Entrer SVP un nombre entre 1 et 20 :  ?")
                if nb_user > nb_python : # Si le nombre saisie est supérieur au random
                    print ('\n\t\t\tVotre nombre est trop grand')
                elif nb_user < nb_python : # Si le nombre saisie est inférieur au random
                    print ('\n\t\t\tVotre nombre est trop petit')
                nb_coup += 1 # On incrémentele nombre de coups
                # Avertissement lorsque il nous reste une chance
                if(nb_coup==4):
                    print("\n\t\t\tIl vous reste une chance !")
                if(nb_python == nb_user): # si le nombre saisie égale le random
                    trouver=True
                else:
                    trouver=False
            except ValueError:
                print("\n\t\t\tVeuillez entrez un NOMBRE SVP !")
        if (trouver): 
            print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————")
            print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n")
            print("\n\n\t\t\t\tBingo ! Vous avez gagné en {} coup(s) !".format(nb_coup))
            nbrparga=nbrparga+1 # Incrémentation de nombre de partie gagnée
            nb_coup_total=nb_tentative+nb_coup # Incrémentation de nombre de tentatives
            # Vérification à quel coup le joueur à réussi, affectation des gains
            if(nb_coup==1):
                newSolde=(2*mise)+solde
                gainA=(2*mise)
                nb_partie_coup=nb_partie_coup+1
            if(nb_coup==2):
                newSolde=mise+solde
                gainA=(mise)
            if(nb_coup==3):
                newSolde=(0.5*mise)+solde
                gainA=(0.5*mise)
            if(nb_coup==4):
                newSolde=(mise*0.25)+solde
                gainA=(0.25*mise)
            if(nb_coup==5):
                newSolde=(mise*0.2)+solde
                gainA=(0.2*mise)
            # Mise à jour des champs : solde, le gain maximum, le nombre de partie gagnée, la mise maximale, le nombre de tentative de la base de données
            if(gainA>gain):
                gain=gainA
            task=(newSolde,gain,nbrparga,mise_max,nb_partie_coup,nb_coup_total,name)
            cursor.execute('UPDATE ca_user SET solde = ?,max_gain=?,nbr_partie_ga=?,max_mise=?,nbr_premier_coup=? ,nbr_tentative=? WHERE user_name = ?',task)
            connexion.commit()
            print("\n\t\t\tBravo, vous avez gagné ! Les statistiques de la partie en cours sont les suivantes : ...")
            # Demande au joueur s'il souhaite continuer la partie en passant au level 3
            print("\n\t\t\tLes statistiques du niveau 2 sont les suivantes :\n")
            stat_niveau(gainA,nb_coup,2,mise,1)
            print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————")
            print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n")
            contin=input("\n\t\t\tSouhaitez-vous continuer la partie (O/N) ?")
            while(contin!='o') and (contin!='O') and (contin!='n') and (contin!='N'):
                contin=input("\t\t\tJe ne comprends pas votre réponse. Veuillez répondre par (O/N) ?")
            if(contin=='n') or (contin=='N'):
                print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n")
                print("\t\t\tAu revoir ! Vous finissez la partie avec {} €.".format(round(newSolde,2)))
                stat(name)
            else:
                print("\t\t\tSuper ! Vous passez au niveau 3.")
                nb_level_3(name_user,name)
        else:
            print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————")
            print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n")
            print("\n\n\t\t\t\tVous avez perdu ! Mon nombre est: {} !".format(nb_python))
            print("\n\t\t\tLes statistiques du niveau 2 sont les suivantes :\n")
            stat_niveau(gainA,nb_coup,2,mise,0)
            nbrparpe=nbrparpe+1 # Incrémentation du nombre de partie perdue
            # Mise à jour des champs : solde, la perte maximale, le nombre de partie perdue, la mise maximale, le nombre de tentative de la base de données
            newSolde=solde-mise
            if(perte<mise):
                perte=mise
            nb_tentative=nb_tentative+5
            if(mise>mise_max):
                mise_max=mise
            task=(newSolde,perte,nbrparpe,mise_max,nb_tentative,name)
            cursor.execute('UPDATE ca_user SET solde=?, max_perte=?, nbr_partie_pe=?, max_mise=?, nbr_tentative=? WHERE user_name=?',task)
            connexion.commit()
            # Demande au joueur la possibilté de retenter sa chance avec le reste de son solde
            if(newSolde!=0):
                contin=input("\n\t\t\tRetentez votre chance avec {} € qui vous reste (O/N) ?".format(round(newSolde,2)))
                while(contin!='o') and (contin!='O') and (contin!='n') and (contin!='N'):
                    contin=input("\t\t\tJe ne comprends pas votre réponse. Veuillez répondre par (O/N) ?")
                if(contin=='n') or (contin=='N'):
                    print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n")
                    print("\t\t\tAu revoir ! Vous finissez la partie avec {} €.".format(round(newSolde,2)))
                    stat(name)
                else: # Possibilité de rejouer les niveaux actuel et inférieurs
                    print("\t\t\tSuper ! Allons-y !!")
                    while True:
                        rep=int(input("\t\t\tChoisissez un niveau entre 1 et {} !".format(level)))
                        try:
                            if (rep==1):
                                nb_level_1(name_user,name)
                                break
                            if (rep==2):
                                nb_level_2(name_user,name)
                                break
                            if (rep==3):
                                nb_level_3(name_user,name)
                                break
                            print("\t\t\tEntrer un niveau entre 1 et {} !!! ".format(level))
                        except ValueError:
                            print("\t\t\tEntrer un niveau entre 1 et {} !!! ".format(level))
            else:
                print("\n\n\t\t\tOups !!! Vous n'avez plus de solde. Vous ne pouvez pas continuer !\n\n")



# la fonction nb_level_1, permet de jouer quand le joeuer est au level 1
def nb_level_1(name_user,name):
    # On récupère le solde dans la base de données
    cursor.execute('SELECT solde FROM ca_user WHERE user_name =?', name_user)
    row=cursor.fetchone()
    solde=row[0]
    # On vérifie si le solde n'est pas nul pour pouvoir continuer à jouer, s'il est nul on affiche un message et arrête le jeu
    if(solde==0):
        partie_continue=False
        print("\t\t\tOups !!! Vous n'avez plus de solde!\n")
    else:
        partie_continue=True
    if(partie_continue):
        # On récupère le nombres de partie 'nbr_partie' dans la base de données
        cursor.execute('SELECT nbr_partie FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        nb_partie=row[0]
        nb_partie=nb_partie+1 # On incrémente le nombre de partie à chaque fois l'utilisateur joue
        # On récupère le gain maximum 'max_gain' dans la base de données
        cursor.execute('SELECT max_gain FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        gain=row[0]
        # On récupère le nombre de partie gangnée 'nbr_partie_ga' dans la base de données
        cursor.execute('SELECT nbr_partie_ga FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        nbrparga=row[0]
        # On récupère la mise maximale 'max_mise' dans la base de données
        cursor.execute('SELECT max_mise FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        mise_max=row[0]
        # On récupère le nombre de partie gagnéé sur le premier coup 'nbr_premier_coup' dans la base de données
        cursor.execute('SELECT nbr_premier_coup FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        nb_partie_coup=row[0]
        # On récupère le cumule de la mise 'commul_mise' dans la base de données
        cursor.execute('SELECT commul_mise FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        commul_mise=row[0]
        # On récupère le nombre de tentative ( tout les coups ) 'nbr_tentative' dans la base de données
        cursor.execute('SELECT nbr_tentative FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        nb_tentative=row[0]
        # On récupère la perte maximale 'max_perte' dans la base de données
        cursor.execute('SELECT max_perte FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        perte=row[0]
        # On récupère le nombre de partie perdue 'nbr_partie_pe' dans la base de données
        cursor.execute('SELECT nbr_partie_pe FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        nbrparpe=row[0]
        # On récupère le niveau maximum atteint 'max_level' dans la base de données
        cursor.execute('SELECT max_level FROM ca_user WHERE user_name =?', name_user)
        row=cursor.fetchone()
        level=row[0]
        if(level>1):
            level=level
        else:
            level=1
        task=(level,nb_partie,name)
        # mise à jour de la base de donné pour la ligne de l'utilisateur avec le nouveau level et le nombre de partie
        cursor.execute('UPDATE ca_user SET max_level=?,nbr_partie=?WHERE user_name=?',task)
        connexion.commit()
        print("\n\t\t\tVotre solde est : {} ".format(round(solde,2)))
        print("\n\t\t\tRappelez vous, le principe est le même sauf que mon nombre est maintenant entre 1 et 10 et vous avez le droit à 3 essais !")
        while partie_continue:
            try:
                mise=float(input("\t\t\tle jeu commence, entrez votre mise: ?"))
                if (mise>solde) or (mise<=0): # si la mise est inférieur à 0 ou supérieur au solde du joueur
                    print("\t\t\tOups!!! Votre mise est suprérieure à votre solde.")
                    print("\t\t\tEntrez une mise inférieure ou égale à {} € : ?".format(round(solde,2)))
                if (mise>0) and (mise<=solde): # la saisie de la mise est correcte
                    partie_continue=False
                    # Mise à jour du cumule de la mise sur la base de données
                    commul_mise=mise+commul_mise
                    task=(commul_mise,name)
                    cursor.execute('UPDATE ca_user SET commul_mise=? WHERE user_name=?',task)
                    connexion.commit()
                    if(mise>mise_max):
                        mise_max=mise  
            except ValueError:
                print("\n\t\t\t  Veuillez entrer un NOMBRE SVP !")
        from random import randrange
        nb_python = randrange(1, 11, 1) # Un random de 1 à 10
        nb_user = -1
        nb_coup = 0
        gainA=0
        # Tant que le nombre saisie est différent du random, et le nombre de coups ne dépasse pas 3 : 
        while (nb_python != nb_user) and (nb_coup<3) :
            try:  
                #nb_user = int(input("\n\t\t\tAlors, mon nombre est : ?\n"))
                nb_user = int(inputimeout("\n\t\t\tAlors, mon nombre est : ?\n", timeout=10))
                if (nb_user<1) or (nb_user>10): # Si le nombre saisie est inférieur à 0 ou supérieur à 10 
                    print("\t\t\tJe ne comprends pas ! Entrer SVP un nombre entre 1 et 10 :  ?")
                if nb_user > nb_python : # Si le nombre saisie est supérieur au random
                    print ('\n\t\t\tVotre nombre est trop grand')
                elif nb_user < nb_python : # Si le nombre saisie est inférieur au random
                    print ('\n\t\t\tVotre nombre est trop petit')
                if (nb_user>=1) and (nb_user<=10):
                    nb_coup += 1 # Incrémentation de nombre de coups
                if(nb_coup==2): # Avertissement quand il nous reste qu'une chance
                    print("\n\t\t\tIl vous reste une chance !")
                if(nb_python == nb_user): # Si le nombre saisie est égal au random,
                    trouver=True
                else:
                    trouver=False
            except ValueError:
                print("\n\t\t\t Veuillez entrer un NOMBRE SVP !")
        if (trouver): # Si le nombre saisie est égal au random
            print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————")
            print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n")
            print("\n\n\t\t\t\tBingo ! Vous avez gagné en {} coup(s) !".format(nb_coup))
            nbrparga=nbrparga+1 # Incrémentation de nombre de partie gagnée
            nb_coup_total=nb_tentative+nb_coup # Mise à jour du nombre de tentatives
            # Vérification à quel coup le joueur à réussi, affectation des gains
            if(nb_coup==1):
                newSolde=(2*mise)+solde
                gainA=(2*mise)
                nb_partie_coup=nb_partie_coup+1
            if(nb_coup==2):
                newSolde=mise+solde
                gainA=(mise)
            if(nb_coup==3):
                newSolde=(0.5*mise)+solde
                gainA=(0.5*mise)
            # Mise à jour des champs : solde, le gain maximum, le nombre de partie gagnée, la mise maximale, le nombre de tentative de la base de données
            if(gainA>gain):
                gain=gainA
            task=(newSolde,gain,nbrparga,mise_max,nb_partie_coup,nb_coup_total,name)
            cursor.execute('UPDATE ca_user SET solde = ?,max_gain=?,nbr_partie_ga=?,max_mise=?,nbr_premier_coup=?,nbr_tentative=? WHERE user_name = ?',task)
            connexion.commit()
            print("\n\t\t\tBravo, vous avez gagné ! Les statistiques de la partie sont les suivantes : ...")
            # Demande au joueur s'il souhaite continuer la partie en passant au level 2
            print("\n\t\t\tLes statistiques du level 1 sont les suivantes :\n")
            stat_niveau(gainA,nb_coup,1,mise,1)
            print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————")
            print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n")
            contin=input("\n\t\tSouhaitez-vous continuer la partie (O/N) ?")
            while(contin!='o') and (contin!='O') and (contin!='n') and (contin!='N'):
                contin=input("\t\t\tJe ne comprends pas votre réponse. Veuillez répondre par (O/N) ?")
            if(contin=='n') or (contin=='N'):
                print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n")
                print("\t\t\tAu revoir ! Vous finissez la partie avec {} €.".format(round(newSolde,2)))
                stat(name)
            else:
                print("Super ! Vous passez au Level 2.")
                nb_level_2(name_user,name)
        else: # Si le nombre saisie est différent du random
            print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————")
            print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n")
            print("\n\n\t\t\t\tVous avez perdu ! Mon nombre est: {} !".format(nb_python))
            print("\n\t\t\tLes statistiques du level 1 sont les suivantes :\n")
            stat_niveau(gainA,nb_coup,1,mise,0)
            nbrparpe=nbrparpe+1 # Incrémentation du nombre de partie perdue
            # Mise à jour des champs : solde, la perte maximale, le nombre de partie perdue, la mise maximale, le nombre de tentative de la base de données
            newSolde=solde-mise 
            if(perte<mise):
                perte=mise
            nb_tentative=nb_tentative+3
            if(mise>mise_max):
                mise_max=mise 
            task=(newSolde,perte,nbrparpe,mise_max,nb_tentative,name)
            cursor.execute('UPDATE ca_user SET solde=?, max_perte=?, nbr_partie_pe=?, max_mise=?, nbr_tentative=? WHERE user_name=?',task)
            connexion.commit()
            # Demande au joueur la possibilté de retenter sa chance avec le reste de son solde
            if(newSolde != 0):
                contin=input("\n\t\t\tRetenter votre chance avec {} € qui vous reste (O/N) ?".format(round(newSolde,2)))
                while(contin!='o') and (contin!='O') and (contin!='n') and (contin!='N'):
                    contin=input("\t\t\tJe ne comprends pas votre réponse. Veuillez répondre par (O/N) ?")
                if(contin=='n') or (contin=='N'):
                    print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n")
                    print("\t\t\tAu revoir ! Vous finissez la partie avec {} €.".format(round(newSolde,2)))
                    stat(name)
                else:
                    print("\t\t\tSuper ! Allons-y !")
                    while True:
                        rep=int(input("\t\t\tChoisissez un niveau entre 1 et {} !".format(level)))
                        try:
                            if (rep==1):
                                nb_level_1(name_user,name)
                                break
                            if (rep==2):
                                nb_level_2(name_user,name)
                                break
                            if (rep==3):
                                nb_level_3(name_user,name)
                                break
                            print("\t\t\tEntrez un niveau entre 1 et {} !!! ".format(level))
                        except ValueError:
                            print("\t\t\tEntrez un niveau entre 1 et {} !!! ".format(level))
            else:
                print("\n\n\t\t\tOups !!! Vous n'avez plus de solde. Vous ne pouvez pas continuer !\n\n")




def stat(name):
    # Connexion a notre base de donnée
    connexion = sqlite3.connect("db-casino.db")
    cursor = connexion.cursor()
    name_user = (name,)
    cursor.execute('SELECT * FROM ca_user WHERE user_name =?', name_user)
    records = cursor.fetchall()
    #Récuperation de chaque champs de la ligne recherchée
    for row in records:
        date = row[4]
        max_level = row[3]
        nbr_pc = row[11]
        max_gain = row[5]
        max_mise = row[10]
        max_perte = row[6]
        nbr_perte = row[9]
        nbr_gagnier = row[8]
        nbr_partie = row[7]
        commule_mise = row[12]
        nbr_tentative = row[13]

    moy_mise = round((commule_mise/nbr_partie),1)
    moy_tent = round((nbr_tentative/nbr_gagnier),1)

    print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————")
    print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n")
    print('Voici vos statistiques depuis la 1ère fois', date,'\n')
    print('\tVos meilleures statistiques :\n')
    print('\t\t-Le niveau le plus élevé est de :', max_level)
    print('\t\t-Vous avez reussie à trouver le nombre du premier coup', nbr_pc, 'fois')
    print('\t\t-Le gain le plus elevé est de:', max_gain)
    print('\t\t-La mise la plus elevée est de:' , max_mise)
    print('\tVos pires statistiques:')
    print('\t\t-La perte la plus elevée est de :', max_perte)
    print('\t\t-Le nombre de partie perdue est de:', nbr_perte)
    print('Vos moyennes:')
    print('\t-la mise moyenne : ', moy_mise)
    print('\t-le nombre moyen de tentatives pour trouver le bon chiffre est de:', moy_tent)
    print("\n\n————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————")
    print("————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————\n")




def stat_niveau (gain,nb_coup,level,perte,etat):
    nb = nb_coup
    pert=perte
    taux_reussite=0
    if (etat==1):
        pert=0
    #CAS DE VICTOIR DU JOUEUR
    if (pert==0):
        gai = gain
        print("\n\t\t\tLors de cette partie la valeur ajouter a votre solde est : {} €".format(gai) + "\n\t le nombre de coups jouer lors de cette partie est: {} coups ".format(nb))
        if (level == 1):
            taux_reussite = ((4-nb_coup) * 100) / 3
        if (level == 2):
            taux_reussite = ((6-nb_coup) * 100) / 5
        if (level == 3):
            taux_reussite = ((8-nb_coup) * 100) / 7
        tx = taux_reussite
        print("\tAvec un taux de réussite de : {} % ".format(round(tx,2)))
    #CAS DEFAITE DU JOUEUR
    else:
        print("\t-Ohh Helas vous avez perdu {} € de votre solde ".format(pert))
        print("\t-le nombre de coups joués est: {}".format(nb))
        print("\t-Le taux de réussite a 0%")



level()
#nb_level_1()
connexion.close()



