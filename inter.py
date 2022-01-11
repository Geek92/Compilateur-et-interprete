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
            return 4

#print(12);
def LigneToprint(ligne):#fonction qui servira lorsque le fichier à interpréter contient un print
    caractereDebut = ligne.find("(")
    caractereFin = ligne.find(")")
    #print (ligne[caractereDebut + 1: caractereFin])
    chaine = "Print: "
    elementAafficher = ligne[caractereDebut + 1: caractereFin]
    chaine += elementAafficher
    print(chaine)
    return 0