#sudo apt-get install python-vtk
python2 write_output.py $1
cmake $PWD
make
./Importer
paraview output.vtu
