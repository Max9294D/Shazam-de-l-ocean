import numpy as np
import sqlite3
from Creation_bdd import *
import glob
from sklearn.model_selection import train_test_split

class Interro(modifBDD):

    # Hérite de modifBDD, sert à ressortir en console des valeurs des tables

    def __init__(self,nom_BDD,nom_table):
        super().__init__(nom_BDD,nom_table)


    def gation_ID(self,ID,Colonne):
        conn = sqlite3.connect(self.nomBDD)
        c = conn.cursor()
        c.execute('SELECT {cn} FROM {tn} WHERE {idf}={ID}'.\
                  format(cn=str(Colonne),tn=self.nom_table,idf='ID', ID=ID))
        row = c.fetchone()
        print(row[0])
        conn.close()
        #Cette fonction va renvoyer la valeur présente dans la colonne Colonne, pour l'entrée ayant l'id ID
        return str(row[0])

    def gation_index(self,val,Colonne):
        conn = sqlite3.connect(self.nomBDD)
        c = conn.cursor()
        c.execute('SELECT {idf} FROM {tn} WHERE {cn}={val}'.\
                  format(idf='ID', tn=self.nom_table,cn=str(Colonne), val=val))
        row=c.fetchone()
        print(row[0])
        conn.close()
        #Cette fonction va renvoyer l'id ayant pour valeur val dans la colonne Colonne

    def gation_path(self,val,Colonne):
        conn = sqlite3.connect(self.nomBDD)
        c = conn.cursor()
        c.execute('SELECT {idf} FROM {tn} WHERE {cn}={val}'.\
                  format(idf='Path', tn=self.nom_table,cn=str(Colonne), val=val))
        row=c.fetchone()
        print(row[0])
        conn.close()
        #Cette fonction va renvoyer le path ayant pour valeur val dans la colonne Colonne
        return str(row[0])

#if __name__ == "__main__":
#    
# # Ici ça créer la BDD et une première table avec toutes les images + le chemin
#    M = Interro('Images','Images')
#    M.creation()
#    M.ajoutColonne('Index_1', 'REAL')
#    M.ajoutColonne('Index_2', 'REAL')
#    M.ajoutColonne('Path', 'TEXT', 'Oui')
#    i=1
#    list = glob.glob('./BDD/shazam_images/' + '*.png')
#    for x in list:
#        M.insertion(i,'Index_1',0.0)
#        M.update(i,'Path',x)
#        i+=1

#print(type(M))
#
# # Ça, ça créer les listes test et banque (le truc 80/20)
#     list_banque, list_test = train_test_split(list, test_size=0.2)
#
#
# # Là, on créer la table banque, avec les 80% d'images de la table images
#     A=Interro('Images','Interro')
#     A.creation()
#     A.ajoutColonne('Index_1', 'REAL')
#     A.ajoutColonne('Index_2', 'REAL')
#     A.ajoutColonne('Path', 'TEXT', 'Oui')
#     i = 1
#     for x in list_banque:
#         A.insertion(i, 'Index_1', 0.0)
#         A.update(i, 'Path', x)
#         i += 1
#
#
# #Et ici la table de test, avec les 20% restants
#     T = Interro('Images', 'Test')
#     T.creation()
#     T.ajoutColonne('Index_1', 'REAL')
#     T.ajoutColonne('Index_2', 'REAL')
#     T.ajoutColonne('Path', 'TEXT', 'Oui')
#     i = 1
#     for x in list_test:
#         T.insertion(i, 'Index_1', 0.0)
#         T.update(i, 'Path', x)
#         i += 1

#En conclusion tu as 3 tables
# Pour interroger les tables, récupérer les index, le path et tout :

# T.gation_ID(ID,Colonne) : prend en entré un identifiant de la table test et une colonne et te renvoie la valeur qu'il
#y a dans cettte case

# T.gation_index(val,colonne) : prend en entrée une valeur et une colonne et te renvoie l'ID correspondant
# par exemple si tu essaie avec (0.034,Index_1) il va te renvoyer l'ID je sais pas combien mais de l'image qui a un
#index_1 de 0.034

#T.gation_path(val,colonne) te renvoie le path, utilisation : path=T.gation_path(2,'ID') ; path sera donc le chemin de
# l'image 2 de la table Test

# Si t'as des questions, hésites pas 06.46.77.62.02