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


"""
scratchpad
to do:
     Test if this will work with wav files
     and rename mp3_bytes to audio_bytes if it does
     
     Test if this will work with video files
     and rename mp3_bytes/audio_bytes to media 
     bytes if it does
     
     write logical tests to ensure the length of
     the image_bytes is less than the mp3_bytes
     
     encode the filetype as bytes and insert
     into the audio file and append filetpye
     to output filename
     
     look at embedding file over a many different
     ranges
     
     look at using an encryption of the 
     image_bytes before inserting into the 
     mp3_bytes
     
"""            
   
"""
tests:
"""

def test_jpg_to_mp3_hide_and_back(im_file, mp3_file, mp3_out, im_out):
    imageHide(im_file, mp3_file, mp3_out)
    imageFind(mp3_out, im_out)
    return

"""
test 1 - jpg and mp3 hide and find from resulting
            file
"""
im_file = '/home/steve/Pictures/20160616_163313.jpg'
mp3_file = 'The Divine Comedy - To The Rescue..mp3'
mp3_out = 'Test.mp3'
im_out = 'Test.jpg'

test_jpg_to_mp3_hide_and_back(im_file, mp3_file, mp3_out, im_out)


"""
pass
"""

"""
test 2 - a different jpg and mp3 hide and find
         from resulting file
"""

test_jpg_to_mp3_hide_and_back('second.jpg', '03.Tripping Out.mp3', 'test.mp3', 'test.jpg')

"""
fail

 - test.mp3 created
 - test.jpg created but not recognised as a jpg
"""


