class AuthenticatorBase(object):
  ALGORITHM = None

  def __init__(self, db_settings):
    self.db_settings = db_settings

  def check_login(self, username, password):
    pass
