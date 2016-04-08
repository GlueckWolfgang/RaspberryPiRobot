# -*- coding: utf-8 -*-
###############################################################################
# Class Prozess webserver
# Version:  2016.04.08
#
###############################################################################
import tornado.ioloop
import tornado.web
import json


class ProcessWebserver:

    def Run(self, WLQueue, WPQueue, WMQueue, MQueue, LQueue, PQueue):

        class MainHandler(tornado.web.RequestHandler):

            def initialize(self, db):
                self.MQueue = db

            def get(self, url):
                self.MQueue.put("I@Mainhandler url: " + url)
                siteUrl = url

                # handle html sources
                self.render("../Robbi/" + siteUrl)

        class StaticHandler(tornado.web.RequestHandler):

            def initialize(self, db):
                self.MQueue = db

            # deliver static files to page
            def get(self, url):
                self.MQueue.put("I@Static Handler: " + url)
                if url.endswith(".png")\
                or url.endswith(".ico")\
                or url.endswith(".jpg")\
                or url.endswith(".gif"):
                    fh = open("static/" + url, "br")  # binary mode for png
                else:
                    fh = open("static/" + url, "r")
                content = fh.read()
                fh.close()
                if content:
                    # write to page
                    if url.endswith(".css"):
                        self.set_header("Content-Type", "text/css")
                    elif url.endswith(".js"):
                        self.set_header("Content-Type", "text/javascript")
                    elif url.endswith(".png"):
                        self.set_header("Content-Type", "image/png")
                    self.write(content)
                else:
                    self.write("Error 404: File '{}' not Found.".format(url))

        # execute commands and deliver data to page
        class AjaxHandler(tornado.web.RequestHandler):

            def initialize(self, db):
                self.LQueue = db[0]
                self.WLQueue = db[1]
                self.MQueue = db[2]
                self.PQueue = db[3]
                self.WPQueue = db[4]
                self.WMQueue = db[5]

            def get(self, url):
                self.MQueue.put("I@ AjaxHandler " + url)
                if url.startswith("Alarmlist"):
                    if url.endswith("/data"):
                        # acquire data
                        self.LQueue.put(["R@", ""])
                        output = self.WLQueue.get()
                        self.write(output)

                    elif url.endswith("/acknowledge"):
                        self.LQueue.put(["Q@", ""])
                        dictionary = {"phantasy": "&nbsp;"}
                        output = json.dumps(dictionary)
                        self.write(output)
                    else:
                        key = url.split("/")
                        self.LQueue.put(["P@", key[1]])
                        dictionary = {"phantasy": "&nbsp;"}
                        output = json.dumps(dictionary)
                        self.write(output)

                elif url.startswith("Panel"):
                    if url.endswith("/data"):
                        # acquire data
                        self.PQueue.put("R@Panel")
                        output = self.WPQueue.get()
                        self.write(output)
                    else:
                        command = url.split("/")
                        self.PQueue.put("C@" + command[1])
                        dictionary = {"phantasy": "&nbsp;"}
                        output = json.dumps(dictionary)
                        self.write(output)

                elif url.startswith("Map"):
                    if url.endswith("/canvasRectData"):
                        # acquire data
                        self.MQueue.put("R@")
                        output = json.dumps(self.WMQueue.get())
                        self.write(output)
                    elif url.endswith("/canvasCircleData"):
                        self.MQueue.put("C@")
                        output = json.dumps(self.WMQueue.get())
                        self.write(output)
                    elif url.endswith("/canvasLineData"):
                        self.MQueue.put("L@")
                        output = json.dumps(self.WMQueue.get())
                        self.write(output)
                    elif url.endswith("/canvasPathData"):
                        self.MQueue.put("P@")
                        output = json.dumps(self.WMQueue.get())
                        self.write(output)
                    elif url.endswith("/canvasRobotData"):
                        self.MQueue.put("RP@")
                        output = json.dumps(self.WMQueue.get())
                        self.write(output)
                    elif url.endswith("/data"):
                        # acquire data
                        self.PQueue.put("R@Map")
                        output = self.WPQueue.get()
                        self.write(output)
                    else:
                        # command
                        command = url.split("/")
                        # button or mouse click
                        self.PQueue.put("C@" + command[1])
                        dictionary = {"phantasy": "&nbsp;"}
                        output = json.dumps(dictionary)
                        self.write(output)

                else:
                    self.write("Error 404: File '{}' not Found.".format(url))

        self.settings = {
            "debug": True}

        def make_app():
            return tornado.web.Application([
                (r"/Robbi/(.*)", MainHandler, dict(db=MQueue)),
                (r"/static/(.*)", StaticHandler, dict(db=MQueue)),
                (r"/ajax/(.*)", AjaxHandler, dict(db=[LQueue, WLQueue, MQueue, PQueue, WPQueue, WMQueue]))
            ], **self.settings)

        app = make_app()
        app.listen(8080)
        tornado.ioloop.IOLoop.current().start()
