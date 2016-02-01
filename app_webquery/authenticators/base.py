class AuthenticatorBase(object):
  ALGORITHM = None

  def __init__(self, db_settings):
    self.db_settings = db_settings

  def check_login(self, username, password):
    pass

  def check_password(self, username, password):
    result = self.db_settings.get_data(
      'SELECT password FROM users WHERE name=? and password=?',
      None,
      (username, password))[1]
    if result:
      return True
    else:
      return False
