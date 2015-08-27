<!DOCTYPE html>
<html>
  <head>
    <title>Configure catalogs</title>
    <link type="text/css" rel="stylesheet" href="static/css/styles.css">
    <link type="text/css" rel="stylesheet" href="static/css/parameters.css">
    <link type="text/css" rel="stylesheet" href="static/css/table.css">
  </head>

  <body>
% include('%s/div_error_messages.inc' % MODULE, ERRORS=VALUES['ERRORS'])
    <!-- Begin of request form -->
    <form method="get" accept-charset="UTF-8">
      <table id="parameters">
        <caption>Catalog configuration</caption>
        <tbody>
          <tr>
            <td>Catalog name:</td>
            <td><input type="text" name="catalog" value="{{ ARGS['CATALOG'] }}"></td>
          </tr>
          <tr>
            <td>Description:</td>
            <td><input type="text" name="description" value="{{ ARGS['DESCRIPTION'] }}"></td>
          </tr>
          <tr>
            <td>Engine:</td>
            <td><select name="engine">
% include('%s/select_options_from_data.inc' % MODULE, DATA_ROWS=False, FIELD_ID=0, FIELD_VALUE=1, SELECTED=ARGS['ENGINE'], DATA=VALUES['ENGINES'])
            </select></td>
          </tr>
          <tr>
            <td>Connection string:</td>
            <td><input type="text" name="connection" value="{{ ARGS['CONNECTION'] }}"></td>
          </tr>
          <tr>
            <td>Server:</td>
            <td><input type="text" name="server" value="{{ ARGS['SERVER'] }}"></td>
          </tr>
          <tr>
            <td>Database:</td>
            <td><input type="text" name="database" value="{{ ARGS['DATABASE'] }}"></td>
          </tr>
          <tr>
            <td>Username:</td>
            <td><input type="text" name="username" value="{{ ARGS['USERNAME'] }}"></td>
          </tr>
          <tr>
            <td>Password:</td>
            <td><input type="password" name="password" value="{{ ARGS['PASSWORD'] }}"></td>
          </tr>
          <tr>
            <td>Encoding:</td>
            <td><input type="text" name="encoding" value="{{ ARGS['ENCODING'] }}"></td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="2">
              <input type="submit" name="confirm" value="Confirm">
% if ARGS['CATALOG'] and not VALUES['ERRORS']:
              <input type="button" name="cancel" value="Cancel" onclick="javascript:location.href='catalogs';">
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
      <caption>Existing catalogs</caption>
      <thead>
        <tr>
          <th>Name</th>
          <th>Description</th>
          <th>Engine</th>
          <th>Connection string</th>
          <th>Database</th>
        </tr>
      </thead>
      <tbody>
  % for row in VALUES['DATA']:
        <tr>
          <td><a href="?catalog={{ row[0] }}">{{ row[0] }}</a></td>
          <td>{{ row[1] }}</td>
          <td>{{ row[2] }}</td>
          <td>{{ row[3] }}</td>
          <td>{{ row[4] }}</td>
        </tr>
  % end
      </tbody>
    </table>
    <!-- End of response data -->
% end
  </body>
</html>
