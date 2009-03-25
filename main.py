#!/usr/bin/env python
# -*- coding:utf-8 -*-
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext.webapp.util import login_required
from django import newforms
from django.newforms import models
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms

class Word(db.Model):
  user = db.UserProperty()
  word = db.StringProperty(verbose_name="単語",required=True)
  yomi = db.StringProperty(verbose_name="読み",required=True)
  date = db.DateTimeProperty(auto_now_add=True)
  annotation = db.StringProperty(verbose_name="注釈",required=False)

class WordForm(djangoforms.ModelForm):
  class Meta:
    model = Word
    exclude = ['user']

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
    words = db.GqlQuery("SELECT * FROM Word WHERE user = :1 ORDER BY yomi ASC",
                        user)
    count = words.count()
    last = db.GqlQuery("SELECT * FROM Word WHERE user = :1 ORDER BY date DESC LIMIT 1",user).get()

    self.render('home',{
        'nickname': user.nickname(),
        'words': words,
        'words_count':count,
        'last_mod':last.date if last else None
        })

class DictHandler(BaseHandler):
  def post(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url('/'))
    form = WordForm(self.request)
    if form.is_valid():
      model = form.save(commit=False)
      model.user = user
      model.put()
      self.redirect('/home')
    else:
      self.render('dict_add',{
          'form': form
          })

  @login_required
  def get(self):
    form = WordForm()
    self.render('dict_add',{
        'form': form
        })


def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/home',HomeHandler),
                                        ('/dict/add',DictHandler)
                                        ],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()
