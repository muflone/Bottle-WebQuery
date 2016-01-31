import urllib2

from app_webquery import authenticators

from .base import RequestBase

class RequestLogin(RequestBase):
  def __init__(self):
    """Class initialization"""
    super(self.__class__, self).__init__()
    self.login_required = False

  def serve(self):
    """Handle the request and serve the response"""
    super(self.__class__, self).serve()
    invalid = False
    arg_username = self.params.get_username()
    arg_password = self.params.get_password()
    arg_forward = self.params.get_forward()
    if self.params.get_action() == 'logout':
      # When a logout was issued the session is cleared (invalidated or deleted)
      self.set_authenticated(
        status=False,
        username='',
        fullname='',
        roles='')
    else:
      if arg_username:
        # Authenticate for valid access
        result = authenticators.check_login(self.open_settings_db(),
                                            arg_username,
                                            arg_password)
        if result:
          self.set_authenticated(
            status=True,
            username=result[authenticators.KEY_USERNAME],
            fullname=result[authenticators.KEY_FULLNAME],
            roles=result[authenticators.KEY_ROLES])
          if arg_forward:
            return 'REDIRECT:%s' % urllib2.unquote(arg_forward)
          else:
            return 'REDIRECT:queries'
        else:
          # When the authentication has not succeeded then session is
          # not cleared (not invalidated nor deleted) and a simple message
          # with invalid credentials is shown
          invalid = True
    return self.get_template('login.tpl',
                             INVALID=invalid,
                             FORWARD=arg_forward)
