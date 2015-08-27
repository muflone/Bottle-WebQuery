import pypyodbc
import logging

from engine_base import WebQueryEngineBase

class WebQueryEngineODBC(WebQueryEngineBase):
  description = 'ODBC'
  descriptor = 'odbc'

  def __init__(self, connection=None, username=None, password=None, database=None):
    """
    Create a new connection using the specified connection string, username
    and password.
    """
    super(WebQueryEngineODBC, self).__init__(
      connection, username, password, database)
    self.connection = None
  
  def open(self):
    """Open the connection"""
    super(WebQueryEngineODBC, self).open()
    self.connection = pypyodbc.connect(
      connectString = '%s%s' % (self.connection_string, 
        self.database if self.database else ''))

  def close(self):
    """Close the connection"""
    super(WebQueryEngineODBC, self).close()
    if self.connection:
      self.connection.close()
      self.connection = None

  def execute(self, statement, parameters=None):
    """Execute a statement"""
    super(WebQueryEngineODBC, self).execute(statement, parameters)
    cursor = self.connection.cursor()
    if parameters is None:
      cursor.execute(statement)
    else:
      cursor.execute(statement, parameters)
    cursor.close()

  def get_data(self, statement, replaces=None, parameters=None):
    """Execute a statement and returns the data"""
    super(WebQueryEngineODBC, self).get_data(statement, replaces, parameters)
    if replaces is not None:
      statement = statement % replaces
    cursor = self.connection.cursor()
    if parameters is None:
      cursor.execute(statement)
    else:
      cursor.execute(statement, parameters)
    fields = [r[0] for r in cursor.description]
    data = cursor.fetchall()
    cursor.close()
    logging.info('%s: Got %d records' % (
      self.__class__.__name__, len(data)))
    return (fields, data)

  def list_tables(self):
    """List all the tables"""
    super(WebQueryEngineODBC, self).list_tables()
    tables = []
    return tables

  def save(self):
    """Save any pending data"""
    super(WebQueryEngineODBC, self).save()
    self.connection.commit()

engine_classes = (WebQueryEngineODBC, )
