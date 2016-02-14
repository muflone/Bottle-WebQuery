import configuration
import logging
from .base import RequestBase

class RequestParameters(RequestBase):
  def __init__(self):
    """Class initialization"""
    RequestBase.__init__(self)
    self.valid_roles = ['admin', ]

  def serve(self):
    """Handle the request and serve the response"""
    RequestBase.serve(self)
    # Request values
    self.args = {}
    self.args['CONFIRM'] = self.params.get_item('confirm')
    self.args['DELETE'] = self.params.get_item('delete')
    self.args['PARAMETER'] = self.params.get_utf8_item('parameter')
    self.args['DESCRIPTION'] = self.params.get_utf8_item('description')
    self.args['CONTENT'] = self.params.get_utf8_item('content')
    # Avoid empty description
    if not self.args['DESCRIPTION']:
      self.args['DESCRIPTION'] = self.args['PARAMETER']
    # Response values
    self.values = {}
    self.values['ERRORS'] = []
    self.values['DATA'] = None
    existing_parameter = ''
    existing_description = ''
    existing_content = ''
    
    engine = self.open_settings_db()
    # Get existing catalog details
    if self.args['PARAMETER']:
      existing_fields, existing_data = engine.get_data(
          'SELECT name, description, content '
          'FROM parameters '
          'WHERE name=?',
          None,
          (self.args['PARAMETER'], ))
      if existing_data:
        if self.args['DELETE']:
          # Delete existing parameter
          logging.debug('Deleting parameter: %s' % self.args['PARAMETER'])
          engine.execute('DELETE FROM parameters WHERE name=?', (
            self.args['PARAMETER'], ))
          engine.save()
          logging.info('Deleted parameter: %s' % self.args['PARAMETER'])
          # Reload empty page afer save
          return 'REDIRECT:parameters'
        else:
          existing_parameter, existing_description, existing_content = \
            existing_data[0]
    # Check the requested arguments for errors
    if self.args['CONFIRM']:
      # Check parameters for errors
      if not self.args['PARAMETER']:
        self.values['ERRORS'].append('Missing parameter name')
      # Process data
      if not self.values['ERRORS']:
        if existing_parameter:
          # Update existing parameter
          logging.debug('Updating parameter: %s' % self.args['PARAMETER'])
          engine.execute('UPDATE parameters '
                         'SET description=?, content=? '
                         'WHERE name=?', (
                           self.args['DESCRIPTION'],
                           self.args['CONTENT'],
                           self.args['PARAMETER']))
          logging.info('Updated parameter: %s' % self.args['PARAMETER'])
        else:
          # Insert new parameter
          logging.debug('Inserting parameter: %s' % self.args['PARAMETER'])
          engine.execute('INSERT INTO parameters(name, description, '
                         'content) '
                         'VALUES(?, ?, ?)', (
                         self.args['PARAMETER'],
                         self.args['DESCRIPTION'],
                         self.args['CONTENT']))
          logging.info('Inserted parameter: %s' % self.args['PARAMETER'])
        engine.save()
        # Reload empty page afer save
        return 'REDIRECT:parameters'
    else:
      # Use existing details
      self.args['DESCRIPTION'] = existing_description
      self.args['CONTENT'] = existing_content
    # Get existing parameters list
    self.values['FIELDS'], self.values['DATA'] = engine.get_data(
      'SELECT name, description '
      'FROM parameters '
      'ORDER BY name')
    engine.close()
    configuration.set_locale(None)
    return self.get_template('parameters.tpl',
      ARGS=self.args,
      VALUES=self.values,
      printable_text_for_encoding=self.printable_text_for_encoding)
