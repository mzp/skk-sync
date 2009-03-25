#! /usr/bin/python
from google.appengine.api import users

def login_required(handler_method):
    def check_login(self, *args):
        user = users.get_current_user()
        if not user:
            if self.request.method != 'GET':
                self.redirect(users.create_login_url(self.request.uri))
            else:
                self.redirect('/')
        else:
            handler_method(self, *args)
    return check_login
