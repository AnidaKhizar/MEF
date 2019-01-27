# -*- coding: utf-8 -*-
import sys
from scipy.sparse.linalg import spsolve
from write_output import *

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

# écriture de la solution dans 2 fichiers

# extension .vtu : si le maillage est trop fin, on ne pourra pas forcément visualiser la solution sur paraview avec ce fichier
write_output(x, msh)

# extension .tri : même si le maillage est fin, on pourra visualiser la solution avec paraview, mais avec une étape supplémentaire dans la compilation
write_outputVTK(x, msh)
