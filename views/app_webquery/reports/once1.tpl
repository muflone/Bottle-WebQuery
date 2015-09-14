<!DOCTYPE html>
<html>
  <head>
    <title>{{ VALUES['DESCRIPTION'] }}</title>
    <link type="text/css" rel="stylesheet" href="static/css/styles.css">
    <link type="text/css" rel="stylesheet" href="static/css/parameters.css">
    <link type="text/css" rel="stylesheet" href="static/css/table.css">
% include('%s/requires.inc' % MODULE)
  </head>

  <body>
% include('%s/div_error_messages.inc' % MODULE, ERRORS=VALUES['ERRORS'])
% include('%s/table_parameters.inc' % MODULE)
% include('%s/rows_count.inc' % MODULE)
% if VALUES['DATA']:
    <!-- Begin of response data -->
    <div class="tablesorter-wrapper">
      <table class="data">
        <thead>
          <tr>
  % for field in VALUES['FIELDS']:
            <th>{{ field }}</th>
  % end
          </tr>
        </thead>
        <tbody>
  % last_value = None
  % for row in VALUES['DATA']:
          <tr>
    % if last_value is None or last_value != row[0]:
            <td>{{ row[0] }}</td>
    % else:
            <td>&nbsp;</td>
    % end
    % for column in range(1, len(VALUES['FIELDS'])):
            <td>{{ !printable_text_for_encoding(row[column], VALUES['ENCODING']) }}</td>
    % end
          </tr>
    % last_value = row[0]
  % end
        </tbody>
      </table>
    </div>
    <!-- End of response data -->
% end
  </body>
</html>
