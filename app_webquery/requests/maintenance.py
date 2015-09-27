import configuration
import logging
from .base import RequestBase

class RequestMaintenance(RequestBase):
  def __init__(self):
    """Class initialization"""
    RequestBase.__init__(self)

  def serve(self):
    """Handle the request and serve the response"""
    RequestBase.serve(self)
    # Request values
    self.args = {}
    self.args['CONFIRM'] = self.params.get_item('confirm')
    self.args['ACTION'] = self.params.get_item('action')
    self.args['ID'] = self.params.get_item('id')
    self.args['NAME'] = self.params.get_utf8_item('name')
    self.args['DESCRIPTION'] = self.params.get_utf8_item('description')
    self.args['SQL'] = self.params.get_utf8_item('sql')
    self.args['APPLIED'] = self.params.get_item('applied')
    self.args['IGNORE ERRORS'] = self.params.get_item('ignore errors')
    # Avoid empty description
    if not self.args['DESCRIPTION']:
      self.args['DESCRIPTION'] = self.args['NAME']
    # Response values
    self.values = {}
    self.values['ERRORS'] = []
    self.values['DATA'] = None
    existing_id = 0
    existing_name = ''
    existing_description = ''
    existing_sql = ''
    existing_applied = ''
    existing_ignore_errors = ''
    
    engine = self.open_settings_db()
    # Get existing catalog details
    if self.args['ID']:
      existing_fields, existing_data = engine.get_data(
          'SELECT id, name, description, sql, applied, ignore_errors '
          'FROM maintenance '
          'WHERE id=?',
          None,
          (self.args['ID'], ))
      if existing_data:
        existing_id, existing_name, existing_description, \
          existing_sql, existing_applied, \
          existing_ignore_errors = existing_data[0]
        if self.args['ACTION'].upper() == 'DELETE':
          # Delete existing query
          logging.debug('Deleting operation: %s' % existing_name)
          engine.execute('DELETE FROM maintenance WHERE id=?', (
            self.args['ID'], ))
          engine.save()
          logging.info('Deleted operation: %s' % existing_name)
          # Reload empty page afer save
          return 'REDIRECT:maintenance'
        if self.args['ACTION'].upper() == 'APPLY':
          # Execute the requested operation
          logging.debug('Applying operations: %s' % existing_name)
          if existing_ignore_errors:
            # Execute operation and ignore errors
            try:
              engine.execute(existing_sql)
            except:
              logging.info('Ignored errors during operations: %s' % (
                existing_name, ))
          else:
            # Execute operation without any error handling
            engine.execute(existing_sql)
            
          engine.execute('UPDATE maintenance SET applied="*" '
            'WHERE id=?', (
            self.args['ID'], ))
          engine.save()
          logging.info('Applied operations: %s' % existing_name)
          # Reload empty page afer save
          return 'REDIRECT:maintenance'
    # Check the requested arguments for errors
    if self.args['CONFIRM']:
      # Check parameters for errors
      if not self.args['NAME']:
        self.values['ERRORS'].append('Missing operation name')
      if not self.args['SQL']:
        self.values['ERRORS'].append('Missing SQL statement')
      # Process data
      if not self.values['ERRORS']:
        if existing_id:
          # Update existing query
          logging.debug('Updating operation: %s' % self.args['ID'])
          engine.execute('UPDATE maintenance '
                         'SET name=?, description=?, sql=?, applied=?, '
                         'ignore_errors=? '
                         'WHERE id=?', (
                           self.args['NAME'],
                           self.args['DESCRIPTION'],
                           self.args['SQL'],
                           self.args['APPLIED'],
                           self.args['IGNORE ERRORS'],
                           self.args['ID']))
          logging.info('Updated operation: %s' % self.args['NAME'])
        else:
          # Insert new query
          logging.debug('Inserting operation: %s' % self.args['NAME'])
          engine.execute('INSERT INTO maintenance(name, description, '
                         'sql, applied, ignore_errors) '
                         'VALUES(?, ?, ?, ?, ?)', (
                         self.args['NAME'],
                         self.args['DESCRIPTION'],
                         self.args['SQL'],
                         self.args['APPLIED'],
                         self.args['IGNORE ERRORS']))
          logging.info('Inserted operaton: %s' % self.args['NAME'])
        engine.save()
        # Reload empty page afer save
        return 'REDIRECT:maintenance'
    else:
      # Use existing details
      self.args['ID'] = existing_id
      self.args['NAME'] = existing_name
      self.args['DESCRIPTION'] = existing_description
      self.args['SQL'] = existing_sql
      self.args['APPLIED'] = existing_applied
      self.args['IGNORE ERRORS'] = existing_ignore_errors
    # Get existing operations list
    self.values['FIELDS'], self.values['DATA'] = engine.get_data(
      'SELECT id, name, description, applied, ignore_errors '
      'FROM maintenance '
      'ORDER BY id')
    engine.close()
    configuration.set_locale(None)
    return self.get_template('maintenance.tpl',
      ARGS=self.args,
      VALUES=self.values,
      printable_text_for_encoding=self.printable_text_for_encoding)
