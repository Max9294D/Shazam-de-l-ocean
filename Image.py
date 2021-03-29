# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 11:43:33 2020

@author: Max
"""




import cv2 # pip install opencv-python
import skimage.measure # pip install scikit-image


class Image:
    """
    Classe permettant de récupérer les données utiles à la comparaison d'une image
    
    """
    def __init__(self,chemin):
        self.image = cv2.imread(chemin,cv2.IMREAD_COLOR)
        self.image_gris = cv2.imread(chemin,cv2.IMREAD_GRAYSCALE)
        self.histo = cv2.calcHist([self.image_gris],[0],None,[256],[0,256])                 


    def compare(self, image2, image2_histo):
        """Test de comparaison entre 2 images
        """
        
        #on compare des images en niveaux de gris donc on récupère les niveaux de gris 
        #des 2 images qu'on veut comparer
        Image1_gris = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        Image2_gris = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        
        #on utilise la fct déjà implémentée ssim qui compare la structure de 2 images
        #en niveau de gris (on peut le remplacer par la fct mse si on se rend compte qu'il
        #n'est pas assez efficace mais alors l'indice n'est plus entre 0 et 1 mais plus entre
        # 0 et l'infini)
        s = skimage.measure.compare_ssim(Image1_gris, Image2_gris)
        indice1 = abs(1-s)  
        #plus l'indice est proche de 0 plus les 2 images ont une structure identique
        #plus l'indice est proche de 1 plus les 2 images ont une stucture différentes
        #print("ssim :",indice1)
        
        #on utilise la fct déjà implémentée pour comparer 2 histogrammes
        indice2 = cv2.compareHist(self.histo, image2_histo, cv2.HISTCMP_BHATTACHARYYA) 
        #plus l'indice2 est proche de 0 plus les 2 images ont une structure identique
        #plus l'indice2 est proche de 1 plus les 2 images ont une stucture différentes
        #print("comparaison histo de couleur",indice2)
        return indice1,indice2
        
        

#
# if __name__ == "__main__":
#     #notre image initiale
#     img = Image("C:/Users/Max/Documents/Documents/ENSTA/cours/S2/projet_info/repertoire_images/humpback_whale/images_brutes/humpback_whale38.png")
#     #l'image à laquellle on veut comparer notre image initiale
#     image2 = cv2.imread("C:/Users/Max/Documents/Documents/ENSTA/cours/S2/projet_info/repertoire_images/humpback_whale/images_brutes/humpback_whale0.png",cv2.IMREAD_COLOR)
#     #on récupère l'image2 en niveaux de gris
#     image2_gris = cv2.imread("C:/Users/Max/Documents/Documents/ENSTA/cours/S2/projet_info/repertoire_images/humpback_whale/images_brutes/humpback_whale0.png",cv2.IMREAD_GRAYSCALE)
#     #on calcule l'histo des couleurs pour notre image2
#     image2_histo = cv2.calcHist([image2_gris],[0],None,[256],[0,256])
#
#     #on compare nos 2 images
#     img.compare(image2, image2_histo)
