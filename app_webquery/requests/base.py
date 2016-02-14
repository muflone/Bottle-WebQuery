import bottle
import urllib2
import configuration
import logging
import StringIO
import csv

from app_webquery import authenticators
import app_webquery.paths
import app_webquery.parameters
import app_webquery.session
import app_webquery.webquery
from app_webquery.constants import MODULE_NAME, SETTINGS_DB

SESSION_AUTHENTICATED = 'authenticated'
SESSION_USERNAME = 'username'
SESSION_FULLNAME = 'fullname'
SESSION_ROLES = 'roles'

# List of engines modules
db_engines = app_webquery.webquery.detect_db_engines()

class RequestBase(object):
  def __init__(self):
    """Baseclass initialization for all the Request response pages"""
    self.paths = app_webquery.paths.Paths()
    self.params = app_webquery.parameters.Parameters()
    self.login_required = True
    self.valid_roles = []
    self.session = app_webquery.session.ExpiringSession(
      bottle.request.environ.get('beaker.session'))
    self.engines = db_engines

  def serve(self):
    """Base method for serving the response page"""
    if not self.authentication_required():
      if bool(self.params.get_username()):
        bottle.abort(403, 'Invalid username or password')
      else:
        bottle.redirect('login?forward=%s%s%s' % (
          self.get_request_page(),
          urllib2.quote('?'),
          urllib2.quote(self.get_request_query())))
    elif SESSION_ROLES in self.session and self.valid_roles:
      # Check for a valid role
      if not ((self.valid_roles) and any(
          role in self.valid_roles for role in self.session[SESSION_ROLES])):
        error_message = 'Unauthorized access for the user "{username}".\n' \
                        'User roles: {user_roles}\n' \
                        'Valid roles: {page_roles}'.format(
                          username=self.session[SESSION_USERNAME],
                          user_roles=', '.join(self.session[SESSION_ROLES]),
                          page_roles=', '.join(self.valid_roles))
        bottle.abort(403, error_message)

  def get_template(self, template_name, **extra_arguments):
    """Return the template associated to the template_name with its
    module and extra arguments"""
    return bottle.template(self.paths.template(template_name),
                           MODULE=MODULE_NAME,
                           OBJECT=self,
                           quote=urllib2.quote,
                           REQUEST=bottle.request,
                           ACTION=self.params.get_action(),
                           **extra_arguments)

  def get_request_page(self):
    """Return the requested page"""
    return bottle.request.fullpath

  def get_request_query(self):
    """Return the request querystring"""
    return bottle.request.query_string

  def open_settings_db(self):
    """Open the common settings database"""
    logging.debug('Opening settings database: %s' % SETTINGS_DB)
    engine = self.open_db_from_engine_type(
      engine_type='sqlite3',
      name='Settings',
      connection=configuration.get_database(MODULE_NAME, SETTINGS_DB),
      username=None,
      password=None,
      database=None,
      server=None)
    engine.open()
    return engine

  def open_db_from_engine_type(self, engine_type, name, connection, username, password, database, server):
    """Open a database by its connection using an engine type"""
    engine_class = self.engines.get(engine_type, None)
    if engine_class:
      logging.info('Opening database: (type: %s, name: %s)' % (
        engine_type, name))
      engine = engine_class(connection, username, password, database, server)
      engine.open()
      return engine
    else:
      logging.critical('Unable to open the catalog %s, '
        'Engine %s not found' % (name, engine_type))

  def printable_text_for_encoding(self, text, encoding):
    """Return a string valid for printing"""
    if text is None:
      return 'Null'
    elif type(text) is unicode:
      return text.encode(encoding).replace('\\n', '<br />')
    elif type(text) is str:
      return text.decode(encoding).replace('\\n', '<br />')
    elif type(text) is float:
      return '%.2f' % text
    else:
      return str(text).replace('\\n', '<br />')

  def prepare_connection_string(self, connection, engine, server, database, username, password):
    """Return a prepared connection string"""
    return connection % {
      'ENGINE': engine,
      'SERVER': server,
      'DATABASE': database,
      'USERNAME': username,
      'PASSWORD': password,
    }

  def set_content_type(self, content_type):
    """Set the content-type"""
    bottle.response.set_header('Content-Type', content_type)

  def set_filename(self, filename):
    """Set the content-disposition filename"""
    bottle.response.set_header('Content-Disposition',
      'attachment; filename="%s"' % filename)

  def output_to_csv(self, data):
    """Returns data in csv format"""
    writer = StringIO.StringIO()
    csvwriter = csv.writer(
      writer,
      delimiter=',',
      quotechar='"',
      quoting=csv.QUOTE_NONNUMERIC)
    csvwriter.writerows(data)
    writer.seek(0)
    return writer

  def authentication_required(self):
    """Check if the user session is authenticated"""
    if self.login_required:
      if SESSION_AUTHENTICATED in self.session:
        # Already authenticated (in session)
        return True
      elif self.params.get_username():
        # Check for automatic login by providing valid username and password
        result = authenticators.check_login(self.open_settings_db(),
                                            self.params.get_username(),
                                            self.params.get_password())
        if result:
          self.set_authenticated(
            status=True,
            username=result[authenticators.KEY_USERNAME],
            fullname=result[authenticators.KEY_FULLNAME],
            roles=result[authenticators.KEY_ROLES])
          return True
        else:
          return False
      else:
        # Not authenticated
        return False
    else:
      # Authentication not needed
      return True

  def set_authenticated(self, status, username, fullname, roles):
    """Set the authentication status"""
    if status:
      self.session[SESSION_AUTHENTICATED] = status
      self.session[SESSION_USERNAME] = username
      self.session[SESSION_FULLNAME] = fullname
      self.session[SESSION_ROLES] = roles
    else:
      self.session.delete()
