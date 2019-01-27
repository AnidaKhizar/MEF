#gmsh $1 -2                           # génération du maillage
#IFS='.' read -ra mesh <<< "$1"       # tronquer l'extension .geo du fichier d'entrée
#python2 write_output.py $mesh.msh    # résolution du problème

mkdir -p bin                         
cmake $PWD                           # génération du Makefile
make
./Importer                           # importation de la triangulation en vtk
paraview outputVTK.vtu                  # visualisation de la solution
