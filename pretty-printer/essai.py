import json

#ligne 370 à 480
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
    
    #Si l'expression contient un seul argument on le retourne
    if dico["type"] == "NumericLiteral":
        return str(dico["value"])
   
   #Si l'expression est constituée de plusieurs elments on evalue recursivement les elements 
   # de gauche puis de droite et on retourne le resultat 
    else:
        left = interpreter_expression(dico["left"])
        right = interpreter_expression(dico["right"])
        if dico["operator"] == "+":
            try:
                if dico["extra"]["parenthesized"]:
                    return "(" + str(left) + " + " + str(right) + ")"
                else:
                    return str(left) + " + " + str(right)
            except KeyError:
                return str(left) + " + " + str(right)
        elif dico["operator"] == "*":
            try:
                if dico["extra"]["parenthesized"]:
                    return "(" + str(left) + " * " + str(right) + ")"
                else:
                    return str(left) + " * " + str(right)
            except KeyError:
                return str(left) + " * " + str(right)


try:
    #On ouvre le fichier json contenant notre AST 
    #with open("/Users/patrickfrank/Downloads/ast.json","r") as jsonFile:
    with open("test.json","r") as jsonFile:
        #On deserialise le fichier json et on recupere son contenu 
        pythonTree = json.load(jsonFile)
        body = pythonTree['program']['body']
        f = open('originale.js','w')
        for i in range(len(body)):
            result = interpreter_expression(body[i])  #Pour chaque element de body autrement dit pour chaque expression on appele la fonction interpreter_expression
            expression_type = body[i]["type"]
            print(f"{expression_type}: {result}")
            result += ";\n"
            f.write(result)
        f.close()

except OSError:
    print("erreur! impossible d'ouvrir le fichier")





