# -*- coding: utf-8 -*-
"""
Created on Sat May 16 10:30:13 2020

@author: Max
"""
import numpy
import glob
import unittest
import Interro as i
import Creation_bdd as c
import testttttttttttt as t

class Test_testttttttttttt(unittest.TestCase):
    def test_type_image(self):
        imA = t.Image("C:/Users/Max/Documents/Documents/ENSTA/cours/S2/projet_info/repertoire_images/humpback_whale/images_brutes/humpback_whale38.png")
                
        self.assertIsInstance(imA, t.Image)        
        self.assertTrue(isinstance(imA.image,numpy.ndarray))
        self.assertTrue(isinstance(imA.image_gris,numpy.ndarray))
        self.assertTrue(isinstance(imA.histo,numpy.ndarray))

    def test_type_indice(self):
        imA = t.Image("C:/Users/Max/Documents/Documents/ENSTA/cours/S2/projet_info/repertoire_images/humpback_whale/images_brutes/humpback_whale38.png")
        image2 = t.Image("C:/Users/Max/Documents/Documents/ENSTA/cours/S2/projet_info/repertoire_images/humpback_whale/images_brutes/humpback_whale0.png")
        imA.compare(image2)
        indice1 = imA.compare(image2)[0]
        indice2 = imA.compare(image2)[1]
        
        self.assertTrue(isinstance(indice1,float))
        self.assertTrue(isinstance(indice2,float))

        
    def test_var(self):
        imA = t.Image("C:/Users/Max/Documents/Documents/ENSTA/cours/S2/projet_info/repertoire_images/humpback_whale/images_brutes/humpback_whale38.png")
        imA.compare(imA)
        indice1 = imA.compare(imA)[0]
        indice2 = imA.compare(imA)[1]
        
        self.assertEqual(indice1,0.0)
        self.assertEqual(indice2,0.0)
  
      
class Test_Interro_et_Creation_BDD(unittest.TestCase):
    def test_type(self):
        M = i.Interro('Images','Images')
        M.creation()
        M.ajoutColonne('Index_1', 'REAL')
        M.ajoutColonne('Index_2', 'REAL')
        M.ajoutColonne('Path', 'TEXT', 'Oui')
        j=1
        list = glob.glob('./BDD/shazam_images/' + '*.png')
        for x in list:
            M.insertion(j,'Index_1',0.0)
            M.update(j,'Path',x)
            j+=1
            
        self.assertIsInstance(M,i.Interro)
        self.assertNotIsInstance(c.modifBDD,c.Bdd)
    
        
        
if __name__ == '__main__':
    unittest.main()