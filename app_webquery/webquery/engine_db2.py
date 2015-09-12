import logging

import configuration
from app_webquery.constants import SETTINGS_FILENAME

try:
  # Use the db2 native module for iSeries
  import db2
  logging.debug('Using native db2 for iSeries module')
  __NATIVE_DB2__ = True
except ImportError:
  # Use the JDBC bridge api to access to the remote server
  import jaydebeapi
  logging.debug('Using jaydebeapi for JDBC module')
  __NATIVE_DB2__ = False

from engine_base import WebQueryEngineBase

class WebQueryEngineDB2(WebQueryEngineBase):
  description = 'IBM DB2'
  descriptor = 'db2'

  def __init__(self, connection, username, password, database, server):
    """
    Create a new connection using the specified connection string, username
    and password.
    """
    super(self.__class__, self).__init__(
      connection, username, password, database, server)
    self.connection = None
  
  def open(self):
    """Open the connection"""
    super(self.__class__, self).open()
    if __NATIVE_DB2__:
      # Connect to the local system using db2
      self.connection = db2.connect('')
    else:
      # Connect to the remote system using JDBC
      self.connection = jaydebeapi.connect(
                            jclassname='com.ibm.as400.access.AS400JDBCDriver',
                            driver_args=[
                              'jdbc:as400://%s' % self.connection_string,
                              self.username,
                              self.password],
                              jars=configuration.get_config_string(
                                SETTINGS_FILENAME,
                                'GENERAL',
                                'JT400.JAR'),
                            libs=None)

  def close(self):
    """Close the connection"""
    super(self.__class__, self).close()
    if self.connection:
      self.connection.close()
      self.connection = None

  def execute(self, statement, parameters=None):
    """Execute a statement"""
    super(self.__class__, self).execute(statement, parameters)
    if parameters is None:
      self.cursor.execute(statement)
    else:
      self.cursor.execute(statement, parameters)

  def get_data(self, statement, replaces=None, parameters=None):
    """Execute a statement and returns the data"""
    super(self.__class__, self).get_data(statement, replaces, parameters)
    cursor = self.connection.cursor()
    if replaces is not None:
      statement = statement % replaces
    statement = str(statement)
    if parameters is None:
      cursor.execute(statement)
    else:
      cursor.execute(statement, parameters)
    if cursor.description is not None:
      fields = [r[0] for r in cursor.description]
      data = cursor.fetchall()
      logging.debug('%s: Got %d records' % (
        self.__class__.__name__, len(data)))
    else:
      fields = None
      data = None
      logging.debug('%s: No records were returned' % (
        self.__class__.__name__, ))
    cursor.close()
    self.save()
    return (fields, data)

  def list_tables(self):
    """List all the tables"""
    super(self.__class__, self).list_tables()
    tables = []
    for row in self.get_data('SELECT '
      'TRIM(system_table_schema) || \'.\' || '
      'TRIM(system_table_name) '
      'FROM qsys2.systables '
      'ORDER BY system_table_schema, system_table_name')[1]:
      tables.append(row[0].encode('utf-8'))
    return tables

  def save(self):
    """Save any pending data"""
    super(self.__class__, self).save()
    self.connection.commit()

engine_classes = (WebQueryEngineDB2, )
