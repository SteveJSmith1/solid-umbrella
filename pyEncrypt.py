#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 16:16:05 2017

@author: steveJSmith1

This function 'hides' one file inside another
and is also able to 'find' it again.

V1.0

to hide a file:
    
    fileHide(
            file to encode, 
            file to use for encoding in, 
            )
    
to find a file hidden using the above function

    fileFind(
            filename of encoded file
            )
"""



#=============================================

# The main functions to call when running

def fileHide(file_to_enc, f_to_enc_in):
    """
    to hide a file:
    
    fileHide(
            file to encode, 
            file to use for encoding in)
    
    
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
    
    enc_check = encodeCheck(file_to_enc_b, out_file_name)
    # returning bytes for equality check in
    # testFunction()
    if enc_check==True:
        print("Encoding check: pass")
        return out_file_name
    else:
        print("Encoding check: Fail")
        return out_file_name


def fileFind(enc_file):
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
   
    return filename

#===============================================

# Bytes processing functions


def splitBytes(file_to_encode_bytes):
    b = file_to_encode_bytes
    num_of_regions = len(b) % 10 
    region_length = int(len(b)/num_of_regions)
    split_bytes = [b[i*region_length:(i+1)*region_length] for i in range(num_of_regions - 1)]
    split_bytes.append(b[(num_of_regions - 1)*region_length:len(b)])
    
    
    return split_bytes


def splitBytesInfo(split_bytes):
    length_of_list = len(split_bytes)
    len_list_as_bytes = length_of_list.to_bytes(10, byteorder='big')
    
    len_elements = (len(split_bytes[0])).to_bytes(10, byteorder='big')
    
    len_last_element = (len(split_bytes[-1])).to_bytes(10, byteorder='big')
    
    return len_list_as_bytes, len_elements, len_last_element


def byteArrayInfo(split_bytes, f_to_enc_in_b):
    start = 5000
    end = int(len(f_to_enc_in_b)-5000)
    len_split = int((end - start) / len(split_bytes))
    len_split_bytes = len_split.to_bytes(10, byteorder='big')
    return len_split, len_split_bytes


def fetchInfo(enc_bytes):
    
    # extracting encoded filename
    name_array = enc_bytes[2000:2350]
    # converting bytes to string of filename
    filename = 'D-' + bytesToFilename(name_array)
    
    # extracting number of encoding regions
    number_of_regions = int.from_bytes(enc_bytes[4000:4010], byteorder='big')
    # fetching length of elements
    elem_len = int.from_bytes(enc_bytes[4100:4110], byteorder='big')
    # fetching the length of last element
    last_elem_len = int.from_bytes(enc_bytes[4200:4210], byteorder='big')
    # fetching the length of each split region
    region_len = int.from_bytes(enc_bytes[4300:4310], byteorder='big')
    
    return filename, number_of_regions, elem_len, last_elem_len, region_len
    

#===========================================
# Encoding/Decoding functions

def encodeBytes(file_to_enc, f_to_enc_in_b, file_to_enc_b):
    
    split_bytes = splitBytes(file_to_enc_b)
    
    
    # fetching the array containing the filename   
    name_array = filenameToBytes(file_to_enc)
    # overwriting bytes with filename
    f_to_enc_in_b[2000:2350] = name_array
    # fetching split_bytes information as bytes
    llab, le, lle = splitBytesInfo(split_bytes)
    # encoding length of list
    f_to_enc_in_b[4000:4010] = llab
    # emcding the length of an element
    f_to_enc_in_b[4100:4110] = le
    # encoding the length of last element
    f_to_enc_in_b[4200:4210] = lle
                 
    
    # find length of bytes allocated for each
    # bytearray in the list
    ls, lsb = byteArrayInfo(split_bytes, f_to_enc_in_b)
    f_to_enc_in_b[4300:4310] = lsb
                 
    # encoding each bytearray element 
    for i in range(len(split_bytes)):
        f_to_enc_in_b[5000+i*ls:5000+i*ls+len(split_bytes[i])] = split_bytes[i]
                
    return f_to_enc_in_b


def decodeBytes(enc_bytes):
    
    filename, nor, el, lel, rl = fetchInfo(enc_bytes)
    
    #fetching data
    orig = []
    for i in range(nor - 1):
        orig.append(enc_bytes[5000+i*rl:5000+i*rl+el])
    #last one
    orig.append(enc_bytes[5000+(nor-1)*rl:5000+(nor-1)*rl+lel])
        
    out_file_bytes = bytearray(b''.join(orig))
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
# Post-processiong checks

def encodeCheck(in_bytes, encoded_file):
    
    read_bytes = readBytes(encoded_file)
    bytes_to_check, _ = decodeBytes(read_bytes)
    if in_bytes == bytes_to_check:
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

#=========================================

# User interface

    

def welcome():
    import time
    print('-'*40)
    print('Welcome to pyEncrypt')
    print('-'*40)
    print('Do you wish to [h]ide or [f]ind a file? ')
    time.sleep(0.1)
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
# Scratchpad:


#   4:  look at using an encryption of the 
#     image_bytes before inserting into the 
#     mp3_bytes

    
#===============================================           
#==============================================

if __name__ == '__main__':
    welcome()
    
 
