#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  3 15:56:51 2025

@author: tijn
"""

# from pydub import AudioSegment
# from pydub.playback import play
# import random

# #importeer alle letters
# a = AudioSegment.from_mp3("a.mp3")
# b = AudioSegment.from_mp3("b.mp3")
# c = AudioSegment.from_mp3("c.mp3")
# d = AudioSegment.from_mp3("d.mp3")
# e = AudioSegment.from_mp3("e.mp3")
# f = AudioSegment.from_mp3("f.mp3")
# g = AudioSegment.from_mp3("g.mp3")
# h = AudioSegment.from_mp3("h.mp3")
# i = AudioSegment.from_mp3("i.mp3")
# j = AudioSegment.from_mp3("j.mp3")
# k = AudioSegment.from_mp3("k.mp3")
# l = AudioSegment.from_mp3("l.mp3")
# m = AudioSegment.from_mp3("m.mp3")
# n = AudioSegment.from_mp3("n.mp3")
# o = AudioSegment.from_mp3("o.mp3")
# p = AudioSegment.from_mp3("p.mp3")
# q = AudioSegment.from_mp3("q.mp3")
# r = AudioSegment.from_mp3("r.mp3")
# s = AudioSegment.from_mp3("s.mp3")
# t = AudioSegment.from_mp3("t.mp3")
# u = AudioSegment.from_mp3("u.mp3")
# v = AudioSegment.from_mp3("v.mp3")
# w = AudioSegment.from_mp3("w.mp3")
# x = AudioSegment.from_mp3("x.mp3")
# y = AudioSegment.from_mp3("y.mp3")
# z = AudioSegment.from_mp3("z.mp3")

# alfabet = [q,w,e,r,t,y,u,i,o,p,a,s,d,f,g,h,j,k,l,z,x,c,v,b,n,m]
# for x in range(500):
#     nr = random.randint(0, 25)
#     play(alfabet[nr])
    
    
import pygame
import random
import time
import os 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

pygame.mixer.init()

letters = [
    "a.mp3","b.mp3","c.mp3","d.mp3","e.mp3","f.mp3","g.mp3",
    "h.mp3","i.mp3","j.mp3","k.mp3","l.mp3","m.mp3","n.mp3",
    "o.mp3","p.mp3","q.mp3","r.mp3","s.mp3","t.mp3","u.mp3",
    "v.mp3","w.mp3","x.mp3","y.mp3","z.mp3"
]

for _ in range(500):
    sound = pygame.mixer.Sound(
    os.path.join(BASE_DIR, random.choice(letters))
)
    sound.play()
    time.sleep(sound.get_length())