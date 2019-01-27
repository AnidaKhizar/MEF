# Project Title

Résolution d'EDP avec la méthode des éléments finis [Anida Khizar - Janvier 2019]

## Getting Started

Ce projet a pour objectif de résoudre un problème physique, donné sous forme d'équations aux dérivés partielles, sur le domaine souhaité et de visualiser la solution.
Pour cela:
* on génère un maillage du domaine avec GMSH
* on importe le maillage en Python et on résoud le système d'équations par la méthode des éléments finis (aucune librairie n'est utilisée, tout est implémentée à la main).
Cette étape génère 2 fichiers: un fichier d'extension .vtu et un fichier d'extension .tri. 
* on visualise la solution avec 2 méthodes possibles. La première consiste à directement observer la solution sur paraview en exploitant le fichier .vtu généré précédemment. Seulement le format de ce fichier est tel que Paraview ne parvient pas à le lire si le maillage est trop fin. La deuxième option est d'utiliser le fichier d'extension .tri, qui va être traduit en un fichier .vtu (mais dans un format différent) par le fichier Importer.cpp, qui se base sur la librairie VTK. 

Certains fichiers .geo sont fournis dans le projet, mais il est possible d'en créer d'autres et d'appliquer la méthode de résolution dessus.

Le problème par défaut est celui de l'équation d'Helmhotz. Le code doit donc être légèrement modifié (ou plutôt ajusté, toutes les fonctions nécessaires sont implémentées) si l'on souhaite résoudre un autre problème.


### Prerequisites

Le programme s'exécute avec Python2.

Pour faire tourner le programme, il suffit de suivre les étapes suivantes:
* ouvrir un terminal
* aller dans le dossier contenant le projet
* taper les commandes suivantes : 
```
gmsh fichier.geo -2
python2 main.py fichier.msh
```
L'équation a donc été résolue. Pour visualiser la solution, vous avez 2 possibilités:
* vous pouvez directement la visualiser avec paraview en tapant la commande suivante:
```
paraview output.vtu
```
* vous pouvez utiliser VTK, ce qui permet de visualiser la solution même si le maillage est fin, en tapant la commande suivante:
```
./build.sh
```

En résumé, si vous souhaitez par exemple, résoudre le problème sur un domaine défini dans le fichier sous_marin.geo, alors vous devez taper les commandes suivantes:
```
gmsh sous_marin.geo -2
python2 main.py sous_marin.msh
```
Ensuite vous pouvez tapez l'une des 2 commandes suivantes:
```
paraview output.vtu
```
ou
```
./build.sh
```

### Installing

ATTENTION ! La 2ème méthode de visualisation (celle avec le fichier intermédiaire .tri) nécessite l'installation de VTK (peu importe la version) et de cmake. Voici les étapes à suivre si vous êtes sur Linux:
* ouvrir un terminal
* taper les commandes suivantes : 
```
sudo apt-get install python-vtk
sudo apt-get install cmake
```


