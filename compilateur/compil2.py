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
            if i["declarations"][0]["type"] == 'VariableDeclarator':# on déclare une variable
                if len(i["declarations"]) == 1:# on ne déclare qu'une seule variable
                    var = i["declarations"][0]
                    nomVar = var["id"]["name"]
                    valVar = var["init"]
                    if type(valVar) == type(None):# la variable est déclarée mais non initialisée
                        chaineAecrire = "word_u " + nomVar +";\n"
                        fichier.write(chaineAecrire)
                    else:# la variable est initialisée
                        valVar = valVar["extra"]["raw"]
                        valVar = str(valVar)#python ne veut pas que l'on concatène des chaines de caractères avec des entiers donc on caste en string
                        chaineAecrire = "word_u " + nomVar + " = " + valVar +";\n"
                        fichier.write(chaineAecrire)
                else:#on déclare plusieurs variables sur la même ligne
                    for j in range(len(i["declarations"])):
                        var = i["declarations"][j]
                        nomVar = var["id"]["name"]
                        valVar = var["init"]
                        if type(valVar) == type(None):# la variable est déclarée mais non initialisée
                            chaineAecrire = "word_u " + nomVar +";\n"
                            fichier.write(chaineAecrire)
                        else:# la variable est initialisée
                            if valVar["type"] == "NullLiteral":# la variable est initialisée à null
                                valVar = "null"
                                chaineAecrire = "word_u " + nomVar + " = " + valVar +";\n"
                                fichier.write(chaineAecrire)
                            else:
                                valVar = valVar["extra"]["raw"]
                                valVar = str(valVar)#python ne veut pas que l'on concatène des chaines de caractères avec des entiers donc on caste en string
                                chaineAecrire = "word_u " + nomVar + " = " + valVar +";\n"
                                fichier.write(chaineAecrire)
        fichier.write("return 0;\n ")#on a fini de lire le json, rajoutons ce qu'il faut pour terminer
        fichier.write("}")
        fichier.close()
        return 0
                
                