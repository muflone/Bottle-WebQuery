<!DOCTYPE html>
<html>
  <head>
    <title>Configure queries</title>
    <link type="text/css" rel="stylesheet" href="static/css/styles.css">
    <link type="text/css" rel="stylesheet" href="static/css/parameters.css">
    <link type="text/css" rel="stylesheet" href="static/css/table.css">
  </head>

  <body>
% include('%s/div_error_messages.inc' % MODULE, ERRORS=VALUES['ERRORS'])
    <!-- Begin of request form -->
    <form method="get" accept-charset="UTF-8">
      <input type="hidden" name="uuid" value="{{ ARGS['UUID'] }}">
      <table id="parameters">
        <caption>Query configuration</caption>
        <tbody>
          <tr>
            <th>Query name:</th>
            <td><input type="text" name="name" value="{{ ARGS['NAME'] }}"></td>
          </tr>
          <tr>
            <th>Description:</th>
            <td><input type="text" name="description" value="{{ ARGS['DESCRIPTION'] }}"></td>
          </tr>
          <tr>
            <th>Associated catalog:</th>
            <td><select name="catalog">
% include('%s/select_options_from_data.inc' % MODULE, DATA_ROWS=False, FIELD_ID=0, FIELD_VALUE=1, SELECTED=ARGS['CATALOG'], DATA=VALUES['CATALOGS'])
            </select></td>
          </tr>
          <tr>
            <th>SQL statement:</th>
            <td><textarea name="sql">{{ ARGS['SQL'] }}</textarea></td>
          </tr>
          <tr>
            <th>Parameters:</th>
            <td><textarea name="parameters">{{ ARGS['PARAMETERS'] }}</textarea></td>
          </tr>
          <tr>
            <td>Report:</td>
            <td><select name="report">
% include('%s/select_options_from_data.inc' % MODULE, DATA_ROWS=False, FIELD_ID=0, FIELD_VALUE=1, SELECTED=ARGS['REPORT'], DATA=VALUES['REPORTS'])
            </select></td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="2">
              <input type="submit" name="confirm" value="Confirm">
% if ARGS['CATALOG'] and not VALUES['ERRORS']:
              <input type="button" name="cancel" value="Cancel" onclick="javascript:location.href='queries';">
              <input type="submit" name="delete" value="Delete">
% end
            </td>
          </tr>
        </tfoot>
      </table>
    </form>
    <!-- End of request form -->

% if VALUES['DATA']:
    <hr />
    <!-- Begin of response data -->
    <table class="data">
      <caption>Existing queries</caption>
      <thead>
        <tr>
          <th>Name</th>
          <th>Description</th>
          <th>Catalog</th>
          <th>Report</th>
        </tr>
      </thead>
      <tbody>
  % for row in VALUES['DATA']:
        <tr>
          <td><a href="run?uuid={{ row[0] }}"><img src="static/images/run.png"></a>
            <a href="?uuid={{ row[0] }}">{{ row[1] }}</a></td>
          <td>{{ row[2].encode('utf-8') }}</td>
          <td>{{ row[3].encode('utf-8') }}</td>
          <td>{{ row[4].encode('utf-8') }}</td>
        </tr>
  % end
      </tbody>
    </table>
    <!-- End of response data -->
% end
  </body>
</html>
