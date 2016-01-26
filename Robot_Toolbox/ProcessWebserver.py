# -*- coding: utf-8 -*-
###############################################################################
# Class Prozess webserver
# Version:  2016.01.26
#
###############################################################################
import tornado.ioloop
import tornado.web



class ProcessWebserver:

    def Run(self, WLQueue, WPQueue, MQueue, LQueue, PQueue):

        class MainHandler(tornado.web.RequestHandler):

            def get(self):
                self.write("Tornado webserver is running!")

        class StoryHandler1(tornado.web.RequestHandler):
            def initialize(self, db):
                self.LQueue = db[0]
                self.WLQueue = db[1]

                # read template
                self.template = open("templates/Robbi.html", "r")
                self.site = self.template.read()
                self.template.close()

            def get(self, Robbi_id):
                # the site requests data in a cycle of 1s
                # check argument from site
                if Robbi_id == "1":
                    self.LQueue.put(["Q@", ""])
                elif Robbi_id == "2":
                    self.LQueue.put(["P@", "bwd"])
                elif Robbi_id == "3":
                    self.LQueue.put(["P@", "fwd"])
                elif Robbi_id == "4":
                    self.LQueue.put(["P@", "ft"])
                elif Robbi_id == "5":
                    self.LQueue.put(["P@", "lt"])

                # get actual alarm list page
                # ask LQueue for data
                self.LQueue.put(["R@", ""])

                # read WLQueue
                message = WLQueue.get()

                # put data to head table
                self.siteCopy = self.site.replace("?actual", message[0][0])
                self.siteCopy = self.siteCopy.replace("?last", message[0][1])

                # put data to main table
                for i in range(1, len(message)):
                    row = message[i]
                    for j in range(0, len(row)):
                        self.siteCopy = self.siteCopy.replace('title="' + str(i) + "." + str(j + 1) + '">' + '&nbsp;',
                                                              'title="' + str(i) + "." + str(j + 1) + '">' + row[j])

                # write to page
                self.write(self.siteCopy)

        class StoryHandler2(tornado.web.RequestHandler):

            def get(self, filename):
                # deliver files to page
                # read file
                self.file = open("static/" + filename, "r")
                self.script = self.file.read()
                self.file.close()
                # write to page
                if filename.endswith(".css"):
                    self.set_header("Content-Type", "text/css")
                elif filename.endswith(".js"):
                   self.set_header("Content-Type", "text/javascript")
                self.write(self.script)

        def make_app():
            return tornado.web.Application([
                (r"/", MainHandler),
                (r"/Robbi/([0-5]+)", StoryHandler1, dict(db=[LQueue, WLQueue])),
                (r"/static/(.*)", StoryHandler2)
            ])

        app = make_app()
        app.listen(8080)
        tornado.ioloop.IOLoop.current().start()