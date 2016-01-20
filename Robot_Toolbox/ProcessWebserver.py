# -*- coding: utf-8 -*-
###############################################################################
# Class Prozess webserver
# Version:  2016.01.20
#
###############################################################################
import tornado.ioloop
import tornado.web


class ProcessWebserver:

    def Run(self, WLQueue,WPQueue, MQueue, LQueue, PQueue):

        class MainHandler(tornado.web.RequestHandler):

            def initialize(self, db):
                self.MQueue = db

            def get(self):
                self.write("Tornado webserver is running!")
                self.MQueue.put("I@Main Handler was executed")

        db1 = []  # control board
#        db2 = []  # alarm list
        db3 = []  # map

        class StoryHandler1(tornado.web.RequestHandler):

            def initialize(self, db):
                self.db = db
                # get initial status and mesured value to db

            def get(self):
                self.write("This is story: Status and measured values")
                # get actual status and mesured value to db
                # ask PQueue for data
                # read WPQueue not blocking
                # write to page

        class StoryHandler2(tornado.web.RequestHandler):
            def initialize(self, db):
                self.LQueue = db[0]
                self.WLQueue = db[1]
                # get initial alarm list page to db
                # ask LQueue for data
                self.LQueue.put(["R@", ""])
                # read WLQueue blocking

            def get(self):
                self.write("This is story: Alarm list")
                # get actual alarm list page to db
                # ask LQueue for data
                self.LQueue.put(["R@", ""])
                # read WLQueue not blocking

                # write to page

        class StoryHandler3(tornado.web.RequestHandler):
            def initialize(self, db):
                self.db = db
                # get initial map to db

            def get(self):
                self.write("This is story: Map")
                # get actual map to db

        def make_app():
            return tornado.web.Application([
                (r"/", MainHandler, dict(db=MQueue)),
                (r"/story/1", StoryHandler1, dict(db=db1)),
                (r"/story/2", StoryHandler2, dict(db=[LQueue, WLQueue])),
                (r"/story/3", StoryHandler3, dict(db=db3))
            ])

        app = make_app()
        app.listen(8080)
        tornado.ioloop.IOLoop.current().start()