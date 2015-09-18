import bottle
import urllib2
import configuration
import logging

import app_webquery.paths
import app_webquery.parameters
import app_webquery.webquery
from app_webquery.constants import MODULE_NAME, SETTINGS_DB

# List of engines modules
db_engines = app_webquery.webquery.detect_db_engines()

class RequestBase(object):
  def __init__(self):
    """Baseclass initialization for all the Request response pages"""
    self.paths = app_webquery.paths.Paths()
    self.params = app_webquery.parameters.Parameters()
    self.engines = db_engines

  def serve(self):
    """Base method for serving the response page"""
    pass

  def get_template(self, template_name, **extra_arguments):
    """Return the template associated to the template_name with its
    module and extra arguments"""
    return bottle.template(self.paths.template(template_name),
                           MODULE=MODULE_NAME,
                           OBJECT=self,
                           quote=urllib2.quote,
                           REQUEST=bottle.request,
                           **extra_arguments)

  def get_request_page(self):
    """Return the requested page"""
    return bottle.request.fullpath

  def get_request_query(self):
    """Return the request querystring"""
    return bottle.request.query_string

  def open_settings_db(self):
    """Open the common settings database"""
    logging.debug('Opening settings database: %s' % SETTINGS_DB)
    engine = self.open_db_from_engine_type(
      engine_type='sqlite3',
      name='Settings',
      connection=configuration.get_database(MODULE_NAME, SETTINGS_DB),
      username=None,
      password=None,
      database=None,
      server=None)
    engine.open()
    return engine

  def open_db_from_engine_type(self, engine_type, name, connection, username, password, database, server):
    """Open a database by its connection using an engine type"""
    engine_class = self.engines.get(engine_type, None)
    if engine_class:
      logging.info('Opening database: (type: %s, name: %s)' % (
        engine_type, name))
      engine = engine_class(connection, username, password, database, server)
      engine.open()
      return engine
    else:
      logging.critical('Unable to open the catalog %s, '
        'Engine %s not found' % (name, engine_type))

  def printable_text_for_encoding(self, text, encoding):
    """Return a string valid for printing"""
    if text is None:
      return 'Null'
    elif type(text) is unicode:
      return text.encode(encoding).replace('\\n', '<br />')
    elif type(text) is str:
      return text.decode(encoding).replace('\\n', '<br />')
    elif type(text) is float:
      return '%.2f' % text
    else:
      return str(text).replace('\\n', '<br />')

  def prepare_connection_string(self, connection, engine, server, database, username, password):
    """Return a prepared connection string"""
    return connection % {
      'ENGINE': engine,
      'SERVER': server,
      'DATABASE': database,
      'USERNAME': username,
      'PASSWORD': password,
    }

  def set_content_type(self, content_type):
    """Set the content-type"""
    bottle.response.set_header('Content-Type', content_type)
