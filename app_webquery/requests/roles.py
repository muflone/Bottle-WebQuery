import configuration
import logging
from .base import RequestBase

class RequestRoles(RequestBase):
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
    self.args['ROLE'] = self.params.get_utf8_item('role')
    self.args['DESCRIPTION'] = self.params.get_utf8_item('description')
    # Avoid empty description
    if not self.args['DESCRIPTION']:
      self.args['DESCRIPTION'] = self.args['ROLE']
    # Response values
    self.values = {}
    self.values['ERRORS'] = []
    self.values['DATA'] = None
    existing_role = ''
    existing_description = ''
    
    engine = self.open_settings_db()
    # Get existing role details
    if self.args['ROLE']:
      existing_fields, existing_data = engine.get_data(
          'SELECT name, description '
          'FROM roles '
          'WHERE name=?',
          None,
          (self.args['ROLE'], ))
      if existing_data:
        if self.args['DELETE']:
          # Delete existing role
          logging.debug('Deleting role: %s' % self.args['ROLE'])
          engine.execute('DELETE FROM roles WHERE name=?', (
            self.args['ROLE'], ))
          engine.save()
          logging.info('Deleted role: %s' % self.args['ROLE'])
          # Reload empty page afer save
          return 'REDIRECT:roles'
        else:
          existing_role, existing_description = \
            existing_data[0]
    # Check the requested arguments for errors
    if self.args['CONFIRM']:
      # Check parameters for errors
      if not self.args['ROLE']:
        self.values['ERRORS'].append('Missing role name')
      # Process data
      if not self.values['ERRORS']:
        if existing_role:
          # Update existing role
          logging.debug('Updating role: %s' % self.args['ROLE'])
          engine.execute('UPDATE roles '
                         'SET description=? '
                         'WHERE name=?', (
                           self.args['DESCRIPTION'],
                           self.args['ROLE']))
          logging.info('Updated role: %s' % self.args['ROLE'])
        else:
          # Insert new role
          logging.debug('Inserting role: %s' % self.args['ROLE'])
          engine.execute('INSERT INTO roles(name, description) '
                         'VALUES(?, ?)', (
                         self.args['ROLE'],
                         self.args['DESCRIPTION']))
          logging.info('Inserted role: %s' % self.args['ROLE'])
        engine.save()
        # Reload empty page afer save
        return 'REDIRECT:roles'
    else:
      # Use existing details
      self.args['DESCRIPTION'] = existing_description
    # Get existing roles list
    self.values['FIELDS'], self.values['DATA'] = engine.get_data(
      'SELECT name, description '
      'FROM roles '
      'ORDER BY name')
    engine.close()
    configuration.set_locale(None)
    return self.get_template('roles.tpl',
      ARGS=self.args,
      VALUES=self.values,
      printable_text_for_encoding=self.printable_text_for_encoding)
