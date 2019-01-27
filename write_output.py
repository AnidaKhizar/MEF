# -*- coding: utf-8 -*-
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
import sys
from matrice_construction import *


def write_output(sol, msh):
    '''
    Donnée d'entrée: 
     - sol  : solution du problème (array)
     - msh  : maillage du problème (Maillage)

    Écrit un fichier temporaire d'extension .tri 
    Ce fichier va être transcrit en un fichier .vtu grâce au langage vtk pour visualiser la solution sur paraview   
    '''
    output  = open("output.tri", "w")

    output.write("2 4 {0} {1}\n".format(msh._Ns, msh._Nt))
    
    #on écrit les coordonnées de chaque point
    for i in range(1,msh._Ns+1):
        x = msh.getNode(i).getCoord()[0]
        y = msh.getNode(i).getCoord()[1]
        z = msh.getNode(i).getCoord()[2]
        value = sol[i-1].real
        
        output.write("{0} {1} {2} {3}\n".format(x,y,z,value))

    #on écrit les indices des sommets composant les triangles
    for e in msh._Elems:
        if e._type == 2:  #l'élément est un triangle
            output.write("{0} {1} {2}\n".format(e.getSommet(1)-1, e.getSommet(2)-1, e.getSommet(3)-1))

    output.close() 


# importer le maillage
input_filename = sys.argv[1]
msh = Maillage(input_filename)

# construction des matrices
M = matrice_masse(msh)
D = matrice_rigidite(msh)
Mb = matrice_masse_bord(msh)
A = (k**2)*M - D -(1j*k)*Mb

# construction du membre de droite
B = membre_droite(msh)

#application des conditions de Dirichlet
cond_Dirichlet(A,B, msh)

# résolution du système
x = spsolve(A, B)

# écriture de la solution dans un fichier
write_output(x, msh)
