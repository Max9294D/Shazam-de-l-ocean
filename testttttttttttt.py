# -*- coding: utf-8 -*-
"""
Created on Sun May  3 10:20:04 2020

@author: Max
"""

import cv2 # pip install opencv-python
import skimage.measure # pip install scikit-image
import scipy.ndimage


class Image:
    """
    Classe permettant de récupérer les données utiles à la comparaison d'une image
    
    """
    def __init__(self,chemin):
        
        self.image = cv2.imread(chemin,cv2.IMREAD_COLOR)
        
        self.image_gris = cv2.imread(chemin,cv2.IMREAD_GRAYSCALE)
       
        self.histo = cv2.calcHist([self.image_gris],[0],None,[256],[0,256])   

                   


        
      
        
    def compare(self, image2):
        """Test de comparaison entre 2 images
        """
                #filtre LoG (contour dérivé seconde)

        #opening the image and converting it to grayscale
        imA = self.image_gris
        #performing Laplacian of Gaussian filter
        imA = scipy.ndimage.filters.gaussian_laplace(imA,1,mode='reflect')
        #opening the image and converting it to grayscale
        imB = image2.image_gris
        #performing Laplacian of Gaussian filter
        imB = scipy.ndimage.filters.gaussian_laplace(imB,1,mode='reflect')
        #distance de hausdorff
        d1 = scipy.spatial.distance.directed_hausdorff(imA,imB)
        
        d2 = scipy.spatial.distance.directed_hausdorff(imB,imA)
        
        indice2 = max(d1,d2)[0]
        
        #on utilise la fct déjà implémentée pour comparer 2 histogrammes
        indice1 = cv2.compareHist(self.histo, image2.histo, cv2.HISTCMP_BHATTACHARYYA) 
        #plus l'indice2 est proche de 0 plus les 2 images ont une structure identique
        #plus l'indice2 est proche de 1 plus les 2 images ont une stucture différentes
        #print("comparaison histo de couleur",indice2)
        

        
        return indice1,indice2
    
    
if __name__ == "__main__":
    #notre image initiale
    img = Image("C:/Users/Max/Documents/Documents/ENSTA/cours/S2/projet_info/repertoire_images/humpback_whale/images_brutes/humpback_whale38.png")
    #l'image à laquellle on veut comparer notre image initiale
    image2 = Image("C:/Users/Max/Documents/Documents/ENSTA/cours/S2/projet_info/repertoire_images/humpback_whale/images_brutes/humpback_whale0.png")
    img.compare(image2)
    print(img.compare(img)[0],img.compare(img)[1]  )
    















