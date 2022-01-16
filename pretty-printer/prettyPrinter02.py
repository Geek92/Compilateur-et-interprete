import json 
import pretty_printer01


def afficher_condition(dico,result):
    """ Afficher la condition de la boucle while.
        Cette fonction prends en parametre un dictionaire et une chaine de caractere vide 
        et retourne comme resultat une chaine de caractere.
        
        Parametres
        ----------
        dico: dictionaire
        result: chaine de caractere vide
        
        Returns
        -------
        chaine de cararctere
        
        la condition de la boucle while.
    """
    
    if dico["type"] == "BinaryExpression":  
        left = dico["left"]["name"]  #on recupere recupere la variable a comparer
        operator = dico["operator"]  #on recupere l'operateur de comparaison
        right = dico["right"]["extra"]["raw"]  #on recupere la valeur a utiliser pour la comparaison
        result = "("+f"{left} {operator} {right}"+")"+"{"
        return result
    else:
        pass


def afficher_corps_boucle(dico,liste):
    """ Afficher le coprs de la boucle while.
        Cette fonction prends en parametre un dictionaire et une liste vide 
        et retourne comme resultat une liste contenant les differentes expressions qui composent le corps de la boucle.
        
        Parametres
        ----------
        dico: dictionaire
        liste: liste vide
        
        Returns
        -------
        liste 
        
        la liste des expressions du coprs de la boucle.
    """
    
    body = dico["body"]
    for number in (range(len(body))):
        expression = body[number]["expression"]  #on recupere le contenu de l'expression
        if expression["type"] == "UpdateExpression":
            liste.append("  "+expression["argument"]["name"]+expression["operator"]+";")
        elif expression["type"] == "CallExpression":
            liste.append("  "+expression["callee"]["name"]+"("+expression["arguments"][0]["name"]+");")
    liste.append("}")
    return liste
 
    
file = "/Users/patrickfrank/Desktop/matieres deuxieme semestre/compilation de logiciels/pretty printer/ast-5.json"
try:
    with open(file,"r") as jsonFile:  #on deserialise le fichier json
        pythonTree = json.load(jsonFile)
        body = pythonTree["program"]["body"] #on recupere le contenu du programme
        result = ''
        liste = list()
        for number in (range(len(body))):
            if body[number]["type"] == "WhileStatement":
                test = body[number]["test"] #on recupere la condition de la boucle
                expression_body = body[number]["body"]  #on recupere le coprs de la boucle
                pretty_printer01.afficher_declaration(file)
                print(afficher_condition(test,result))
                for element in afficher_corps_boucle(expression_body,liste):
                    print(element)
            else:
                pass

except OSError:
    print("impossible d'ouvrir le fichier")


