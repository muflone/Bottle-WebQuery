% if INCLUDE == 'stylesheets':
    <link type="text/css" rel="stylesheet" href="static/css/tablesorter.css">
  % if 'pager' in OPTIONS:
    <link rel="stylesheet" href="static/tablesorter-2.23.3/jquery.tablesorter.pager.css">
  % end
% elif INCLUDE == 'scripts':
    <script type="text/javascript" src="static/tablesorter-2.23.3/jquery.tablesorter.min.js"></script>
    <script type="text/javascript" src="static/tablesorter-2.23.3/jquery.tablesorter.widgets.min.js"></script>
  % if 'pager' in OPTIONS:
    <script src="static/tablesorter-2.23.3/jquery.tablesorter.pager.js"></script>
  % end
    <script>
    $(function(){
      $('.data')
        .tablesorter({
          sortReset: true,
          widgets: [
  % if 'resizable' in OPTIONS:
            'resizable',
  % end
  % if 'pager' in OPTIONS:
            'pager',
  % end
          ],
          widgetOptions: {
            storage_useSessionStorage: true,  /* Save to session */
  % if 'resizable' in OPTIONS:
            resizable_addLastColumn: false,   /* Resize freely */
            resizable: false,                 /* Don't restore columns width */
  % end
          },
        })
  % if 'pager' in OPTIONS:
        .tablesorterPager({
          container: $(".pager"),             /* Container for pager */
          output: 'Rows {startRow} - {endRow} of {totalRows}', /* Pager format */
          page: 0,                            /* Starting page */
          size: 100,                          /* Default page size */
          removeRows: true,                   /* Remove hidden rows */
          updateArrows: true,                 /* Disable arrows on first and last page */
        })
  % end
      ;
    });
    </script>
% elif INCLUDE == 'body':
  % pass
% elif INCLUDE == 'pager':
      <div class="pager center">
        <form>
          <img src="static/tablesorter-2.23.3/first.png" class="first" />
          <img src="static/tablesorter-2.23.3/prev.png" class="prev" />
          <input type="text" class="pagedisplay" readonly="readonly" />
          <img src="static/tablesorter-2.23.3/next.png" class="next"/>
          <img src="static/tablesorter-2.23.3/last.png" class="last"/>
          <select class="pagesize">
            <option value="10">10</option>
            <option selected="selected" value="100">100</option>
            <option value="200">200</option>
            <option value="500">500</option>
            <option value="1000">1000</option>
            <option value="10000">10000</option>
          </select>
        </form>
      </div>
% end
