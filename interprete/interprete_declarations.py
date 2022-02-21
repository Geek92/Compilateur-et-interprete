import json
def interprete_declarations(dico):
    result = {}
    variableName = ""
    if dico["type"] == 'VariableDeclaration':
            declarations = dico["declarations"]
            for number in range(0,len(declarations)):
                declaration = declarations[number]
                variableName = declaration["id"]["name"]
                variableValue = None
                if declaration["init"] is not None:
                        variableValue = declaration["init"]["value"] if "value" in declaration["init"].keys() else variableValue
                result[variableName] = variableValue
    return result

'''def test(jsonFile):
    try:
        #On ouvre le fichier json contenant notre AST 
        with open(jsonFile,"r") as jsonFile:
            #On deserialise le fichier json et on recupere son contenu 
            pythonTree = json.load(jsonFile)
            body = pythonTree['program']['body']
            for i in range(len(body)):
                result = interprete_declarations(body[i])  #Pour chaque element de body autrement dit pour chaque expression on appele la fonction interpreter_expression
                expression_type = body[i]["type"]
                print(f"{expression_type}: {result}")

    except OSError:
        print("erreur! impossible d'ouvrir le fichier")

test("/Users/patrickfrank/Desktop/matieres deuxieme semestre/compilation de logiciels/interprete/compact json files/02-declarations-compact.json")
'''

                    
                
            
        
        
    