from collections import OrderedDict
import datetime

import configuration
from .base import RequestBase

class RequestRun(RequestBase):
  def __init__(self):
    """Class initialization"""
    RequestBase.__init__(self)
    self.login_required = False

  def serve(self):
    """Handle the request and serve the response"""
    RequestBase.serve(self)
    # Request values
    self.args = {}
    self.args['UUID'] = self.params.get_item('uuid')
    self.args['FORMAT'] = self.params.get_item('format')
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
    self.values['REQUIRES'] = []
    self.values['REQUIRES'].append('jquery')
    self.values['REQUIRES'].append('tablesorter')
    # Parameters
    self.parameters = OrderedDict()
    self.extra_parameters = {}
    engine = None
    engine_settings = self.open_settings_db()
    # Get query information
    existing_fields, existing_data = engine_settings.get_data(
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
        existing_fields, existing_data = engine_settings.get_data(
          'SELECT engine, connstr, server, database, username, '
          'password, encoding '
          'FROM catalogs '
          'WHERE name=?',
          None,
          (self.values['CATALOG'], ))
        if existing_data:
          self.values['ENGINE'] = existing_data[0][0]
          self.values['SERVER'] = existing_data[0][2]
          self.values['DATABASE'] = existing_data[0][3]
          self.values['USERNAME'] = existing_data[0][4]
          self.values['PASSWORD'] = existing_data[0][5]
          self.values['ENCODING'] = existing_data[0][6]
          self.values['CONNECTION'] = self.prepare_connection_string(
            connection=existing_data[0][1],
            engine=self.values['ENGINE'],
            server=self.values['SERVER'],
            database=self.values['DATABASE'],
            username=self.values['USERNAME'],
            password=self.values['PASSWORD'])
        else:
          self.values['ERRORS'].append('Catalog not found')
    if not self.values['ERRORS']:
      # Open catalog database
      engine = self.open_db_from_engine_type(
        self.values['ENGINE'],
        self.values['CATALOG'],
        self.values['CONNECTION'],
        self.values['USERNAME'],
        self.values['PASSWORD'],
        self.values['DATABASE'],
        self.values['SERVER'])
      # Parse parameters
      if self.values['PARAMETERS']:
        list_parameters = self.values['PARAMETERS'].replace(
          '\r\n', '\n').replace('\r', '\n').split('\n')
        for parameter in list_parameters:
          param_name, param_config = parameter.split('=', 1)
          # Get the parameter from the parameters table if needed
          if param_config.startswith('parameter:'):
            existing_fields, existing_data = engine_settings.get_data(
              statement='SELECT content FROM parameters WHERE name=?',
              replaces=None,
              parameters=(param_config[10:], ))
            if existing_data:
              param_config = existing_data[0][0]
              list_parameters.insert(
                list_parameters.index(parameter),
                '%s=%s' % (param_name, param_config))
              list_parameters.remove(parameter)
        for parameter in list_parameters:
          param_name, param_config = parameter.split('=', 1)
          # Parameter configuration
          if param_config.startswith('list:'):
            # List of values
            param_values = param_config[5:].split(',')
          elif param_config.startswith('range:'):
            # Range between two values
            param_value1, param_value2 = param_config[6:].split('-', 1)
            param_values = range(
              int(param_value1), int(param_value2) + 1)
          elif param_config.startswith('sql:'):
            # Result of a SQL statement
            existing_fields, existing_data = engine.get_data(
              param_config[4:])
            param_values = []
            for param_value1 in existing_data:
              param_values.append(param_value1[0])
          elif param_config.startswith('text:'):
            # Input text
            param_values = ''
          elif param_config.startswith('date:'):
            # Date input text
            param_values = datetime.date.today()
            if 'jquery-ui' not in self.values['REQUIRES']:
              self.values['REQUIRES'].append('jquery-ui')
          elif param_config.startswith('values:'):
            # List of key=description values
            param_values = []
            for param_value1 in param_config[7:].split(','):
              param_values.append(param_value1.split('=', 1))
          elif param_config.startswith('parameters:'):
            param_values = []
            for param_value1 in param_config[11:].split(','):
              param_values.append(param_value1.split('=', 1)[0])
          else:
            # Not implemented parameter type
            raise Exception('Not implemented parameter type: %s' % 
               param_config)
          self.parameters[param_name] = param_values
        # Check all the parameters for parameters type values
        for parameter in list_parameters:
          param_name, param_config = parameter.split('=', 1)
          # param_name is the parameters: name
          if param_config.startswith('parameters:'):
            # A parameter of type parameters has the following syntax:
            # NAME=parameters:PARAMVALUE1=FIELD1=VALUE1,PARAMVALUE2=FIELD1=VALUE1
            self.args[param_name] = self.params.get_item(param_name, None)
            # self.args[param_name] is the selected PARAMVALUE
            param_values = param_config[11:].split(',')
            for param_values in param_values:
              param_name2, param_values = param_values.split('=', 1)
              # param_name2 is each PARAMVALUE
              # param_values is the FIELD=VALUE pairs list
              param_values = param_values.split(';')
              for parameter in param_values:
                # parameter is each FIELD=value pair
                param_value1, param_value2 = parameter.split('=', 1)
                # Check if the parameters parameter was set
                if self.args[param_name] == param_name2:
                  self.args[param_value1] = param_value2
                else:
                  self.args[param_value1] = None
                self.extra_parameters[param_value1] = self.args[param_value1]
              # Exit after the current PARAMVALUE was found
              if self.args[param_name] == param_name2:
                break
            break
        # Check all the parameters if they were configured
        for parameter in self.parameters.keys():
          self.args[parameter] = self.params.get_item(parameter, None)
          if self.args[parameter] is not None:
            self.args[parameter] = self.args[parameter].replace(
              '\'', '\'\'')
          else:
            self.values['ERRORS'].append(
              'Parameter %s was not provided' % parameter)
        # Fill parameters with extra parameters
        for parameter in self.extra_parameters.keys():
          if self.extra_parameters.get(parameter, None) is not None:
            self.args[parameter] = self.extra_parameters[parameter].replace(
              '\'', '\'\'')
    if engine:
      if not self.values['ERRORS']:
        # Get the data from the query
        self.values['FIELDS'], self.values['DATA'] = engine.get_data(
          self.values['SQL'], self.args, None)
      engine.close()
    engine_settings.close()
    engine_settings = None
    configuration.set_locale(None)
    if not self.values['ERRORS'] and self.args['FORMAT'].lower() == 'csv':
      # Returns results like text/csv
      self.set_content_type('text/csv')
      self.set_filename('%s.csv' % self.values['DESCRIPTION'])
      return self.output_to_csv(self.values['DATA'])
    else:
      return self.get_template('reports/%s.tpl' % self.values['REPORT'],
        ARGS=self.args,
        VALUES=self.values,
        PARAMETERS=self.parameters,
        printable_text_for_encoding=self.printable_text_for_encoding,
        datetime=datetime)
