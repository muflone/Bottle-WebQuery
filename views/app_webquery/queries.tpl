<!DOCTYPE html>
<html>
  <head>
    <title>Configure queries</title>
    <link type="text/css" rel="stylesheet" href="static/css/styles.css">
    <link type="text/css" rel="stylesheet" href="static/css/parameters.css">
    <link type="text/css" rel="stylesheet" href="static/css/table.css">
% include('%s/codemirror.inc' % MODULE, INCLUDE='stylesheets')
% include('%s/codemirror.inc' % MODULE, INCLUDE='scripts')
% include('%s/jquery.inc' % MODULE, INCLUDE='scripts')
% include('%s/jquery.inc' % MODULE, INCLUDE='ui')
% include('%s/fancytree.inc' % MODULE, INCLUDE='stylesheets')
% include('%s/fancytree.inc' % MODULE, INCLUDE='scripts')
% include('%s/fancytree.inc' % MODULE, INCLUDE='scripts-table')
    <!-- Initialize the tree when the page is loaded -->
    <script type="text/javascript">
      $(function(){
        // Create the tree inside the <table id="treetable"> element
        $("#treetable").fancytree({
          extensions: ["table"],
          table: {
            indentation: 0,       // indent 0px per node level
            nodeColumnIdx: 1,     // render the node title into the 2nd column
            checkboxColumnIdx: 1  // render the checkboxes into the 1st column
          }, // End of table field
          source: {
            url: "?format=json"
          }, // End of source field
          checkbox: false,
          clickFolderMode: 4, // 1:activate, 2:expand, 3:activate and expand, 4:activate (dblclick expands)
          renderColumns: function(event, data) {
            var node = data.node;
            var $tdList = $(node.tr).find(">td");
            if (!node.isFolder()) {
              $tdList.eq(0).html('<a href="run?uuid=' + node.key + '"><img src="static/images/run.png"></a>');
              $tdList.eq(3).text(node.data.catalog);
              $tdList.eq(4).text(node.data.report);
            }
            $tdList.eq(2).text(node.tooltip);
          } // End of renderColumns field
        }); // End of fancytree definition
      }); // End of document function
    </script>
  </head>

  <body>
% include('%s/div_error_messages.inc' % MODULE, ERRORS=VALUES['ERRORS'])
% include('%s/codemirror.inc' % MODULE, INCLUDE='body')
    <!-- Begin of request form -->
    <form method="get" accept-charset="UTF-8">
      <input type="hidden" name="uuid" value="{{ ARGS['UUID'] }}">
      <table id="parameters">
        <caption>Query configuration</caption>
        <tbody>
          <tr>
            <th>Folder:</th>
            <td><select name="folder">
% include('%s/select_options_from_data.inc' % MODULE, DATA_ROWS=False, FIELD_ID=0, FIELD_VALUE=1, SELECTED=ARGS['FOLDER'], DATA=VALUES['FOLDERS'])
            </select></td>
          </tr>
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
            <td><textarea name="sql" id="codemirror" placeholder="< SQL CODE >">{{ ARGS['SQL'] }}</textarea></td>
          </tr>
          <tr>
            <th>Parameters:</th>
            <td><textarea name="parameters">{{ ARGS['PARAMETERS'] }}</textarea></td>
          </tr>
          <tr>
            <th>Report:</th>
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
    <table id="treetable" class="data">
      <colgroup>
        <col width="36px"></col>
        <col></col>
        <col></col>
        <col></col>
        <col></col>
      </colgroup>
      <caption>Existing queries</caption>
      <thead>
        <tr>
          <th>Run</th>
          <th>Name</th>
          <th>Description</th>
          <th>Catalog</th>
          <th>Report</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
          <td></td>
        </tr>
      </tbody>
    </table>
% end
    <!-- End of response data -->
  </body>
</html>
