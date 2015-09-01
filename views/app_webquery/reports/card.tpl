<!DOCTYPE html>
<html>
  <head>
    <title>{{ VALUES['DESCRIPTION'] }}</title>
    <link type="text/css" rel="stylesheet" href="static/css/styles.css">
    <link type="text/css" rel="stylesheet" href="static/css/parameters.css">
    <link type="text/css" rel="stylesheet" href="static/css/card.css">
% include('%s/requires.inc' % MODULE)
  </head>

  <body>
% include('%s/div_error_messages.inc' % MODULE, ERRORS=VALUES['ERRORS'])
% include('%s/table_parameters.inc' % MODULE)
% if VALUES['DATA']:
    <!-- Begin of response data -->
  % for row in VALUES['DATA']:
    <table class="data">
      <tbody>
    % for column in range(len(VALUES['FIELDS'])):
        <tr>
          <th>{{ VALUES['FIELDS'][column] }}</th>
          <td>{{ printable_text_for_encoding(row[column], VALUES['ENCODING']) }}</td>
        </tr>
    % end
      </tbody>
    </table>
  % end
    <!-- End of response data -->
% end
  </body>
</html>
