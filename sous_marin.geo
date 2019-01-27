Mesh.MshFileVersion = 2.2;
h = 1;
R1 = 1.2;
R2 = 0.6;

//points de l'ellipse extérieure
Point(1) = {0,0,0,h};
Point(2) = {0,R2,0,h};
Point(3) = {R1,0,0,h};
Point(4) = {0,-R2,0,h};
Point(5) = {-R1,0,0,h};


// points du sous-marin
Point(6) = {0.4,0.1,0,h};
Point(7) = {0.5,0,0,h};
Point(8) = {0.4,-0.1,0,h};
Point(9) = {-0.2,-0.1,0,h};
Point(10) = {-0.5,0,0,h};
Point(11) = {-0.2,0.1,0,h};
Point(12) = {0.4,0,0,h};
Point(13) = {-0.2,0,0,h};


//ailerons
Point(14) = {-0.3,0.095,0,h};
Point(15) = {-0.34,0.09,0,h};
Point(16) = {-0.3,-0.095,0,h};
Point(17) = {-0.34,-0.09,0,h};

Point(18) = {-0.3,0.14,0,h};
Point(19) = {-0.34,0.12,0,h};
Point(20) = {-0.3,-0.14,0,h};
Point(21) = {-0.34,-0.12,0,h};

Point(22) = {0.1,0.1,0,h};
Point(23) = {0.12,0.2,0,h};
Point(24) = {0.19,0.25,0,h};
Point(25) = {0.21,0.1,0,h};

Point(26) = {-0.34,0,0,h};

// génération des 4 arcs elliptiques
Ellipse(1) = {2,1,3,3};
Ellipse(2) = {3,1,3,4};
Ellipse(3) = {4,1,5,5};
Ellipse(4) = {5,1,5,2};


// génération du bord du sous-marin
Line(5) = {11,22};
Spline(6) = {22,23,24,25};
Line(7) = {25,6};
Circle(8) = {6,12,7};
Circle(9) = {7,12,8};
Line(10) = {8,9};

Spline(11) = {9,16};
Line(12) = {16,20};
Line(13) = {20,21};
Line(14) = {21,17};
Spline(15) = {16,17};   //pas dans le bord
Ellipse(16) = {17,26,10,10};


Ellipse(17) = {10,26,10,15};
Line(18) = {15,19};
Line(19) = {19,18};
Line(20) = {18,14};
Spline(21) = {15,14};   //pas dans le bord
Spline(22) = {14,11};

Line Loop(1) = {1,2,3,4};
Line Loop(2) = {5,6,7,8,9,10,11,12,13,14,16,17,18,19,20,22};


Plane Surface(1) = {1,2};     //Définition d'une surface
Physical Surface(1) = {1};  //A sauvegarder dans le fichier de maillage
Physical Line(2) = {1,2,3,4};
