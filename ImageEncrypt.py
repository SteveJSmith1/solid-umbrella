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

def imageHide(im_file, mp3_file, output_file):
    # creating bytearrays
    image_bytes = readBytes(im_file)
    mp3_bytes = readBytes(mp3_file)
    # encoding image byte length info into mp3_bytes
    len_im_bytes = int(len(image_bytes))
    len_im_as_bytes = len_im_bytes.to_bytes(10, byteorder='big')
    mp3_bytes[1000:1010] = len_im_as_bytes
    # encoding image information
    halfway = int(len(mp3_bytes)/2)
    mp3_bytes[halfway:halfway+len_im_bytes] = image_bytes
    # writing mp3
    writeBytes(mp3_bytes, output_file)
    return



def imageFind(mp3_file, output_file):
    # fetching bytes
    mp3_bytes = readBytes(mp3_file)
    # extracting info about image length
    im_file_len = int.from_bytes(mp3_bytes[1000:1010], byteorder='big')
    # extracting image bytes
    halfway = int(len(mp3_bytes)/2)
    im_bytes = mp3_bytes[halfway:halfway + im_file_len]
    # write jpg
    writeBytes(im_bytes, output_file)
    return

def testFunction(in_file, enc_file, out_enc, out_file):
    """
    This function performs a test operation
    by first Hiding then Finding the file
    to encode. Used to ascertain if the
    output is usable
    """
    imageHide(in_file, enc_file, out_enc)
    imageFind(out_enc, out_file)
    # add functionality to check if the
    # found file is the same as the hidden file
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