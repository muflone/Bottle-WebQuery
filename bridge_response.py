import bottle
import StringIO
import json

def bridge_response(response):
  """Handle both responses and redirects"""
  # Always close the connection after the request
  bottle.response.set_header('Connection', 'close')
  if type(response) is bottle.HTTPResponse:
    # Direct HTTP response like a static file already served (shouldn't happen)
    return response
  elif isinstance(response, StringIO.StringIO):
    # Direct StringIO response like a static file already served
    return response
  elif type(response) is dict:
    # Direct dictionary response
    return response
  elif type(response) is list:
    # Direct list response
    return json.dumps(response)
  elif response.startswith('REDIRECT:'):
    # Redirect to another page
    bottle.redirect(response[9:])
    return
  elif response.startswith('STATIC:'):
    # Static file served without the download option
    name, path = response[7:].split(':', 1)
    return bottle.static_file(name, root=path)
  elif response.startswith('DOWNLOAD:'):
    # Static file served with the download option
    name, path = response[9:].split(':', 1)
    return bottle.static_file(name, root=path, download=name)
  elif response.startswith('ABORT:'):
    # Error page
    code, message = response[6:].split(':', 1)
    bottle.abort(int(code), message)
  elif response.startswith('ERROR:'):
    # Error page without format
    code, message = response[6:].split(':', 1)
    return bottle.HTTPResponse(message, int(code))
  else:
    return response
