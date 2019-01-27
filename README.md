Project Title
Résolution d'EDP avec la méthode des éléments finis.  Anida Khizar - Janvier 2019

Ce projet a pour objectif de résoudre un problème physique, donné sous forme d'équations aux dérivés partielles, sur le domaine souhaité et de visualiser la solution.
Pour cela:
- on génère un maillage du domaine avec GMSH
- on importe le maillage en Python et on résoud le système d'équations par la méthode des éléments finis (aucune librairie n'est utilisée, tout est implémentée à la main).
- on utilise VTK pour générer un fichier d'extension .vtu (à partir du fichier d'extension .tri généré à l'étape précédente) correspondant à la solution trouvée. Ce fichier peut ensuite être lu par Paraview pour visualiser la solution.

Certains maillages sont fournis dans le projet, mais il est possible d'en créer d'autres et d'appliquer la méthode de résolution dessus.

Le problème par défaut est celui de l'équation d'Helmhotz. Le code doit donc être légèrement modifié (ou plutôt ajusté, toutes les fonctions nécessaires sont implémentées) si l'on souhaite résoudre un autre problème.

Getting Started

Le programme s'exécute avec Python2.

Pour faire tourner le programme, il suffit de suivre les étapes suivantes:
- ouvrir un terminal
- aller dans le dossier contenant le projet
- taper la commande suivante : ./build.sh fichier.geo

Par exemple, si vous souhaitez résoudre le problème sur un domaine défini dans le fichier cercle.geo, alors vous devez taper la commande suivante:
./build.sh cercle.geo

Ce script shell effectue toutes les étapes automatiquement : il va importer le maillage en Python, résoudre l'équation, générer le fichier de sortie output.vtu et lancer paraview pour visualiser la solution. 


Prerequisites

ATTENTION ! Ce programme nécessite l'installation de VTK (peu importe la version). Voici les étapes à suivre si vous êtes sur Linux:
- ouvrir un terminal
- taper la commande suivante : sudo apt-get install python-vtk

Il faut aussi avoir installé cmake. Voici les étapes à suivre si vous êtes sur Linux:
- ouvrir un terminal
- taper la commande suivante : sudo apt-get install cmake


