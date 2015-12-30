# -*- coding: utf-8 -*-
###############################################################################
# Class Audio process
# Version:  2015.12.30
###############################################################################
import pyglet


class Audioprocess:

    def __str__(self):
        nachricht = "Audio process"
        return nachricht

    def Audiorun(self, MQueue, AQueue):

        # get order from AQueue(block by default)
        # structure:
        # [type, no, stAlert, stCg, status , cTextNo]
        while True:
            Audio = AQueue.get()

            # play pieep (0)
            url = "data/CG/0.mp3"
            clip = pyglet.resource.media(url)
            clip.play()
            pyglet.app.run

            if Audio[0] == "MV":
                # play description text for measured value according to no
                url = "data/MV/" + str(Audio[1]) + ".mp3"
                clip = pyglet.resource.media(url)
                clip.play()
                pyglet.app.run

                if Audio[4] == 1:
                    # play comming text according to status == 1 and cTextNo
                    url = "data/CG/" + str(Audio[5]) + ".mp3"
                else:
                    # play going text (4) according to status == 0
                    url = "data/CG/4.mp3"
                clip = pyglet.resource.media(url)
                clip.play()
                pyglet.app.run

            elif Audio[0] == "ST":
                # play description text for status according to no
                url = "data/ST/" + str(Audio[1]) + ".mp3"
                clip = pyglet.resource.media(url)
                clip.play()
                pyglet.app.run

                if Audio[3] is True:
                    if Audio[4] == 1:
                        # play comming text (3) according to status == 1
                        url = "data/ST/3.mp3"
                    else:
                        # play going text (4) according to status == 0
                        url = "data/ST/4.mp3"
                    clip = pyglet.resource.media(url)
                    clip.play()
                    pyglet.app.run
        # never executed
        return










