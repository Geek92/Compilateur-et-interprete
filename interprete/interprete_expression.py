import json

GOODVALUE = 0
BADVALUE = 1
def interpreter_expression(dico,variable = 0):
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
    
    if dico["type"] == "ExpressionStatement":
        expression = dico["expression"]
        return inter_expression_statement(expression,variable)
    elif dico["type"] == "BinaryExpression" and dico["operator"] == "<":
        if variable < dico["right"]["value"]:
            return GOODVALUE
        else:
            return BADVALUE
    elif dico["type"] == "BinaryExpression" and dico["operator"] == ">":
        if variable > dico["right"]["value"]:
            return GOODVALUE
        else:
            return BADVALUE
    
    
def inter_expression_statement(expression,variable = 0):
    if expression["type"] == "UpdateExpression" and expression["operator"] == "++":
        variable = variable + 1
        return variable
    elif  expression["type"] == "UpdateExpression" and expression["operator"] == "--":
          variable = variable - 1
          return variable
    elif expression["type"] == "BinaryExpression":
        left = inter_expression_statement(expression["left"])
        right = inter_expression_statement(expression["right"])
        if expression["operator"] == "+":
            return left + right
        elif expression["operator"] == "*":
            return left * right
    elif expression["type"] == "NumericLiteral":
            return expression["value"]
 
'''def test(jsonFile):
    try:
        #On ouvre le fichier json contenant notre AST 
        with open(jsonFile,"r") as jsonFile:
            #On deserialise le fichier json et on recupere son contenu 
            pythonTree = json.load(jsonFile)
            body = pythonTree['program']['body']
            for i in range(len(body)):
                result = interpreter_expression(body[i])  #Pour chaque element de body autrement dit pour chaque expression on appele la fonction interpreter_expression
                expression_type = body[i]["type"]
                print(expression_type +" "+str(result))

    except OSError:
        print("erreur! impossible d'ouvrir le fichier")

test("/Users/patrickfrank/Desktop/matieres deuxieme semestre/compilation de logiciels/interprete/compact json files/01-expressions-compact.json")
'''

