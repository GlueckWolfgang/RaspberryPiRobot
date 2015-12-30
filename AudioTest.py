# -*- coding: utf-8 -*-
###############################################################################
# Audio test
# Version:  2015.12.30
# MQueue    Could be used for fault messages (related status must exist)
# AQueue    order queue for audio output, structure see below
###############################################################################
import pyglet

# configuration of a player
player = pyglet.media.Player()



# play pieep (0)
url = "data/CG/0.mp3"
clip0 = pyglet.media.load(url, streaming = False)
player.queue(clip0)

Audio = ["ST", str(2),
              True,
              True,
              str(0),
              "0"]

if Audio[0] == "MV":
    # play description text for measured value according to no
    url = "data/MV/" + int(Audio[1]) + ".mp3"
    clip1 = pyglet.media.load(url, streaming = False)
    player.queue(clip1)


    if int(Audio[4]) == 1:
        # play comming text according to status == 1 and cTextNo
        url = "data/CG/" + int(Audio[5]) + ".mp3"
    else:
        # play going text (4) according to status == 0
        url = "data/CG/4.mp3"
    clip2 = pyglet.media.load(url, streaming = False)
    player.queue(clip2)
    player.play()


elif Audio[0] == "ST":
    # play description text for status according to no
    url = "data/ST/" + Audio[1] + ".mp3"
    clip1 = pyglet.media.load(url, streaming = False)
    player.queue(clip1)

    # check if status has Cg character
    if Audio[3] is True:
        if int(Audio[4]) == 1:
            # play comming text (3) according to status == 1
            url = "data/CG/3.mp3"
        else:
            # play going text (4) according to status == 0
            url = "data/CG/5.mp3"
        clip2 = pyglet.media.load(url, streaming = False)
        player.queue(clip2)
        player.play()