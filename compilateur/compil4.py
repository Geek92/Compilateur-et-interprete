import json

#compil_json("test.json")



# /* g: globals[0] */
#    globals[0] = iconst(1);

# Var x = 5;
# globals[0] = iconst(5);
# Var y = 6;
# globals[1] = iconst(6);


# nombreVarGlobal = 0 # cette valeur sera toujours égale à len(tableValVar) donc pas besoin de créer cette variable

tableVar = list()  # tableVar = ["x", "y"]
tableValVar = list() # tableValVar = [5, 6]


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
            if i["type"] == "WhileStatement":# on a une boucle while
                if i["test"]["type"] == "BooleanLiteral":# on a probablement quelque chose du style while(true) ou while(false)
                    value = i["test"]["value"]# probablement un true
                    bodyWhile = i["body"]["body"]
                    chaineAecrire = "while(" + str(int(value)) + "){\n"                              
                    fichier.write(chaineAecrire)
                    for j in bodyWhile:
                        if j["expression"]["type"] == "CallExpression":# on appelle une fonction
                            nomFonction = j["expression"]["callee"]["name"]
                            argumentsFonction = j["expression"]["arguments"][0]                      
                            if argumentsFonction["type"] == "Identifier":# le paramètre de la fonction appeler est un paramètre global
                                nomParam = argumentsFonction["name"]# on suppose que la fonction n'a qu'un seul paramètre
                                nomParam = tableVar.index(nomParam)
                                nomParam = "globals[" + str(nomParam) + "]"
                                
                            elif argumentsFonction["type"] == "StringLiteral":
                                nomParam = argumentsFonction["value"]
                            chaineAecrire = str(nomFonction) +"(" + nomParam +");\n"                              
                            fichier.write(chaineAecrire)
                    chaineAecrire = "}\n"
                    fichier.write(chaineAecrire)
                    
                
                elif i["test"]["type"] == "BinaryExpression":# on a probablement quelque chose du style while(x <= 10) 
                    test = i["test"]
                    left = test["left"]["name"]# on supposera que l'on aura jamais quelque du style while(10 > x), while(1<2),while(x != "10"), on supposera que la partie gauche sera toujours constituée d'une variable
                    operator = test["operator"]
                    right = test["right"]["value"]
                    bodyWhile = i["body"]["body"]
                    nomParam = tableVar.index(left)
                    nomParam = "globals[" + str(nomParam) + "]"
                    chaineAecrire = "while(" + nomParam + str(operator) + str(right) + "){\n"                              
                    fichier.write(chaineAecrire)
                    for j in bodyWhile:
                        if j["expression"]["type"] == "UpdateExpression":
                            operator = j["expression"]["operator"]
                            nomParam = j["expression"]["argument"]["name"]
                            nomParam = tableVar.index(nomParam)
                            nomParam = "globals[" + str(nomParam) + "]"
                            chaineAecrire = nomParam + operator +";\n"                              
                            fichier.write(chaineAecrire)
                        elif j["expression"]["type"] == "CallExpression":
                            nomFonction = j["expression"]["callee"]["name"]
                            argumentsFonction = j["expression"]["arguments"][0]                      
                            if argumentsFonction["type"] == "Identifier":# le paramètre de la fonction appeler est un paramètre global
                                nomParam = argumentsFonction["name"]# on suppose que la fonction n'a qu'un seul paramètre
                                nomParam = tableVar.index(nomParam)
                                nomParam = "globals[" + str(nomParam) + "]"
                                
                            elif argumentsFonction["type"] == "StringLiteral":
                                nomParam = argumentsFonction["value"]
                            chaineAecrire = str(nomFonction) +"(" + nomParam +");\n"                              
                            fichier.write(chaineAecrire)
                    chaineAecrire = "}\n"
                    fichier.write(chaineAecrire)
                
            elif "expression" in i and i["expression"]["type"] == "AssignmentExpression":# on change la valeur d'une variable
                nomVar = i["expression"]["left"]["name"]
                ValVar = i["expression"]["right"]["value"]# on a récupérer le nom et la valeur de la variable
                positionVar = tableVar.index(nomVar)
                tableValVar[positionVar] = ValVar# on a changé la valeur de la variable dans python, écrivons ce changement dans le fichier c
                positionVar = str(positionVar)
                ValVar = str(ValVar)
                chaineAecrire = "globals[" + positionVar +"] = iconst(" + ValVar + ");\n"                              
                fichier.write(chaineAecrire)
                
                
            elif i["declarations"][0]["type"] == 'VariableDeclarator':# on déclare une variable
                if len(i["declarations"]) == 1:# on ne déclare qu'une seule variable
                    var = i["declarations"][0]
                    nomVar = var["id"]["name"]
                    valVar = var["init"]
                    if type(valVar) == type(None):# la variable est déclarée mais non initialisée # Var x;    
                        #chaineAecrire = "word_u " + nomVar +";\n" # il faut changer cette ligne
                        #globals[0] = iconst(1);
                        chaineAecrire = "globals[" + str(len(tableVar)) +"] = iconst(null);\n"
                        tableVar.append(nomVar)
                        tableValVar.append(valVar)
                        #print(valVar)
                        fichier.write(chaineAecrire)
                    else:# la variable est initialisée
                        if valVar["type"] == "BinaryExpression": #pour le cas ou l'on a un truc du style: var t = y + 5;
                            left = valVar["left"]
                            right = valVar["right"]
                            operator = valVar["operator"]
                            if "extra" in left:# si la partie gauche contient une valeur déja initialisé
                                left = left["value"]
                            else: # dans var t = y + 5, il faut récupérer la valeur de y
                                left = left["name"] #on a le nom de la variable
                                left = tableValVar[tableVar.index(left)]#on a récupéré la valeur de la variable
                                                        
                            if "extra" in right:# si la partie droite contient une valeur déja initialisé
                                right = right["value"]
                            else: # dans var t = y + 5, il faut récupérer la valeur de y
                                right = right["name"] #on a le nom de la variable
                                right = tableValVar[tableVar.index(right)]#on a récupéré la valeur de la variable
                            
                            if operator =="+":
                                ValVar = left + right
                            elif operator == "*":
                                ValVar = left * right
 
                            tableValVar.append(ValVar)# on rajoute la valeur de la variable avant le nom de sa variable dans tableVar pour éviter que toutes les variables soit des chaines de caractères
                            valVar = str(ValVar)#python ne veut pas que l'on concatène des chaines de caractères avec des entiers donc on caste en string                           
                            chaineAecrire = "globals[" + str(len(tableVar)) +"] = iconst(" + valVar + ");\n"
                            tableVar.append(nomVar)                               
                            fichier.write(chaineAecrire)
                        
                        elif type("") == type(valVar["extra"]["rawValue"]):# si notre variable est une chaine de caractère
                            valVar = valVar["extra"]["rawValue"]
                            tableValVar.append(valVar)
                            chaineAecrire = "globals[" + str(len(tableVar)) +"] = iconst(\"" + valVar + "\");\n"
                            tableVar.append(nomVar)                               
                            fichier.write(chaineAecrire)
                            
                        else:# si la variable n'est pas une chaine de caractère
                            valVar = valVar["extra"]["rawValue"]                          
                            tableValVar.append(valVar)# on rajoute la valeur de la variable avant le nom de sa variable dans tableVar pour éviter que toutes les variables soit des chaines de caractères
                            valVar = str(valVar)#python ne veut pas que l'on concatène des chaines de caractères avec des entiers donc on caste en string                           
                            chaineAecrire = "globals[" + str(len(tableVar)) +"] = iconst(" + valVar + ");\n"
                            tableVar.append(nomVar)                               
                            fichier.write(chaineAecrire)
                        
                else:#on déclare plusieurs variables sur la même ligne
                    for j in range(len(i["declarations"])):
                        var = i["declarations"][j]
                        nomVar = var["id"]["name"]
                        valVar = var["init"]
                        if type(valVar) == type(None):# la variable est déclarée mais non initialisée
                            chaineAecrire = "globals[" + str(len(tableVar)) +"] = iconst(null);\n"
                            tableVar.append(nomVar)
                            tableValVar.append(valVar)
                            fichier.write(chaineAecrire)
                        else:# la variable est initialisée
                            if valVar["type"] == "NullLiteral":# la variable est initialisée à null
                                chaineAecrire = "globals[" + str(len(tableVar)) +"] = iconst(null);\n"
                                tableVar.append(nomVar)
                                tableValVar.append(None)
                                fichier.write(chaineAecrire)
                            else:
                                valVar = valVar["extra"]["rawValue"]
                                tableValVar.append(valVar)
                                valVar = str(valVar)#python ne veut pas que l'on concatène des chaines de caractères avec des entiers donc on caste en string
                                chaineAecrire = "globals[" + str(len(tableVar)) +"] = iconst(" + valVar + ");\n"
                                tableVar.append(nomVar)
                                fichier.write(chaineAecrire)
        fichier.write("return 0;\n ")#on a fini de lire le json, rajoutons ce qu'il faut pour terminer
        fichier.write("}")
        fichier.close()
        return 0
                
                

