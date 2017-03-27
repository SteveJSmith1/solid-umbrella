# solid-umbrella
## A program which manipulate bytes amongst media filetypes for encryption purposes

*This function 'hides' one file inside another
and is also able to 'find' it again.*

File information and contents is read as bytes and then written as bytes into
another file. E.g. A .jpg can be encoded into a .mp3 or a .pdf can be encoded 
into a .wav.

### V1.0

#### Usage: 

run **python pyEncrypt.py** to start the user interface
or import the following functions.

**from pyEncrypt import fileHide, fileFind**

to hide a file:
    
**fileHide(file to encode, file to use for encoding in)**

to find a file hidden using the above function

**fileFind(filename of encoded file)**
