import sqlite3
import logging

from engine_base import WebQueryEngineBase

class WebQueryEngineSQLite3(WebQueryEngineBase):
  description = 'SQLite 3'
  descriptor = 'sqlite3'

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
    self.connection = sqlite3.connect(self.connection_string)

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
      self.connection.execute(statement)
    else:
      self.connection.execute(statement, parameters)

  def get_data(self, statement, replaces=None, parameters=None):
    """Execute a statement and returns the data"""
    super(self.__class__, self).get_data(statement, replaces, parameters)
    cursor = self.connection.cursor()
    if replaces is not None:
      statement = statement % replaces
    if parameters is None:
      cursor.execute(statement)
    else:
      cursor.execute(statement, parameters)
    fields = [r[0] for r in cursor.description]
    data = cursor.fetchall()
    logging.info('%s: Got %d records' % (
      self.__class__.__name__, len(data)))
    cursor.close()
    return (fields, data)

  def list_tables(self):
    """List all the tables"""
    super(self.__class__, self).list_tables()
    tables = []
    for row in self.get_data('SELECT name FROM sqlite_master '
          'WHERE type="table" ORDER BY name')[1]:
      tables.append(row[0])
    return tables

  def save(self):
    """Save any pending data"""
    super(self.__class__, self).save()
    self.connection.commit()

engine_classes = (WebQueryEngineSQLite3, )
