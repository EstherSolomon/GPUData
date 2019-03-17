import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from design import GPUData

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class UpdateGpuData(webapp2.RequestHandler):
    def get(self, gpu_name):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        gpu_data = GPUData.query(GPUData.name == gpu_name).get()
        template_values = {
            'url': url,
            'gpu_data': gpu_data,
        }
        template = JINJA_ENVIRONMENT.get_template('update_gpu_details.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        if self.request.POST['submit'] == 'Update':

            name = self.request.POST['name']
            manufacturer = self.request.POST['manufacturer']
            dateIssue = self.request.POST['dateIssue']
            geometry_shader = bool(self.request.POST.get('GeometryShader', False))
            tesselation_shader = bool(self.request.POST.get('TesselationShaderr', False))
            shader_int16 = bool(self.request.POST.get('ShaderInt16', False))
            sparse_binding = bool(self.request.POST.get('SparseBinding', False))
            texture_compressionetc2 = bool(self.request.POST.get('TextureCompressionETC2', False))
            vertex_pipeline_stores_and_atomics = bool(self.request.POST.get('vertexPipelineStoresAndAtomics', False))

            gpu_data = GPUData.query(GPUData.name == name).get()

            gpu_data.name = name
            gpu_data.manufacturer = manufacturer
            gpu_data.dateIssue = dateIssue
            gpu_data.geometry_shader = geometry_shader
            gpu_data.tesselation_shader = tesselation_shader
            gpu_data.shader_int16 = shader_int16
            gpu_data.sparse_binding = sparse_binding
            gpu_data.texture_compressionetc2 = texture_compressionetc2
            gpu_data.vertex_pipeline_stores_and_atomics = vertex_pipeline_stores_and_atomics

            gpu_data.put()

            self.redirect('/')
        elif self.request.get('button') == 'Cancel':
            self.redirect('/')
