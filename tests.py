#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 11:40:16 2017

@author: steve
"""

from ImageEncrypt import testFunction

#=============================================

## Testing

#==============================================

# test 1 - jpg and mp3 

testFunction('test.jpg', 'test.mp3', 'out1.mp3', 'out1.jpg')

# pass            
# Notes:
    # There is an audible period of silence and
    # missing "words" in the output file, this
    # may be corrected by (5) in the to-do list
    # in ImageEncrypt.py

# Test 2 -  jpg and wav

testFunction('test.jpg', 'test.wav', 'out2.wav', 'out2.jpg')

# pass
# Notes:
    # puts "encoded noise" into the wav

# test 3 - jpg and mp4

testFunction('test.jpg', 'test.mp4', 'out3.mp4', 'out3.jpg')

# test 4 - txt to mp3
    
testFunction('test.txt', 'test.mp3', 'out4.mp3', 'out4.txt') 

# pass

# test 5 -  doc to mp3

testFunction('test.doc', 'test.mp3', 'out5.mp3', 'out5.doc') 

# pass

# test 6 - pdf to mp3

testFunction('test.pdf', 'test.mp3', 'out6.mp3', 'out6.pdf') 

# fails
# Notes:
    # Breaks both output audio and output pdf
    # are the bytes encoded differently for a pdf?
    # pdf was ~= 1/2 the size of the audio file

# test 7 - doc to mp4

testFunction('test.doc', 'test.mp4', 'out7.mp4', 'out4.doc') 

#pass 

# test 8 - pdf to mp4

testFunction('test.pdf', 'test.mp4', 'out8.mp4', 'out8.pdf') 

# pass
# Notes:
    # large pause then artefacts, but it was large pdf

# test 9 - mp3 to mp4

testFunction('test.mp3', 'test.mp4', 'out9.mp4', 'out9.mp3') 

# pass
# Notes:
    # large pause then artefacts, mp3 approx 0.1*mp4


