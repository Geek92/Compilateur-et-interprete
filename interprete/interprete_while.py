import json 
import inter2
from interprete_declarations import interprete_declarations
import interprete_expression 

def evaluer_boucle(liste):
    #on utilise un dictionaire pour stocker les variables declarees ainsi que leurs valeurs 
    variableDeclarations = {}
    for dico in liste:
        #on parcours l'AST si on a une declaration de varialbe on recupere son nom et sa valeur
        #qu'on va stocker dans variableDeclarations
        if dico["type"] == "VariableDeclaration":
                result = interprete_declarations(dico)
                for key in result.keys():
                    variableDeclarations[key] = result[key]
        
        #si on a une boucle while
        elif dico["type"] == "WhileStatement":
            body = dico["body"]["body"]
            test = dico["test"]
            #on recuperer la valeur de la variable a tester
            #variableDeclarations[test["left"]["name"]]
            if test["type"] == "BinaryExpression":
                while result := interprete_expression.interpreter_expression(test,variableDeclarations[test["left"]["name"]]) != interprete_expression.BADVALUE:
                    for number in range(0,len(body)):
                        dico = body[number]
                        if dico["type"] == "ExpressionStatement" and dico["expression"]["type"] == "UpdateExpression":
                            variableDeclarations[test["left"]["name"]] = interprete_expression.interpreter_expression(dico,variableDeclarations[test["left"]["name"]])
                        elif dico["type"] == "ExpressionStatement" and dico["expression"]["callee"]["name"] == "print":
                            print_function(dico,variableDeclarations)
                        
                     

def print_function(dico1,dico2):
    if dico1["type"] == "ExpressionStatement" and dico1["expression"]["type"] == "CallExpression":
        if dico1["expression"]["callee"]["name"] == "print" and dico1["expression"]["arguments"][0]["name"] in dico2.keys():
            print(dico2[dico1["expression"]["arguments"][0]["name"]])
        else:
            print(dico1["expression"]["callee"]["value"])
            

'''def test(jsonFile):
    try:
        jsonFile = open(jsonFile,"r")
        tree = json.load(jsonFile)
        body = tree["program"]["body"]
        evaluer_boucle(body)
            #print(body[number])
            #print("\n")
        jsonFile.close()
    except OSError as error:
        print(error)

test("/Users/patrickfrank/Desktop/matieres deuxieme semestre/compilation de logiciels/interprete/compact json files/03-while-compact.json")
 '''   
    
            
            
            
            