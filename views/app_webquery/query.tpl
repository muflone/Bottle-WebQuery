<!DOCTYPE html>
<html>
  <head>
    <title>Create query</title>
    <link type="text/css" rel="stylesheet" href="static/css/styles.css">
    <link type="text/css" rel="stylesheet" href="static/css/parameters.css">
    <link type="text/css" rel="stylesheet" href="static/css/table.css">
    <link type="text/css" rel="stylesheet" href="static/css/codemirror.css">
    <link type="text/css" rel="stylesheet" href="static/codemirror-5.6/lib/codemirror.css" />
    <link type="text/css" rel="stylesheet" href="static/codemirror-5.6/addon/hint/show-hint.css" />
    <link type="text/css" rel="stylesheet" href="static/css/codemirror-theme-custom.css">
    <script src="static/codemirror-5.6/lib/codemirror.js"></script>
    <script src="static/codemirror-5.6/addon/hint/show-hint.js"></script>
    <script src="static/codemirror-5.6/addon/hint/sql-hint.js"></script>
    <script src="static/js/codemirror-sql-custom.js"></script>
    <script src="static/codemirror-5.6/addon/display/placeholder.js"></script>
  </head>

  <body>
    <script>
    window.onload = function() {
      window.editor = CodeMirror.fromTextArea(document.getElementById('codemirror'), {
        mode: 'text/x-sql-custom',
        extraKeys: {
          "Ctrl-Space": "autocomplete",
        },
        theme: "custom",
        lineWrapping: false,
      });
    };
    </script>
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
