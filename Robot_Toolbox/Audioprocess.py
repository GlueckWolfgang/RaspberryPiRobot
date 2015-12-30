# -*- coding: utf-8 -*-
###############################################################################
# Class Audio process
# Version:  2015.12.30
# MQueue    Could be used for fault messages (related status must exist)
# AQueue    order queue for audio output, structure see below
###############################################################################
import pyglet
import time

class Audioprocess:

    def __str__(self):
        nachricht = "Audio process"
        return nachricht

    def Audiorun(self, MQueue, AQueue):
        # configuration of a player
        player = pyglet.media.Player()

        # get order from AQueue(block by default)
        # structure:
        # [type, no, stAlert, stCg, status , cTextNo]
        while True:
            Audio = AQueue.get()

            # play pieep (0)
            url = "data/CG/0.mp3"
            clip0 = pyglet.media.load(url, streaming = False)
            player.queue(clip0)

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
                time.sleep(4)  # pause between 2 messages

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
                time.sleep(4)  # pause between 2 messages
        # never executed
        return
