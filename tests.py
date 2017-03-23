#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 11:40:16 2017

@author: steve
"""

from pyEncrypt import testFunction

#=============================================

## Testing

#==============================================

def passingTests():
    # test 1 - jpg and mp3 
    testFunction('test.jpg', 'test.mp3', 'out1.mp3', 'out1.jpg')
    # Test 2 -  jpg and wav
    testFunction('test.jpg', 'test.wav', 'out2.wav', 'out2.jpg')
    # test 3 - jpg and mp4
    testFunction('test.jpg', 'test.mp4', 'out3.mp4', 'out3.jpg')
    # test 4 - txt to mp3
    testFunction('test.txt', 'test.mp3', 'out4.mp3', 'out4.txt') 
    # test 5 -  doc to mp3
    testFunction('test.doc', 'test.mp3', 'out5.mp3', 'out5.doc') 
    # test 7 - doc to mp4
    testFunction('test.doc', 'test.mp4', 'out7.mp4', 'out7.doc') 
    # test 8 - pdf to mp4
    testFunction('test.pdf', 'test.mp4', 'out8.mp4', 'out8.pdf') 
    # test 9 - mp3 to mp4
    testFunction('test.mp3', 'test.mp4', 'out9.mp4', 'out9.mp3') 
    
    return


def failingTests():
    #==================================
    # Expected fails
    # Both fail as the output file is not encoded
    # due to the bytearray size check
    
    # test 6 - pdf to mp3
    testFunction('test.pdf', 'test.mp3', 'out6.mp3', 'out6.pdf') 
    # test 10 - mp4 to mp3
    testFunction('test.mp4', 'test.mp3', 'out10.mp3', 'out10.mp4')
    #===================================
    
    return


# passingTests()

"""
test.jpg  equals  out1.jpg True
test.jpg  equals  out2.jpg True
test.jpg  equals  out3.jpg True
test.txt  equals  out4.txt True
test.doc  equals  out5.doc True
test.doc  equals  out7.doc True
test.pdf  equals  out8.pdf True
test.mp3  equals  out9.mp3 True
"""
# failingTests()
"""

    WARNING: Size of file to encode in is too 
    small, file not hidden.
    Suggest using a larger file;
        try a .wav, .mp4 instead of an .mp3 perhaps
"""
from pyEncrypt import filenameToBytes, bytesToFilename


filename = "testing_with_a_lengthy_string_of_many_characters_for_a_test_to_see_what_sort_of_size_the_bytearray_may_need_to_be_to_cover_strings_of_this_length.wav"

filename_bytes = filenameToBytes(filename)
dec_filename = bytesToFilename(filename_bytes)
if filename == dec_filename:
    print("Extracted encoded filename successfully")
    
