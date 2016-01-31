import bottle
from beaker.middleware import SessionMiddleware

import configuration
from app_constants import DIR_STATIC, DIR_BEAKER_CACHE, DIR_BEAKER_LOCKS, SESSION_TIMEOUT
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

    @self.post('/login')
    @self.route('/login')
    def serve():
      """Serve the login page"""
      return serve_object_page(RequestLogin())

    @self.route('/logout')
    def serve():
      """Serve the login page"""
      return serve_object_page(RequestLogout())

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

    @self.route('/parameters')
    @self.post('/parameters')
    def serve():
      """Serve the page"""
      return serve_object_page(RequestParameters())

    @self.route('/run')
    @self.post('/run')
    def serve():
      """Serve the page"""
      return serve_object_page(RequestRun())

def setup():
  """Initial setup, called during the application mount"""
  # Create a new application
  session_opts = {
      'session.type': 'file',
      'session.cookie_expires': True,
      'session.data_dir': DIR_BEAKER_CACHE,
      'session.lock_dir': DIR_BEAKER_LOCKS,
      'session.auto': True,
      'session.timeout': SESSION_TIMEOUT,
      'session.secret': None,
      'session.encrypt_key': False,
      'session.validate_key': False,
      'session.invalidate_corrupt': True,
  }

  app = SessionMiddleware(
      BottleApplication(),
      config=session_opts,
      environ_key='beaker.session',
      key='beaker.session.id')
  return app
