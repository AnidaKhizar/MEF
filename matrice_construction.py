# -*- coding: utf-8 -*-
import numpy as np
from scipy.sparse import csr_matrix, coo_matrix
from read_file import *

######################################################
# CONSTRUCTION DES MATRICES DU PROBLEME
######################################################


# définition des paramètres physiques
k = 6*np.pi

# définition des fonctions de forme
Phi_1     = lambda ksi, eta: 1 - ksi - eta
Phi_2     = lambda ksi, eta: ksi
Phi_3     = lambda ksi, eta: eta


def f(x,y):
    '''
    Données d'entrée: 
      - x      : abcisse du point  (float)
      - y      : ordonnée du point (float)
    Donnée de sortie:
      - f(x,y) : valeur de f en (x,y) (float)

    Définit la fonction f qui représente le terme source du problème
    '''
    return 0

def uinc(x,y):
    '''
    Données d'entrée: 
      - x      : abcisse du point  (float)
      - y      : ordonnée du point (float)
    Donnée de sortie:
      - uinc(x,y) : valeur de uinc en (x,y) (float)

    Définit la fonction uinc du problème
    '''

    alpha = np.pi / 3
    return np.exp( 1j*k * (x*np.cos(alpha) + y*np.sin(alpha)) )

def matrice_masse(msh):
    '''
    Donnée d'entrée: 
      - msh    : maillage du problème (Maillage)
    Donnée de sortie:
      - Masse  : matrice de masse du problème (matrice au format csr)

    Calcule la matrice de masse du problème
    '''

    row_list = []    #contient les indices de ligne des éléments non-nuls de la matrice
    col_list = [] #contient les indices de colonne des éléments non-nuls de la matrice
    data_list = []   #contient les valeurs des éléments non-nuls de la matrice

    
    for p in range(1,msh._Ne+1):

        # vérifier que l'élément est un triangle
        elem = msh.getElement(p)
        if elem._type == 2:
            
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

                    row_list.append(I-1)
                    col_list.append(J-1)

                    # ajouter les contributions élémentaires
                    if I == J:
                        data_list.append( area / 6 )

                    else:
                        data_list.append( area / 12 )
                        


    row = np.array(row_list)
    col = np.array(col_list)
    data = np.array(data_list)
    
    #contient les éléments non nuls de la matrice
    Masse = coo_matrix((data, (row, col)), shape=(msh._Ns, msh._Ns), dtype=complex)

    #conversion au format csr
    #(les indices dupliqués vont être sommés automatiquement)
    Masse = Masse.tocsr()
    
    return Masse

def matrice_rigidite(msh):
    '''
    Donnée d'entrée: 
      - msh       : maillage du problème (Maillage)
    Donnée de sortie:
      - Rigidite  : matrice de rigidité du problème (matrice au format csr)

    Calcule la matrice de rigidité du problème
    '''
    
    # gradient des fonctions de forme dans le triangle de référence
    grad_phi_chap = np.array([ [-1,-1], [1,0], [0,1] ])

    row_list = []    #contient les indices de ligne des éléments non-nuls de la matrice
    col_list = [] #contient les indices de colonne des éléments non-nuls de la matrice
    data_list = []   #contient les valeurs des éléments non-nuls de la matrice

    for p in range(1,msh._Ne+1):

        # vérifier que l'élément est un triangle
        elem = msh.getElement(p)
        if elem._type == 2:
            
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

                    #  ajouter les contributions élémentaires
                    c_elem = area * grad_phi_chap_j.dot( Bk_p * Bk_p.transpose() ).dot(grad_phi_chap_i)

                    row_list.append(I-1)
                    col_list.append(J-1)
                    data_list.append( c_elem.item(0) )
                    

    row = np.array(row_list)
    col = np.array(col_list)
    data = np.array(data_list)
    
    #contient les éléments non nuls de la matrice
    Rigidite = coo_matrix((data, (row, col)), shape=(msh._Ns, msh._Ns), dtype=complex)

    #conversion au format csr
    #(les indices dupliqués vont être sommés automatiquement)
    Rigidite = Rigidite.tocsr()

    return Rigidite



