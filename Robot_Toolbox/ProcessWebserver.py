# -*- coding: utf-8 -*-
###############################################################################
# Class Prozess webserver
# Version:  2016.01.24
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

            def get(self, Panel_id):
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

                # read template
                self.template = open("templates/Alarmlist.html", "r")
                self.site = self.template.read()
                self.template.close()

            def get(self, Alarmlist_id):
                # the site requests data in a cycle of 1s
                MQueue.put("I@" + Alarmlist_id)
                # check argument from site
                if Alarmlist_id == "1":
                    self.LQueue.put(["Q@", ""])
                elif Alarmlist_id == "2":
                    self.LQueue.put(["P@", "bwd"])
                elif Alarmlist_id == "3":
                    self.LQueue.put(["P@", "fwd"])
                elif Alarmlist_id == "4":
                    self.LQueue.put(["P@", "ft"])
                elif Alarmlist_id == "5":
                    self.LQueue.put(["P@", "lt"])

                # get actual alarm list page
                # ask LQueue for data
                self.LQueue.put(["R@", ""])

                # read WLQueue
                message = WLQueue.get()

                # put data to head table
                self.siteCopy = self.site.replace("?actual", message[0][0])
                self.siteCopy = self.siteCopy.replace("?last", message[0][1])
                del message[0]

                # put data to main table
                for i in range(0, len(message)):
                    row = message[i]
                    for j in range(0, 5):
                        self.siteCopy = self.siteCopy.replace('title="' + str(i + 1) + "." + str(j + 1) + '">' + '&nbsp;',
                                                              'title="' + str(i + 1) + "." + str(j + 1) + '">' + row[j])

                # write to page
                self.write(self.siteCopy)

        class StoryHandler3(tornado.web.RequestHandler):
            def initialize(self, db):
                self.db = db

            def get(self, Map_id):
                self.write("This is story: Map")
                # the site requests data in a cycle of 1s
                # get actual map

                # write to page

        class StoryHandler4(tornado.web.RequestHandler):

            def get(self, filename):
                # deliver js files to page
                MQueue.put("I@" + filename)
                # read js file
                self.file = open("static/" + filename, "r")
                self.script = self.file.read()
                self.file.close()
                # write to page
                self.write(self.script)

        def make_app():
            return tornado.web.Application([
                (r"/", MainHandler, dict(db=MQueue)),
                (r"/Panel/([0-20]+)", StoryHandler1, dict(db=[PQueue, WPQueue])),
                (r"/Alarmlist/([0-5]+)", StoryHandler2, dict(db=[LQueue, WLQueue])),
                (r"/Map/([0-5]+)", StoryHandler3, dict(db=db3)),
                (r"/static/(.*)", StoryHandler4)
            ])

        app = make_app()
        app.listen(8080)
        tornado.ioloop.IOLoop.current().start()