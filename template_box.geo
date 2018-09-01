SetFactory("OpenCASCADE");

a = 5;
b = 5;
z = 5;

Box(1) = {-a/2, -b/2, -z/2, a, b, z};

Physical Surface("top") = {2};

Physical Surface("bottom") = {3};

Physical Surface("side") = {1};

Physical Volume("volume") = {1};

Characteristic Length {2, 1, 6, 5, 3, 4, 8, 7} = 5.0;
