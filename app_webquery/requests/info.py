import StringIO
import sys

import configuration
import bottle
import user_agents

from .base import RequestBase
from app_constants import FILE_CONFIGURATION

class RequestInfo(RequestBase):
  def __init__(self):
    """Class initialization"""
    super(self.__class__, self).__init__()
    self.login_required = False

  def _gather_from_dict(self, context, excluded):
    """Return a list of keys and values from a context dictionary"""
    result = []
    for key in sorted(context.keys()):
      if not self._exclude_item(key, context[key], excluded):
        result.append((key, context[key]))
    return result

  def _gather_from_list(self, context, excluded):
    """Return a list of items from a context list"""
    result = []
    for item in range(len(context)):
      if not self._exclude_item(item, context[item], excluded):
        result.append((item, context[item]))
    return result

  def _gather_from_ini(self, ini, section, excluded):
    """Return a list of items from an ini setting file"""
    result = []
    result.append(('FILENAME', ini))
    for item in configuration.get_config_options(ini, section):
      if not self._exclude_item(item.upper(), item, excluded):
        result.append((item.upper(), 
          configuration.get_config_string(ini, section, item)))
    return result

  def _gather_members(self, context, excluded):
    """Return a list of keys and values from an object members"""
    return [
      (key, getattr(context, key))
      for key in dir(context)
      if not key.startswith('_') and
      not self._exclude_item(key, getattr(context, key), excluded)
    ]

  def _exclude_item(self, name, value, excluded):
    """Exclude item from name or by its value type"""
    # BUG: On ISeriesPython sometimes (?) the StringIO and FormsDict objects
    # are not properly printed
    return (excluded and name in excluded) or \
        isinstance(value, StringIO.StringIO) or \
        isinstance(value, bottle.FormsDict) or \
        callable(value)
    
  def serve(self):
    """Handle the request and serve the response"""
    super(self.__class__, self).serve()
    contexts = (
                ('General INI', self._gather_from_ini(
                  FILE_CONFIGURATION, 'APPLICATION',
                  None)),
                ('Sys', self._gather_members(sys, (
                  'builtin_module_names', 'copyright', 'modules', 'meta_path', 'path_importer_cache'))),
                ('App', self._gather_members(bottle.request.app, (
                  'routes', 'plugins'))),
                ('Routes', self._gather_from_list(bottle.request.app.routes, None)),
                ('Browser', self._gather_members(user_agents.parse(bottle.request.environ['HTTP_USER_AGENT']), None)),
                ('Request', self._gather_members(bottle.request, (
                  'environ', 'headers', 'route', 'urlparts'))),
                ('Environment', self._gather_from_dict(bottle.request.environ, (
                  'beaker.sessions',
                  'bottle.request', 'bottle.request.json',
                  'bottle.request.urlparts', 'bottle.route', 'route.handle',
                  'wsgi.errors'))),
                ('Session', self._gather_from_dict(self.session, None)),
                ('Session Object', self._gather_members(self.session.session._sess, (
                  'accessed_dict', 'cookie', 'request', 'namespace'))),
                ('Headers', self._gather_from_dict(bottle.request.headers, None)),
                ('Cookies', self._gather_from_dict(bottle.request.cookies, None)),
                ('Query', self._gather_from_dict(bottle.request.query, None)),
                ('Forms', self._gather_from_dict(bottle.request.forms, None)),
               )
    return self.get_template('info.tpl',
                             CONTEXTS = contexts)
