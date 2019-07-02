# Coding Standards

These following rules and guidelines are used through the nodeeditor package:

## File naming guidelines

* files in nodeeditor package start with ```node_```
* files containing graphical representation (PyQt5 overriden classes) start with ```node_graphics_```
* files for window/widget start with ```node_editor_```

## Coding guidelines

* methods use Camel case naming
* variables/properties use Snake case naming

* constructor ```__init__``` always contains all class variables for entire class. This is helpful for new users 
  to just look at the constractor and read about all properties that class is using. Nobody want's any 
  surprises hidden in the code later
* nodeeditor uses custom callbacks and listeners. Methods for adding callback functions
  are usually named ```addXYListener```
* custom events are usually named ```onXY```
* methods named ```doXY``` usually *do* certain tas and also take care off low level operations
* classes always contain methods in this order:
    * ```__init__```
    * ```initXY``` functions
    * listener functions
    * nodeeditor event fuctions
    * nodeeditor ```doXY``` and ```getXY``` helping functions 
    * Qt5 event functions
    * python magic methods (i.e. ```__str__```), setters and getters 
    * other functions
    * optionally overriden Qt ```paint``` method
    * ```serialize``` and ```deserialize``` methods at the end    