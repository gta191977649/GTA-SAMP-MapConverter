kdff by Kalcor (SA-MP Team)
---------------------------------------

kdff is a collision generator, and model viewer, for GTA San Andreas models. It can generate
various types of GTA col (version 3) collision files given a dff model.

The generated collision can be edited externally and then attached to the dff.

Instructions:

Extract the files to their own folder and then run either kdffgui.exe or kdff.exe (console application)
depending on your needs.

Files:

kdffgui.exe : The main GUI program.
kdff.exe : The console application. Run this on the command line with no arguments for example usage.
kdff.dll : A dll required by kdffgui.exe, containing the col generation code.

---------------------------------------

v0.2.5b 2/2019
- kdff console couldn't read quoted paths from the command line.

v0.2.5a 12/2018
- Expands kdff gui 'Easy Color' feature. You can add cheap directional lighting (from a single light source) to the dff
  without having to import the model in to blender or 3dsmax.

v0.2.0b 12/2017
- kdff will still attempt to import night vertex colors, even when the vertex counts of the imported model don't match.

v0.2.0a 12/2017
- Adds -v option to kdff console to import night vertex colors from vertex colors of another dff (same model lit for night time).
- Adds 'Import NV' button kdff gui which is the same as the -v console option. Night vertex colors are imported
  from the vertex colors of the same model lit for night.
- Adds 'Easy Colors' buttons to kdff gui. All vertex colors are set to a single color. The first color is the day color, second
  color is the night color.

v0.1.1e 11/2017 
- Generate collision won't fail when the geometry has multiple textures assigned to a material. 
- More dff extension types are read, and won't cause col generation failures.

v0.1.1d 11/2017
- (fixed) A corrupt dff would be generated when attaching .col to a .dff containing lights.

v0.1.1c 11/2017
- Adds -p mode to kdff.exe console app

v0.1.1(a/b) 11/2017
- First release