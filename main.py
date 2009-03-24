#!/usr/bin/env python
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import os


class MainHandler(webapp.RequestHandler):
  def get(self):
    self.response.out.write(template.render(
        "templates/index.html",{}))


def main():
  application = webapp.WSGIApplication([('/', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
