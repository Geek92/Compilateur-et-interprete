#interprete("test.js")

def interprete(fichier):#fonction principale pour interpréter le code
    f = open(fichier, 'r')
    text=f.readlines()
    NumberOfLine = len(text)#on a le nombre de ligne du fichier
    f.close()#on ferme le fichier
    f = open(fichier, 'r')#on rouvre le fichier pour le relire depuis le début
    for i in range(NumberOfLine):
        ligne = f.readline()#on prend une ligne et on regarde ce qu'elle contient
        if 'print(' in ligne:# on suppose que l'on aura jamais un truc du style : var s = "je veux que print() affiche ..."
            LigneToprint(ligne)
            return 5
        elif 'var' in ligne:#on suppose que l'on aura jamais un truc du style : "bonjour mon ami " + "var"
            Affectevar(ligne)
            return 4

#print(12);
def LigneToprint(ligne):#fonction qui servira lorsque le fichier à interpréter contient un print
    caractereDebut = ligne.find("(")
    caractereFin = ligne.find(")")
    chaine = "Print: "
    elementAafficher = ligne[caractereDebut + 1: caractereFin]
    chaine += elementAafficher
    print(chaine)
    return 0

def Affectevar(ligne):# fonction qui servira lorsque le fichier contient une ligne qui souhaite associer à une variable une valeur
    print(ligne)
    return 0
    if ligne.find("=") == -1:#si on souhaite juste déclarer une variable sans lui associer de valeur
        nomVar = ligne[4:]
        nomVar = nomVar[:-2]
        chaine = 'VariableDeclaration: '
        chaine +=nomVar
        print(chaine)
        return 0
    elif ligne.find("\"") == -1:#on souhaite associer à une variable une chaine de caractère
        print(ligne)
        return 0
        caractereDebut = ligne.find("\"")# on trouve le premier " de notre chaine de caractère a associer
        caractereFin = ligne.rfind("\"")# on trouve le premier " de notre chaine de caractère a associer
        chaine = 'VariableDeclaration: '
        valeurVar = ligne[caractereDebut + 1: caractereFin]# la valeur qui sera affectée à la variable
        caractereDebut = ligne.find("r")
        caractereFin = ligne.find("=")
        nomVar = ligne[caractereDebut + 1: caractereFin]# le nom de la variable
        chaine += nomVar
        chaine += " "
        chaine += valeurVar
        print(chaine)
        return 0
        
        