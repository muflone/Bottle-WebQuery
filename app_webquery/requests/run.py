from collections import OrderedDict

import configuration
from .base import RequestBase

class RequestRun(RequestBase):
  def __init__(self):
    """Class initialization"""
    RequestBase.__init__(self)

  def serve(self):
    """Handle the request and serve the response"""
    RequestBase.serve(self)
    # Request values
    self.args = {}
    self.args['UUID'] = self.params.get_item('uuid')
    # Response values
    self.values = {}
    self.values['ENGINE'] = None
    self.values['CONNECTION'] = None
    self.values['CATALOG'] = None
    self.values['DESCRIPTION'] = None
    self.values['SQL'] = None
    self.values['REPORT'] = None
    self.values['ERRORS'] = []
    self.values['FIELDS'] = None
    self.values['DATA'] = None
    # Parameters
    self.parameters = OrderedDict()
    engine = self.open_settings_db()
    # Get query information
    existing_fields, existing_data = engine.get_data(
        'SELECT catalog, description, sql, report, parameters '
        'FROM queries '
        'WHERE uuid=?',
        None,
        (self.args['UUID'], ))
    if existing_data:
      self.values['CATALOG'] = existing_data[0][0]
      self.values['DESCRIPTION'] = existing_data[0][1]
      self.values['SQL'] = existing_data[0][2].encode('utf-8').replace(
        '\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
      self.values['REPORT'] = existing_data[0][3]
      self.values['PARAMETERS'] = existing_data[0][4].encode('utf-8')
    else:
      self.values['ERRORS'].append('Query not found')
    if not self.values['ERRORS']:
        # Get the catalog information
        existing_fields, existing_data = engine.get_data(
          'SELECT engine, connstr, database, username, password, '
          'encoding '
          'FROM catalogs '
          'WHERE name=?',
          None,
          (self.values['CATALOG'], ))
        if existing_data:
          self.values['ENGINE'] = existing_data[0][0]
          self.values['CONNECTION'] = existing_data[0][1]
          self.values['DATABASE'] = existing_data[0][2]
          self.values['USERNAME'] = existing_data[0][3]
          self.values['PASSWORD'] = existing_data[0][4]
          self.values['ENCODING'] = existing_data[0][5]
    engine.close()
    engine = None
    if not self.values['ERRORS']:
      # Open catalog database
      engine = self.open_db_from_engine_type(
        self.values['ENGINE'],
        self.values['CATALOG'],
        self.values['CONNECTION'],
        self.values['USERNAME'],
        self.values['PASSWORD'],
        self.values['DATABASE'])
      # Parse parameters
      if self.values['PARAMETERS']:
        list_parameters = self.values['PARAMETERS'].replace(
          '\r\n', '\n').replace('\r', '\n').split('\n')
        for parameter in list_parameters:
          param_name, param_config = parameter.split('=', 1)
          # Parameter configuration
          if param_config.startswith('list:'):
            param_values = param_config[5:].split(',')
          elif param_config.startswith('range:'):
            param_value1, param_value2 = param_config[6:].split('-', 1)
            param_values = range(
              int(param_value1), int(param_value2) + 1)
          elif param_config.startswith('sql:'):
            existing_fields, existing_data = engine.get_data(
              param_config[4:])
            param_values = []
            for param_value1 in existing_data:
              param_values.append(param_value1[0])
          elif param_config.startswith('text:'):
            param_values = ''
          else:
            raise Exception('Not implemented')
          self.parameters[param_name] = param_values
        # Check all the parameters if they were configured
        for parameter in self.parameters.keys():
          self.args[parameter] = self.params.get_item(parameter, None)
          if self.args[parameter] is not None:
            self.args[parameter].replace('\'', '\'\'')
          else:
            self.values['ERRORS'].append(
              'Parameter %s was not provided' % parameter)
    if engine:
      if not self.values['ERRORS']:
        # Get the data from the query
        self.values['FIELDS'], self.values['DATA'] = engine.get_data(
          self.values['SQL'], self.args, None)
      engine.close()
    configuration.set_locale(None)
    return self.get_template('reports/%s.tpl' % self.values['REPORT'],
      ARGS=self.args,
      VALUES=self.values,
      PARAMETERS=self.parameters,
      printable_text_for_encoding=self.printable_text_for_encoding)
