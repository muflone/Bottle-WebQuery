from .base import RequestBase

class RequestLogout(RequestBase):
  def __init__(self):
    """Class initialization"""
    super(self.__class__, self).__init__()
    self.login_required = False

  def serve(self):
    """Handle the request and serve the response"""
    super(self.__class__, self).serve()
    return 'REDIRECT:login?action=logout'
