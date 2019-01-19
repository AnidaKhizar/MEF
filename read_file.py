# -*- coding: utf-8 -*-

class Element:
    """
    Classe qui représente un élément du maillage.
    """
    def __init__(self, ident, physical):
        """
        Constructeur de la classe Element.
        
        Paramètres: 
          - _id        : indice de l'élément (entier)
          - _physical  : indice physical de l'élément (entier)
        """

        self._id = ident
        self._physical = physical


class Triangle(Element):
    """
    Classe définissant un triangle.
    Elle hérite de la classe Element.
    """
    def __init__(self, ident, physical, s1, s2, s3):
        """
        Constructeur de la classe Triangle.

        Paramètres:
          - _sommets : indices globaux des sommets composant le triangle (tuple d'entiers)
        """
        
        Element.__init__(self, ident, physical)
        self._sommets = (s1,s2,s3)

    def getSommet(self, i):
        '''
        Retourne l'indice du i-ème sommet du triangle
        '''
        return self._sommets[i-1]
        
    def __str__(self):
        return "Element {0} : ({1}, {2}, {3})".format(self._id, self.getSommet(1), self.getSommet(2), self.getSommet(3))
    

class Segment(Element):
    """
    Classe définissant un segment.
    Elle hérite de la classe Element.
    """
    def __init__(self, ident, physical, p1, p2):
        """
        Constructeur de la classe Segment.
       
        Paramètres:
          - _sommets : indices globaux des sommets composant le segment (tuple d'entiers)
          
        """
        
        Element.__init__(self, ident, physical)
        self._sommets = (p1, p2)
        
    def getSommet(self, i):
        '''
        Retourne l'indice du i-ème sommet du segment
        '''
        return self._sommets[i-1]

    
    def __str__(self):
        return "Element {0} : ({1}, {2})".format(self._id, self.getSommet(1), self.getSommet(2))

class Node:
    """
    Classe définissant un point du maillage.
    """
    def __init__(self, ident, x, y, z):
        """
        Constructeur de la classe Node.

        Paramètres:
          - _id : indice du noeud (entier)
          - _x  : coordonnées x du noeud
          - _y  : coordonnées y du noeud
          - _z  : coordonnées z du noeud

        """
        self._id = ident
        self._x = x
        self._y = y
        self._z = z

    def getCoord(self):
        """
        Retourne les coordonnées du noeud
        """
        return (self._x, self._y, self._z)
        
    def __str__(self):
        return "Node {0} : ({1}, {2}, {3})".format(self._id, self._x, self._y, self._z)

class Maillage:
    """
    Classe définissant le maillage sur lequel on travaille.
    """
    def __init__(self, FileName):
        """
        Constructeur de la classe Maillage.

        Paramètres:
          - _FileName : nom du fichier à partir duquel on va charger le maillage (string)
          - _Ns       : nombre de sommets dans le maillage (entier)
          - _Ne       : nombre d'éléments dans le maillage (entier)
          - _Nodes    : ensemble des noeuds du maillage (liste de Node)
          - _Elems    : ensemble des éléments du maillage (liste d'Element)        

        """
        
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


    def getElement(self, i):
        '''
        Retourne l'élément d'indice i du maillage
        '''
        return self._Elems[i-1]

    def getNode(self, i):
        '''
        Retourne le noeud d'indice i du maillage
        '''
        return self._Nodes[i-1]


    def getCoord(self, e, i):
        '''
        Données d'entrée: 
          - e        : indice de l'élément (triangle ou sommet) en question (entier)
          - i        : indice local du sommet dans l'élément e (entier)
        Données de sortie: 
          - (x,y,z)  : coordonnées du i-ème sommet de l'élément e (tuple de float)
        
        Retourne les coordonnées du i-ème sommet de l'élément e (triangle, ou segment)
        '''
        
        # récupérer l'élément e
        elem = self.getElement(e)

        # récupérer l'indice global du sommet i dans l'élément e
        s_ind = elem.getSommet(i)

        # récupérer le sommet i du triangle p
        s = self.getNode(s_ind)

        # retourner les coordonnées du sommet i dans le triangle p
        return s.getCoord()      
        
        
    def Loc2Glob(self, e, i):
        '''
        Données d'entrée: 
          - e : indice de l'élément (entier)
          - i : indice local du sommet dans l'élément e (entier)
        Données de sortie: 
          - I : indice global du i-ème sommet de l'élément e (entier)
        
        Retourne l'indice I global du sommet i de l'élément e    
        '''
        elem = self.getElement(e)
        I = elem.getSommet(i)
        return I


    def triArea(self, p):
        '''
        Données d'entrée: 
          - p    : indice du triangle (entier)
        Données de sortie: 
          - area : aire du triangle p (float)
        
        Retourne l'aire du triangle d'indice p    
        '''
        
        # récupérer les coordonnées des sommets du triangle p
        (x1, y1, z1) = self.getCoord(p, 1)
        (x2, y2, z2) = self.getCoord(p, 2)
        (x3, y3, z3) = self.getCoord(p, 3)

        area = 0.5 * abs((x2 - x1)*(y3 - y1) - (x3 - x1)*(y2 - y1))
        return area


    def segLength(self, s):
        '''
        Données d'entrée: 
          - s      : indice du segment (entier)
        Données de sortie: 
          - length : longueur du segment s (float)
        
        Retourne la longueur du segment d'indice s    
        '''
        
        # récupérer les coordonnées des sommets du segment s
        (x1, y1, z1) = self.getCoord(s, 1)
        (x2, y2, z2) = self.getCoord(s, 2)

        length = np.sqrt( (x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2  ) 
        return length

    
    def __str__(self):
        
        string = "-------------\nNODES\n-------------\n"
        for node in self._Nodes:
            string += node.__str__() + "\n"

        string += "-------------\nELEMENTS\n-------------\n"
        for elem in self._Elems:
            string += elem.__str__() + "\n"

        return string

