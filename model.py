#! /usr/bin/python
# -*- mode:python; coding:utf-8 -*-
import logging
from google.appengine.ext import db

def isHiragana(char):
    if u'ぁ' <= char <= u'ん':
        return True
    return False

def hiragana(xs):
    if not all(map(isHiragana,unicode(xs))):
        raise db.BadValueError("This field should be hiragana")

class Word(db.Model):
  user = db.UserProperty()
  word = db.StringProperty(verbose_name="単語", required=True)
  yomi = db.StringProperty(verbose_name="読み", validator=hiragana,
                           required=True)
  date = db.DateTimeProperty(auto_now_add=True)
  annotation = db.StringProperty(verbose_name="注釈",required=False)
