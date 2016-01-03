# -*- coding: utf-8 -*-
###############################################################################
# Class Audio process
# Version:  2016.01.03
# MQueue    Can be used for fault messages
#           (related status must exist for M@ or I@anyString can be sent)
# AQueue    order queue for audio output, structure see below
###############################################################################
import pyglet


class Audioprocess:

    def __str__(self):
        nachricht = "Audio process"
        return nachricht

    def Audiorun(self, MQueue, AQueue):

        def play_next(*args):
            if not AQueue.empty():
                # get order from AQueue
                # structure:
                # [type, no, stAlert, stCg, status , cTextNo]
                Audio = AQueue.get()
                # play pieep (0)
                player.queue(clip0)

                if Audio[0] == "MV":
                    # play description text for measured value according to no
                    url = "data/MV/" + Audio[1] + ".mp3"
                    MQueue.put("I@Clip1URL: " + url)
                    clip1 = pyglet.media.load(url, streaming=False)
                    player.queue(clip1)

                    if  int(Audio[4]) == 1:
                        # play comming text according to status == 1 and cTextNo
                        url = "data/CG/" + Audio[5] + ".mp3"

                    else:
                        # play going text (4) according to status == 0
                        url = "data/CG/4.mp3"
                    MQueue.put("I@Clip2URL: " + url)
                    clip2 = pyglet.media.load(url, streaming=False)
                    player.queue(clip2)

                elif Audio[0] == "ST":
                    # play description text for status according to no
                    url = "data/ST/" + Audio[1] + ".mp3"
                    MQueue.put("I@Clip1URL: " + url)
                    clip1 = pyglet.media.load(url, streaming=False)
                    player.queue(clip1)

                    # check if status has Cg character
                    if Audio[3] is True:
                        if int(Audio[4]) == 1:
                            # play comming text (3) according to status == 1
                            url = "data/CG/3.mp3"
                        else:
                            # play going text (4) according to status == 0
                            url = "data/CG/5.mp3"

                        MQueue.put("I@Clip2URL: " + url)
                        clip2 = pyglet.media.load(url, streaming=False)
                        player.queue(clip2)

            if not player.playing:
                player.play()
            return

        # configuration of a player
        player = pyglet.media.Player()

        # Play peep after startup
        url = "data/CG/0.mp3"
        clip0 = pyglet.media.load(url, streaming=False)
        player.queue(clip0)
        player.play()

        # call pyglet process and timer
        pyglet.clock.schedule_interval(play_next, 1.0)
        pyglet.app.run()  # returns only over timer