def matrice_masse_bord(msh):
    '''
    Donnée d'entrée: 
      - msh         : maillage du problème (Maillage)
    Donnée de sortie:
      - Masse_bord  : matrice de masse au bord du problème (matrice au format csr)

    Calcule la matrice de masse au bord du problème 
    '''
    
    row_list = []    #contient les indices de ligne des éléments non-nuls de la matrice
    col_list = [] #contient les indices de colonne des éléments non-nuls de la matrice
    data_list = []   #contient les valeurs des éléments non-nuls de la matrice
  
    for s in range(1,msh._Ne):

        #le segment s fait partie du bord
        if msh.getElement(s)._physical == 2:   

            # calculer la longueur du segment s
            length = msh.segLength(s)
            
            for i in [1,2]:
                I = msh.Loc2Glob(s,i)
                for j in [1,2]:
                    J = msh.Loc2Glob(s,j)

                    row_list.append(I-1)
                    col_list.append(J-1)

                    # ajouter les contributions élémentaires
                    if I == J:
                        data_list.append( length / 3 )
                    else:
                        data_list.append( length / 6 )



    row = np.array(row_list)
    col = np.array(col_list)
    data = np.array(data_list)
    
    #contient les éléments non nuls de la matrice
    Masse_bord = coo_matrix((data, (row, col)), shape=(msh._Ns, msh._Ns), dtype=complex)

    #conversion au format csr
    #(les indices dupliqués vont être sommés automatiquement)
    Masse_bord = Masse_bord.tocsr()
    

    return Masse_bord  

    
def membre_droite(msh):
    '''
    Donnée d'entrée: 
      - msh    : maillage du problème (Maillage)
    Donnée de sortie:
      - B      : membre de droite du problème (array)

    Renvoie le vecteur du membre de droite du problème
    '''

    B = np.zeros(msh._Ns, dtype=complex)

    ksi_m, eta_m = 1./3, 1./3
    
    for p in range(1,msh._Ne+1):

        # vérifier que l'élément est un triangle
        elem = msh.getElement(p)
        if elem._type == 2:
            
            # récupérer les coordonnées des sommets du triangle p
            (x1, y1, z1) = msh.getCoord(p, 1)
            (x2, y2, z2) = msh.getCoord(p, 2)
            (x3, y3, z3) = msh.getCoord(p, 3)

            # récupérer l'aire du triangle p
            area = msh.triArea(p)
               
            for i in [1,2,3]:
                I = msh.Loc2Glob(p,i)
                
                # définition des points de Gauss
                xm = x1 * Phi_1(ksi_m, eta_m) + x2 * Phi_2(ksi_m, eta_m) + x3 * Phi_3(ksi_m, eta_m)
                ym = y1 * Phi_1(ksi_m, eta_m) + y2 * Phi_2(ksi_m, eta_m) + y3 * Phi_3(ksi_m, eta_m)

                # quadrature de précision 1
                if i == 1:
                    quad = 1./6  * f(xm,ym) * Phi_1(ksi_m, eta_m)
                elif i == 2:
                    quad = 1./6  * f(xm,ym) * Phi_2(ksi_m, eta_m)
                else:
                    quad = 1./6  * f(xm,ym) * Phi_3(ksi_m, eta_m)

                # ajout de la quadrature au second membre
                B[I-1] += area * quad
        

    return B




def cond_Dirichlet(A,B, msh):
    '''
    Données d'entrée: 
      - A    : matrice creuse du problème (matrice au format csr)
      - B    : membre de droite du problème (array)
      - msh  : maillage du problème (Maillage)
      
    Applique les conditions de Dirichlet au système
    '''

    for s in range(1, msh._Ne):
        elem = msh.getElement(s)
        
        #le segment s fait partie du bord du sous-marin
        if elem._physical == 3:

            # récupérer l'indice global du premier sommet de s
            p1_ind = elem.getSommet(1)
            # récupérer l'indice global du deuxième sommet de s
            p2_ind = elem.getSommet(2)

            # récupérer les coordonnées du 1er point:
            (x1, y1, z1) = msh.getCoord(s, 1)
            B[p1_ind-1] = uinc(x1,y1)
            
            # récupérer les coordonnées du 2eme point:
            (x2, y2, z2) = msh.getCoord(s, 2)
            B[p2_ind-1] = uinc(x2,y2)
            
            A[p1_ind-1, :] = 0.0
            A[:, p1_ind-1] = 0.0
                        
            A[p2_ind-1, :] = 0.0
            A[:, p2_ind-1] = 0.0

            A[p1_ind-1, p1_ind-1] = 1.0
            A[p2_ind-1, p2_ind-1] = 1.0
                 

    A.eliminate_zeros()
    
    return
