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
    self.args['SQL'] = self.params.get_utf8_item('sql')
    self.args['CATALOG'] = self.params.get_utf8_item('catalog')
    self.args['LIST_TABLES'] = self.params.get_item('list_tables')
    # Response values
    self.values = {}
    self.values['ERRORS'] = []
    self.values['TABLES'] = []
    self.values['FIELDS'] = None
    self.values['DATA'] = None
    # Get the configured catalogs
    engine = self.open_settings_db()
    self.values['CATALOGS'] = engine.get_data(
      'SELECT name, description, engine, connstr, server, database, '
      'username, password, encoding '
      'FROM catalogs ORDER BY name')[1]
    for catalog in self.values['CATALOGS']:
      if catalog[0] == self.args['CATALOG']:
        catalog_engine = catalog[2]
        catalog_server = catalog[4]
        catalog_database = catalog[5]
        catalog_username = catalog[6]
        catalog_password = catalog[7]
        catalog_connection = self.prepare_connection_string(
          connection=catalog[3],
          engine=catalog_engine,
          server=catalog_server,
          database=catalog_database,
          username=catalog_username,
          password=catalog_password)
        catalog_encoding = catalog[8]
        break
    else:
      catalog_engine = ''
      catalog_connection = ''
      catalog_server = ''
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
        catalog_database,
        catalog_server)
      if engine:
        # List the catalog tables if available and requested
        self.values['TABLES'] = [(t, t) for t in engine.list_tables()] \
          if self.args['LIST_TABLES'] else ()
        # Get fields and data if SQL argument was provided
        self.values['FIELDS'], self.values['DATA'] = engine.get_data(
          self.args['SQL'].encode('utf-8').replace(
          '\r\n', ' ').replace('\n', ' ').replace('\r', ' ')) if len(
          self.args['SQL']) > 0 else ([], [])
        self.values['ENCODING'] = catalog_encoding
        engine.close()
    configuration.set_locale(None)
    return self.get_template('query.tpl',
      ARGS=self.args,
      VALUES=self.values,
      printable_text_for_encoding=self.printable_text_for_encoding)
