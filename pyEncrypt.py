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

def readBytes(file):
    with open(file, 'rb') as f:
        b = bytearray(f.read())
    return b

def writeBytes(bytes_, file):
    with open(file, 'wb') as f:
        f.write(bytes_)
    return



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
          
    # encoding the filename into the file   
    name_array = filenameToBytes(file_to_enc)
    f_to_enc_in_b[2000:2350] = name_array
    
    # encoding file byte length info into   
    # file to encode in
    len_f_t_e_b = int(len(file_to_enc_b))
    len_f_as_bytes = len_f_t_e_b.to_bytes(10, byteorder='big')
    f_to_enc_in_b[1000:1010] = len_f_as_bytes
    # encoding file contents at the halfway point
    halfway = int(len(f_to_enc_in_b)/2)
    f_to_enc_in_b[halfway:halfway+len_f_t_e_b] = file_to_enc_b
    # writing output file
    out_file_name = 'H-' + f_to_enc_in
    writeBytes(f_to_enc_in_b, out_file_name)
    
    # returning bytes for equality check in
    # testFunction()
    if filebytes==True:
        return file_to_enc_b, out_file_name
    else:
        return



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
    # extracting encded
    # info about file length in bytes
    out_file_len = int.from_bytes(enc_bytes[1000:1010], byteorder='big')
    # extracting encoded filename
    name_array = enc_bytes[2000:2350]
    # converting bytes to string of filename
    filename = bytesToFilename(name_array)
    # extracting encoded out_file bytes
    halfway = int(len(enc_bytes)/2)
    
    out_file_bytes = enc_bytes[halfway:halfway + out_file_len]
    # write jpg
    writeBytes(out_file_bytes, filename)
    #returning bytes for equality test in 
    # testFunction()
    if filebytes==True:
        return out_file_bytes
    else:
        return


#     3: write logical tests to ensure the length 
#     of the image_bytes is less than the mp3_bytes

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

     
#     4: encode the filetype as bytes and insert
#     into the audio file and append filetpye
#     to output filename

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


#     5: look at embedding file over a many 
#     different ranges
     
#     6: look at using an encryption of the 
#     image_bytes before inserting into the 
#     mp3_bytes

#     7: Investigate why pdfs fail and 
#        find an avenue to support them
     
#===============================================           