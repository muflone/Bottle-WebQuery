import pymssql
import logging

from engine_base import WebQueryEngineBase

class WebQueryEngineMSSQL(WebQueryEngineBase):
  description = 'Microsoft SQL Server (pymssql)'
  descriptor = 'mssql'

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
    self.connection = pymssql.connect(
      server=self.connection_string,
      user=self.username,
      password=self.password,
      database=self.database)

  def close(self):
    """Close the connection"""
    super(self.__class__, self).close()
    if self.connection:
      self.connection.close()
      self.connection = None

  def execute(self, statement, parameters=None):
    """Execute a statement"""
    super(self.__class__, self).execute(statement, parameters)
    cursor = self.connection.cursor()
    if parameters is None:
      cursor.execute(statement)
    else:
      cursor.execute(statement, parameters)
    cursor.close()

  def get_data(self, statement, replaces=None, parameters=None):
    """Execute a statement and returns the data"""
    super(self.__class__, self).get_data(statement, replaces, parameters)
    return super(self.__class__, self).get_data_full(
      statement, replaces, parameters, True)

  def list_tables(self):
    """List all the tables"""
    super(self.__class__, self).list_tables()
    tables = []
    for row in self.get_data('SELECT QuoteName(User_Name(uid)) + '
      '\'.\' + QuoteName(Object_Name(id)) '
      'FROM sysObjects WHERE xtype IN (\'S\', \'U\', \'V\') '
      'ORDER BY User_Name(uid), Object_Name(id)')[1]:
      tables.append(row[0])
    return tables

  def save(self):
    """Save any pending data"""
    super(self.__class__, self).save()
    self.connection.commit()

engine_classes = (WebQueryEngineMSSQL, )
