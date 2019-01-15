# -*- coding: utf-8 -*-

class Element:
    """
    Classe qui représente un élément du maillage.
    """
    def __init__(self, ident, physical):
        self._id = ident
        self._physical = physical


class Triangle(Element):
    """
    Classe définissant un triangle.
    Elle hérite de la classe Element.
    """
    def __init__(self, ident, physical, s1, s2, s3):
        Element.__init__(self, ident, physical)
        self._s1 = s1
        self._s2 = s2
        self._s3 = s3

    def __str__(self):
        return "Element {0} : ({1}, {2}, {3})".format(self._id, self._s1, self._s2, self._s3)

class Segment(Element):
    """
    Classe définissant un segment.
    Elle hérite de la classe Element.
    """
    def __init__(self, ident, physical, p1, p2):
        Element.__init__(self, ident, physical)
        self._p1 = p1
        self._p2 = p2

    def __str__(self):
        return "Element {0} : ({1}, {2})".format(self._id, self._p1, self._p2)

class Node:
    """
    Classe définissant un point du maillage.
    """
    def __init__(self, ident, x, y, z):
        self._id = ident
        self._x = x
        self._y = y
        self._z = z

    def __str__(self):
        return "Node {0} : ({1}, {2}, {3})".format(self._id, self._x, self._y, self._z)

class Maillage:
    """
    Classe définissant le maillage sur lequel on travaille.
    """
    def __init__(self, FileName):
        self._FileName = FileName
        self._Ns, self._Nodes = self.Nodes()
        self._Ne, self._Elems = self.Elems()
        
    def Nodes(self):        
        mesh = open(self._FileName, "r")

        for i in range(4): #sauter les 4 premières lignes
            line = mesh.readline()

        line = mesh.readline()
        Ns = int(line)
        
        Nodes = []
        for n in range(Ns):    
            line = mesh.readline()
            line = line.split()
            ident = int(line[0])
            x,y,z = float(line[1]), float(line[2]), float(line[3])
            node = Node(ident, x, y, z)
            Nodes.append( node )

        mesh.close()
        return (Ns, Nodes)

    def Elems(self):
        mesh = open(self._FileName, "r")
        
        for i in range(4 + 1 + self._Ns + 2): #sauter les premières lignes
            line = mesh.readline()

        line = mesh.readline()
        Ne = int(line)

        Elements = []
        for e in range(Ne):
            line = mesh.readline()
            line = line.split()

            ident = int(line[0])
            Ntags = int(line[2])
            physical = int(line[3])
            
            typeElem = int(line[1])
            if typeElem == 2:  #triangle
                s1, s2, s3 = int(line[3+Ntags]), int(line[4+Ntags]), int(line[5+Ntags])
                element = Triangle(ident, physical, s1, s2, s3)
            
            elif typeElem == 1: #segment
                p1, p2 = int(line[3+Ntags]), int(line[4+Ntags])
                element = Segment(ident, physical, p1, p2)

            Elements.append(element)
                
        mesh.close()
        return (Ne, Elements)


    def __str__(self):
        
        string = "-------------\nNODES\n-------------\n"
        for node in self._Nodes:
            string += node.__str__() + "\n"

        string += "-------------\nELEMENTS\n-------------\n"
        for elem in self._Elems:
            string += elem.__str__() + "\n"

        return string

    
    
m = Maillage("carre.msh")
print m
