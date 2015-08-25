import logging

class WebQueryEngineBase(object):
  def __init__(self, connection=None, username=None, password=None, database=None):
    """
    Create a new connection using the specified connection string, username
    and password.
    """
    self.connection_string = connection
    self.username = username
    self.password = password
    self.database = database
  
  def open(self):
    """Open the connection"""
    logging.info('%s: Opening database' % self.__class__.__name__)
  
  def close(self):
    """Close the connection"""
    logging.info('%s: Closing database' % self.__class__.__name__)

  def execute(self, statement, parameters=None):
    """Execute a statement"""
    logging.info('%s: Execute from database' % self.__class__.__name__)

  def get_data(self, statement, replaces=None, parameters=None):
    """Execute a statement and returns the data"""
    logging.info('%s: Get data from database' % self.__class__.__name__)
    logging.debug('%s: Statement: %s' % (
      self.__class__.__name__, statement))
    if replaces is not None:
      logging.debug('%s: Replaces: %s' % (
        self.__class__.__name__, replaces))
      logging.debug('%s: Replaced statement: %s' % (
        self.__class__.__name__, statement % replaces))
    logging.debug('%s: Parameters: %s' % (
      self.__class__.__name__, parameters))

  def list_tables(self):
    """List all the tables"""
    logging.info('%s: List tables from database' % self.__class__.__name__)

  def save(self):
    """Save any pending data"""
    logging.info('%s: Saving data in database' % self.__class__.__name__)
