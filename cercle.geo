Mesh.MshFileVersion = 2.2;
// On définit des constantes que l'utilisateur pourra modifier de manière interactive dans l'interface de gmsh
// ex: par défaut, la valeur de R vaut 1 mais elle peut varier entre 0.5 et 10 avec un pas de 0.1
DefineConstant[
  R = {1, Min 0.5, Max 10, Step 0.1, Name "R"}, 
  Rint = {0.1, Min 0.1, Max 0.4, Step 0.1, Name "Rint"},
  h = {0.1, Min 0.01, Max 10, Step 0.01, Name "h"}
];   

xc = 0;
yc = 0;

//points du cercle extérieur
Point(1) = {xc, yc, 0, h};
Point(2) = {xc + R, yc, 0, h};
Point(3) = {xc, yc + R, 0, h};
Point(4) = {xc - R, yc, 0, h};
Point(5) = {xc, yc - R, 0, h};

//points du cercle intérieur
Point(6) = {xc + Rint, yc, 0, h};
Point(7) = {xc, yc + Rint, 0, h};
Point(8) = {xc - Rint, yc, 0, h};
Point(9) = {xc, yc - Rint, 0, h};

// cercle externe
Circle(1) = {2,1,3};
Circle(2) = {3,1,4};
Circle(3) = {4,1,5};
Circle(4) = {5,1,2};

//cercle interne
Circle(5) = {6,1,7};
Circle(6) = {7,1,8};
Circle(7) = {8,1,9};
Circle(8) = {9,1,6};

Line Loop(1) = {1,2,3,4}; //Définition d'un pourtour (d'un bord)
Line Loop(2) = {5,6,7,8}; 

Plane Surface(1) = {1,2};     //Définition d'une surface
Physical Surface(1) = {1};  //A sauvegarder dans le fichier de maillage
Physical Line(2) = {1,2,3,4};

