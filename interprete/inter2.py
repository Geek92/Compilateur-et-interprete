import json


def interpreter_expression(dico,second_param = 0):
    """ Evaluation d'une expression.
    
    Cette fonction prends en paramètre une expression sous forme de 
    dictionaire ainsi qu'un entier optionel et renvoie le resultat de son evaluation.

    Parametres
    ----------
    dico : dictionaire
    second_param: entier

    Returns
    ------  
    le resultat de l'evaluation de l'expression
     """
    
    #On recupere le contenu de l'expression
    if "expression" in dico.keys():
        dico = dico["expression"]

    #on suppose que l'on souhaite déclarer une variable
    if dico["type"] == "VariableDeclaration":
        if len(dico["declarations"]) == 1:
            dico = dico["declarations"][0]
            nomVariable = dico["id"]["name"]
            if type(dico["init"]) == type(dict()): # on déclare une variable avec une valeur
                dico = dico["init"]["value"]
                return "VariableDeclaration: "+ nomVariable + " = " + str(dico)
            else:#on déclare une variable sans lui associer de valeur
                return nomVariable
        
        else:
            chaineFinal = " "
            for i in dico["declarations"]:
                nomVariable = i["id"]["name"]
                if type(i["init"]) == type(dict()):
                    if "extra" in i["init"].keys():
                        valVariable = i["init"]["extra"]["raw"]
                        chaineFinal += nomVariable + " = " + valVariable + "\n"
                    else:# i["init"]["type"] = NullLiteral
                        chaineFinal += nomVariable + " = " + "null" + " " + "\n"
                else:
                    chaineFinal += nomVariable + "\n"
            return chaineFinal
    #on suppose que l'on a une instructions, probablement un print
    if dico["type"] == "CallExpression":
        func = dico["callee"]["name"]
        val = dico["arguments"][0]["name"] if dico["arguments"][0]["type"] == "Identifier" else dico["arguments"][0]["value"]
        return func + " " + val
    #Si l'expression contient un seul argument on le retourne
    if dico["type"] == "NumericLiteral":
        return dico["value"]
    #Si l'expression est constituée de plusieurs elments on evalue recursivement les elements 
   # de gauche puis de droite et on retourne le resultat
    if dico["type"] == "UpdateExpression" and dico["operator"] == "++":
        second_param = second_param + 1
        return second_param
         
    else:
        left = interpreter_expression(dico["left"])
        right = interpreter_expression(dico["right"])
        if dico["operator"] == "+":
            return left + right
        elif dico["operator"] == "*":
            return left * right






