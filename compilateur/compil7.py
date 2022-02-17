import json

#compil_json("test.json")


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
            if i["type"] == "ForStatement":
                fichier.write("for(")
                if type(i["init"]) != type(None):#si on initialise la variable for(int i =0; i<5; i++), on n'a donc pas for(;i<5;i++)
                    init = i["init"]
                    operator = init["operator"]
                    left = init["left"]["name"]
                    nomParam = tableVar.index(left)
                    left = "globals[" + str(nomParam) + "]"
                    right = init["right"]["extra"]["raw"]
                    fichier.write(left + operator + right)                   
                fichier.write("; ")
                
                test = i["test"]
                operator = test["operator"]
                left = test["left"]["name"]
                nomParam = tableVar.index(left)
                left = "globals[" + str(nomParam) + "]"
                right = test["right"]["extra"]["raw"]
                fichier.write(left + operator + right +";")
                
                update = i["update"]
                operator = update["operator"]
                if update["type"] == "UpdateExpression":
                    argument = update["argument"]["name"]
                    nomParam = tableVar.index(argument)
                    argument = "globals[" + str(nomParam) + "]"
                    fichier.write(argument + operator+"){\n")
                elif update["type"] == "AssignmentExpression":
                    left = update["left"]["name"]
                    right = update["right"]["extra"]["raw"]
                    nomParam = tableVar.index(left)
                    argument = "globals[" + str(nomParam) + "]"
                    fichier.write(argument + operator + right +"){\n")
                
                body = i["body"]["body"]
                for j in body:
                    if j["expression"]["type"] == "CallExpression":
                        fonc = j["expression"]["callee"]["name"]#nom de la fonction appelée
                        argument = j["expression"]["arguments"][0]["name"]#nom du paramètre de la fonction, on suppose que la fonction ne possède qu'un seul paramètre
                        nomParam = tableVar.index(argument)
                        argument = "globals[" + str(nomParam) + "]"
                        fichier.write(fonc + "(" + argument + ");\n")
                    elif j["expression"]["type"] == "UpdateExpression":
                        operator = j["expression"]["operator"]
                        argument = j["expression"]["argument"]["name"]
                        nomParam = tableVar.index(argument)
                        argument = "globals[" + str(nomParam) + "]"
                        fichier.write(argument + operator + ";\n")
                        
                fichier.write("}\n")
                
            elif i["type"] == "IfStatement":# il sera supposé que l'on ne déclarera pas de variables global dans un if
                test = i["test"]
                if test["type"] == "LogicalExpression":# if(x != 0 && true)
                    left = test["left"]
                    operator = left["operator"]
                    right = left["right"]["value"]
                    left2 = left["left"]["name"]
                    nomParam = tableVar.index(left2)
                    left2 = "globals[" + str(nomParam) + "]"
                    chaineAecrire = "if(" + str(left2) + str(operator) + str(right)                             
                    fichier.write(chaineAecrire)
                    operator = test["operator"]
                    right = test["right"]["value"]
                    if test["right"]["type"] == "BooleanLiteral":
                        right = int(right)
                    chaineAecrire = operator + str(right) + "){\n"                             
                    fichier.write(chaineAecrire)
                    consequent = i["consequent"]
                    alternate = i["alternate"]# on a un alternate seulement si on a un else
                    consequent = consequent["body"][0]
                    if consequent["expression"]["type"] == "UpdateExpression":
                        operator = consequent["expression"]["operator"]
                        argument = consequent["expression"]["argument"]["name"]
                        nomParam = tableVar.index(argument)
                        left2 = "globals[" + str(nomParam) + "]"
                        chaineAecrire = left2 + str(operator) + ";\n"
                        fichier.write(chaineAecrire)
                        chaineAecrire = "}\n"
                        fichier.write(chaineAecrire)
                    
                    alternate = alternate["body"][0]
                    if alternate["expression"]["type"] == "AssignmentExpression":
                        left = alternate["expression"]["left"]["name"]
                        nomParam = tableVar.index(left)
                        left2 = "globals[" + str(nomParam) + "]"
                        operator = alternate["expression"]["operator"]
                        right = alternate["expression"]["right"]["value"]
                        fichier.write("else{\n")
                        fichier.write(left2 + operator + str(right) + ";\n")
                        fichier.write("}\n")
                    
                    
                elif test["type"] == "BinaryExpression":# if (x == 1), on supposera que l'on aura jamais if (1 == x) ou if (1 == 1)
                    left = test["left"]["name"]
                    operator = test["operator"]
                    right = test["right"]["value"]
                    nomParam = tableVar.index(left)
                    left = "globals[" + str(nomParam) + "]"
                    consequent = i["consequent"]
                    body = consequent["body"][0]
                    chaineAecrire = "if(" + str(left) + str(operator) + str(right) +"){\n"                              
                    fichier.write(chaineAecrire)
                    if body["expression"]["type"] == "AssignmentExpression": # on change la valeur d'une variable globale
                        left = body["expression"]["left"]["name"]
                        operator = body["expression"]["operator"]
                        right = body["expression"]["right"]["value"]
                        nomParam = tableVar.index(left)
                        left = "globals[" + str(nomParam) + "]"
                        chaineAecrire = left + operator + str(right) + ";\n}\n"                              
                        fichier.write(chaineAecrire)
                        
                        
                        
            
            elif i["type"] == "WhileStatement":# on a une boucle while
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
                        if "expression" in j and j["expression"]["type"] == "UpdateExpression":
                            operator = j["expression"]["operator"]
                            nomParam = j["expression"]["argument"]["name"]
                            nomParam = tableVar.index(nomParam)
                            nomParam = "globals[" + str(nomParam) + "]"
                            chaineAecrire = nomParam + operator +";\n"                              
                            fichier.write(chaineAecrire)
                            
                            
                            
                        elif "expression" in j and j["expression"]["type"] == "CallExpression":
                            nomFonction = j["expression"]["callee"]["name"]
                            argumentsFonction = j["expression"]["arguments"]
                            for k in argumentsFonction:
                                if k["type"] == "Identifier":# le paramètre de la fonction appeler est un paramètre global
                                    nomParam = k["name"]# on suppose que la fonction n'a qu'un seul paramètre
                                    nomParam = tableVar.index(nomParam)
                                    nomParam = "globals[" + str(nomParam) + "]"
                                    
                                elif k["type"] == "StringLiteral":
                                    nomParam = k["value"]
                                chaineAecrire = str(nomFonction) +"(" + nomParam +");\n"                              
                                fichier.write(chaineAecrire)
                                
                                
                                
                        elif j["type"] == "IfStatement":
                            test = j["test"]
                            if test["type"] == "LogicalExpression":# if(x != 0 && true)
                                left = test["left"]
                                operator = left["operator"]
                                right = left["right"]["value"]
                                left2 = left["left"]["name"]
                                nomParam = tableVar.index(left2)
                                left2 = "globals[" + str(nomParam) + "]"
                                chaineAecrire = "if(" + str(left2) + str(operator) + str(right)                             
                                fichier.write(chaineAecrire)
                                operator = test["operator"]
                                right = test["right"]["value"]
                                if test["right"]["type"] == "BooleanLiteral":
                                    right = int(right)
                                chaineAecrire = operator + str(right) + "){\n"                             
                                fichier.write(chaineAecrire)
                                consequent = i["consequent"]
                                alternate = i["alternate"]# on a un alternate seulement si on a un else
                                consequent = consequent["body"][0]
                                if consequent["expression"]["type"] == "UpdateExpression":
                                    operator = consequent["expression"]["operator"]
                                    argument = consequent["expression"]["argument"]["name"]
                                    nomParam = tableVar.index(argument)
                                    left2 = "globals[" + str(nomParam) + "]"
                                    chaineAecrire = left2 + str(operator) + ";\n"
                                    fichier.write(chaineAecrire)
                                    chaineAecrire = "}\n"
                                    fichier.write(chaineAecrire)
                                
                                alternate = alternate["body"][0]
                                if alternate["expression"]["type"] == "AssignmentExpression":
                                    left = alternate["expression"]["left"]["name"]
                                    nomParam = tableVar.index(left)
                                    left2 = "globals[" + str(nomParam) + "]"
                                    operator = alternate["expression"]["operator"]
                                    right = alternate["expression"]["right"]["value"]
                                    fichier.write("else{\n")
                                    fichier.write(left2 + operator + str(right) + ";\n")
                                    fichier.write("}\n")
                                    
                            elif test["type"] == "BinaryExpression":# if (x == 1), on supposera que l'on aura jamais if (1 == x) ou if (1 == 1)
                                
                                left = test["left"]["name"]
                                operator = test["operator"]
                                if "value" in test["right"]:
                                    right = test["right"]["value"]
                                else:
                                    right = test["right"]["name"]
                                    nomParam = tableVar.index(right)
                                    right = "globals[" + str(nomParam) + "]"
                                nomParam = tableVar.index(left)
                                left = "globals[" + str(nomParam) + "]"
                                
                                consequent = j["consequent"]
                                
                                for k in range(len(consequent["body"])):                      
                                    body = consequent["body"][k]
                                    chaineAecrire = "if(" + str(left) + str(operator) + str(right) +"){\n"                              
                                    fichier.write(chaineAecrire)
                                    if "expression" in body and body["expression"]["type"] == "AssignmentExpression": # on change la valeur d'une variable globale
                                        left = body["expression"]["left"]["name"]
                                        operator = body["expression"]["operator"]
                                        right = body["expression"]["right"]["value"]
                                        nomParam = tableVar.index(left)
                                        left = "globals[" + str(nomParam) + "]"
                                        chaineAecrire = left + operator + str(right) + ";\n}\n"                              
                                        fichier.write(chaineAecrire)
                                    
                                    elif body["type"] == "BreakStatement":
                                        fichier.write("break;\n}\n")
                                    elif body["type"] == "ContinueStatement":
                                        fichier.write("continue;\n}\n")
                                        
                                    
                        
                        
                        
                        
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
                
                
                
            elif "declarations" in i and 'VariableDeclarator' in i["declarations"][0]["type"] and i["declarations"][0]["type"] == 'VariableDeclarator':# on déclare une variable
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
                
                




