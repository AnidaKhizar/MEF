# -*- coding: utf-8 -*-
import numpy as np
from read_file import *

# importer le maillage
msh = Maillage("carre.msh")
Ns = msh._Ns
Nt = msh._Nt

def matrice_masse():
    '''
    Calcule la matrice de masse du problème
    '''
    
    # matrice de masse élémentaire
    Me = 1./12 * np.matrix([ [2, 1, 1], [1, 2, 1], [1, 1, 2] ]) 

    Masse = np.zeros( (Ns,Ns) )
    for p in range(1,Nt+1):

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

    for p in range(1,Nt+1):

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

# test des matrices
U = np.ones(Ns)
M = matrice_masse()
print( U.dot(M).dot(U) )
D = matrice_rigidite()
print(D.dot(U))
