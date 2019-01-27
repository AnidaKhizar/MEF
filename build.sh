gmsh $1 -2                           # génération du maillage
IFS='.' read -ra mesh <<< "$1"       # tronquer l'extension .geo du fichier d'entrée
python2 write_output.py $mesh.msh    # résolution du problème

mkdir bin
cmake $PWD                           #importation de la triangulation
make
./Importer
paraview output.vtu                  #visualisation de la solution
