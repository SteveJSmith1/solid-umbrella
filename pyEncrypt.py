#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 16:16:05 2017

@author: steveJsmith1
"""

def readBytes(file):
    with open(file, 'rb') as f:
        b = bytearray(f.read())
    return b

def writeBytes(bytes_, file):
    with open(file, 'wb') as f:
        f.write(bytes_)
    return



def fileHide(file_to_enc, f_to_enc_in, output_file):
    # creating bytearrays
    file_to_enc_b = readBytes(file_to_enc)
    f_to_enc_in_b = readBytes(f_to_enc_in)
    # encoding file byte length info into   
    # file to encode in
    len_f_t_e_b = int(len(file_to_enc_b))
    len_f_as_bytes = len_f_t_e_b.to_bytes(10, byteorder='big')
    f_to_enc_in_b[1000:1010] = len_f_as_bytes
    # encoding image information
    halfway = int(len(f_to_enc_in_b)/2)
    f_to_enc_in_b[halfway:halfway+len_f_t_e_b] = file_to_enc_b
    # writing output file
    writeBytes(f_to_enc_in_b, output_file)
    return


def fileFind(enc_file, out_file):
    # fetching bytes from encoded file
    enc_bytes = readBytes(enc_file)
    # extracting encded
    # info about file length in bytes
    out_file_len = int.from_bytes(enc_bytes[1000:1010], byteorder='big')
    # extracting encoded out_file bytes
    halfway = int(len(enc_bytes)/2)
    
    out_file_bytes = enc_bytes[halfway:halfway + out_file_len]
    # write jpg
    writeBytes(out_file_bytes, out_file)
    return

def testFunction(in_file, enc_file, out_enc, out_file):
    """
    This function performs a test operation
    by first Hiding then Finding the file
    to encode. Used to ascertain if the
    output is usable
    """
    fileHide(in_file, enc_file, out_enc)
    fileFind(out_enc, out_file)
    # add functionality to check if the
    # found file is the same as the hidden file
    return
 
 
def checkEquality():
    return

#     2c: try and break it by encoding a video
#         into an audio file

#     3: write logical tests to ensure the length 
#     of the image_bytes is less than the mp3_bytes
     
#     4: encode the filetype as bytes and insert
#     into the audio file and append filetpye
#     to output filename
     
#     5: look at embedding file over a many 
#     different ranges
     
#     6: look at using an encryption of the 
#     image_bytes before inserting into the 
#     mp3_bytes

#     7: Investigate why pdfs fail and 
#        find an avenue to support them
     
#===============================================           