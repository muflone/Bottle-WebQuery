<!DOCTYPE html>
<html>
  <head>
    <title>Configure roles</title>
    <link type="text/css" rel="stylesheet" href="static/css/styles.css">
    <link type="text/css" rel="stylesheet" href="static/css/parameters.css">
    <link type="text/css" rel="stylesheet" href="static/css/table.css">
  </head>

  <body>
% include('%s/div_error_messages.inc' % MODULE, ERRORS=VALUES['ERRORS'])
    <!-- Begin of request form -->
    <form method="get" accept-charset="UTF-8">
      <table id="parameters">
        <caption>Role configuration</caption>
        <tbody>
          <tr>
            <td>Role name:</td>
            <td><input type="text" name="role" value="{{ ARGS['ROLE'] }}"></td>
          </tr>
          <tr>
            <td>Description:</td>
            <td><input type="text" name="description" value="{{ ARGS['DESCRIPTION'] }}"></td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="2">
              <input type="submit" name="confirm" value="Confirm">
% if ARGS['ROLE'] and not VALUES['ERRORS']:
              <input type="button" name="cancel" value="Cancel" onclick="javascript:location.href='roles';">
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
      <caption>Existing roles</caption>
      <thead>
        <tr>
          <th>Name</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
  % for row in VALUES['DATA']:
        <tr>
          <td><a href="?role={{ row[0] }}">{{ row[0] }}</a></td>
          <td>{{ row[1] }}</td>
        </tr>
  % end
      </tbody>
    </table>
    <!-- End of response data -->
% end
% include('%s/footer.inc' % MODULE)
  </body>
</html>
