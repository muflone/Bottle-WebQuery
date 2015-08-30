import bottle

import configuration
from app_constants import DIR_STATIC
from bridge_response import bridge_response
from .constants import MODULE_NAME
from .requests import *

class BottleApplication(bottle.Bottle):
  def __init__(self):
    super(self.__class__, self).__init__()

    def serve_object_page(oPage):
      return bridge_response(oPage.serve())

    @self.route('/static/<filepath:path>')
    def serve(filepath):
      """Serve the static files (resources)"""
      return bridge_response('STATIC:%s:%s' % (filepath, 
        configuration.get_path(MODULE_NAME, DIR_STATIC)))

    @self.route('/')
    def serve():
      """Serve the page"""
      return bridge_response('REDIRECT:query')

    @self.route('/query')
    @self.post('/query')
    def serve():
      """Serve the page"""
      return serve_object_page(RequestQuery())

    @self.route('/queries')
    @self.post('/queries')
    def serve():
      """Serve the page"""
      return serve_object_page(RequestQueries())

    @self.route('/catalogs')
    @self.post('/catalogs')
    def serve():
      """Serve the page"""
      return serve_object_page(RequestCatalogs())

    @self.route('/folders')
    @self.post('/folders')
    def serve():
      """Serve the page"""
      return serve_object_page(RequestFolders())

    @self.route('/run')
    @self.post('/run')
    def serve():
      """Serve the page"""
      return serve_object_page(RequestRun())

def setup():
  """Initial setup, called during the application mount"""
  # Create a new application
  app = BottleApplication()
  return app
