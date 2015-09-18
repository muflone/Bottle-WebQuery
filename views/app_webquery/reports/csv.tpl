% if VALUES['DATA']:
{{ 'CSV:' }}\\
  % str_row = ''
  % for field in VALUES['FIELDS']:
    % if len(str_row) > 0:
    %   str_row += ','
    % end
    % str_row += '"%s"' % field
  % end
{{ !str_row }}
  % for row in VALUES['DATA']:
    % str_row = ''
    % for column in row:
      % if len(str_row) > 0:
      %   str_row += ','
      % end
      % if isinstance(column, str) or isinstance(column, unicode):
        % str_row += '"%s"' % column
      % elif isinstance(column, int):
        % str_row += '%d' % column
      % elif isinstance(column, float):
        % str_row += '%.5f' % column
      % else:
        % str_row += str(type(column))
      % end
    % end
{{ !str_row }}
  % end
% else:
<!DOCTYPE html>
<html>
  <head>
    <title>{{ VALUES['DESCRIPTION'] }}</title>
    <link type="text/css" rel="stylesheet" href="static/css/styles.css">
    <link type="text/css" rel="stylesheet" href="static/css/parameters.css">
  % include('%s/requires.inc' % MODULE)
  </head>

  <body>
  % include('%s/div_error_messages.inc' % MODULE, ERRORS=VALUES['ERRORS'])
  % include('%s/table_parameters.inc' % MODULE)
  </body>
</html>
% end
