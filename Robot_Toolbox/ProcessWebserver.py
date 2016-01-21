# -*- coding: utf-8 -*-
###############################################################################
# Class Prozess webserver
# Version:  2016.01.21
#
###############################################################################
import tornado.ioloop
import tornado.web


class ProcessWebserver:

    def Run(self, WLQueue, WPQueue, MQueue, LQueue, PQueue):

        class MainHandler(tornado.web.RequestHandler):

            def initialize(self, db):
                self.MQueue = db

            def get(self):
                self.write("Tornado webserver is running!")
                self.MQueue.put("I@Main Handler was executed")

        db3 = []  # map

        class StoryHandler1(tornado.web.RequestHandler):

            def initialize(self, db):
                self.PQueue = db[0]
                self.WLQueue = db[1]
                self.status = []
                self.measuredValue = []

            def get(self):
                self.write("This is story: Status and measured values")
                # the site requests data in a cycle of 500 ms
                # get actual status and mesured value
                # ask PQueue for data
                self.PQueue.put(["R@", ""])

                # read WPQueue
                for i in range(0, 2):
                    message = WPQueue.get()
                    if message[0] == "S@":
                        self.status = message[1]
                    if message[0] == "MV@":
                        self.measuredValue = message[1]

                # write to page

        class StoryHandler2(tornado.web.RequestHandler):
            def initialize(self, db):
                self.LQueue = db[0]
                self.WLQueue = db[1]
                self.actualPageNo = "0"
                self.maxPageNo = "0"
                self.numberOFLines = "0"
                self.actualPage = []

            def get(self):
                self.write("This is story: Alarm list")
                # the site requests data in a cycle of 1s
                # get actual alarm list page
                # ask LQueue for data
                self.LQueue.put(["R@", ""])

                # read WLQueue

                message = WLQueue.get()
                # read header
                self.actualPageNo = message[0][0]
                self.maxPageNo = message[0][1]
                self.numberOfLines = message[0][2]
                # remove header
                del message[0]
                # store list
                self.actualPage = message

                # write to page
                self.write("Page number: " + self.actualPageNo +
                            "Maximal page number: " + self.maxPageNo +
                            "Number of lines: " + self.numberOfLines)


        class StoryHandler3(tornado.web.RequestHandler):
            def initialize(self, db):
                self.db = db

            def get(self):
                self.write("This is story: Map")
                # the site requests data in a cycle of 1s
                # get actual map

                # write to page

        def make_app():
            return tornado.web.Application([
                (r"/", MainHandler, dict(db=MQueue)),
                (r"/story/1", StoryHandler1, dict(db=[PQueue, WPQueue])),
                (r"/story/2", StoryHandler2, dict(db=[LQueue, WLQueue])),
                (r"/story/3", StoryHandler3, dict(db=db3))
            ])

        app = make_app()
        app.listen(8080)
        tornado.ioloop.IOLoop.current().start()