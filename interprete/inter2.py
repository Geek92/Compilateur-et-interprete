import json


def interpreter_expression(dico):
    """ Evaluation d'une expression.
    
    Cette fonction prends en paramètre une expression arithmetique sous forme de 
    dictionaire et renvoie le resultat de son evaluation.

    Parametres
    ----------
    dico : dictionaire

    Returns
    ------ 
    int 
    le resultat de l'evaluation de l'expression
     """
    
    #On recupere le contenu de l'expression
    if "expression" in dico.keys():
        dico = dico["expression"]
    
    
    
    #on suppose que l'on souhaite déclarer une variable
    if dico["type"] == "VariableDeclaration":
        dico = dico["declarations"][0]
        nomVariable = dico["id"]["name"]
        if type(dico["init"]) == type(dict()): # on déclare une variable avec une valeur
            dico = dico["init"]["extra"]["raw"]
            return nomVariable + " " + dico
        else:#on déclare une variable sans lui associer de valeur
            return nomVariable
       
    
    
    
    #on suppose que l'on a une instructions, probablement un print
    if dico["type"] == "CallExpression":
        func = dico["callee"]["name"]
        val = dico["arguments"][0]["extra"]["raw"]
        return func + " " + val
    
    
    
    #Si l'expression contient un seul argument on le retourne
    if dico["type"] == "NumericLiteral":
        return dico["value"]
    
   #Si l'expression est constituée de plusieurs elments on evalue recursivement les elements 
   # de gauche puis de droite et on retourne le resultat 
    else:
        left = interpreter_expression(dico["left"])
        right = interpreter_expression(dico["right"])
        if dico["operator"] == "+":
            return left + right
        elif dico["operator"] == "*":
            return left * right


try:
    #On ouvre le fichier json contenant notre AST 
    #with open("/Users/patrickfrank/Downloads/ast.json","r") as jsonFile:
    with open("test.json","r") as jsonFile:
        #On deserialise le fichier json et on recupere son contenu 
        pythonTree = json.load(jsonFile)
        body = pythonTree['program']['body']
        for i in range(len(body)):
            result = interpreter_expression(body[i])  #Pour chaque element de body autrement dit pour chaque expression on appele la fonction interpreter_expression
            expression_type = body[i]["type"]
            print(f"{expression_type}: {result}")
            print("")

except OSError:
    print("erreur! impossible d'ouvrir le fichier")





