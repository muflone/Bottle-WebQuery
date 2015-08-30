import configuration
import logging
from .base import RequestBase

class RequestFolders(RequestBase):
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
    self.args['FOLDER'] = self.params.get_utf8_item('folder')
    self.args['DESCRIPTION'] = self.params.get_utf8_item('description')
    self.args['VISIBLE'] = self.params.get_item('visible')
    # Avoid empty description
    if not self.args['DESCRIPTION']:
      self.args['DESCRIPTION'] = self.args['FOLDER']
    # Response values
    self.values = {}
    self.values['ERRORS'] = []
    self.values['DATA'] = None
    existing_folder = ''
    existing_description = ''
    existing_visible = 1
    
    engine = self.open_settings_db()
    # Get existing catalog details
    if self.args['FOLDER']:
      existing_fields, existing_data = engine.get_data(
          'SELECT name, description, visible '
          'FROM folders '
          'WHERE name=?',
          None,
          (self.args['FOLDER'], ))
      if existing_data:
        if self.args['DELETE']:
          # Delete existing folder
          logging.debug('Deleting folder: %s' % self.args['FOLDER'])
          engine.execute('DELETE FROM folders WHERE name=?', (
            self.args['FOLDER'], ))
          engine.save()
          logging.info('Deleted folder: %s' % self.args['FOLDER'])
          # Reload empty page afer save
          return 'REDIRECT:folders'
        else:
          existing_folder, existing_description, existing_visible = \
            existing_data[0]
    # Check the requested arguments for errors
    if self.args['CONFIRM']:
      # Check parameters for errors
      if not self.args['FOLDER']:
        self.values['ERRORS'].append('Missing folder name')
      # Process data
      if not self.values['ERRORS']:
        if existing_folder:
          # Update existing folder
          logging.debug('Updating folder: %s' % self.args['FOLDER'])
          engine.execute('UPDATE folders '
                         'SET description=?, visible=? '
                         'WHERE name=?', (
                           self.args['DESCRIPTION'],
                           1 if self.args['VISIBLE'] else 0,
                           self.args['FOLDER']))
          logging.info('Updated folder: %s' % self.args['FOLDER'])
        else:
          # Insert new folder
          logging.debug('Inserting folder: %s' % self.args['FOLDER'])
          engine.execute('INSERT INTO folders(name, description, '
                         'visible) '
                         'VALUES(?, ?, ?)', (
                         self.args['FOLDER'],
                         self.args['DESCRIPTION'],
                         1 if self.args['VISIBLE'] else 0))
          logging.info('Inserted folder: %s' % self.args['FOLDER'])
        engine.save()
        # Reload empty page afer save
        return 'REDIRECT:folders'
    else:
      # Use existing details
      self.args['DESCRIPTION'] = existing_description
      self.args['VISIBLE'] = existing_visible
    # Get existing folders list
    self.values['FIELDS'], self.values['DATA'] = engine.get_data(
      'SELECT name, description, visible '
      'FROM folders '
      'ORDER BY name')
    engine.close()
    configuration.set_locale(None)
    return self.get_template('folders.tpl',
      ARGS=self.args,
      VALUES=self.values,
      printable_text_for_encoding=self.printable_text_for_encoding)
