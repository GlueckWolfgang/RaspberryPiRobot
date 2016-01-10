# -*- coding: utf-8 -*-
###############################################################################
# Class Process Audio
# Version:  2016.01.09
# CQueue    for sending commands like amplifier on/off
# MQueue    Can be used for status messages
#           (I@anyString can be sent)
# AQueue    order queue for audio output, structure see below
# Amplifier will be switched on and off by energy saving reason, it takes 500 mA
###############################################################################
from Robot_Toolbox.Audio import *
import pyglet


class ProcessAudio:

    def __str__(self):
        nachricht = "Audio process"
        return nachricht

    def Run(self, MQueue, AQueue, CQueue, CommandList):
        global amplifier
        amplifier = False

        def play_next(*args):
            global amplifier

            if not AQueue.empty():
                # switch on amplifier
                if amplifier is False:
                    CQueue.put(CommandList.sendCommandByNumber(13, "1"))
                    amplifier = True

                # get order from AQueue
                Audio = AQueue.get()
                # play pieep (0)
                url = "data/CG/0.mp3"
                clip0 = pyglet.media.load(url, streaming=False)
                player.queue(clip0)

                # MQueue.put("I@" + Audio.aType + " " + Audio.aNumber + " "
                #       + str(Audio.aCG) + " " + Audio.aValue + " " + Audio.aCAudioNo)

                if Audio.aType == "MV":
                    # play description text for measured value according to no
                    url = "data/MV/" + Audio.aNumber+ ".mp3"
                    # MQueue.put("I@Clip1URL: " + url)
                    clip1 = pyglet.media.load(url, streaming=False)
                    player.queue(clip1)

                    if  Audio.aValue == "1":
                        # play comming text according to status == 1 and cTextNo
                        url = "data/CG/" + Audio.aCAudioNo + ".mp3"

                    else:
                        # play going text (4) according to status == 0
                        url = "data/CG/4.mp3"
                    # MQueue.put("I@Clip2URL: " + url)
                    clip2 = pyglet.media.load(url, streaming=False)
                    player.queue(clip2)

                elif Audio.aType == "ST":
                    # play description text for status according to no
                    url = "data/ST/" + Audio.aNumber + ".mp3"
                    # MQueue.put("I@Clip1URL: " + url)
                    clip1 = pyglet.media.load(url, streaming=False)
                    player.queue(clip1)

                    # check if status has Cg character
                    if Audio.aCG is True:
                        if Audio.aValue == "1":
                            # play comming text (3) according to status == 1
                            url = "data/CG/3.mp3"
                        else:
                            # play going text (4) according to status == 0
                            url = "data/CG/5.mp3"

                        # MQueue.put("I@Clip2URL: " + url)
                        clip2 = pyglet.media.load(url, streaming=False)
                        player.queue(clip2)
                else:
                    # peep only, just for understanding
                    pass
                if not player.playing:
                    player.play()

            if not player.playing\
            and amplifier is True:
                # switch off amplifier and save energy
                CQueue.put(CommandList.sendCommandByNumber(13, "0"))
                amplifier = False

            return

        # configuration of a player
        player = pyglet.media.Player()
        # play peep after startup
        AQueue.put(Audio("Peep only", "0", True, "1", "0"))

        # call pyglet process and timer
        pyglet.clock.schedule_interval(play_next, 1.0)
        pyglet.app.run()  # returns only over timer
