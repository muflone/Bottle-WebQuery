import configuration
import logging
from .base import RequestBase

class RequestCatalogs(RequestBase):
  def __init__(self):
    """Class initialization"""
    RequestBase.__init__(self)

  def serve(self):
    """Handle the request and serve the response"""
    RequestBase.serve(self)
    # Request values
    self.args = {}
    self.args['CONFIRM'] = self.params.get_item('confirm')
    self.args['DELETE'] = self.params.get_item('delete')
    self.args['CATALOG'] = self.params.get_utf8_item('catalog')
    self.args['DESCRIPTION'] = self.params.get_utf8_item('description')
    self.args['ENGINE'] = self.params.get_item('engine')
    self.args['CONNECTION'] = self.params.get_utf8_item('connection')
    self.args['DATABASE'] = self.params.get_utf8_item('database')
    self.args['USERNAME'] = self.params.get_utf8_item('username')
    self.args['PASSWORD'] = self.params.get_utf8_item('password')
    self.args['ENCODING'] = self.params.get_item('encoding')
    # Response values
    self.values = {}
    self.values['ERRORS'] = []
    # Build engines list
    self.values['ENGINES'] = [('', '< select DB engine >')]
    for engine_name in self.engines.values():
      self.values['ENGINES'].append((engine_name.descriptor,
                                     engine_name.description))
    self.values['DATA'] = None
    existing_catalog = ''
    existing_description = ''
    existing_engine = ''
    existing_connection = ''
    existing_database = ''
    existing_username = ''
    existing_password = ''
    existing_encoding = ''
    
    engine = self.open_settings_db()
    # Get existing catalog details
    if self.args['CATALOG']:
      existing_fields, existing_data = engine.get_data(
          'SELECT name, description, engine, connstr, database, '
          'username, password, encoding '
          'FROM catalogs '
          'WHERE name=?',
          None,
          (self.args['CATALOG'], ))
      if existing_data:
        if self.args['DELETE']:
          # Delete existing catalog
          logging.debug('Deleting catalog: %s' % self.args['CATALOG'])
          engine.execute('DELETE FROM catalogs WHERE name=?', (
            self.args['CATALOG'], ))
          engine.save()
          logging.info('Deleted catalog: %s' % self.args['CATALOG'])
          # Reload empty page afer save
          return 'REDIRECT:catalogs'
        else:
          existing_catalog, existing_description, existing_engine, \
            existing_connection, existing_database, \
            existing_username, existing_password, existing_encoding = \
            existing_data[0]
    # Check the requested arguments for errors
    if self.args['CONFIRM']:
      # Check parameters for errors
      if not self.args['CATALOG']:
        self.values['ERRORS'].append('Missing catalog name')
      if not self.args['ENGINE']:
        self.values['ERRORS'].append('Missing engine name')
      if not self.args['CONNECTION']:
        self.values['ERRORS'].append('Missing connection string')
      # Process data
      if not self.values['ERRORS']:
        if existing_catalog:
          # Update existing catalog
          logging.debug('Updating catalog: %s' % self.args['CATALOG'])
          engine.execute('UPDATE catalogs '
                         'SET description=?, engine=?, connstr=?, '
                         'database=?, username=?, password=?, '
                         'encoding=? '
                         'WHERE name=?', (
                           self.args['DESCRIPTION'],
                           self.args['ENGINE'],
                           self.args['CONNECTION'],
                           self.args['DATABASE'],
                           self.args['USERNAME'],
                           self.args['PASSWORD'],
                           self.args['ENCODING'],
                           self.args['CATALOG']))
          logging.info('Updated catalog: %s' % self.args['CATALOG'])
        else:
          # Insert new catalog
          logging.debug('Inserting catalog: %s' % self.args['CATALOG'])
          engine.execute('INSERT INTO catalogs(name, description, '
                         'engine, connstr, database, '
                         'username, password, encoding) '
                         'VALUES(?, ?, ?, ?, ?, ?, ?, ?)', (
                         self.args['CATALOG'],
                         self.args['DESCRIPTION'],
                         self.args['ENGINE'],
                         self.args['CONNECTION'],
                         self.args['DATABASE'],
                         self.args['USERNAME'],
                         self.args['PASSWORD'],
                         self.args['ENCODING']))
          logging.info('Inserted catalog: %s' % self.args['CATALOG'])
        engine.save()
        # Reload empty page afer save
        return 'REDIRECT:catalogs'
    else:
      # Use existing details
      self.args['DESCRIPTION'] = existing_description
      self.args['ENGINE'] = existing_engine
      self.args['CONNECTION'] = existing_connection
      self.args['DATABASE'] = existing_database
      self.args['USERNAME'] = existing_username
      self.args['PASSWORD'] = existing_password
      self.args['ENCODING'] = existing_encoding
    # Get existing catalogs list
    self.values['FIELDS'], self.values['DATA'] = engine.get_data(
      'SELECT name, description, engine, connstr, database '
      'FROM catalogs '
      'ORDER BY name')
    engine.close()
    configuration.set_locale(None)
    return self.get_template('catalogs.tpl',
      ARGS=self.args,
      VALUES=self.values,
      printable_text_for_encoding=self.printable_text_for_encoding)
