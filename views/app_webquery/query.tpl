<!DOCTYPE html>
<html>
  <head>
    <title>Create query</title>
    <link type="text/css" rel="stylesheet" href="static/css/styles.css">
    <link type="text/css" rel="stylesheet" href="static/css/parameters.css">
    <link type="text/css" rel="stylesheet" href="static/css/table.css">
% include('%s/codemirror.inc' % MODULE, INCLUDE='stylesheets')
% include('%s/codemirror.inc' % MODULE, INCLUDE='scripts')
  </head>

  <body>
% include('%s/codemirror.inc' % MODULE, INCLUDE='body')
    <!-- Begin of request form -->
    <form method="get">
      <table id="parameters">
        <caption>Query configuration</caption>
        <tbody>
          <tr>
            <th>Associated catalog:</th>
            <td><select name="catalog">
% include('%s/select_options_from_data.inc' % MODULE, DATA_ROWS=False, FIELD_ID=0, FIELD_VALUE=1, SELECTED=ARGS['CATALOG'], DATA=VALUES['CATALOGS'])
            </select></td>
          </tr>
          <tr>
            <th>SQL statement:</th>
            <td><textarea name="sql" id="codemirror" placeholder="< SQL CODE >">{{ ARGS['SQL'] }}</textarea></td>
          </tr>
          <tr>
            <th>Available tables:</th>
            <td><select name="tables" size="10">
% include('%s/select_options_from_data.inc' % MODULE, DATA_ROWS=False, FIELD_ID=0, FIELD_VALUE=0, SELECTED=None, DATA=VALUES['TABLES'])
            </select></td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="2">
              <input type="submit" name="confirm" value="Confirm">
              <input type="button" name="cancel" value="Cancel" onclick="javascript:location.href='query';">
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
          <td>{{ printable_text_for_encoding(column, VALUES['ENCODING']) }}</td>
    % end
        </tr>
  % end
      </tbody>
    </table>
    <!-- End of response data -->
% end
  </body>
</html>
