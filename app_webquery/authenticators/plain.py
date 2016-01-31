from .base import AuthenticatorBase

class AuthenticatorPlain(AuthenticatorBase):
  ALGORITHM = 'plain'

  def __init__(self, db_settings):
    super(self.__class__, self).__init__(db_settings)

  def check_login(self, username, password):
    super(self.__class__, self).check_login(username, password)
    result = self.db_settings.get_data(
      'SELECT name FROM users WHERE name=? and password=?',
      None,
      (username, password))[1]
    if result:
      return True
    return False
