import os.path

from .constants import MODULE_NAME

class Paths(object):
  def __init__(self):
    pass

  def template(self, template_name):
    """Get the path of a template"""
    return os.path.join(MODULE_NAME, template_name)
