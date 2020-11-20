# Ce fichier contient des fonctions à finir.

#chooselevel
#Cette fonction permit de délimiter les niveau
def chooselevel(level):
    if level != 1:
        print('Rappel! : vous vous êtes arrèté au niveau', level)
        x= input('voulez-vous reprendre ou vous vous êtes arreté? Y/N')
        if x=='N' or x=='NO' or x=='n' or x=='no':
            y= input('Veuillez choisir un niveau' )
            var = int (y)
            x = int(level)
            while var>x or var < 1 :
                val= input ('Le niveau saisi n\'est pas valide, Entrer SVP un niveau Inférieur ou égal a l\'ancien')
                var = int( val)



            level = var 
            print('Vous avez choisi le niveau', level,'\n c\'est parti!!!')
        else :
            print('Vous êtes au niveau', level,'\n c\'est parti!!!') 
    else:
        print('Vous êtes au niveau', level, '\n c\'est parti!!!')
    return level


#Vérifier le solde
#Cette Fonction Vérifie si le solde d'user est nul et lui permit de remettre du solde a sa table a fin de continuer de jour
def checksolde(solde):
    solde = int(solde)
    print (solde)


    if solde == 0:
        solde = input('Combien de solde voulez-vous mettre sur votre table?')
        print('votre nouveau solde est de ', solde)
    return solde



#choosemise
#Code optimal 
level = int(level)
inter = level * 10
solde = int(solde)
if solde < inter:
    inter = solde
    
print('Le jeu commence, entrez votre mise : ? 1-->',inter, '€')
mise = input('Votre mise ?')
i = int (mise)
cmt = 0
for cmt in range(3):
    if not i in range (1,inter):
        print ('Le montant saisi n\'est pas valide. Entrer SVP un montant entre 1 et',inter, ' € :  ?')
        mise = input ('Votre mise ?')
        i = int (mise) 
        cmt = cmt+1
    
print('Votre mise est de',mise,'€')
    
    
        
if cmt == 3:
    #fonction exit
    while True:
        print('Type exit to exit.')
        response = input()
        if response == 'exit':
            sys.exit()
        print('You typed ' + response + '.')


#chrono
#Le compte a rebours
import time
chrono = 10
while chrono > 0:
    print(chrono)
    time.sleep(1)
    chrono -= 1
print ('fin de temps, partie perdue')