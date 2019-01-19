# -*- coding: utf-8 -*-
import numpy as np
from read_file import *

# importer le maillage
msh = Maillage("carre.msh")
Ns = msh._Ns
Ne = msh._Ne

k = 0.1
alpha = np.pi

def uinc(x,y):
    return np.exp( 1j*k * (x*np.cos(alpha) + y*np.sin(alpha))  )


def matrice_masse():
    '''
    Calcule la matrice de masse du problème
    '''

    Masse = np.zeros( (Ns,Ns) )
    for p in range(1,Ne+1):

        # vérifier que l'élément est un triangle
        elem = msh.getElement(p)
        if isinstance(elem, Triangle):
            
            # récupérer les coordonnées des sommets du triangle p
            (x1, y1, z1) = msh.getCoord(p, 1)
            (x2, y2, z2) = msh.getCoord(p, 2)
            (x3, y3, z3) = msh.getCoord(p, 3)

            # récupérer l'aire du triangle p
            area = msh.triArea(p)
               
            for i in [1,2,3]:
                I = msh.Loc2Glob(p,i)
                for j in [1,2,3]:
                    J = msh.Loc2Glob(p,j)
                    
                    if I == J:
                        Masse[(I-1),(J-1)] +=  (area / 6)
                    else:
                        Masse[(I-1),(J-1)] +=  (area / 12)

    return Masse

def matrice_rigidite():
    '''
    Calcule la matrice de rigidité du problème
    '''
    

    # gradient des fonctions de forme dans le triangle de référence
    grad_phi_chap = np.array([ [-1,-1], [1,0], [0,1] ])

    Rigidite = np.zeros( (Ns,Ns) )

    for p in range(1,Ne+1):

        # vérifier que l'élément est un triangle
        elem = msh.getElement(p)
        if isinstance(elem, Triangle):
            
            # récupérer les coordonnées des sommets du triangle p
            (x1, y1, z1) = msh.getCoord(p, 1)
            (x2, y2, z2) = msh.getCoord(p, 2)
            (x3, y3, z3) = msh.getCoord(p, 3)

            # récupérer l'aire du triangle p
            area = msh.triArea(p)

            # construction de la matrice de passage Bk_p
            Bk_p = (1./ (2*area)) * np.matrix([ [y3-y1, y1-y2], [x1-x3, x2-x1] ])
            
            for i in [1,2,3]:
                I = msh.Loc2Glob(p,i)
                for j in [1,2,3]:
                    J = msh.Loc2Glob(p,j)
            
                    grad_phi_chap_i = grad_phi_chap[i-1]
                    grad_phi_chap_j = grad_phi_chap[j-1]

                    Rigidite[(I-1),(J-1)] += area * grad_phi_chap_j.dot( Bk_p * Bk_p.transpose() ).dot(grad_phi_chap_i)

    return Rigidite



def matrice_masse_bord():
    '''
    Calcule la matrice de masse au bord du problème
    '''
    
    Masse_bord = np.zeros( (Ns,Ns) )
    for s in range(1,Ne):

        #le segment s fait partie du bord
        if msh.getElement(s)._physical == 2:   

            # calculer la longueur du segment s
            length = msh.segLength(s)
            
            for i in [1,2]:
                I = msh.Loc2Glob(s,i)
                for j in [1,2]:
                    J = msh.Loc2Glob(s,j)
                    
                    if I == J:
                        Masse_bord[(I-1),(J-1)] +=  (length / 3)
                    else:
                        Masse_bord[(I-1),(J-1)] +=  (length / 6)

    return Masse_bord  
    



def membre_droite():
    '''
    Renvoie le vecteur du membre de droite du problème
    '''
    B = np.zeros(Ns)

    for s in range(1, Ne):
        elem = msh.getElement(s)
        
        #le segment s fait partie du bord
        if elem._physical == 2:

            # récupérer l'indice global du premier sommet de s
            p1_ind = elem.getSommet(1)
            # récupérer l'indice global du deuxième sommet de s
            p2_ind = elem.getSommet(2)

            if B[p1_ind] == 0:
                # récupérer les coordonnées du 1er point:
                (x1, y1, z1) = msh.getCoord(s, 1)
                B[p1_ind] = k**2 * uinc(x1,y1)

            if B[p2_ind] == 0:
                # récupérer les coordonnées du 2eme point:
                (x2, y2, z2) = msh.getCoord(s, 2)
                B[p2_ind] = k**2 * uinc(x2,y2)

    return B

    
# test des matrices
U = np.ones(Ns)
M = matrice_masse()
print( U.dot(M).dot(U) )
D = matrice_rigidite()
print(D.dot(U))
Mb = matrice_masse_bord()
print(Mb)
B = membre_droite()
print(B)
