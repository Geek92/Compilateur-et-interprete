import json

#compil_json("test.json")

def compil_json(file):# fonction a appeller pour compiler un fichier json
        fichier = open(file)
        data = json.load(fichier)# on récupére un dictionnaire
        data = data ["program"]["body"]
        fichier.close()#on ferme le fichier .json, on a récupéré ce qu'il faut
        fichier = open("test.c", "w") # on ouvre un fichier en ouverture
        fichier.write('''#include "base.h"\n''')
        fichier.write("int main() {\n")
        fichier.write("init(8192, 0, 0);\n")#on a écrit dans le fichier les premières lignes nécessaires, commençons à interpréter le fichier
        for i in data:
            if i["expression"]["type"] == 'NumericLiteral':# on a juste un entier
                valeur = i["expression"]["extra"]["raw"] # on récupére la valeur
                chaine = "push(iconst(" + valeur + "));\n "
                fichier.write(chaine)
                fichier.write("pop(r1);\n ")
                fichier.write("debug_reg(r1);\n ")#on a écrit ce qu'il faut, passons à l'instruction suivante              
            elif i["expression"]["type"] == 'BinaryExpression': # on aura un calcul avec une partie gauche et droite qui peuvent être décomposée récursivement en partie gauche et droite
                leftrightprofond(fichier, i["expression"])#on appelle une fonction qui va gérer le cas ou on a un calcul
                #return 0
        fichier.write("return 0;\n ")#on a fini de lire le json, rajoutons ce qu'il faut pour terminer
        fichier.write("}")
        fichier.close()
        return 0



def leftrightprofond(fichier, dico):
    if 'left' in dico["left"].keys() and 'left' in dico["right"].keys():#le calcul se resépare en 2
        pass
    elif 'left' in dico["left"].keys():# seul la partie gauche se sépare en 2
        leftrightprofond(fichier, dico["left"])# le répertoire r1 contient la partie gauche
        operator = dico["operator"]
        right = dico["right"]["extra"]["raw"]
        #chaine = "push(iconst(" + left + "));\n "
        #fichier.write(chaine)
        chaine = "push(iconst(" + right + "));\n "
        fichier.write(chaine)
        fichier.write("pop(r1);\n ")
        fichier.write("pop(r2);\n ")
        if operator == "+":
            chaine = "iadd(r1,r2,r1);\n "
            fichier.write(chaine)
        elif operator == "*":
            chaine = "imul(r1,r2,r1);\n "
            fichier.write(chaine)
        chaine = "push(r1);\n "
        fichier.write(chaine)
        fichier.write("pop(r1);\n ")
        fichier.write("debug_reg(r1);\n ")
        
    elif 'left' in dico["right"].keys():# seul la partie droite se sépare en 2
        operator = dico["operator"]# le répertoire r1 contient la partie droite
        left = dico["left"]["extra"]["raw"]
        chaine = "push(iconst(" + left + "));\n "
        fichier.write(chaine)
        #chaine = "push(iconst(" + right + "));\n "
        #fichier.write(chaine)
        fichier.write("pop(r1);\n ")
        fichier.write("pop(r2);\n ")
        if operator == "+":
            chaine = "iadd(r1,r2,r1);\n "
            fichier.write(chaine)
        elif operator == "*":
            chaine = "imul(r1,r2,r1);\n "
            fichier.write(chaine)
        chaine = "push(r1);\n "
        fichier.write(chaine)
        fichier.write("pop(r1);\n ")
        fichier.write("debug_reg(r1);\n ")
            
    else:#le calcul ne contient que 2 nombres ensembles avec un operator
        left = dico["left"]["extra"]["raw"]
        operator = dico["operator"]
        right = dico["right"]["extra"]["raw"]
        chaine = "push(iconst(" + left + "));\n "
        fichier.write(chaine)
        chaine = "push(iconst(" + right + "));\n "
        fichier.write(chaine)
        fichier.write("pop(r1);\n ")
        fichier.write("pop(r2);\n ")
        if operator == "+":
            chaine = "iadd(r1,r2,r1);\n "
            fichier.write(chaine)
        elif operator == "*":
            chaine = "imul(r1,r2,r1);\n "
            fichier.write(chaine)
        chaine = "push(r1);\n "
        fichier.write(chaine)
        fichier.write("pop(r1);\n ")
        fichier.write("debug_reg(r1);\n ")
    
    
compil_json("test.json")