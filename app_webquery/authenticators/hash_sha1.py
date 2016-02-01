import hashlib

from .base import AuthenticatorBase

class AuthenticatorSHA1(AuthenticatorBase):
  ALGORITHM = 'sha1'

  def __init__(self, db_settings):
    super(self.__class__, self).__init__(db_settings)

  def check_login(self, username, password):
    super(self.__class__, self).check_login(username, password)
    return self.check_password(username, hashlib.sha1(password).hexdigest())
