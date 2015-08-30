<!DOCTYPE html>
<html>
  <head>
    <title>Configure folders</title>
    <link type="text/css" rel="stylesheet" href="static/css/styles.css">
    <link type="text/css" rel="stylesheet" href="static/css/parameters.css">
    <link type="text/css" rel="stylesheet" href="static/css/table.css">
  </head>

  <body>
% include('%s/div_error_messages.inc' % MODULE, ERRORS=VALUES['ERRORS'])
    <!-- Begin of request form -->
    <form method="get" accept-charset="UTF-8">
      <table id="parameters">
        <caption>Folder configuration</caption>
        <tbody>
          <tr>
            <td>Folder name:</td>
            <td><input type="text" name="folder" value="{{ ARGS['FOLDER'] }}"></td>
          </tr>
          <tr>
            <td>Description:</td>
            <td><input type="text" name="description" value="{{ ARGS['DESCRIPTION'] }}"></td>
          </tr>
          <tr>
            <td>Visibility:</td>
            <td>\\
% include('%s/input_check.inc' % MODULE, NAME='visible', VALUE='1', SELECTED=ARGS['VISIBLE'], TITLE='The folder is visible')
</td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="2">
              <input type="submit" name="confirm" value="Confirm">
% if ARGS['FOLDER'] and not VALUES['ERRORS']:
              <input type="button" name="cancel" value="Cancel" onclick="javascript:location.href='folders';">
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
      <caption>Existing folders</caption>
      <thead>
        <tr>
          <th>Name</th>
          <th>Description</th>
          <th>Visibility</th>
        </tr>
      </thead>
      <tbody>
  % for row in VALUES['DATA']:
        <tr>
          <td><a href="?folder={{ row[0] }}">{{ row[0] }}</a></td>
          <td>{{ row[1] }}</td>
          <td>{{ row[2] == 1 }}</td>
        </tr>
  % end
      </tbody>
    </table>
    <!-- End of response data -->
% end
  </body>
</html>
