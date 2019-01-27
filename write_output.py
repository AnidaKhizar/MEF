# -*- coding: utf-8 -*-
import numpy as np
from matrice_construction import *

def write_output(sol, msh):
    '''
    Donnée d'entrée: 
     - sol  : solution du problème (array)
     - msh  : maillage du problème (Maillage)

    Écrit un fichier d'extension .vtu pour visualiser la solution sur paraview   
    '''
    output  = open("output.vtu", "w")

    output.write("<VTKFile type=\"UnstructuredGrid\" version=\"1.0\" byte_order=\"LittleEndian\" header_type=\"UInt64\">\n")
    output.write("<UnstructuredGrid>\n")
    output.write("<Piece NumberOfPoints=\"{0}\" NumberOfCells=\"{1}\">\n".format(msh._Ns,msh._Nt))
    output.write("<Points>\n")
    output.write("<DataArray NumberOfComponents=\"3\" type=\"Float64\">\n")

    #on écrit les coordonnées de chaque point
    for n in msh._Nodes:
        x = n.getCoord()[0]
        y = n.getCoord()[1]
        z = n.getCoord()[2]
        output.write("{0} {1} {2}\n".format(x,y,z))

    output.write("</DataArray>\n</Points>\n<Cells>\n")
    output.write("<DataArray type=\"Int32\" Name=\"connectivity\" format=\"ascii\">\n")

    #on écrit les indices des sommets composant les triangles
    for e in msh._Elems:
        if e._type == 2:  #l'élément est un triangle
            output.write("{0} {1} {2}\n".format(e.getSommet(1)-1, e.getSommet(2)-1, e.getSommet(3)-1))
            

    output.write("</DataArray>\n")
    output.write("<DataArray type=\"UInt8\" Name=\"offsets\" format=\"ascii\">\n")

    for e in range(msh._Nt):
        output.write("{0}\n".format(3*(e+1)))

    output.write("</DataArray>\n")
    output.write("<DataArray type=\"UInt8\" Name=\"types\" format=\"ascii\">\n")

    for e in range(msh._Nt):
        output.write("5\n")

    output.write("</DataArray>\n")
    output.write("</Cells>\n")

    output.write("<PointData Scalars=\"solution\">\n")
    output.write("<DataArray type=\"Float64\" Name=\"Real part\" format=\"ascii\">\n")

    for i in range(msh._Ns):
        output.write("{0}\n".format(sol[i].real))

    output.write("</DataArray>\n")
    output.write("<DataArray type=\"Float64\" Name=\"Imag part\" format=\"ascii\">\n")
    
    for i in range(msh._Ns):
        output.write("{0}\n".format(sol[i].imag))  

    output.write("</DataArray>\n</PointData>\n</Piece>\n</UnstructuredGrid>\n</VTKFile>\n")

    output.close() 




def write_outputVTK(sol, msh):
    '''
    Donnée d'entrée: 
     - sol  : solution du problème (array)
     - msh  : maillage du problème (Maillage)

    Écrit un fichier temporaire d'extension .tri 
    Ce fichier va être transcrit en un fichier .vtu dans un format différent que dans la fonction write_output par le fichier Importer.cpp, grâce au langage vtk
    Cette méthode permet de visualiser des solutions même avec un maillage fin !
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
