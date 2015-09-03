import uuid
import logging

import configuration
from .base import RequestBase

class RequestQueries(RequestBase):
  def __init__(self):
    """Class initialization"""
    RequestBase.__init__(self)

  def serve(self):
    """Handle the request and serve the response"""
    RequestBase.serve(self)
    # Request values
    self.args = {}
    self.args['FORMAT'] = self.params.get_item('format')
    self.args['CONFIRM'] = self.params.get_item('confirm')
    self.args['DELETE'] = self.params.get_item('delete')
    self.args['UUID'] = self.params.get_item('uuid')
    self.args['CATALOG'] = self.params.get_utf8_item('catalog')
    self.args['NAME'] = self.params.get_utf8_item('name')
    self.args['DESCRIPTION'] = self.params.get_utf8_item('description')
    self.args['SQL'] = self.params.get_utf8_item('sql')
    self.args['FOLDER'] = self.params.get_utf8_item('folder')
    self.args['REPORT'] = self.params.get_utf8_item('report')
    self.args['PARAMETERS'] = self.params.get_utf8_item('parameters')
    # Avoid empty description
    if not self.args['DESCRIPTION']:
      self.args['DESCRIPTION'] = self.args['NAME']
    # Response values
    self.values = {}
    self.values['ERRORS'] = []
    self.values['DATA'] = None
    self.values['REPORTS'] = (
      ('table', 'Vertical table'),
      ('card', 'Horizontal table'),
      ('once1', 'Vertical table which shows only once the first element'),
    )
    existing_id = 0
    existing_catalog = ''
    existing_query = ''
    existing_description = ''
    existing_sql = ''
    existing_folder = ''
    existing_report = ''
    existing_parameters = ''
    
    engine = self.open_settings_db()
    # The query configuration is valid when a format is not requested
    if not self.args['FORMAT']:
      # Get existing catalog details
      if self.args['UUID']:
        existing_fields, existing_data = engine.get_data(
            'SELECT uuid, catalog, name, description, sql, folder, '
            'report, parameters '
            'FROM queries '
            'WHERE uuid=?',
            None,
            (self.args['UUID'], ))
        if existing_data:
          if self.args['DELETE']:
            # Delete existing query
            logging.debug('Deleting query: %s' % self.args['UUID'])
            engine.execute('DELETE FROM queries WHERE uuid=?', (
              self.args['UUID'], ))
            engine.save()
            logging.info('Deleted query: %s' % self.args['UUID'])
            # Reload empty page afer save
            return 'REDIRECT:queries'
          else:
            existing_id, existing_catalog, existing_query, \
              existing_description, existing_sql, existing_folder, \
              existing_report, existing_parameters = existing_data[0]
      # Check the requested arguments for errors
      if self.args['CONFIRM']:
        # Check parameters for errors
        if not self.args['NAME']:
          self.values['ERRORS'].append('Missing query name')
        if not self.args['SQL']:
          self.values['ERRORS'].append('Missing SQL statement')
        if not self.args['REPORT']:
          self.values['ERRORS'].append('Missing report')
        # Process data
        if not self.values['ERRORS']:
          if existing_id:
            # Update existing query
            logging.debug('Updating query: %s' % self.args['UUID'])
            engine.execute('UPDATE queries '
                           'SET catalog=?, name=?, description=?, sql=?, '
                           'folder=?, report=?, parameters=? '
                           'WHERE uuid=?', (
                             self.args['CATALOG'],
                             self.args['NAME'],
                             self.args['DESCRIPTION'],
                             self.args['SQL'],
                             self.args['FOLDER'],
                             self.args['REPORT'],
                             self.args['PARAMETERS'],
                             self.args['UUID']))
            logging.info('Updated query: %s' % self.args['UUID'])
          else:
            # Insert new query
            logging.debug('Inserting query: %s' % self.args['NAME'])
            engine.execute('INSERT INTO queries(uuid, catalog, name, '
                           'description, sql, folder, report, '
                           'parameters) '
                           'VALUES(?, ?, ?, ?, ?, ?, ?, ?)', (
                           str(uuid.uuid4()),
                           self.args['CATALOG'],
                           self.args['NAME'],
                           self.args['DESCRIPTION'],
                           self.args['SQL'],
                           self.args['FOLDER'],
                           self.args['REPORT'],
                           self.args['PARAMETERS']))
            logging.info('Inserted catalog: %s' % self.args['NAME'])
          engine.save()
          # Reload empty page afer save
          return 'REDIRECT:queries'
      else:
        # Use existing details
        self.args['CATALOG'] = existing_catalog
        self.args['NAME'] = existing_query
        self.args['DESCRIPTION'] = existing_description
        self.args['SQL'] = existing_sql
        self.args['FOLDER'] = existing_folder
        self.args['REPORT'] = existing_report
        self.args['PARAMETERS'] = existing_parameters
      # Get existing catalogs list
      self.values['FIELDS'], self.values['CATALOGS'] = engine.get_data(
        'SELECT name, description FROM catalogs '
        'ORDER BY name')
      # Get existing folders list
      self.values['FIELDS'], self.values['FOLDERS'] = engine.get_data(
        'SELECT name, description FROM folders '
        'ORDER BY name')
    # Get existing queries list
    self.values['FIELDS'], self.values['DATA'] = engine.get_data(
      'SELECT queries.uuid, queries.folder, queries.name, '
      'queries.description, queries.catalog, queries.report, '
      'folders.visible, folders.description '
      'FROM queries '
      'LEFT JOIN folders '
      'ON folders.name=queries.folder '
      'ORDER BY queries.folder, queries.catalog, queries.name')
    engine.close()
    if not self.args['FORMAT']:
      # Serve the queries page
      configuration.set_locale(None)
      return self.get_template('queries.tpl',
        ARGS=self.args,
        VALUES=self.values,
        printable_text_for_encoding=self.printable_text_for_encoding)
    elif self.args['FORMAT'] == 'json':
      # JSON format queries list
      results = []
      folder = {}
      for row in self.values['DATA']:
        # Add a new folder
        if folder.get('title') != row[1].encode('utf-8'):
          queries = []
          folder = {}
          folder['title'] = row[1].encode('utf-8')
          folder['folder'] = True
          folder['expanded'] = True
          folder['tooltip'] = row[7].encode('utf-8')
          folder['children'] = queries
          results.append(folder)
        # Add the query to the queries list object
        queries.append({
          'title': '<a href="?uuid=%s">%s</a>' % (row[0], row[2]),
          'tooltip': row[3].encode('utf-8'),
          'key': row[0],
          'catalog': row[4],
          'report': row[5],
        })
      return results
    else:
      # Unexpected format
      return 'ABORT:500:Unexpected format: %s' % self.args['FORMAT']
