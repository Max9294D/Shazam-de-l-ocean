from Interro import *
from Creation_bdd import *
from Image import *


if __name__ == "__main__":
# Ici ça créer la BDD et une première table avec toutes les images + le chemin
    M = Interro('Images','Images')
    M.creation()
    M.ajoutColonne('Index_1', 'REAL')
    M.ajoutColonne('Index_2', 'REAL')
    M.ajoutColonne('Path', 'TEXT', 'Oui')
    i=1
    list = glob.glob('./BDD/shazam_images/' + '*.png')
    for x in list:
        M.insertion(i,'Index_1',0.0)
        M.update(i,'Path',x)
        i+=1

# Ça, ça créer les listes test et banque (le truc 80/20)
    list_banque, list_test = train_test_split(list, test_size=0.2)


# Là, on créer la table banque, avec les 80% d'images de la table images
    A=Interro('Images','Banque')
    A.creation()
    A.ajoutColonne('Index_1', 'REAL')
    A.ajoutColonne('Index_2', 'REAL')
    A.ajoutColonne('Path', 'TEXT', 'Oui')
    i = 1
    for x in list_banque:
        A.insertion(i, 'Index_1', 0.0)
        A.update(i, 'Path', x)
        i += 1


#Et ici la table de test, avec les 20% restants
    T = Interro('Images', 'Test')
    T.creation()
    T.ajoutColonne('Index_1', 'REAL')
    T.ajoutColonne('Index_2', 'REAL')
    T.ajoutColonne('Path', 'TEXT', 'Oui')
    i = 1
    for x in list_test:
        T.insertion(i, 'Index_1', 0.0)
        T.update(i, 'Path', x)
        i += 1


    print("La BDD a été crée")





    id_choisi=input("Choisissez un id de la table test : ")
    img=Image(list_test[int(id_choisi)-1])
    i=1
    indices1=[]
    indices2=[]
    for x in list_banque :
        img2 = cv2.imread(x)
        img2 = cv2.imread(x, cv2.IMREAD_COLOR)
        img2_gris = cv2.imread(x, cv2.IMREAD_GRAYSCALE)
        img2_histo = cv2.calcHist([img2_gris], [0], None, [256], [0, 256])
        indice1, indice2=img.compare(img2, img2_histo)
        A.update(i,'Index_1',indice1)
        A.update(i, 'Index_2', indice2)
        indices1.append(indice1)
        indices2.append(indice2)
        i+=1

    indices1=sorted(indices1)
    indices2=sorted(indices2)
    nbr_ele=input("Combien d'éléments en sorties? ")
    list_res1=[]
    list_res2=[]
    for i in range(int(nbr_ele)):
        list_res1.append(A.gation_path(indices1[i],'Index_1'))
        list_res2.append(A.gation_path(indices2[i], 'Index_2'))