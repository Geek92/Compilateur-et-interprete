import json


def afficher_declaration(file):
    """
        Afficher les declaration de variables.

        Cette fonction prends en parametre un fichier json contenant l'arbre syntaxique d'un ensemble 
        de declarations de variables et affiches les differentes declarations en sortie.

        Parametres
        ----------
        file: fichier json

        Returns
        -------
        String

        les declarations de variables. 
    """
    try:
        with open (file,"r") as jsonFile:
            #on deserialise le fichier json
            Pythondiction = json.load(jsonFile)
            #on recupere la liste qui contient les declarations
            body = Pythondiction["program"]["body"]
            initialisation = ''
            result_string = ''
            for i in range(len(body)):
                #on parcours la liste et on recupere les variables ainsi que leurs declarations le cas echeant
                if "declarations" in body[i].keys():
                    declaration = body[i]["declarations"]
                    kind = body[i]["kind"]
                    for number in range(len(declaration)):
                        if number < 1:
                            result_string = ''
                        id = declaration[number]["id"]["name"]
                        #si la variable est initialisée, on recupere sa valeur dans le cas contraire,
                        #on recupere juste la variable
                        if declaration[number]["init"] is not None:
                            initialisation =  "null" if declaration[number]["init"]["type"] == "NullLiteral" else declaration[number]["init"]["extra"]["raw"]
                            result_string = result_string + f"{id} = {initialisation}, " if number < len(declaration) -1 else result_string + f"{id} = {initialisation}"
                        else:
                            result_string = result_string + f"{id}, " if number < len(declaration) -1 else result_string + f"{id}"
                    print(f"{kind} {result_string};")
                else:
                    pass

    except OSError:
        print("impossilble d'ouvrir le fichier")




    






    
