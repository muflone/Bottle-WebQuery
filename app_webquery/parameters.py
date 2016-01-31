import bottle

class Parameters(object):
  def __init__(self):
    pass

  def get_item(self, name, fallback=''):
    """Get the argument specified by name"""
    return bottle.request.params.get(name, fallback)

  def get_utf8_item(self, name, fallback=''):
    """Get the argument specified by name as unicode string"""
    return bottle.request.params.get(name, fallback).decode('utf-8')

  def get_all(self, name):
    """Get all the arguments specified by name"""
    return bottle.request.params.getall(name)

  def get_action(self):
    """Get the action argument"""
    return self.get_item('action')

  def get_username(self):
    """Get the username argument"""
    return self.get_item('username').lower()

  def get_password(self):
    """Get the password argument"""
    return self.get_item('password')

  def get_forward(self):
    """Get the forward argument"""
    return self.get_item('forward')
