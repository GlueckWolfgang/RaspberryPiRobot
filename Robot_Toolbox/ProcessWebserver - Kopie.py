# -*- coding: utf-8 -*-
###############################################################################
# Class Prozess webserver
# Version:  2016.01.31
#
###############################################################################
import tornado.ioloop
import tornado.web


class ProcessWebserver:

    def Run(self, WLQueue, WPQueue, MQueue, LQueue, PQueue):

        class MainHandler(tornado.web.RequestHandler):

            def initialize(self, db):
                self.LQueue = db[0]
                self.WLQueue = db[1]
                self.MQueue = db[2]

            def get(self, url):

                MQueue.put("I@Mainhandler url: " + url)

                # handle buttons
                if url in ("1", "2", "3", "4", "5"):
                    if url.endswith("1"):
                        self.LQueue.put(["Q@", ""])
                    elif url.endswith("2"):
                        self.LQueue.put(["P@", "bwd"])
                    elif url.endswith("3"):
                        self.LQueue.put(["P@", "fwd"])
                    elif url.endswith("4"):
                        self.LQueue.put(["P@", "ft"])
                    elif url.endswith("5"):
                        self.LQueue.put(["P@", "lt"])
                    url = "index.html"

                # handle html sources
                self.file = open("Robbi/" + url, "r")
                self.site = self.file.read()
                self.file.close()

                if url.endswith("Alarmlist.html"):
                    # ask LQueue for data
                    self.LQueue.put(["R@", ""])
                    # read WLQueue
                    message = WLQueue.get()
                    # put data to head table
                    self.site = self.site.replace("?actual", message[0][0])
                    self.site = self.site.replace("?last", message[0][1])
                    # put data to body table
                    for i in range(1, len(message)):
                        row = message[i]
                        for j in range(0, len(row)):
                            self.site = self.site.replace('id="' + str(i) + "." + str(j + 1) + '">' + '&nbsp;',
                                                          'id="' + str(i) + "." + str(j + 1) + '">' + row[j])
                self.write(self.site)

        # deliver static files to page
        class StaticHandler(tornado.web.RequestHandler):

            def initialize(self, db):
                self.MQueue = db

            def get(self, url):
                MQueue.put("I@Static Handler: " + url)
                with open("static/" + url, "r") as fh:
                    content = fh.read()
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

        self.settings = {
            "debug": True}

        def make_app():
            return tornado.web.Application([
                (r"/Robbi/(.*)", MainHandler, dict(db=[LQueue, WLQueue, MQueue])),
                (r"/static/(.*)", StaticHandler, dict(db=MQueue))
            ], **self.settings)

        app = make_app()
        app.listen(8080)
        tornado.ioloop.IOLoop.current().start()