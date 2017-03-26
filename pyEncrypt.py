#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 16:16:05 2017

@author: steveJsmith1

This function 'hides' one file inside another
and is also able to 'find' it again.

see tests.py to see what is currently working

to hide a file:
    
    fileHide(
            file to encode, 
            file to use for encoding in, 
            filename of encoded file)
    
to find a file hidden using the above function

    fileFind(
            filename of encoded file
            desired filename of output
            )
"""



#=============================================

# The main functions to call when running

def fileHide(file_to_enc, f_to_enc_in, filebytes=False):
    """
    to hide a file:
    
    fileHide(
            file to encode, 
            file to use for encoding in, 
            filename of encoded file)
    
    filebytes=True called from testFunction
    """
    # creating bytearrays
    file_to_enc_b = readBytes(file_to_enc)
    f_to_enc_in_b = readBytes(f_to_enc_in)
    
    # check file to encode in is big enough
    check = fileCheck(file_to_enc_b, f_to_enc_in_b)
    
    if check == False:
        print("""
    WARNING: Size of file to encode in is too 
    small, file not hidden.
    Suggest using a larger file;
        try a .wav, .mp4 instead of an .mp3 perhaps""")
        return
    
    # processing the bytes
    encoded_bytes = encodeBytes(file_to_enc, f_to_enc_in_b, file_to_enc_b)    
    
    # naming output file
    out_file_name = 'H-' + f_to_enc_in
    # check if file already exists
    out_file_name = checkExists(out_file_name)
    writeBytes(encoded_bytes, out_file_name)
    
    # returning bytes for equality check in
    # testFunction()
    if filebytes==True:
        return file_to_enc_b, out_file_name
    else:
        return out_file_name


def fileFind(enc_file, filebytes=False):
    """
    to find a file hidden using fileHide()

    fileFind(
            filename of encoded file
            desired filename of output
            )
    
    filebytes=True called from testFunction()
    """
    # fetching bytes from encoded file
    enc_bytes = readBytes(enc_file)
    # fetching information from encoded bytes
    out_file_bytes, filename = decodeBytes(enc_bytes)
    # check if file exists
    filename = checkExists(filename)
    # write file
    writeBytes(out_file_bytes, filename)
    #returning bytes for equality test in 
    # testFunction()
    if filebytes==True:
        return out_file_bytes
    else:
        return filename

#===============================================

# Bytes processing functions


def encodeBytes(file_to_enc, f_to_enc_in_b, file_to_enc_b):
    # fetching the array containing the filename   
    name_array = filenameToBytes(file_to_enc)
    # overwriting bytes with filename
    f_to_enc_in_b[2000:2350] = name_array
    
    
    # getting the length of the bytes to hide
    len_f_t_e_b = int(len(file_to_enc_b))
    # turning this integer it a bytes object
    # of length 10
    len_f_as_bytes = len_f_t_e_b.to_bytes(10, byteorder='big')
    # overwriting bytes with the bytes of length
    f_to_enc_in_b[1000:1010] = len_f_as_bytes
    # finding point in file to start 'hiding'
    halfway = int(len(f_to_enc_in_b)/2)
    # overwrite the bytes with the bytes to 'hide'
    f_to_enc_in_b[halfway:halfway+len_f_t_e_b] = file_to_enc_b
    return f_to_enc_in_b


def decodeBytes(enc_bytes):
    # extracting encded
    # info about file length in bytes
    out_file_len = int.from_bytes(enc_bytes[1000:1010], byteorder='big')
    # extracting encoded filename
    name_array = enc_bytes[2000:2350]
    # converting bytes to string of filename
    filename = 'F-' + bytesToFilename(name_array)
    # extracting encoded out_file bytes
    halfway = int(len(enc_bytes)/2)
    
    out_file_bytes = enc_bytes[halfway:halfway + out_file_len]
    
    return out_file_bytes, filename

#============================================

# pre-processing checks  

def fileCheck(in_file_bytes, enc_file_bytes):
    """
    Check that the file to encode in is twice
    the length of the file to hide
    (this is arbirtary at the moment)
    """
    if len(enc_file_bytes) > (2*len(in_file_bytes)):
        return True
    else:
        return False

#============================================

# Filename Operations

def filenameToBytes(filename):
    # setting up a fairly large bytearray
    # to contain the filename.
    # if 350 is altered, the corresponding 
    # slices in the main functions will
    # need to be changed
    name_array = bytearray(350)
    # create a bytearray of the filename
    filename_bytes = bytearray(filename, 'utf-8')
    # inserting filename_bytes into the beginning
    # of the name array
    name_array[0:len(filename_bytes)] = filename_bytes
    return name_array
     
def bytesToFilename(name_array):
    # filename between beginning of array
    # and first null byte
    filename_bytes = name_array[0:name_array.find(0)]
    filename = filename_bytes.decode()
    return filename


def checkExists(filename):
    import os
    
    if os.path.isfile(filename):
        print(filename, " already exists, overwrite? [y]es, [n]o")
        overwrite = input(str("> "))
        if overwrite == 'y':
            os.remove(filename)
            print(filename, " deleted")
        else:
            print("Enter a filename to save as: ")
            filename = str(input("> "))
    return filename


#=============================================

# Functions to read/write bytes


def readBytes(file):
    with open(file, 'rb') as f:
        b = bytearray(f.read())
    return b

def writeBytes(bytes_, file):
    with open(file, 'wb') as f:
        f.write(bytes_)
    return


#===========================================
# The testing function called from tests.py

def testFunction(in_file, enc_file):
    """
    This function performs a test operation
    by first Hiding then Finding the file
    to encode. Used to ascertain if the
    output is usable
    """
    in_bytes, out_file_name = fileHide(in_file, enc_file, filebytes=True)
    out_bytes = fileFind(out_file_name, filebytes=True)
    
    print('Files are equal ', in_bytes==out_bytes)
    return

#=========================================

# User interface

    

def welcome():
    print('-'*40)
    print('Welcome to pyEncrypt')
    print('-'*40)
    print('Do you wish to [h]ide or [f]ind a file? ')
    choice = str(input('> '))
    if choice == 'h':
        hChoice()
        
    elif choice == 'f':
        dChoice()
        
    else:
        print("f or h must be given")
    
    return
 
#===============================================

# processing user input

def hChoice():
    print("Enter filename to hide")
    file_to_enc=str(input("> "))
    print("Enter filename to hide the file in")
    f_to_enc_in = str(input("> "))
    out_file_name = fileHide(file_to_enc, f_to_enc_in)
    
    
    print("Do you wish to delete the original file? [y]es | [n]o")
    del_choice = str(input("> "))
    if del_choice == 'y':
        warning(file_to_enc)
      
    print(out_file_name, " has been created")
    return



def dChoice():
    print("Enter filename of file to decode")
    enc_file = str(input("> "))
    filename = fileFind(enc_file)
    print("Do you wish to delete the original file? [y]es | [n]o")
    del_choice = str(input("> "))
    if del_choice == 'y':
        warning(enc_file)
    
    print(filename, " has been created")
    return 
    

def warning(filename):
    
    print("Warning: File will be lost if encoding/decoding fails")
    print("Do you wish to proceed? [y]es | [n]o")
    confirm = str(input("> "))
    if confirm == 'y':
        import os
        print(filename, " removed.")
        os.remove(filename)
        
    else:
        print("File not deleted")
    
    return
    

#==============================================

if __name__ == '__main__':
    welcome()
    
    
        
        
#==============================================
# Scratchpad:


#   
#   1: integrate checkExists 



#   2: When encoded, extract, run a test
#   : if file is okay, delete original file
#   : if not raise an error



        
#   3: look at embedding file over a many 
#     different ranges
     
#   4:  look at using an encryption of the 
#     image_bytes before inserting into the 
#     mp3_bytes

#   5:  Investigate why pdfs fail and 
#        find an avenue to support them
#        (it may just need a larger file)
     
#===============================================           

