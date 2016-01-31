<!DOCTYPE html>
<html>
  <head>
    <title>Info</title>
    <link type="text/css" rel="stylesheet" href="static/css/styles.css">
  </head>

  <body>
    <div class="center">|
% for context_string, context in CONTEXTS:
      <a href="#{{ context_string }}">{{ context_string }}</a> |
% end
    </div>
% for context_string, context in CONTEXTS:
    <h1><a name="{{ context_string }}"></a>{{ context_string }}</h1>
  % for k, v in context:
  %   if type(v) in (int, float):
  %     icon_type = 'type_number.png'
  %   elif type(v) in (str, unicode):
  %     icon_type = 'type_string.png'
  %   elif type(v) in (bool, ):
  %     icon_type = 'type_boolean.png'
  %   elif type(v) in (tuple, list, dict):
  %     icon_type = 'type_list.png'
  %   elif isinstance(v, object):
  %     icon_type = 'type_object.png'
  %   else:
  %     icon_type = 'unknown.png'
  %   end
    <div><img src="static/images/{{ quote(icon_type) }}" title="{{ type(v) }}"> {{ k }} = {{ v }}</div>
  % end
  <hr />
% end
% include('%s/footer.inc' % MODULE)
  </body>
</html>
