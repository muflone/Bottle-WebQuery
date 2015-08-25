import configuration
from .base import RequestBase

class RequestQuery(RequestBase):
  def __init__(self):
    """Class initialization"""
    RequestBase.__init__(self)

  def serve(self):
    """Handle the request and serve the response"""
    RequestBase.serve(self)
    # Request values
    self.args = {}
    self.args['CONFIRM'] = self.params.get_item('confirm')
    self.args['SQL'] = self.params.get_utf8_item('sql').replace(
      '\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
    self.args['CATALOG'] = self.params.get_utf8_item('catalog')
    # Response values
    self.values = {}
    self.values['ERRORS'] = []
    self.values['TABLES'] = []
    self.values['FIELDS'] = None
    self.values['DATA'] = None
    # Get the configured catalogs
    engine = self.open_settings_db()
    self.values['CATALOGS'] = engine.get_data(
      'SELECT name, description, engine, connstr, database, '
      'username, password, encoding '
      'FROM catalogs ORDER BY name')[1]
    for catalog in self.values['CATALOGS']:
      if catalog[0] == self.args['CATALOG']:
        catalog_engine = catalog[2]
        catalog_connection = catalog[3]
        catalog_database = catalog[4]
        catalog_username = catalog[5]
        catalog_password = catalog[6]
        catalog_encoding = catalog[7]
        break
    else:
      catalog_engine = ''
      catalog_connection = ''
      catalog_database = ''
      catalog_username = ''
      catalog_password = ''
      catalog_encoding = ''
    engine.close()
    # Check the requested arguments for errors
    if self.args['CONFIRM']:
      # Get data
      engine = self.open_db_from_engine_type(
        catalog_engine,
        self.args['CATALOG'],
        catalog_connection,
        catalog_username,
        catalog_password,
        catalog_database)
      if engine:
        self.values['TABLES'] = [(t, t) for t in engine.list_tables()]
        self.values['FIELDS'], self.values['DATA'] = engine.get_data(
          self.args['SQL'].encode('utf-8')) \
          if len(self.args['SQL']) > 0 else ([], [])
        self.values['ENCODING'] = catalog_encoding
        engine.close()
    configuration.set_locale(None)
    return self.get_template('query.tpl',
      ARGS=self.args,
      VALUES=self.values,
      printable_text_for_encoding=self.printable_text_for_encoding)
