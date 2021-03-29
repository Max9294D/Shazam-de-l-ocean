# -*- coding: utf-8 -*-
"""
Created on Thu May  7 12:23:07 2020

@author: Max
"""

import sys
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from Interro import *
from Creation_bdd import *
from testttttttttttt import *
import operator


class MonAppli(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.lets_go() #On lance la création de la BDD
        self.ui = uic.loadUi('IHM2.ui', self)
        self.nbr_sortie = 1 #Par défaut le nombre de résultat sortant est 1

        #On initialise les boutons
        ###################################################################################
        self.ui.Rechercher.clicked.connect(self.rechercher) #lance la recherche
        self.ui.nbr_choix.valueChanged.connect(self.valuechange_nbr_img) # Change le nombre d'image en sortie
        self.ui.bouton_gauche.clicked.connect(self.go_gauche) #Passe à l'image de gauche
        self.ui.bouton_droit.clicked.connect(self.go_droite) #Passe à celle de Droite
        
        ####################################################################################

        self.nbr_gauche = len(self.list_test) #Nombre de fois qu'on a décalé à gauche
        self.nbr_droite = 0 #idem à droite
        self.image_en_cours=0 #sur quelle image on est en ce moment


#####################################################################################################
        #On met par défaut des images blanches dans le resultat avant de lancer une recherche

        pixmap = QtGui.QPixmap("blanc.jpg")
        self.label_img_result1.setPixmap(pixmap)
        self.label_img_result1.setScaledContents(True)
        self.label_img_result2.setPixmap(pixmap)
        self.label_img_result2.setScaledContents(True)
        self.label_img_result3.setPixmap(pixmap)
        self.label_img_result3.setScaledContents(True)


####################################################################################
        #on affiche l'image en cours et en attente de recherche comparative

        pixmap = QtGui.QPixmap(self.list_test[self.image_en_cours])
        self.label_img_request.setPixmap(pixmap)
        self.label_img_request.setScaledContents(True)



####################################################################################
#le nombre d'image en sortie
    def valuechange_nbr_img(self):
        self.nbr_sortie = self.ui.nbr_choix.value()
##################################################################################
    #faire défiler les images de gauche à droite

    def go_gauche(self):
        if self.nbr_droite==0:
            QtWidgets.QMessageBox.question(self, 'Attention !',
                                           'Vous êtes sur la première image.',
                                           QtWidgets.QMessageBox.Ok)
        else :
            self.nbr_gauche+=1
            self.nbr_droite-=1
            self.image_en_cours-=1
            pixmap = QtGui.QPixmap(self.list_test[self.image_en_cours])
            self.label_img_request.setPixmap(pixmap)
            self.label_img_request.setScaledContents(True)


    def go_droite(self):
        if self.nbr_gauche==0:
            QtWidgets.QMessageBox.question(self, 'Attention !',
                                           'Vous êtes sur la dernière image.',
                                           QtWidgets.QMessageBox.Ok)
        else :
            self.nbr_droite+=1
            self.nbr_gauche-=1
            self.image_en_cours += 1
            pixmap = QtGui.QPixmap(self.list_test[self.image_en_cours])
            self.label_img_request.setPixmap(pixmap)
            self.label_img_request.setScaledContents(True)


##########################################################################################
    #Création de la base de données et de 3 tables, une où il y a tout, une test, et une banque oùu on va chercher la
    #comparaison

    def lets_go(self):
        self.M = Interro('Images', 'Images')
        self.M.creation()
        self.M.ajoutColonne('Index_1', 'REAL')
        self.M.ajoutColonne('Index_2', 'REAL')
        self.M.ajoutColonne('Path', 'TEXT', 'Oui')
        i = 1
        list = glob.glob('./BDD/shazam_images/' + '*.png')
        for x in list:
            self.M.insertion(i, 'Index_1', 0.0)
            self.M.update(i, 'Path', x)
            i += 1

        # Ça, ça créer les listes test et banque (le truc 80/20)
        self.list_banque, self.list_test = train_test_split(list, test_size=0.2)

        # Là, on créer la table banque, avec les 80% d'images de la table images
        self.A = Interro('Images', 'Banque')
        self.A.creation()
        self.A.ajoutColonne('Index_1', 'REAL')
        self.A.ajoutColonne('Index_2', 'REAL')
        self.A.ajoutColonne('Path', 'TEXT', 'Oui')
        i = 1
        for x in self.list_banque:
            self.A.insertion(i, 'Index_1', 0.0)
            self.A.update(i, 'Path', x)
            i += 1

        # Et ici la table de test, avec les 20% restants
        self.T = Interro('Images', 'Test')
        self.T.creation()
        self.T.ajoutColonne('Index_1', 'REAL')
        self.T.ajoutColonne('Index_2', 'REAL')
        self.T.ajoutColonne('Path', 'TEXT', 'Oui')
        i = 1
        for x in self.list_test:
            self.T.insertion(i, 'Index_1', 0.0)
            self.T.update(i, 'Path', x)
            i += 1

############################################################################################################
    #La fonction rechercher va rechercher dans la table Banque selon le critère couleur ou distance l'image la plus
    #proche de l'image en cours

    def rechercher(self):
        self.valuechange_nbr_img()
        id_choisi = self.image_en_cours #l'image en cours
        img = Image(self.list_test[int(id_choisi)]) #on la transforme en une image "comparable" (Image est définie dans
        
        i = 1
        indices1 = []
        indices2 = []
        indices = []
        for x in self.list_banque:
            img2 = Image(x) #on transforme chaque image de la banque
            indice1, indice2 = img.compare(img2) #On compare à l'image en cours
            self.A.update(i, 'Index_1', indice1)
            self.A.update(i, 'Index_2', indice2) #on range tout les indice de comparaison dans la table
            indices1.append(indice1)
            indices2.append(indice2)
            indices.append([indice1,indice2]) # et on met tout ça dans une grosse liste
            i += 1

        indices = sorted(indices, key=operator.itemgetter(0)) #on effectue un premier trie sur la couleur
        indices_finaux = []
        for i in range(int(self.nbr_sortie)):
            indices_finaux.append(indices[i])
        indices_finaux = sorted(indices_finaux, key=operator.itemgetter(1)) #☺on effectue un second trie selon la distance
        list_res = []
        for i in range(int(self.nbr_sortie)):
            list_res.append(self.A.gation_path(indices_finaux[i][0],'Index_1'))
        

        #Et on les affiches selon le nombre de sorties voulu

        if self.nbr_sortie==1:
            pixmap = QtGui.QPixmap(list_res[0])
            self.label_img_result1.setPixmap(pixmap)
            self.label_img_result1.setScaledContents(True)


        if self.nbr_sortie==2:
            pixmap = QtGui.QPixmap(list_res[0])
            self.label_img_result1.setPixmap(pixmap)
            self.label_img_result1.setScaledContents(True)

            pixmap = QtGui.QPixmap(list_res[1])
            self.label_img_result2.setPixmap(pixmap)
            self.label_img_result2.setScaledContents(True)


        if self.nbr_sortie==3:
            pixmap = QtGui.QPixmap(list_res[0])
            self.label_img_result1.setPixmap(pixmap)
            self.label_img_result1.setScaledContents(True)

            pixmap = QtGui.QPixmap(list_res[1])
            self.label_img_result2.setPixmap(pixmap)
            self.label_img_result2.setScaledContents(True)

            pixmap = QtGui.QPixmap(list_res[2])
            self.label_img_result3.setPixmap(pixmap)
            self.label_img_result3.setScaledContents(True)




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MonAppli()
    window.show()
    app.exec_()
