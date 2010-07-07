#!/usr/bin/env python
import os
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db

# Email specific imports
import email
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler

# Markdown2
import markdown2

def render(template_name, values):
    path = os.path.join('templates', template_name)
    return template.render(path, values)

class Post(db.Model):
    title = db.StringProperty()
    body = db.TextProperty()
    added = db.DateTimeProperty(auto_now_add=True)
    author = db.StringProperty()

class EmailHandler(InboundMailHandler):
    def receive(self, mail_message):
        post = Post()
        post.title = mail_message.subject
        for content_type, body in mail_message.bodies():
            post.body = markdown2.markdown(body.decode())
        post.author = 'John Smith'
        post.put()
        

class Index(webapp.RequestHandler):
    def get(self):
        posts = Post.all().order('-added').fetch(10)
        values = {
            'posts': posts,
            }
        self.response.out.write(render('index.html', values))
        

application = webapp.WSGIApplication([
    ('/', Index),
    EmailHandler.mapping()
    
  ], debug=True)


def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
