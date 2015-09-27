<!DOCTYPE html>
<html>
  <head>
    <title>Configure maintenance operations</title>
    <link type="text/css" rel="stylesheet" href="static/css/styles.css">
    <link type="text/css" rel="stylesheet" href="static/css/parameters.css">
    <link type="text/css" rel="stylesheet" href="static/css/table.css">
% include('%s/codemirror.inc' % MODULE, INCLUDE='stylesheets')
% include('%s/codemirror.inc' % MODULE, INCLUDE='scripts')
% include('%s/jquery.inc' % MODULE, INCLUDE='scripts')
  </head>

  <body>
% include('%s/div_error_messages.inc' % MODULE, ERRORS=VALUES['ERRORS'])
% include('%s/codemirror.inc' % MODULE, INCLUDE='body')
    <!-- Begin of request form -->
    <form method="get" accept-charset="UTF-8">
      <input type="hidden" name="id" value="{{ ARGS['ID'] }}">
      <table id="parameters">
        <caption>Operation configuration</caption>
        <tbody>
          <tr>
            <th>Operation name:</th>
            <td><input type="text" name="name" value="{{ ARGS['NAME'] }}"></td>
          </tr>
          <tr>
            <th>Description:</th>
            <td><input type="text" name="description" value="{{ ARGS['DESCRIPTION'] }}"></td>
          </tr>
          <tr>
            <th>SQL statement:</th>
            <td><textarea name="sql" id="codemirror" placeholder="< SQL CODE >">{{ ARGS['SQL'] }}</textarea></td>
          </tr>
          <tr>
            <th>Options:</th>
            <td>
              <div>\\
% include('%s/input_check.inc' % MODULE, NAME='applied', VALUE='*', SELECTED=ARGS['APPLIED'], TITLE='Applied')
</div>
              <div>\\
% include('%s/input_check.inc' % MODULE, NAME='ignore errors', VALUE='*', SELECTED=ARGS['IGNORE ERRORS'], TITLE='Ignore errors')
</div>
            </td>
          </tr>
        </tbody>
        <tfoot>
          <tr>
            <td colspan="2">
              <input type="submit" name="confirm" value="Confirm">
% if ARGS['ID'] and not VALUES['ERRORS']:
              <input type="button" name="cancel" value="Cancel" onclick="javascript:location.href='maintenance';">
              <input type="submit" name="action" value="Delete">
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
      <colgroup>
        <col width="36px"></col>
        <col></col>
        <col></col>
        <col></col>
        <col></col>
      </colgroup>
      <caption>Existing operations</caption>
      <thead>
        <tr>
          <th></th>
          <th>Name</th>
          <th>Description</th>
          <th>Status</th>
          <th>Errors handling</th>
        </tr>
      </thead>
      <tbody>
  % for row in VALUES['DATA']:
        <tr>
          <td><a href="?action=apply&id={{ row[0] }}"><img src="static/images/run.png"></a></td>
          <td><a href="?id={{ row[0] }}">{{ row[1] }}</a></td>
          <td>{{ row[2] }}</td>
          <td>{{ 'Applied' if row[3] else 'Not applied' }}</td>
          <td>{{ 'Ignore errors' if row[4] else 'Not ignore errors' }}</td>
        </tr>
  % end
      </tbody>
    </table>
    <!-- End of response data -->
% end
% include('%s/footer.inc' % MODULE)
  </body>
</html>
