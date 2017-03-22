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


 
 
#=============================================

## Testing

#==============================================

# test 1 - jpg and mp3 hide and find from resulting file

def test_jpg_to_mp3_hide_and_back(im_file, mp3_file, mp3_out, im_out):
    imageHide(im_file, mp3_file, mp3_out)
    imageFind(mp3_out, im_out)
    return

            
# Notes:
    # There is an audible period of silence and
    # missing "words" in the output file, this
    # may be corrected by (5) in the to-do list

im_file = '/home/steve/Pictures/20160616_163313.jpg'
mp3_file = 'The Divine Comedy - To The Rescue..mp3'
mp3_out = 'Test.mp3'
im_out = 'Test.jpg'

test_jpg_to_mp3_hide_and_back(im_file, mp3_file, mp3_out, im_out)

test_jpg_to_mp3_hide_and_back('third.jpg', 'third.mp3', 'test.mp3', 'test.jpg')

"""passes"""
  


#===============================================
# scratchpad
# to do:
#     1: Test if this will work with wav files
#     and rename mp3_bytes to audio_bytes if it does

def test_jpg_to_wav_hide_and_back(im_file, wav_file, wav_out, im_out):
    imageHide(im_file, wav_file, wav_out)
    imageFind(wav_out, im_out)
    return

test_jpg_to_wav_hide_and_back('test.jpg', 'test.wav', 'out.jpg', 'out.wav')
 
#     2: Test if this will work with video files
#     and rename mp3_bytes/audio_bytes to media 
#     bytes if it does
     
#     3: write logical tests to ensure the length 
#     of the image_bytes is less than the mp3_bytes
     
#     4: encode the filetype as bytes and insert
#     into the audio file and append filetpye
#     to output filename
     
#     5: look at embedding file over a many 
#     different ranges
     
#     look at using an encryption of the 
#     image_bytes before inserting into the 
#     mp3_bytes
     
#===============================================           