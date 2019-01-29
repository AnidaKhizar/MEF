# -*- coding: utf-8 -*-
import sys, time
from scipy.sparse.linalg import spsolve
from write_output import *

##########################################################################
# MAIN:
# résoud le problème
# génère les fichiers nécessaires à la visualisation de la solution
##########################################################################

# importer le maillage
input_filename = sys.argv[1]
start = time.time()
msh = Maillage(input_filename)
t1 = time.time()
print("Importation du maillage : {0}s\n".format(t1 - start))

# construction des matrices
M = matrice_masse(msh)
D = matrice_rigidite(msh)
Mb = matrice_masse_bord(msh)
A = (k**2)*M - D -(1j*k)*Mb

# construction du membre de droite
B = k**2*membre_droite(msh)
t2 = time.time()
print("Construction des matrices et du membre de droite : {0}s\n".format(t2-t1))

#application des conditions de Dirichlet
cond_Dirichlet(A,B, msh)
t3 = time.time()
print("Application des conditions de Dirichlet : {0}s\n".format(t3-t2))

# résolution du système
x = spsolve(A, B)
t4 = time.time()
print("Résolution du système : {0}s\n".format(t4-t3))

# écriture de la solution dans 2 fichiers

# extension .vtu : si le maillage est trop fin, on ne pourra pas forcément visualiser la solution sur paraview avec ce fichier
write_output(x, msh)

# extension .tri : même si le maillage est fin, on pourra visualiser la solution avec paraview, mais avec une étape supplémentaire dans la compilation
write_outputVTK(x, msh)
fin = time.time()
print("Ecriture des fichiers : {0}s\n".format(fin-t4))

print("==> Temps total: {0}s\n".format(fin-start))
