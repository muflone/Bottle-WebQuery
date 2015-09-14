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
  % include('%s/tablesorter.inc' % MODULE, INCLUDE='pager')
      <table class="data">
        <thead>
          <tr>
  % for field in VALUES['FIELDS']:
            <th>{{ field }}</th>
  % end
          </tr>
        </thead>
        <tbody>
  % for row in VALUES['DATA']:
          <tr>
    % for column in row:
            <td>{{ !printable_text_for_encoding(column, VALUES['ENCODING']) }}</td>
    % end
          </tr>
  % end
        </tbody>
      </table>
  % include('%s/tablesorter.inc' % MODULE, INCLUDE='pager')
    </div>
    <!-- End of response data -->
% end
  </body>
</html>
