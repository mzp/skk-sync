#!/usr/bin/env python
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext.webapp.util import login_required

class BaseHandler(webapp.RequestHandler):
  def render(self,name,context={}):
    user = users.get_current_user()
    if user:
      context['greeting'] = ("<a href=\"%s\">ログアウト</a>" %
                             users.create_logout_url('/'))
    else:
      context['greeting'] = ("<a href=\"%s\">登録/ログイン</a>" %
                             users.create_login_url('/home'))
    self.response.out.write(template.render("templates/%s.html" % name,
                                            context))

class MainHandler(BaseHandler):
  def get(self):
    self.render('index')

class HomeHandler(BaseHandler):
  @login_required
  def get(self):
    user = users.get_current_user()
    self.render('home',{'nickname': user.nickname()})

def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/home',HomeHandler)
                                        ],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
