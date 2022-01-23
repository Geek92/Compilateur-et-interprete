import json 
import inter2

def evaluer_boucle(dico):
    """ Evaluation d'une boucle while
    Cette fonction prends en parametre un dictionaire representant l'AST d'une boucle while et renvoie le resultat de son evaluation.
    
    Parameters
    ----------
    dico : un dictionaire
    
    Returns
    -------
    resultat de l'evaluation de la condition et des differentes expressions contenues dans la boucle
    """
   
   #si on a une expression on l'evalue 
    if dico["type"] == "VariableDeclaration":
       print(inter2.interpreter_expression(dico))
    
    #si on a une boucle while on l'evalue et on affiche le resultat
    elif dico["type"] == "WhileStatement":
        test = dico['test']
        body = dico['body']['body']
        condition = "while statement condition: "+test['left']['name'] +" "+ test['operator'] +" "+ str(test['right']['value']) #on recupere et on affiche la condition de la boucle
        print(condition)
        variable_condition = 0
        while variable_condition < test['right']['value'] - 1:
            for number in range(len(body)):
                if body[number]["expression"]["type"] == "UpdateExpression":  #si on a une operation d'incrementation
                    variable_condition = inter2.interpreter_expression(body[number],variable_condition)
            else:
                    #si on a une instruction d'affichage de la forme print(variable) ou print(String) 
                    # en supposant que notre chaine  de caracteres contienne au mois 2 mots a afficher
                    result = inter2.interpreter_expression(body[number])  
                    final_result = result if result.count(" ") > 1 else result+": "+str(variable_condition)
                    print(final_result)
                    
                                 
#on ouvre le fichier json et on recupere le contenu de notre programme
file_path = "/Users/patrickfrank/Desktop/matieres deuxieme semestre/compilation de logiciels/interprete/compact json files/03-while-compact.json"
with open(file_path,"r") as jsonFile:
    Tree = json.load(jsonFile)
    programme = Tree["program"]["body"]
    valeur_variable= 0
    declaration = list()
    
    #on recupere le 
    for i in range(len(programme)):
        if programme[i]["type"] == "VariableDeclaration": #si on a une declaration de variable
            declaration = programme[i]["declarations"]
            for j in range(len(declaration)):
                if "init" in declaration[j].keys():  #si la variable est initialisée
                    valeur_variable= declaration[j]["init"]["value"]
                    evaluer_boucle(programme[i])
                    
        elif programme[i]["type"] == "WhileStatement":  #si on a une boucle
            evaluer_boucle(programme[i])
    
            
            
            
            