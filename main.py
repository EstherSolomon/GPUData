from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
import os
from design import GPUData
from edit import AddGPUData
from edit import DisplayGpuData
from editfeature import UpdateGpuData
from edit import GpuQuery

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        logout_string = ''
        gpu_data = None
        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            logout_string = 'logout'
            gpu_data = GPUData.query().fetch()

        else:
            url = users.create_login_url(self.request.uri)
            logout_string = 'login'
            gpu_data = GPUData.query().fetch()
        template_values = {
            'url': url,
            'logout_string': logout_string,
            'user': user,
            'gpu_data': gpu_data
        }
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


class CompareGpuData(webapp2.RequestHandler):
    def post(self):


        gpus = self.request.params.getall('compare')
        gpu_names = [str(x) for x in gpus]

        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        logout_string = ''
        user = users.get_current_user()
        obj = GPUData.query(ndb.OR(GPUData.name.IN(gpu_names)))
        gpu_data = obj.fetch()
        template_values = {
            'url': url,
            'logout_string': logout_string,
            'user': user,
            'gpu_data': gpu_data
        }

        template = JINJA_ENVIRONMENT.get_template('compare.html')
        self.response.write(template.render(template_values))




class DeleteGPUData(webapp2.RequestHandler):
    def get(self, gpu_name):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        logout_string = ''
        gpu_data = None
        user = users.get_current_user()
        delete_row = GPUData.query(GPUData.name == gpu_name)
        for row in delete_row.fetch(limit=1):
            row.key.delete()
        gpu_data = GPUData.query().fetch()
        template_values = {
            'url': url,
            'logout_string': logout_string,
            'user': user,
            'gpu_data': gpu_data
        }
        self.redirect('/')



app = webapp2.WSGIApplication([

    ('/edit', AddGPUData),
    ('/features/([\w|\W]+)', DisplayGpuData),
    ('/editfeatures/([\w|\W]+)', UpdateGpuData),
    ('/editfeatures', UpdateGpuData),
    ('/select', GpuQuery),
    ('/compare', CompareGpuData),
    ('/delete/([\w|\W]+)', DeleteGPUData),
    ('/', MainPage),
], debug=True)
