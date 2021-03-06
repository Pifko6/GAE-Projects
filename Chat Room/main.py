#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Message

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)

class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

class MainHandler(BaseHandler):
    def get(self):
        messages = Message.query().order(Message.date).fetch()

        params = {"messages": messages}

        return self.render_template("chat.html", params=params)

class AddMessage(BaseHandler):
    def post(self):
        title = self.request.get("title")
        message = self.request.get("message")

        if "<script>" in title or "<script>" in message:
            title = title.replace("<script>", "")
            title = title.replace("</script>", "")
            message = description.replace("<script>", "")
            message = description.replace("</script>", "")

        movie = Message(title=title, message=message)

        movie.put()
        return self.redirect_to("main")

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main"),
    webapp2.Route('/add', AddMessage)

], debug=True)
