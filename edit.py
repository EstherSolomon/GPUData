from google.appengine.api import users
from google.appengine.ext import ndb
import webapp2
import jinja2
import os
from design import GPUData
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)



class GpuQuery (webapp2.RequestHandler):

    def post(self, *args, **kwargs):
        if len(self.request.POST.keys()) == 0:
            self.redirect('/')

        query_dict = dict()
        for key in self.request.POST.keys():
            query_dict[key] = bool(self.request.POST[key])

        gpu_data = None
        gpu_details = GPUData.query()
        for key, value in query_dict.items():
            gpu_data = gpu_details.filter(ndb.BooleanProperty(key) == value)
        gpu_data = gpu_data.fetch()
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            logout_string = 'logout'
        else:
            url = users.create_login_url(self.request.uri)
            logout_string = 'login'

        template_values = {
            'url': url,
            'logout_string': logout_string,
            'user': user,
            'gpu_data': gpu_data,
            'gpu_all_data': gpu_data,
            'filter_key' : key,
            'filter_value' : value
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


class DisplayGpuData(webapp2.RequestHandler):

    def get(self, gpu_name):

        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        gpu_data = GPUData.query(GPUData.name == gpu_name).get()
        user = users.get_current_user()
        template_values = {
            'url': url,
            'user': user,
            'gpu_data': gpu_data,
        }

        template = JINJA_ENVIRONMENT.get_template('feature.html')
        self.response.write(template.render(template_values))


class AddGPUData(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        template_values = {
            'myuser': user
        }
        template = JINJA_ENVIRONMENT.get_template('add_gpu_data.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        if self.request.get('button') == 'Add':
            name = self.request.get('device_name')
            driver_device = float(self.request.get('driver_device', 0))
            manufacturer = self.request.get('manufacturer', name)
            dateIssue = self.request.get('dateIssue',name)
            geometry_shader = bool(self.request.get('GeometryShader', False))
            tesselation_shader = bool(self.request.get('TesselationShaderr', False))
            shader_int16 = bool(self.request.get('ShaderInt16', False))
            sparse_binding = bool(self.request.get('SparseBinding', False))
            texture_compressionetc2 = bool(self.request.get('TextureCompressionETC2', False))
            vertex_pipeline_stores_and_atomics = bool(self.request.get('vertexPipelineStoresAndAtomics', False))

            if GPUData.query(GPUData.name==name).get():
                 self.response.headers['Content-Type'] = 'text/html'
                 template_values = {
                 "error" : "The Name already exists. Please enter another device name."
                 }
                 template = JINJA_ENVIRONMENT.get_template('add_gpu_data.html')
                 self.response.write(template.render(template_values))
            else :
                update_gpu_details = GPUData(name=name, manufacturer=manufacturer,
                                                dateIssue=dateIssue, geometry_shader=geometry_shader,
                                                tesselation_shader=tesselation_shader, shader_int16=shader_int16,
                                                sparse_binding=sparse_binding,
                                                texture_compressionetc2=texture_compressionetc2,
                                                vertex_pipeline_stores_and_atomics=vertex_pipeline_stores_and_atomics)

                update_gpu_details.put()
                self.redirect('/')
        elif self.request.get('button') == 'Cancel':
            self.redirect('/')
